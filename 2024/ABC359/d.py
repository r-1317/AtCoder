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
  s = input()

  s_list = [0]*n

  for i in range(n):
    if s[i] == "A":
      s_list[i] = 1
    elif s[i] == "B":
      s_list[i] = -1 

  ic(s_list)

  ans = 0

  for i in range(n-k+1):
    tmp_list = [False]*(k//2 + k%2)
    ic(s_list[i:i+k])
    for j in range(len(tmp_list)):
      tmp_list[j] = (s_list[i+j]*s_list[i+k-1-j]) != -1
    ic(tmp_list)
    ic(not all(tmp_list))
    if not all(tmp_list):
      ans += 1

  print(ans%998244353)

if __name__ == "__main__":
  main()