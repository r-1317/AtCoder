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
  s_list = [(input().lower()) for _ in range(N)]
  ic(s_list)
  count_dict = dict()

  for s in s_list:
    if not s in count_dict:
      count_dict[s] = 1
    else:
      count_dict[s] += 1

  ans = 0

  for s in s_list:
    ans = max(ans, count_dict[s])

  print(ans)

if __name__ == "__main__":
  main()