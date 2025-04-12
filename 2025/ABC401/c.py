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
  n, k = map(int, input().split())

  a_list = [0]*(n+1)

  shakutori = 0

  for i in range(n+1):
    if i < k:
      a_list[i] = 1
      shakutori += 1
    else:
      a = shakutori % 10**9
      a_list[i] = a
      shakutori -= a_list[i - k]
      shakutori += a

  print(a_list[n])

if __name__ == "__main__":
  main()