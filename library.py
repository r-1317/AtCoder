# Union-Find
# https://github.com/r-1317/AtCoder/blob/main/library.py
class UnionFind:
  # n個の頂点がすべて孤立した状態で初期化
  def __init__(self, n):
    self.parent_list = [-1] * n
    self.size_list = [1] * n

  # xが属する根付き木の根を返す
  def root(self, x):
    # xの親が-1ならxが根
    if self.parent_list[x] == -1:
      return x
    # xの親が-1でなければ、再帰的に親をたどって根を探す
    self.parent_list[x] = self.root(self.parent_list[x])  # パス圧縮
    return self.parent_list[x]
  
  # xとyが同じ根を持つかどうかを判定
  def is_same(self, x, y):
    return self.root(x) == self.root(y)
  
  # xの属する根付き木とyの属する根付き木を併合
  def unite(self, x, y):
    root_x = self.root(x)
    root_y = self.root(y)
    
    # すでに同じ根を持つ場合は何もしない
    if root_x == root_y:
      return None
    
    # 根のサイズを比較して、小さい方を大きい方に結合
    if self.size_list[root_x] < self.size_list[root_y]:
      root_x, root_y = root_y, root_x  # root_xを常に大きい方にする
    self.parent_list[root_y] = root_x  # root_yをroot_xの子にする
    self.size_list[root_x] += self.size_list[root_y]  # root_xのサイズにroot_yのサイズを加える
    self.size_list[root_y] = 0  # root_yが根ではなくなったのでサイズを0にする。この操作は必要ないが、明示的にサイズを管理するために行う
    return None

  # xの属する根付き木のサイズを返す
  def size(self, x):
    return self.size_list[self.root(x)]


##############################################################################################################################################################################


# セグメント木
# op: 結合則を満たす二項演算、e: 単位元を返す関数
"""
使用例（区間和）
seg = SegmentTree(lambda a, b: a + b, lambda: 0, [1, 2, 3, 4])
seg.prod(1, 4)  # 9
seg.set(2, 10)
seg.all_prod()  # 17
"""
class SegmentTree:
  # vには初期配列、または要素数を指定する
  def __init__(self, op, e, v):
    self.op = op
    self.e = e

    if isinstance(v, int):
      assert v >= 0
      self.n = v
      values = [e() for _ in range(v)]
    else:
      values = list(v)
      self.n = len(values)

    self.size = 1 << (self.n - 1).bit_length() if self.n else 1
    self.log = self.size.bit_length() - 1
    self.data = [e() for _ in range(2 * self.size)]
    self.data[self.size:self.size + self.n] = values

    for k in range(self.size - 1, 0, -1):
      self._update(k)

  def _update(self, k):
    self.data[k] = self.op(self.data[2 * k], self.data[2 * k + 1])

  # a[p]をxに更新する: O(log N)
  def set(self, p, x):
    assert 0 <= p < self.n
    p += self.size
    self.data[p] = x
    for i in range(1, self.log + 1):
      self._update(p >> i)

  # a[p]を返す: O(1)
  def get(self, p):
    assert 0 <= p < self.n
    return self.data[p + self.size]

  # op(a[l], ..., a[r - 1])を返す: O(log N)
  def prod(self, l, r):
    assert 0 <= l <= r <= self.n
    sml = self.e()
    smr = self.e()
    l += self.size
    r += self.size

    while l < r:
      if l & 1:
        sml = self.op(sml, self.data[l])
        l += 1
      if r & 1:
        r -= 1
        smr = self.op(self.data[r], smr)
      l >>= 1
      r >>= 1

    return self.op(sml, smr)

  # 配列全体の積を返す: O(1)
  def all_prod(self):
    return self.data[1]

  # f(prod(l, r))が真となる最大のrを返す: O(log N)
  # fは副作用を持たず、f(e()) == Trueであること
  def max_right(self, l, f):
    assert 0 <= l <= self.n
    assert f(self.e())
    if l == self.n:
      return self.n

    l += self.size
    sm = self.e()
    while True:
      while l % 2 == 0:
        l >>= 1
      if not f(self.op(sm, self.data[l])):
        while l < self.size:
          l *= 2
          nxt = self.op(sm, self.data[l])
          if f(nxt):
            sm = nxt
            l += 1
        return l - self.size
      sm = self.op(sm, self.data[l])
      l += 1
      if l & -l == l:
        break

    return self.n

  # f(prod(l, r))が真となる最小のlを返す: O(log N)
  # fは副作用を持たず、f(e()) == Trueであること
  def min_left(self, r, f):
    assert 0 <= r <= self.n
    assert f(self.e())
    if r == 0:
      return 0

    r += self.size
    sm = self.e()
    while True:
      r -= 1
      while r > 1 and r % 2:
        r >>= 1
      if not f(self.op(self.data[r], sm)):
        while r < self.size:
          r = 2 * r + 1
          nxt = self.op(self.data[r], sm)
          if f(nxt):
            sm = nxt
            r -= 1
        return r + 1 - self.size
      sm = self.op(self.data[r], sm)
      if r & -r == r:
        break

    return 0


