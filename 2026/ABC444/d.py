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
  N = int(input())
  a_list = list(map(int, input().split()))

  imos_list = [0]*10**6

  for a in a_list:
    ic(a)
    imos_list[a-1] += 1  # その桁までで止まる数
  
  ans_list = []

  current = N
  kurikoshi = 0

  # ic(ans_list[:10])
  # ic(imos_list[:31])

  for i in range(len(imos_list)):
    ans_list.append((current + kurikoshi) % 10)
    kurikoshi = (current + kurikoshi) // 10
    current -= imos_list[i]

  while kurikoshi:
    ans_list.append(kurikoshi%10)
    kurikosi //= 10

  # ic(ans_list)
  
  while ans_list[-1] == 0:
    ans_list.pop()

  ans_list.reverse()
  # ic(ans_list)

  print(*ans_list, sep="")

if __name__ == "__main__":
  main()