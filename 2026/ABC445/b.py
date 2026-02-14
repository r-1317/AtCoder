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

  s_list = [input() for _ in range(N)]

  max_len = -1
  for s in s_list:
    max_len = max(max_len, len(s))

  for s in s_list:
    k = (max_len - len(s)) // 2
    print("."*k + s + "."*k)

if __name__ == "__main__":
  main()