##############################################################################################################################################################################


# セグメント木2(これはcodonでも動くはず)
class SegmentTree:
  def __init__(self, op, e, v):
    self.op = op
    self.e = e

    self._n = len(v)

    self.size = 1
    self.log = 0
    while self.size < self._n:
      self.size <<= 1
      self.log += 1

    self.d = [e() for _ in range(2 * self.size)]

    for i in range(self._n):
      self.d[self.size + i] = v[i]

    for i in range(self.size - 1, 0, -1):
      self._update(i)

  def _update(self, k: int):
    self.d[k] = self.op(
      self.d[2 * k],
      self.d[2 * k + 1]
    )

  def set(self, p: int, x):
    assert 0 <= p < self._n

    p += self.size
    self.d[p] = x

    i = 1
    while i <= self.log:
      self._update(p >> i)
      i += 1

  def get(self, p: int):
    assert 0 <= p < self._n
    return self.d[p + self.size]

  def prod(self, l: int, r: int):
    assert 0 <= l <= r <= self._n

    sml = self.e()
    smr = self.e()

    l += self.size
    r += self.size

    while l < r:
      if l & 1:
        sml = self.op(sml, self.d[l])
        l += 1

      if r & 1:
        r -= 1
        smr = self.op(self.d[r], smr)

      l >>= 1
      r >>= 1

    return self.op(sml, smr)

  def all_prod(self):
    return self.d[1]

  def max_right(self, l: int, f):
    assert 0 <= l <= self._n
    assert f(self.e())

    if l == self._n:
      return self._n

    l += self.size
    sm = self.e()

    while True:
      while l % 2 == 0:
          l >>= 1

      if not f(self.op(sm, self.d[l])):
        while l < self.size:
          l *= 2

          if f(self.op(sm, self.d[l])):
            sm = self.op(sm, self.d[l])
            l += 1

        return l - self.size

      sm = self.op(sm, self.d[l])
      l += 1

      if (l & -l) == l:
        break

    return self._n

  def min_left(self, r: int, f):
    assert 0 <= r <= self._n
    assert f(self.e())

    if r == 0:
        return 0

    r += self.size
    sm = self.e()

    while True:
      r -= 1

      while r > 1 and (r & 1):
        r >>= 1

      if not f(self.op(self.d[r], sm)):
        while r < self.size:
          r = 2 * r + 1

          if f(self.op(self.d[r], sm)):
            sm = self.op(self.d[r], sm)
            r -= 1

        return r + 1 - self.size

      sm = self.op(self.d[r], sm)

      if (r & -r) == r:
        break

    return 0


##############################################################################################################################################################################


