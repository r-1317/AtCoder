import os
import heapq

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  T = int(input())

  for _ in range(T):
    S = input()
    char_count = [0]*26
    for c in S:
      char_count[ord(c) - 97] += 1
    hq = []
    heapq.heapify(hq)
    for i, count in enumerate(char_count):
      heapq.heappush(hq, [10**9 - count, i])
    ans = ""
    flag = True
    for i in range(len(S)):
      count, c_id = heapq.heappop(hq)
      count = 10**9 - count
      count_2, c_id_2 = heapq.heappop(hq)
      count_2 = 10**9 - count_2
      ic(count, count_2)
      if len(ans) == 0 or (len(ans) > 0 and ans[-1] != chr(c_id+97)):
        ans += chr(c_id + 97)
        count -= 1
      elif count_2 > 0:
        ans += chr(c_id_2 + 97)
        count_2 -= 1
      else:
        flag = False
        break
      heapq.heappush(hq, [10**9 - count, c_id])
      heapq.heappush(hq, [10**9 - count_2, c_id_2])
    print("Yes" if flag else "No")
    if flag:
      print(ans)

if __name__ == "__main__":
  main()