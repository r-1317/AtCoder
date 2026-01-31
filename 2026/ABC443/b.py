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
  N, K = map(int, input().split())

  bean_count = 0

  for i in range(10**8):
    bean_count += N + i
    if bean_count >= K:
      print(i)
      break

if __name__ == "__main__":
  main()