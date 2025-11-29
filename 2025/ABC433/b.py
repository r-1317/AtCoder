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
  a_list = list(map(int, input().split()))

  a_list = [0] + a_list

  for i in range(1, N+1):
    b = -1
    for j in range(i-1, 0, -1):
      if a_list[i] < a_list[j]:
        b = j
        break
    print(b)

if __name__ == "__main__":
  main()