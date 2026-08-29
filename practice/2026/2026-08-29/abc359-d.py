import os
from collections import defaultdict

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def is_palindrome(s):
  return s == s[::-1]

def main():
  N, K = map(int, input().split())
  S = input()

  dp_dict = defaultdict(int)

if __name__ == "__main__":
  main()