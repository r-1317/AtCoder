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
  n = int(input())
  s_list = [input() for _ in range(n)]
  # ic(s_list)

  t_set = set()

  for i in range(n):
    for j in range(n):
      if i == j:
        continue
      t = s_list[i] + s_list[j]
      t_set.add(t)

  print(len(t_set))

if __name__ == "__main__":
  main()