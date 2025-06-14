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
  n, q = map(int, input().split())

  a_list = list(range(1, n + 1))
  head_index = 0

  for _ in range(q):
    query = list(map(int, input().split()))
    if query[0] == 1:
      p, x = query[1], query[2]
      p -= 1
      p_index = (head_index + p) % n
      a_list[p_index] = x
    elif query[0] == 2:
      p = query[1]
      p -= 1
      p_index = (head_index + p) % n
      ic(a_list[p_index])
      print(a_list[p_index])
    elif query[0] == 3:
      k = query[1]
      head_index += k
      head_index %= n

    # ic(head_index)
    # ic(a_list)



if __name__ == "__main__":
  main()