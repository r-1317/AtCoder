import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# AWC0001/e.py から
class AVLTree:
  class _Node:
    __slots__ = ("key", "cnt", "height", "size", "left", "right")
    def __init__(self, key):
      self.key = key
      self.cnt = 1
      self.height = 1
      self.size = 1
      self.left = None
      self.right = None

  def __init__(self):
    self._root = None

  @staticmethod
  def _h(n):
    return n.height if n else 0

  @staticmethod
  def _sz(n):
    return n.size if n else 0

  @classmethod
  def _recalc(cls, n):
    n.height = 1 + max(cls._h(n.left), cls._h(n.right))
    n.size = n.cnt + cls._sz(n.left) + cls._sz(n.right)
    return n

  @classmethod
  def _bal(cls, n):
    return cls._h(n.left) - cls._h(n.right)

  @classmethod
  def _rot_r(cls, y):
    x = y.left
    t2 = x.right
    x.right = y
    y.left = t2
    cls._recalc(y)
    cls._recalc(x)
    return x

  @classmethod
  def _rot_l(cls, x):
    y = x.right
    t2 = y.left
    y.left = x
    x.right = t2
    cls._recalc(x)
    cls._recalc(y)
    return y

  @classmethod
  def _rebalance(cls, n):
    cls._recalc(n)
    b = cls._bal(n)
    if b > 1:
      if cls._bal(n.left) < 0:
        n.left = cls._rot_l(n.left)
      return cls._rot_r(n)
    if b < -1:
      if cls._bal(n.right) > 0:
        n.right = cls._rot_r(n.right)
      return cls._rot_l(n)
    return n

  def add(self, key):
    self._root = self._insert(self._root, key)

  def _insert(self, n, key):
    if n is None:
      return self._Node(key)
    if key == n.key:
      n.cnt += 1
      return self._recalc(n)
    if key < n.key:
      n.left = self._insert(n.left, key)
    else:
      n.right = self._insert(n.right, key)
    return self._rebalance(n)

  def get_min(self):
    n = self._root
    if n is None:
      return None
    while n.left is not None:
      n = n.left
    return n.key

  def get_max(self):
    n = self._root
    if n is None:
      return None
    while n.right is not None:
      n = n.right
    return n.key

  def discard(self, key):
    self._root, removed = self._erase(self._root, key)
    return removed

  def _pop_min(self, n):
    if n.left is None:
      return n.right, n
    n.left, mn = self._pop_min(n.left)
    return self._rebalance(n), mn

  def _erase(self, n, key):
    if n is None:
      return None, False
    if key < n.key:
      n.left, removed = self._erase(n.left, key)
      if not removed:
        return n, False
      return self._rebalance(n), True
    if key > n.key:
      n.right, removed = self._erase(n.right, key)
      if not removed:
        return n, False
      return self._rebalance(n), True

    # key == n.key
    if n.cnt > 1:
      n.cnt -= 1
      return self._recalc(n), True

    if n.left is None:
      return n.right, True
    if n.right is None:
      return n.left, True

    n.right, succ = self._pop_min(n.right)
    n.key, n.cnt = succ.key, succ.cnt
    succ.cnt = 1
    return self._rebalance(n), True

def main():
  H, W, N = map(int, input().split())
  h_w_list = [list(map(int, input().split())) for _ in range(N)]

  current_size = [H, W]
  current_top_left = [1, 1]

  h_w_avl = AVLTree()  # 縦の長さ順で格納しているやつ。(h, w)のタプルを格納
  w_h_avl = AVLTree()  # 横の長さ順で格納しているやつ。(w, h)のタプルを格納

  for i in range(N):
    h, w = h_w_list[i]
    h_w_avl.add((h, w, i))
    w_h_avl.add((w, h, i))

  ans_list = [None]*N  # (x, y) を格納

  for i in range(N):
    max_h_w = h_w_avl.get_max()  # 縦が最も長いもの
    max_w_h = w_h_avl.get_max()  # 横が最も長いもの

    if max_h_w[0] == current_size[0]:  # 縦が現在の長方形のサイズならはめる
      h, w, idx = max_h_w
      ans_list[idx] = current_top_left[:]
      current_top_left[1] += w
      current_size[1] -= w
      # 今入れた要素を削除
      h_w_avl.discard((h, w, idx))
      w_h_avl.discard((w, h, idx))
    else:  # そうでないなら横が最大のはず。最大でないならこのプログラムは破綻する
      w, h, idx = max_w_h
      ans_list[idx] = current_top_left[:]
      current_top_left[0] += h
      current_size[0] -= h
      # 今入れた要素を削除
      h_w_avl.discard((h, w, idx))
      w_h_avl.discard((w, h, idx))

  for row in ans_list:
    print(*row)


if __name__ == "__main__":
  main()