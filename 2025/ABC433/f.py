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
  s_list = list(S)
  N = len(S)

  for i in range(N):
    s_list[i] = int(s_list[i])

  count_list = [0]*10  # Cのcount_listとは別

  for i in range(N):
    s_list[i] = int(s_list[i])

if __name__ == "__main__":
  main()