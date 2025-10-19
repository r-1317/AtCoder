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
  N, K = map(int, input().split())
  S = input()

  arr = []  # []"部分文字列", 個数]

  for i in range(N - K + 1):
    sub_s = S[i:i+K]
    flag = False
    for a in arr:
      if sub_s == a[0]:
        a[1] += 1
        flag = True
        break
    if not flag:
      arr.append([sub_s, 1])

  max_count = -1

  for a in arr:
    max_count = max(max_count, a[1])

  print(max_count)

  ic(max_count)

  subs_list = []

  for a in arr:
    if a[1] == max_count:
      subs_list.append(a[0])

  ic(subs_list)

  subs_list.sort

  ic(subs_list)
  ic(sorted(subs_list))

  print(*sorted(subs_list))

if __name__ == "__main__":
  main()