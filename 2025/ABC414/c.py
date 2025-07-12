import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

NUMS = "0123456789"

def make_palindromes(length, current):
  if length % 2 == 0:
    if len(current) == length // 2:
      return current + current[::-1]
  else:
    if len(current) == length // 2 + 1:
      return current + current[-2::-1]

  palindromes = []
  for num in NUMS:
    new_current = current + num
    palindromes.extend(make_palindromes(length, new_current))

def get_palindromes():
  p_list = []
  for i in range(1, 12):
    current_p_list = make_palindromes(i, "")

    for p in current_p_list:
      if p[0] != '0':
        p_list.append(int(p))

def main():
  A = int(input())
  N = int(input())

if __name__ == "__main__":
  main()