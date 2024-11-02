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
  q_r_list = [list(map(int, input().split())) for _ in range(n)]
  q = int(input())
  t_d_list = [list(map(int, input().split())) for _ in range(q)]

  for t,d in t_d_list:
    q, r = q_r_list[t-1]
    ans = d + (r - d % q)
    if r < d % q:
      ans += q
    print(ans)

if __name__ == "__main__":
  main()