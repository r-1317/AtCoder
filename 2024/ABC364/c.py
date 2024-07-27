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
  n, a_lim, b_lim = map(int, input().split())
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))

  a_list.sort(reverse=True)
  b_list.sort(reverse=True)

  a_ans = 0
  tmp = 0
  for i in range(n):
    tmp += a_list[i]
    a_ans = i+1
    if a_lim < tmp:
      break

  ic(a_ans)

  b_ans = 0
  tmp = 0
  for i in range(n):
    tmp += b_list[i]
    b_ans += 1
    if b_lim < tmp:
      break

  ic(b_ans)

  print(min(a_ans, b_ans))

if __name__ == "__main__":
  main()