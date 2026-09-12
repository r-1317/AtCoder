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


# 新版SortedSet (旧版はABC370の提出履歴から探せば見つかると思う)
# 配列で管理するtreap + 値からノード番号へのdict。CPython / Codon両対応。
# 要素は同じ型でハッシュ可能であること。格納中に値やkeyの結果を変えない。
# len: O(1)、in / count: 平均O(1)
# add / discard / remove / pop / 添字 / bisect / index: 期待O(log N)
# 走査・コピー: O(N)、連続範囲の走査: 期待O(log N + 出力数)。
# 初期化: O(N log N)。乱数は64bit xorshift(13, 7, 17)、固定の非ゼロseed。
# 削除したノード領域は再利用する。メモリはclear / 再構築以降の最大要素数に比例。
# keyは挿入時に計算して保存。比較演算の相手はSortedSetまたはset。
# Codonで空集合を作るときはNoneを渡さず、SortedSet()か型付き空リストを使う。
# 内部用_check / _reset、pickle、frozensetとの比較は対象外。
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
