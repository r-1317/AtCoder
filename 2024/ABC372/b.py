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
  m = int(input())
  
  ans_list = []

  while m:
    for i in range(10, -1, -1):
      if 0 <= m - 3**i:
        m -= 3**i
        ans_list.append(i)
        break
  
  print(len(ans_list))
  print(*ans_list)

if __name__ == "__main__":
  main()