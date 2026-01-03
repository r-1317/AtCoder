import os
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def happy(m):
  m_list = list(map(int, list(str(m))))
  # ic(m_list)

  h = 0
  for md in m_list:
    h += md**2
  
  return h

def main():
  N = int(input())
  happy_set = set()
  current_num = N
  ic(list(map(int, list(str(N)))))

  for i in range(10**6):
    current_num = happy(current_num)
    if current_num == 1:
      print("Yes")
      sys.exit()
    elif current_num in happy_set:
      print("No")
      sys.exit()
    happy_set.add(current_num)
  print("No")

if __name__ == "__main__":
  main()