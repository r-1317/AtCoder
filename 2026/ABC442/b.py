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
  Q = int(input())

  volume = 0
  is_playng = False

  for _ in range(Q):
    a = int(input())
    if a == 1:
      volume += 1
    elif a == 2:
      volume = max(0, volume - 1)
    elif a == 3:
      is_playng = not(is_playng)
    
    ans = volume >= 3 and is_playng
    print("Yes" if ans else "No")

if __name__ == "__main__":
  main()