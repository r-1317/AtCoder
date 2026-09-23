import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def list_xor(group_list):
  x = 0
  for g in group_list:
    x = x ^ g

  return x

def dfs(N, a_list, i, xor_set, group_list):
  if i == N:
    xor_set.add(list_xor(group_list))
    return None

  for j in range(N):
    new_group_list = group_list[:]
    new_group_list[j] += a_list[i]

    # xor_set.add(list_xor(group_list))
    dfs(N, a_list, i + 1, xor_set, new_group_list)

    if new_group_list[j] == a_list[i]:  # この先はすべて空なので結果が同じになる
      break

  return None


def main():
  N = int(input())
  a_list = list(map(int, input().split()))

  group_list = [0]*N
  xor_set = set()

  dfs(N, a_list, 0, xor_set, group_list)

  print(len(xor_set))

if __name__ == "__main__":
  main()