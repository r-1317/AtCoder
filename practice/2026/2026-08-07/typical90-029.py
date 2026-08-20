import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

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

"""
使用例（区間和）
seg = SegmentTree(lambda a, b: a + b, lambda: 0, [1, 2, 3, 4])
seg.prod(1, 4)  # 9
seg.set(2, 10)
seg.all_prod()  # 17
"""

def main():
  W, N = map(int, input().split())

  seg = SegmentTree(lambda a, b: max(a, b), lambda: 0, W)

  for _ in range(N):
    l, r = map(int, input().split())
    l -= 1
    r -= 1
    h = seg.prod(l, r+1) + 1
    for i in range(l,r+1):
      seg.set(i, h)
    ic(h)
    print(h)


if __name__ == "__main__":
  main()