# 遅延セグメント木（Codon対応）
# 参考: https://github.com/atcoder/ac-library/blob/master/atcoder/lazysegtree.hpp
# op(S, S) -> S: 結合則を満たす演算、e() -> S: その単位元
# mapping(F, S) -> S: 区間の値に作用を適用する
# composition(f, g) -> F: gを適用した後にfを適用する作用（f ∘ g）
# id() -> F: 恒等作用
# mappingはopを保つこと: mapping(f, op(x, y)) == op(mapping(f, x), mapping(f, y))
# 値S・作用Fにはそれぞれ同じ型を使い、上記関数は引数を破壊的に変更しないこと。
# 添字は0始まり、区間は半開区間[l, r)。構築O(N)、領域O(N)。
# 各関数の計算量をO(1)とすると、all_prodはO(1)、その他の操作はO(log N)。
class LazySegmentTree:
  # v: 初期配列、または要素数（全要素をe()で初期化）
  def __init__(self, op, e, mapping, composition, id, v):
    self.op = op
    self.e = e
    self.mapping = mapping
    self.composition = composition
    self.id = id
    if isinstance(v, int):
      assert v >= 0
      values = [e() for _ in range(v)]
    else:
      values = list(v)
    self._n = len(values)
    self.size = 1
    self.log = 0
    while self.size < self._n:
      self.size <<= 1
      self.log += 1
    self.d = [e() for _ in range(2 * self.size)]
    self.lz = [id() for _ in range(self.size)]
    for i in range(self._n):
      self.d[self.size + i] = values[i]
    for k in range(self.size - 1, 0, -1):
      self._update(k)

  def _update(self, k: int):
    self.d[k] = self.op(self.d[2 * k], self.d[2 * k + 1])

  def _all_apply(self, k: int, f):
    self.d[k] = self.mapping(f, self.d[k])
    if k < self.size:
      self.lz[k] = self.composition(f, self.lz[k])

  def _push(self, k: int):
    self._all_apply(2 * k, self.lz[k])
    self._all_apply(2 * k + 1, self.lz[k])
    self.lz[k] = self.id()

  # a[p]をxに置き換える
  def set(self, p: int, x):
    assert 0 <= p < self._n
    p += self.size
    for i in range(self.log, 0, -1):
      self._push(p >> i)
    self.d[p] = x
    for i in range(1, self.log + 1):
      self._update(p >> i)

  def get(self, p: int):
    assert 0 <= p < self._n
    p += self.size
    for i in range(self.log, 0, -1):
      self._push(p >> i)
    return self.d[p]

  def prod(self, l: int, r: int):
    assert 0 <= l <= r <= self._n
    if l == r:
      return self.e()
    l += self.size
    r += self.size
    for i in range(self.log, 0, -1):
      if ((l >> i) << i) != l:
        self._push(l >> i)
      if ((r >> i) << i) != r:
        self._push((r - 1) >> i)
    sml = self.e()
    smr = self.e()
    while l < r:
      if l & 1:
        sml = self.op(sml, self.d[l])
        l += 1
      if r & 1:
        r -= 1
        smr = self.op(self.d[r], smr)
      l >>= 1
      r >>= 1
    return self.op(sml, smr)

  def all_prod(self):
    return self.d[1]

  # apply(p, f): 一点に作用、apply(l, r, f): 区間に作用
  # Codon専用のstatic.lenで引数の個数をコンパイル時に判定する。
  def apply(self, l: int, *args):
    if len(args) == 1:  # CPython, PyPyの場合
    # if static.len(args) == 1:  # Codonの場合
      assert 0 <= l < self._n
      p = l + self.size
      for i in range(self.log, 0, -1):
        self._push(p >> i)
      self.d[p] = self.mapping(args[0], self.d[p])
      for i in range(1, self.log + 1):
        self._update(p >> i)
    elif len(args) == 2:  # CPython, PyPyの場合
    # elif static.len(args) == 2:  # Codonの場合
      r, f = args
      assert 0 <= l <= r <= self._n
      if l == r:
        return
      l += self.size
      r += self.size
      for i in range(self.log, 0, -1):
        if ((l >> i) << i) != l:
          self._push(l >> i)
        if ((r >> i) << i) != r:
          self._push((r - 1) >> i)
      left, right = l, r
      while l < r:
        if l & 1:
          self._all_apply(l, f)
          l += 1
        if r & 1:
          r -= 1
          self._all_apply(r, f)
        l >>= 1
        r >>= 1
      for i in range(1, self.log + 1):
        if ((left >> i) << i) != left:
          self._update(left >> i)
        if ((right >> i) << i) != right:
          self._update((right - 1) >> i)
    else:
      raise TypeError("apply expects (p, f) or (l, r, f)")

  # g(prod(l, r))が真となる最大のrを返す。
  # g(e()) == True、副作用なし、区間を伸ばすと真から偽への変化は高々1回。
  def max_right(self, l: int, g):
    assert 0 <= l <= self._n
    assert g(self.e())
    if l == self._n:
      return self._n
    l += self.size
    for i in range(self.log, 0, -1):
      self._push(l >> i)
    sm = self.e()
    while True:
      while l % 2 == 0:
        l >>= 1
      if not g(self.op(sm, self.d[l])):
        while l < self.size:
          self._push(l)
          l *= 2
          nxt = self.op(sm, self.d[l])
          if g(nxt):
            sm = nxt
            l += 1
        return l - self.size
      sm = self.op(sm, self.d[l])
      l += 1
      if (l & -l) == l:
        break
    return self._n

  # g(prod(l, r))が真となる最小のlを返す。gの条件はmax_rightと同じ。
  def min_left(self, r: int, g):
    assert 0 <= r <= self._n
    assert g(self.e())
    if r == 0:
      return 0
    r += self.size
    for i in range(self.log, 0, -1):
      self._push((r - 1) >> i)
    sm = self.e()
    while True:
      r -= 1
      while r > 1 and r % 2:
        r >>= 1
      if not g(self.op(self.d[r], sm)):
        while r < self.size:
          self._push(r)
          r = 2 * r + 1
          nxt = self.op(self.d[r], sm)
          if g(nxt):
            sm = nxt
            r -= 1
        return r + 1 - self.size
      sm = self.op(self.d[r], sm)
      if (r & -r) == r:
        break
    return 0


