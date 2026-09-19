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

  top3 = [-10**9]*3  # 数でいうと降順

  for a in a_list:
    top3.append(a)
    top3.sort(reverse=True)
    top3.pop()
    if top3[2] < 0:
      continue
    ic(top3[2])
    print(top3[2])

if __name__ == "__main__":
  main()