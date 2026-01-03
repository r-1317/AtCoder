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
  N = int(input())
  
  count_list = [0]*(10**7 + 1)

  for y in range(1, 3164):
    for x in range(1, y):
      m = x**2 + y**2
      if m > N:
        continue
      count_list[m] += 1

  # 集計
  gool_list = []
  for i in range(1, N+1):
    if count_list[i] == 1:
      gool_list.append(i)

  print(len(gool_list))
  print(*gool_list)

if __name__ == "__main__":
  main()