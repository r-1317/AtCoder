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
  n = int(input())
  a_list = list(map(int, input().split()))
  a_list.sort()

  ans_list = []

  for i in range(n):
    if not a_list[i] in ans_list:
      ans_list.append(a_list[i])

  print(len(ans_list))
  print(*ans_list)

if __name__ == "__main__":
  main()