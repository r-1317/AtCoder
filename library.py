# Union-Find
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


# NxNの盤面を表現するビットボード 
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