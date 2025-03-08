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
  q = int(input())
  
  x_list = [0]*100

  for _ in range(q):
    query = list(map(int, input().split()))
    if query[0] == 1:
      x = query[1]
      x_list.append(x)
    elif query[0] == 2:
      x = x_list.pop()
      print(x)

if __name__ == "__main__":
  main()