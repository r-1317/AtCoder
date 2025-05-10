import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def choice(n, m):
  ans = 1
  for i in range(m):
    ans *= n-i
    ans /= i+1
  return ans

def main():
  pass

if __name__ == "__main__":
  main()