"""
使用例（この文字列内のコードをクラス定義の後にコピーして実行）
実行: codon run -release example.py（LazySegmentTreeのクラス定義も含める）
区間最大値の取得・区間代入（非負の高さを管理）。
典型90問 029 - Long Bricks で使う操作の例:
https://atcoder.jp/contests/typical90/tasks/typical90_ac
S = 区間の最大の高さ、F = 代入する高さ。どちらもint型。
高さに現れない-1を、空区間の単位元・「更新なし」の作用に使う。

def op(x, y):
  return max(x, y)

def e():
  return -1

def mapping(f, x):
  # 更新なし、または空区間ならそのまま。
  return x if f == -1 or x == -1 else f

def composition(f, g):
  # 後から来た代入fを優先する。fが更新なしなら以前の作用gを残す。
  return g if f == -1 else f

def identity():
  return -1

# 初期の高さは0。要素数だけ渡すとe() == -1で埋まるため、配列を渡す。
seg = LazySegmentTree(op, e, mapping, composition, identity, [0 for _ in range(5)])
seg.apply(1, 4, 2)                # [0, 2, 2, 2, 0]（加算ではなく代入）
print(seg.prod(2, 5))             # 2: 区間[2, 5)の最大の高さ
height = seg.prod(2, 5) + 1       # その区間に置くレンガの上面の高さ
seg.apply(2, 5, height)           # [0, 2, 3, 3, 3]
print(seg.get(2))                 # 3
print(seg.all_prod())             # 3
seg.apply(0, 2, 0)                # [0, 0, 3, 3, 3]（高さ0への代入も可能）
print(seg.prod(0, 2))             # 0

# 問題の1始まりの閉区間[L, R]は、このクラスでは[L - 1, R)に対応。
"""



##############################################################################################################################################################################


# NxNの盤面を表現するビットボード
# https://github.com/r-1317/AtCoder/blob/main/library.py 
class BitBoard:
  # N: 盤面のサイズ, board: ビットボードの初期値(指定しない場合はすべて0)
  def __init__(self, N: int, board: int = 0):
    self.N = N
    self.board = board

  # (x, y)のマスを1にする
  def set(self, x: int, y: int):
    self.board |= (1 << (x * self.N + y))

  # (x, y)のマスを0にする
  def unset(self, x: int, y: int):
    self.board &= ~(1 << (x * self.N + y))

  # (x, y)のマスが1かどうかを返す
  def is_set(self, x: int, y: int) -> bool:
    return (self.board >> (x * self.N + y)) & 1 == 1

  # ビットボードを文字列で表示する
  def __str__(self):
    res = []
    for i in range(self.N):
      row = []
      for j in range(self.N):
        if self.is_set(i, j):
          row.append('1')
        else:
          row.append('0')
      res.append(''.join(row))
    return '\n'.join(res)


##############################################################################################################################################################################


