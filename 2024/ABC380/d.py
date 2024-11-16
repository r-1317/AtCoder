import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 折り返し地点を求める  効率化の余地あり
def find_hinge(index, n):  # 今思えばhingeという名前は適切ではない
  hinge = n
  while 2*hinge-1 < index:
    hinge *= 2
  return hinge

def main():
  s_list = list(input())
  q = int(input())
  k_list = list(map(int, input().split()))

  n = len(s_list) 
  ans_list = [""]*q
  # hinge_list = []  # 大文字・小文字が逆転する境目のindex

  for i in range(q):
    k = k_list[i]-1
    c = s_list[k%n]
    index = k
    count = 0

    hinge = find_hinge(index, n)
    ic(hinge)

    while n-1 < index:
      index -= hinge
      count += 1
      hinge = find_hinge(index, n)
      ic(hinge)

    count %= 2

    if count and c.islower():
      ans_list[i] = c.upper()
    elif count and c.isupper():
      ans_list[i] = c.lower()
    else:
      ans_list[i] = c

  ic(ans_list)
  print(*ans_list)

if __name__ == "__main__":
  main()