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
  h_list = list(map(int, input().split()))

  ans = 1

  for i in range(n):
    tmp_h = h_list[i]
    dist_list = []
    for j in range(i+1, n):
      if tmp_h == h_list[j]:
        dist_list.append(j-i)

    ic(dist_list)

    for dist in dist_list:
      tmp_ans = 1
      tmp_index = i
      while tmp_index+dist < n and h_list[tmp_index] == h_list[tmp_index+dist]:
        tmp_ans += 1
        tmp_index += dist
      ans = max(ans, tmp_ans)

  print(ans)

if __name__ == "__main__":
  main()