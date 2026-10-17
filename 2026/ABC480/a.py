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
  S_list = [(input()) for _ in range(2)]

  if sorted([S_list[0][0], S_list[1][1]]) == ["A", "D"] or sorted([S_list[0][1], S_list[1][0]]) == ["A", "D"]:
    print("No")
  else:
    print("Yes")

if __name__ == "__main__":
  main()