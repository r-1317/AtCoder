import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def tail_4(stack):
  flag = True

  if len(stack) < 4:
    return False

  if stack[-1] != stack[-2]:
    flag = False
  if stack[-1] != stack[-3]:
    flag = False
  if stack[-1] != stack[-4]:
    flag = False

  return flag

def main():
  N = int(input())
  a_list = list(map(int, input().split()))

  stack = []

  ans = N

  for a in a_list:
    stack.append(a)
    if tail_4(stack):
      for _ in range(4):
        stack.pop()
      ans -= 4

  print(ans)

if __name__ == "__main__":
  main()