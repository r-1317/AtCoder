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
  s = input()
  n = len(s)

  s_list = [0] * n
  for i in range(n):
    s_list[i] = int(s[i])

  ans = 0

  for i in range(n):
    if i != 0:
      d = (s_list[i-1] - s_list[i]) % 10
      ans += d
    ans += 1
  ans += s_list[n-1]

  print(ans)


if __name__ == "__main__":
  main()