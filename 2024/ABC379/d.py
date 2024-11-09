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
  q = int(input())
  
  sum_t = 0
  pots_list = [float("inf")]*(2*10**5)
  plant_index = 0
  harvest_index = 0

  for i in range(q):
    query = list(map(int, input().split()))
    q_type = query[0]
    if q_type == 1:
      pots_list[plant_index] = sum_t
      plant_index += 1
    elif q_type == 2:
      t = query[1]
      sum_t += t
    elif q_type == 3:
      h = query[1]
      max_t = sum_t - h
      ans = 0
      while pots_list[harvest_index] <= max_t:
        harvest_index += 1
        ans += 1
      print(ans)
      ic(ans)

if __name__ == "__main__":
  main()