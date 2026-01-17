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
  N, K, X = map(int, input().split())
  a_list = list(map(int, input().split()))
  a_list.sort(reverse=True)
  a_list = [0]*(N-K) + a_list[N-K:]
  ic(a_list)

  ans = 0
  nokori = X

  for a in a_list:
    if nokori <= 0:
      break
    ans += 1
    nokori -= a
  
  ic(nokori)
  
  if ans > N:
    ans = -1
  elif nokori > 0:
    ans = -1

  print(ans)

if __name__ == "__main__":
  main()