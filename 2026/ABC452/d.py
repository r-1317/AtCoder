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
  S = input()
  T = input()

  N = len(S)

  cum_sum_list = [[0]*26 for _ in range(N)]

  cum_sum_list[0][ord(S[0])-97] += 1

  for i in range(1, N):
    s = S[i]
    for j in range(26):
      cum_sum_list[i][j] = cum_sum_list[i-1][j]
    cum_sum_list[i][ord(s)] += 1

  

if __name__ == "__main__":
  main()