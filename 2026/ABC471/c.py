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
  N = int(input())
  a_list = list(map(int, input().split())) + [0]  # 長さN+1
  a_list.sort()

  back_pointers = list(range(-1, N))
  back_pointers[0] = None
  forward_pointers = list(range(1, N+2))
  forward_pointers[-1] = None

  current_idx = a_list.index(0)
  pos = 0  # 今いる座標
  ans = 0

  ic(a_list)
  ic(back_pointers)
  ic(forward_pointers)

  for _ in range(N):
    l = a_list[back_pointers[current_idx]] if back_pointers[current_idx] is not None else -10**18
    r = a_list[forward_pointers[current_idx]] if forward_pointers[current_idx] is not None else 10**18

    if pos - l <= r - pos:
      new_current_idx = back_pointers[current_idx]
      ans += pos - l
      new_pos = l
    else:
      new_current_idx = forward_pointers[current_idx]
      ans += r - pos
      new_pos = r

    if back_pointers[current_idx] is not None:
      forward_pointers[back_pointers[current_idx]] = forward_pointers[current_idx]
    if forward_pointers[current_idx] is not None:
      back_pointers[forward_pointers[current_idx]] = back_pointers[current_idx]

    # print()
    # ic(current_idx, pos)
    pos = new_pos
    current_idx = new_current_idx
    # ic(a_list)
    # ic(back_pointers)
    # ic(forward_pointers)
    # ic(current_idx, pos)
  print(ans)

if __name__ == "__main__":
  main()