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
  stack = []

  flag = True

  for i in range(len(s)):
    # 左側の括弧の場合
    if s[i] == "(":
      stack.append("(")
    elif s[i] == "[":
      stack.append("[")
    elif s[i] == "<":
      stack.append("<")
    # 右側の括弧の場合
    if not stack:  # スタックが空の場合は不正
      flag = False
      break
    elif s[i] == ")":
      if stack[-1] != "(":
        flag = False
        break
      stack.pop()
    elif s[i] == "]":
      if stack[-1] != "[":
        flag = False
        break
      stack.pop()
    elif s[i] == ">":
      if stack[-1] != "<":
        flag = False
        break
      stack.pop()

  if stack:
    flag = False

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()