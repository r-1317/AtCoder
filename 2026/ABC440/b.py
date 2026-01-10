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
  t_list = list(map(int, input().split()))

  h_list = list(range(1, N+1))

  h_list.sort(key=lambda x: t_list[x-1])

  print(*h_list[:3])

if __name__ == "__main__":
  main()