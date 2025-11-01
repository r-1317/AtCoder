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
  M = int(input())

  ans_list = [-1]*M  # ans_list[x] に y を格納

  for y in range(M):
    x = y**3
    x %= M
    ans_list[x] = y

  for ans in ans_list:
    # ic(ans)
    print(ans)

if __name__ == "__main__":
  main()