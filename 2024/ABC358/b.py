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
  n, a = map(int, input().split())
  t_list = list(map(int, input().split()))

  time = 0

  for i in range(n):
    if time < t_list[i]:
      time = t_list[i]

    time += a

    print(time)

if __name__ == "__main__":
  main()