# SortedSet
# 平方分割 + set。外部ライブラリ不要、Python / Codon両対応。
# 要素は同じ型で、ハッシュ可能であること。格納中に値やkeyの結果を変えない。
# len: O(1)、in / count: 平均O(1)
# add / discard / remove / pop: 償却O(√N)、添字 / bisect / index: O(√N)
# key指定時、同じkeyの要素を探すindex / remove / discardは最悪O(N)。
# 初期化・集合演算: O(N log N)程度、走査・コピー: O(N)、メモリ: O(N)。
# keyは比較時に評価するため、軽く副作用のない関数を指定する。
# sortedcontainersの主要な公開操作に対応（内部用_check / _reset、pickleは対象外）。
# 比較演算の相手はSortedSetまたはset（Codonにはfrozensetがない）。
# Codonで空集合を作るときはNoneを渡さず、SortedSet()か型付き空リストを使う。
class SortedSet:
  def __init__(self, iterable=(), key=None):
    self.key = key
    self._set = set(() if iterable is None else iterable)
    a = sorted(self._set, key=key)
    self._buckets = [a] if a else []
    self._built_size = 0
    self._bucket_size = 16
    self._build(a)

  def _build(self, a):
    self._built_size = len(a)
    self._bucket_size = max(16, int(len(a) ** 0.5) + 1)
    size = self._bucket_size
    self._buckets = [a[i:i + size] for i in range(0, len(a), size)]

  def _key(self, value):
    if self.key is None:
      return value
    else:
      return self.key(value)

  # バケット内の二分探索。right=Trueなら同じkeyの直後。
  def _bisect(self, bucket, key, right=False):
    lo, hi = 0, len(bucket)
    while lo < hi:
      mid = (lo + hi) // 2
      k = self._key(bucket[mid])
      if (not key < k) if right else (k < key):
        lo = mid + 1
      else:
        hi = mid
    return lo

  def __len__(self):
    return len(self._set)

  def __bool__(self):
    return bool(self._set)

  def __contains__(self, value):
    return value in self._set

  def __iter__(self):
    for bucket in self._buckets:
      for value in bucket:
        yield value

  def __reversed__(self):
    for bucket in reversed(self._buckets):
      for value in reversed(bucket):
        yield value

  def __repr__(self):
    return 'SortedSet(' + repr(list(self)) + ')'

  def _position(self, index):
    if index < 0:
      index += len(self)
    if index < 0 or index >= len(self):
      raise IndexError('SortedSet index out of range')
    # 最大値や末尾付近へのアクセスも高速にする。
    if index < len(self) // 2:
      for b, bucket in enumerate(self._buckets):
        if index < len(bucket):
          return b, index
        index -= len(bucket)
    else:
      index = len(self) - 1 - index
      for b in range(len(self._buckets) - 1, -1, -1):
        size = len(self._buckets[b])
        if index < size:
          return b, size - 1 - index
        index -= size
    raise IndexError('SortedSet index out of range')

  def __getitem__(self, index):
    if isinstance(index, slice):
      start, stop, step = index.indices(len(self))
      if step == 1:
        return list(self.islice(start, stop))
      if step == -1:
        return list(self.islice(stop + 1, start + 1, reverse=True))
      return list(self)[index]
    else:
      b, i = self._position(index)
      return self._buckets[b][i]

  def __delitem__(self, index):
    if isinstance(index, slice):
      removed = self[index]
      self._set.difference_update(set(removed))
      self._build([x for x in self if x in self._set])
    else:
      self.pop(index)

  def add(self, value):
    if value in self._set:
      return
    key = self._key(value)
    if not self._buckets:
      self._buckets.append([value])
    else:
      b = 0
      while b + 1 < len(self._buckets) and not key < self._key(self._buckets[b][-1]):
        b += 1
      bucket = self._buckets[b]
      bucket.insert(self._bisect(bucket, key, True), value)
      if len(bucket) > self._bucket_size * 2:
        self._build(list(self))
    self._set.add(value)

  def _pop(self, b, i):
    value = self._buckets[b].pop(i)
    self._set.remove(value)
    if not self._buckets[b] or len(self) * 2 < self._built_size:
      self._build(list(self))
    return value

  def pop(self, index=-1):
    b, i = self._position(index)
    return self._pop(b, i)

  def discard(self, value):
    if value in self._set:
      self.pop(self.index(value))

  def remove(self, value):
    if value not in self._set:
      raise KeyError(str(value))
    self.discard(value)

  def clear(self):
    self._set.clear()
    self._buckets.clear()
    self._built_size = 0
    self._bucket_size = 16

  def copy(self):
    a = list(self)
    result = SortedSet(a[:0], self.key)
    result._set = self._set.copy()
    result._build(a)
    return result

  def count(self, value):
    return int(value in self._set)

  def bisect_key_left(self, key):
    rank = 0
    for bucket in self._buckets:
      if not self._key(bucket[-1]) < key:
        return rank + self._bisect(bucket, key)
      rank += len(bucket)
    return rank

  def bisect_key_right(self, key):
    rank = 0
    for bucket in self._buckets:
      if key < self._key(bucket[-1]):
        return rank + self._bisect(bucket, key, True)
      rank += len(bucket)
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
    if value not in self._set:
      raise ValueError('value is not in SortedSet')
    lo, hi, step = slice(start, stop).indices(len(self))
    key = self._key(value)
    rank = 0
    for bucket in self._buckets:
      if rank >= hi:
        break
      if rank + len(bucket) > lo and not self._key(bucket[-1]) < key:
        i = max(self._bisect(bucket, key), lo - rank)
        while i < len(bucket) and rank + i < hi:
          if key < self._key(bucket[i]):
            break
          if bucket[i] == value:
            return rank + i
          i += 1
      rank += len(bucket)
    raise ValueError('value is not in SortedSet')

  # [start, stop)を走査。reverse=Trueでも範囲は昇順の添字で指定する。
  def islice(self, start=None, stop=None, reverse=False):
    lo, hi, step = slice(start, stop).indices(len(self))
    if lo >= hi:
      return
    if reverse:
      rank = len(self)
      for bucket in reversed(self._buckets):
        rank -= len(bucket)
        for i in range(min(len(bucket), hi - rank) - 1, max(0, lo - rank) - 1, -1):
          yield bucket[i]
        if rank <= lo:
          break
    else:
      rank = 0
      for bucket in self._buckets:
        for i in range(max(0, lo - rank), min(len(bucket), hi - rank)):
          yield bucket[i]
        rank += len(bucket)
        if rank >= hi:
          break

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
    values = self._set.copy()
    # 空の可変長引数でもCodonがループ変数の型を推論できるようにする。
    for iterable in ((), *iterables):
      values.update(iterable)
    self._set = values
    self._build(sorted(values, key=self.key))
    return self

  def difference_update(self, *iterables):
    values = self._set.copy()
    for iterable in ((), *iterables):
      values.difference_update(set(iterable))
    self._set = values
    self._build([x for x in self if x in values])
    return self

  def intersection_update(self, *iterables):
    values = self._set.copy()
    for iterable in (self._set, *iterables):
      values.intersection_update(set(iterable))
    self._set = values
    self._build([x for x in self if x in values])
    return self

  def symmetric_difference_update(self, other):
    values = self._set.symmetric_difference(set(other))
    self._set = values
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
    return self._set.issubset(set(other))

  def issuperset(self, other):
    return self._set.issuperset(set(other))

  def isdisjoint(self, other):
    return self._set.isdisjoint(set(other))

  def __eq__(self, other):
    if isinstance(other, (SortedSet, set)):
      return self._set == set(other)
    return False

  def __ne__(self, other):
    return not self == other

  def __le__(self, other):
    if isinstance(other, (SortedSet, set)):
      return self.issubset(other)
    raise TypeError('set comparison requires SortedSet or set')

  def __lt__(self, other):
    if isinstance(other, (SortedSet, set)):
      return self._set < set(other)
    raise TypeError('set comparison requires SortedSet or set')

  def __ge__(self, other):
    if isinstance(other, (SortedSet, set)):
      return self.issuperset(other)
    raise TypeError('set comparison requires SortedSet or set')

  def __gt__(self, other):
    if isinstance(other, (SortedSet, set)):
      return self._set > set(other)
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


"""
使用例（SortedSetのクラス定義と一緒にコピーし、codon run -releaseで実行）
s = SortedSet([3, 1, 4, 1])
s.add(2)
print(list(s))                   # [1, 2, 3, 4]
print(s[0], s[-1], s[1:3])        # 1 4 [2, 3]
print(s.bisect_left(3))           # 2: 3未満の要素数
print(s.bisect_right(3))          # 3: 3以下の要素数
print(list(s.irange(2, 3)))       # [2, 3]
print(s.pop())                   # 4: 最大値を削除して返す
s.discard(10)                    # 存在しなくてもエラーにしない
print(list(s | {0, 5}))          # [0, 1, 2, 3, 5]

# 空から作る場合、Codonでは後続のaddなどから要素型を推論させる。
empty = SortedSet()
empty.add(42)
# 型を推論できない場合は、型付きの空リストを渡す。
values: list[int] = []
empty_int = SortedSet(values)

descending = SortedSet([1, 3, 2], key=lambda x: -x)
print(list(descending))          # [3, 2, 1]
"""
