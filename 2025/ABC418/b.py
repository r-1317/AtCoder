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
  max_filling_rate = 0
  for i in range(len(S) - 2):
    for j in range(i + 2, len(S)):
      if not(S[i] == "t" and S[j] == "t"):
        continue
      filling_rate = S[i+1:j].count("t") / (j - i - 1)
      max_filling_rate = max(max_filling_rate, filling_rate)
  print(max_filling_rate)

if __name__ == "__main__":
  main()