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
  N, Q = map(int, input().split())

  adj_list = [[None, None] for _ in range(N*2)]  # [親,子], N番目以降のiは山i-Nの土台

  for i in range(N):
    adj_list[i][0] = i+N
    adj_list[i+N][1] = i

  for _ in range(Q):
    c, p = map(int, input().split())
    c -= 1
    p -= 1

    c_parent = adj_list[c][0]

    adj_list[c_parent][1] = None
    adj_list[c][0] = p
    adj_list[p][1] = c

  ans_list = [0]*N

  for i in range(N):
    current_node = i+N

    while adj_list[current_node][1] is not None:
      ans_list[i] += 1
      current_node = adj_list[current_node][1]

  print(*ans_list)


if __name__ == "__main__":
  main()