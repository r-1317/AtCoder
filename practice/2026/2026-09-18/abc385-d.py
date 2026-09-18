import os
# from sortedcontainers import SortedSet

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

class SortedSet:
  def __init__(self, iterable=(), key=None):
    self.key = key
    a = sorted(set(() if iterable is None else iterable), key=key)
    self._values = a
    self._keys = a.copy() if key is None else [key(x) for x in a]
    self._nodes = {x: i + 1 for i, x in enumerate(a)}
    # ノード番号0は空の部分木。値とkeyだけは「ノード番号 - 1」で参照。
    self._left = [0]
    self._right = [0]
    self._parent = [0]
    self._size = [0]
    self._priority = [0]
    self._free = [i for i in range(0)]
    self._root = 0
    self._rng = 88172645463325252
    self._build(a)

  def _key(self, value):
    if self.key is None:
      return value
    else:
      return self.key(value)

  def _random64(self):
    x = self._rng
    x ^= x << 13
    # Codonの符号付き右シフトを、64bitの論理右シフトに直す。
    x ^= (x >> 7) & 0x01ffffffffffffff
    x ^= x << 17
    # CPythonの多倍長intとCodonのint64で同一の符号付き64bit値にする。
    # 2回に分けて引くことで、正の2**63をint64で表現せずに済む。
    high = ((x >> 63) & 1) << 62
    self._rng = (x & 0x7fffffffffffffff) - high - high
    return self._rng

  def _build(self, a):
    self._values = a
    self._keys = [self._key(x) for x in a]
    self._nodes = {x: i + 1 for i, x in enumerate(a)}
    n = len(a)
    self._left = [0] * (n + 1)
    self._right = [0] * (n + 1)
    self._parent = [0] * (n + 1)
    self._size = [0] * (n + 1)
    self._priority = [0] + [self._random64() for _ in a]
    self._free.clear()
    # ソート済み配列からCartesian treeをO(N)で構築。
    stack = [i for i in range(0)]
    for i in range(1, n + 1):
      last = 0
      while stack and self._priority[stack[-1]] < self._priority[i]:
        last = stack.pop()
      self._left[i] = last
      if last:
        self._parent[last] = i
      if stack:
        self._right[stack[-1]] = i
        self._parent[i] = stack[-1]
      stack.append(i)
    self._root = stack[0] if stack else 0
    order = [self._root] if self._root else []
    pos = 0
    while pos < len(order):
      i = order[pos]
      pos += 1
      if self._left[i]:
        order.append(self._left[i])
      if self._right[i]:
        order.append(self._right[i])
    for i in reversed(order):
      self._size[i] = 1 + self._size[self._left[i]] + self._size[self._right[i]]

  def __len__(self):
    return len(self._nodes)

  def __bool__(self):
    return bool(self._root)

  def __contains__(self, value):
    return value in self._nodes

  def __iter__(self):
    return self.islice()

  def __reversed__(self):
    return self.islice(reverse=True)

  def __repr__(self):
    return 'SortedSet(' + repr(list(self)) + ')'

  # iを親の位置へ回転する。祖先の部分木サイズは変わらない。
  def _rotate(self, i):
    p = self._parent[i]
    g = self._parent[p]
    if i == self._left[p]:
      child = self._right[i]
      self._left[p] = child
      self._right[i] = p
    else:
      child = self._left[i]
      self._right[p] = child
      self._left[i] = p
    if child:
      self._parent[child] = p
    self._parent[p] = i
    self._parent[i] = g
    if not g:
      self._root = i
    elif self._left[g] == p:
      self._left[g] = i
    else:
      self._right[g] = i
    self._size[i] = self._size[p]
    self._size[p] = 1 + self._size[self._left[p]] + self._size[self._right[p]]

  def add(self, value):
    if value in self._nodes:
      return
    key = self._key(value)
    if self._free:
      i = self._free.pop()
      self._values[i - 1] = value
      self._keys[i - 1] = key
      self._left[i] = self._right[i] = 0
      self._size[i] = 1
      self._priority[i] = self._random64()
    else:
      i = len(self._size)
      self._values.append(value)
      self._keys.append(key)
      self._left.append(0)
      self._right.append(0)
      self._parent.append(0)
      self._size.append(1)
      self._priority.append(self._random64())
    p, node = 0, self._root
    while node:
      p = node
      self._size[p] += 1
      node = self._left[p] if key < self._keys[p - 1] else self._right[p]
    self._parent[i] = p
    if not p:
      self._root = i
    elif key < self._keys[p - 1]:
      self._left[p] = i
    else:
      self._right[p] = i
    self._nodes[value] = i
    while self._parent[i] and self._priority[self._parent[i]] < self._priority[i]:
      self._rotate(i)

  def _erase(self, i):
    value = self._values[i - 1]
    # 子を回転して上げ、削除対象の子が高々1つになったら取り外す。
    while self._left[i] and self._right[i]:
      l, r = self._left[i], self._right[i]
      self._rotate(l if self._priority[l] > self._priority[r] else r)
    child = self._left[i] or self._right[i]
    p = self._parent[i]
    if child:
      self._parent[child] = p
    if not p:
      self._root = child
    elif self._left[p] == i:
      self._left[p] = child
    else:
      self._right[p] = child
    while p:
      self._size[p] -= 1
      p = self._parent[p]
    del self._nodes[value]
    self._free.append(i)
    return value

  def discard(self, value):
    i = self._nodes.get(value, 0)
    if i:
      self._erase(i)

  def remove(self, value):
    i = self._nodes.get(value, 0)
    if not i:
      raise KeyError(str(value))
    self._erase(i)

  def _node_at(self, index):
    if index < 0:
      index += len(self)
    if index < 0 or index >= len(self):
      raise IndexError('SortedSet index out of range')
    node = self._root
    while node:
      size = self._size[self._left[node]]
      if index < size:
        node = self._left[node]
      elif index == size:
        return node
      else:
        index -= size + 1
        node = self._right[node]
    raise IndexError('SortedSet index out of range')

  def pop(self, index=-1):
    return self._erase(self._node_at(index))

  def __getitem__(self, index):
    if isinstance(index, slice):
      start, stop, step = index.indices(len(self))
      if step == 1:
        return list(self.islice(start, stop))
      if step == -1:
        return list(self.islice(stop + 1, start + 1, reverse=True))
      return list(self)[index]
    else:
      return self._values[self._node_at(index) - 1]

  def __delitem__(self, index):
    if isinstance(index, slice):
      removed = set(self[index])
      self._build([x for x in self if x not in removed])
    else:
      self.pop(index)

  def clear(self):
    self._build(self._values[:0])

  def copy(self):
    result = SortedSet(self._values[:0], self.key)
    result._build(list(self))
    return result

  def count(self, value):
    return int(value in self._nodes)

  def bisect_key_left(self, key):
    rank, node = 0, self._root
    while node:
      if self._keys[node - 1] < key:
        rank += self._size[self._left[node]] + 1
        node = self._right[node]
      else:
        node = self._left[node]
    return rank

  def bisect_key_right(self, key):
    rank, node = 0, self._root
    while node:
      if key < self._keys[node - 1]:
        node = self._left[node]
      else:
        rank += self._size[self._left[node]] + 1
        node = self._right[node]
    return rank

  def bisect_key(self, key):
    return self.bisect_key_right(key)

  def bisect_left(self, value):
    return self.bisect_key_left(self._key(value))

  def bisect_right(self, value):
    return self.bisect_key_right(self._key(value))

  def bisect(self, value):
    return self.bisect_right(value)

  def index(self, value, start=None, stop=None):
    node = self._nodes.get(value, 0)
    if not node:
      raise ValueError('value is not in SortedSet')
    rank = self._size[self._left[node]]
    while self._parent[node]:
      p = self._parent[node]
      if self._right[p] == node:
        rank += self._size[self._left[p]] + 1
      node = p
    lo, hi, step = slice(start, stop).indices(len(self))
    if lo <= rank < hi:
      return rank
    raise ValueError('value is not in SortedSet')

  # 親ポインタで後続・先行要素をたどり、範囲全体を期待O(log N + 出力数)で走査。
  def islice(self, start=None, stop=None, reverse=False):
    lo, hi, step = slice(start, stop).indices(len(self))
    if lo >= hi:
      return
    node = self._node_at(hi - 1 if reverse else lo)
    forward = self._left if reverse else self._right
    backward = self._right if reverse else self._left
    for _ in range(hi - lo):
      yield self._values[node - 1]
      if forward[node]:
        node = forward[node]
        while backward[node]:
          node = backward[node]
      else:
        p = self._parent[node]
        while p and forward[p] == node:
          node, p = p, self._parent[p]
        node = p

  def irange_key(self, min_key=None, max_key=None, inclusive=(True, True), reverse=False):
    lo = 0 if min_key is None else (self.bisect_key_left(min_key) if inclusive[0] else self.bisect_key_right(min_key))
    hi = len(self) if max_key is None else (self.bisect_key_right(max_key) if inclusive[1] else self.bisect_key_left(max_key))
    return self.islice(lo, hi, reverse)

  def irange(self, minimum=None, maximum=None, inclusive=(True, True), reverse=False):
    lo = 0 if minimum is None else (self.bisect_left(minimum) if inclusive[0] else self.bisect_right(minimum))
    hi = len(self) if maximum is None else (self.bisect_right(maximum) if inclusive[1] else self.bisect_left(maximum))
    return self.islice(lo, hi, reverse)

  def update(self, *iterables):
    # 先に集合化して、update(self)や自分自身のイテレータにも対応。
    values = set(self._nodes)
    # 空の可変長引数でもCodonがループ変数の型を推論できるようにする。
    for iterable in ((), *iterables):
      values.update(iterable)
    self._build(sorted(values, key=self.key))
    return self

  def difference_update(self, *iterables):
    values = set(self._nodes)
    for iterable in ((), *iterables):
      values.difference_update(set(iterable))
    self._build([x for x in self if x in values])
    return self

  def intersection_update(self, *iterables):
    values = set(self._nodes)
    for iterable in (self._nodes, *iterables):
      values.intersection_update(set(iterable))
    self._build([x for x in self if x in values])
    return self

  def symmetric_difference_update(self, other):
    values = set(self._nodes).symmetric_difference(set(other))
    self._build(sorted(values, key=self.key))
    return self

  def union(self, *iterables):
    return self.copy().update(*iterables)

  def difference(self, *iterables):
    return self.copy().difference_update(*iterables)

  def intersection(self, *iterables):
    return self.copy().intersection_update(*iterables)

  def symmetric_difference(self, other):
    return self.copy().symmetric_difference_update(other)

  def issubset(self, other):
    return set(self._nodes).issubset(set(other))

  def issuperset(self, other):
    return set(self._nodes).issuperset(set(other))

  def isdisjoint(self, other):
    return set(self._nodes).isdisjoint(set(other))

  def __eq__(self, other):
    if isinstance(other, (SortedSet, set)):
      return set(self._nodes) == set(other)
    return False

  def __ne__(self, other):
    return not self == other

  def __le__(self, other):
    if isinstance(other, (SortedSet, set)):
      return self.issubset(other)
    raise TypeError('set comparison requires SortedSet or set')

  def __lt__(self, other):
    if isinstance(other, (SortedSet, set)):
      return set(self._nodes) < set(other)
    raise TypeError('set comparison requires SortedSet or set')

  def __ge__(self, other):
    if isinstance(other, (SortedSet, set)):
      return self.issuperset(other)
    raise TypeError('set comparison requires SortedSet or set')

  def __gt__(self, other):
    if isinstance(other, (SortedSet, set)):
      return set(self._nodes) > set(other)
    raise TypeError('set comparison requires SortedSet or set')

  def __or__(self, other):
    return self.union(other)

  def __and__(self, other):
    return self.intersection(other)

  def __sub__(self, other):
    return self.difference(other)

  def __xor__(self, other):
    return self.symmetric_difference(other)

  def __ror__(self, other):
    return self.union(other)

  def __rand__(self, other):
    return self.intersection(other)

  def __rxor__(self, other):
    return self.symmetric_difference(other)

  def __ior__(self, other):
    return self.update(other)

  def __iand__(self, other):
    return self.intersection_update(other)

  def __isub__(self, other):
    return self.difference_update(other)

  def __ixor__(self, other):
    return self.symmetric_difference_update(other)

