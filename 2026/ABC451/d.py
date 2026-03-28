import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

good_int_set = set()

pows_list = [2**i for i in range(30)]
keta_list = [len(str(pows_list[i])) for i in range(30)]
ic(keta_list)

def dfs(x):
  if x > 10**9:
    return None
  good_int_set.add(x)

  for i in range(len(pows_list)):
    p = pows_list[i]
    keta = keta_list[i]

    new_x = x
    new_x *= 10**keta
    new_x += p
    dfs(new_x)

def main():
  N = int(input())


  for i in range(len(pows_list)):
    p = pows_list[i]
    keta = keta_list[i]

    new_x = 0
    new_x *= 10**keta
    new_x += p
    dfs(new_x)

  good_int_list = list(good_int_set)
  good_int_list.sort()

  print(good_int_list[N-1])


if __name__ == "__main__":
  main()