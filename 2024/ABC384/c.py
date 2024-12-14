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
  points_list = list(map(int, input().split()))
  score_list = [[0, ""] for _ in range(31)]

  for i in range(31):
    x = i+1
    for j in range(5):
      if x >> j & 1:
        score_list[i][0] += points_list[j]
        score_list[i][1] += chr(65+j)

  score_list.sort(key = lambda x: (-x[0], x[1]))

  for i in range(31):
    print(score_list[i][1])



if __name__ == "__main__":
  main()