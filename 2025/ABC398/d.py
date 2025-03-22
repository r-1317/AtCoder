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
  n, r, c = map(int, input().split())
  takahashi_x, takahashi_y = r, c
  ic(takahashi_x, takahashi_y)
  s_list = list(input())

  center_x, center_y = 0, 0
  smoke_set = set()
  smoke_set.add((center_x, center_y))

  d_dict = {
    "W": [0, 1],
    "E": [0, -1],
    "S": [-1, 0],
    "N": [1, 0]
  }

  ans_list = [0]*n

  for i, s in enumerate(s_list):
    center_x += d_dict[s][0]
    center_y += d_dict[s][1]
    takahashi_x += d_dict[s][0]
    takahashi_y += d_dict[s][1]
    smoke_set.add((center_x, center_y))
    if (takahashi_x, takahashi_y) in smoke_set:
      ans_list[i] = 1

    # ic(s)
    # ic(center_x, center_y, takahashi_x, takahashi_y)
    # ic(smoke_set)

  print(*ans_list, sep="")


if __name__ == "__main__":
  main()