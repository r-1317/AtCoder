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
  a_list = list(map(int, input().split()))

  num_count_list = [0] * 14

  for a in a_list:
    num_count_list[a] += 1

  a = 0
  b = 0

  for num in num_count_list:
    if 2 <= num:
      a += 1
    if 3 <= num:
      b += 1

  ic(a, b)

  print("Yes" if 2 <= a and 1 <= b else "No")

if __name__ == "__main__":
  main()