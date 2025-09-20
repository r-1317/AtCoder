import os
import heapq
import bisect

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N, Q = map(int, input().split())

  pair_list = [-1]*N

  used_queue = []
  heapq.heapify(used_queue)

  ans = 0

  for _ in range(Q):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    if len(used_queue) == 0:
      pair_list[a] = b
      pair_list[b] = a
      heapq.heappush(used_queue, (a))
      heapq.heappush(used_queue, (b))
      print("Yes")
    else:
      flag = True
      a_right_idx = bisect.bisect(used_queue, a)
      a_left_idx = a_right_idx - 1

      if a_right_idx == len(used_queue):
        right_used = 0
      
      if a_left_idx == -1:
        left_used = len(used_queue) - 1

      a_right = used_queue[a_right_idx]
      a_left = used_queue[a_left_idx]

      if not(pair_list[a_left] == a_right and pair_list[a_right] == a_left):
        flag = False

      new_a_left = min(a_left, a_right)
      new_a_right = max(a_left, a_right)

      a_x = 1 if a_left < a < a_right else 0
      b_x = 1 if a_left < b < a_right else 0

      if a_x == b_x:
        flag = True
        pair_list[a] = b
        pair_list[b] = a
        heapq.heappush(used_queue, (a))
        heapq.heappush(used_queue, (b))
      
      print("Yes" if flag else "No")

  # print(ans)




if __name__ == "__main__":
  main()