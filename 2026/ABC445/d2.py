import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  H, W, N = map(int, input().split())
  入力_h_w_list = [list(map(int, input().split())) for _ in range(N)]

  current_size = [H, W]
  current_top_left = [1, 1]

  # h_w_avl = AVLTree()  # 縦の長さ順で格納しているやつ。(h, w)のタプルを格納
  # w_h_avl = AVLTree()  # 横の長さ順で格納しているやつ。(w, h)のタプルを格納

  h_w_list = [None]*N
  w_h_list = [None]*N
  is_used_list = [False]*N

  for i in range(N):
    h, w = 入力_h_w_list[i]
    # h_w_avl.add((h, w, i))
    # w_h_avl.add((w, h, i))
    h_w_list[i] = (h, w, i)
    w_h_list[i] = (w, h, i)

  h_w_list.sort()
  w_h_list.sort()

  ic(h_w_list)
  ic(w_h_list)

  ans_list = [None]*N  # (x, y) を格納

  for i in range(N):
    # max_h_w = h_w_avl.get_max()  # 縦が最も長いもの
    # max_w_h = w_h_avl.get_max()  # 横が最も長いもの
    while True:
      max_h_w = h_w_list[-1]
      if not is_used_list[max_h_w[2]]:
        break
      h_w_list.pop()
    while True:
      max_w_h = w_h_list[-1]
      if not is_used_list[max_w_h[2]]:
        break
      w_h_list.pop()

    if max_h_w[0] == current_size[0]:  # 縦が現在の長方形のサイズならはめる
      h, w, idx = max_h_w
      ans_list[idx] = current_top_left[:]
      current_top_left[1] += w
      current_size[1] -= w
      # # 今入れた要素を削除
      # h_w_avl.discard((h, w, idx))
      # w_h_avl.discard((w, h, idx))
    else:  # そうでないなら横が最大のはず。最大でないならこのプログラムは破綻する
      w, h, idx = max_w_h
      ans_list[idx] = current_top_left[:]
      current_top_left[0] += h
      current_size[0] -= h
      # # 今入れた要素を削除
      # h_w_avl.discard((h, w, idx))
      # w_h_avl.discard((w, h, idx))
    # 今入れた要素を使用済みにする
    is_used_list[idx] = True

  ic(ans_list)

  for row in ans_list:
    print(*row)


if __name__ == "__main__":
  main()