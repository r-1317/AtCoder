import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# https://qiita.com/ytaki0801/items/cc58da6eafd3ec4d91ba
x = 10**7
a = [True] * (x+1)
a[1], r = False, []

for i in range(1, x+1):
  if a[i]:
    if i <= x**0.5:
      for j in range(i*i, x+1, i):
        a[j] = False
    r += [i]

ic(len(r))

def is_valid(S, str_p):
  if len(S) != len(str_p):
    return False

  num_to_chr = [""]*10
  chr_to_num = [-1]*26

  for i in range(len(S)):
    chr = S[i]
    num = int(str_p[i])
    if (num_to_chr[num] and num_to_chr[num] != chr) or (chr_to_num[ord(chr) - 97] > -1 and chr_to_num[ord(chr) - 97] != num):
      return False

    num_to_chr[num] = chr
    chr_to_num[ord(chr) - 97] = num

  return True

def main():
  S = input()
  prime_list = r

  ans = -1
  for p in prime_list:
    str_p = str(p)
    if is_valid(S, str_p):
      ans = p
      break

  print(ans)

if __name__ == "__main__":
  main()