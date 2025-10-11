import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def f(x):
  x = list(str(x))
  sum_d = 0

  for i in x:
    sum_d += int(i)

  return sum_d

def main():
  N = int(input())

  a_list = [1]

  for i in range(1, 101):
    a = 0
    for j in range(i):
      a += f(a_list[j])
    a_list.append(a)

  print(a_list[N])


if __name__ == "__main__":
  main()