dir = {"U": 1, "D": -1, "L": -1, "R": 1}

def main():
  N, M, x, y = list(map(int, input().split()))
  v_set_dict = dict()
  h_set_dict = dict()

  for _ in range(N):
    hx, hy = list(map(int, input().split()))
    if hx not in v_set_dict:
      v_set_dict[hx] = SortedSet()
    v_set_dict[hx].add(hy)
    if hy not in h_set_dict:
      h_set_dict[hy] = SortedSet()
    h_set_dict[hy].add(hx)

  ans = 0

  for _ in range(M):
    d, str_c = input().split()
    c = int(str_c)

    if d in ["U", "D"]:  # 水平方向の移動
      nx = x
      ny = y + c * dir[d]
      ly = min(y, ny)
      ry = max(y, ny)
      if x in v_set_dict:
        pop_idx = v_set_dict[x].bisect_left(ly)
        for _ in range(pop_idx, v_set_dict[x].bisect_right(ry)):
          py = v_set_dict[x].pop(pop_idx)  # 毎回indexが1つ詰まるはずなので同じ値を指定
          h_set_dict[py].discard(x)
          ans += 1
    elif d in ["L", "R"]:  # 垂直方向の移動
      nx = x + c * dir[d]
      ny = y
      lx = min(x, nx)
      rx = max(x, nx)
      if y in h_set_dict:
        pop_idx = h_set_dict[y].bisect_left(lx)
        for _ in range(pop_idx, h_set_dict[y].bisect_right(rx)):
          px = h_set_dict[y].pop(pop_idx)
          v_set_dict[px].discard(y)
          ans += 1

    x = nx
    y = ny

  print(x, y, ans)

if __name__ == "__main__":
  main()