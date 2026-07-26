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
  M, D = map(int, input().split())
  S = input()

  kanshi_list = [False]*M

  for i, c in enumerate(list(S)):
    if c != "G":
      continue
    for j in range(-D, D+1):
      if 0 <= i+j < M:
        kanshi_list[i+j] = True

  print(kanshi_list.count(False))

if __name__ == "__main__":
  main()