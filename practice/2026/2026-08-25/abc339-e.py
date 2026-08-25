import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

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

def main():
  N, D = map(int, input().split())
  a_list = list(map(int, input().split()))

  seg = SegmentTree(lambda a, b: max(a, b), lambda: 0, [0]*(5*10**5 + 1))

  for i, a in enumerate(a_list):
    l = max(0, a - D)
    r = min(5*10**5, a + D)
    max_num = seg.prod(l, r+1)
    seg.set(a, max_num + 1)
    ic(l, r, max_num)

  print(seg.all_prod())

if __name__ == "__main__":
  main()