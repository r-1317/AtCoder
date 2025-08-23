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
  s_list = [input().strip() for _ in range(200)]
  total_score = 0

  for s in s_list:
    if s[0] != "[":
      total_score += int(s)

  ic(total_score)

if __name__ == "__main__":
  main()