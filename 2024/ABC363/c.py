import os
import sys
import math

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

pattern_set = set()

IsPalindrome_dict = {}

def IsPalindrome(s):
  if s in IsPalindrome_dict:
    return IsPalindrome_dict[s]

  n = len(s)
  for i in range(n//2):
    if s[i] != s[n-i-1]:
      IsPalindrome_dict[s] = False
      return False

  IsPalindrome_dict[s] = True
  return True

def FindPalindrome(s_list, k):
  flag = False
  for i in range(len(s_list)-k+1):
    if IsPalindrome(s_list[i:i+k]):
      flag = True
      break
  
  return flag

def count_alphabet(s):
  flag = True
  for i in range(26):
    if 2 <= s.count(chr(97+i)):
      flag = False
      break

  return flag

def main():
  n, k = map(int, input().split())
  s = input()

  if count_alphabet(s):
    print(math.factorial(n))
    sys.exit()

  s_list = list(s)

  ic(s_list)

  tmp_list = [[] for _ in range(n)]

  ic(tmp_list)

  tmp_str_list = [""]*n

  # sを並べ替えて得られる文字列を総当り
  # len(s)は最大で10なので、10回のループで全てのパターンを網羅できる
  for i_0 in range(n):
    tmp_list[0] = s_list[:]
    tmp_str_list[0] = tmp_list[0][i_0]
    tmp_list[0][0], tmp_list[0][i_0] = tmp_list[0][i_0], tmp_list[0][0]

    for i_1 in range(1,n):
      tmp_list[1] = tmp_list[0][:]
      tmp_str_list[1] = tmp_str_list[0] + tmp_list[1][i_1]
      tmp_list[1][1], tmp_list[1][i_1] = tmp_list[1][i_1], tmp_list[1][1]
      if len(tmp_str_list[1]) == n:
        pattern_set.add(tmp_str_list[1])
        continue

      for i_2 in range(2,n):
        tmp_list[2] = tmp_list[1][:]
        tmp_str_list[2] = tmp_str_list[1] + tmp_list[2][i_2]
        tmp_list[2][2], tmp_list[2][i_2] = tmp_list[2][i_2], tmp_list[2][2]
        if len(tmp_str_list[2]) == n:
          pattern_set.add(tmp_str_list[2])
          continue

        for i_3 in range(3,n):
          tmp_list[3] = tmp_list[2][:]
          tmp_str_list[3] = tmp_str_list[2] + tmp_list[3][i_3]
          tmp_list[3][3], tmp_list[3][i_3] = tmp_list[3][i_3], tmp_list[3][3]
          if len(tmp_str_list[3]) == n:
            pattern_set.add(tmp_str_list[3])
            continue

          for i_4 in range(4,n):
            tmp_list[4] = tmp_list[3][:]
            tmp_str_list[4] = tmp_str_list[3] + tmp_list[4][i_4]
            tmp_list[4][4], tmp_list[4][i_4] = tmp_list[4][i_4], tmp_list[4][4]
            if len(tmp_str_list[4]) == n:
              pattern_set.add(tmp_str_list[4])
              continue

            for i_5 in range(5,n):
              tmp_list[5] = tmp_list[4][:]
              tmp_str_list[5] = tmp_str_list[4] + tmp_list[5][i_5]
              tmp_list[5][5], tmp_list[5][i_5] = tmp_list[5][i_5], tmp_list[5][5]
              if len(tmp_str_list[5]) == n:
                pattern_set.add(tmp_str_list[5])
                continue

              for i_6 in range(6,n):
                tmp_list[6] = tmp_list[5][:]
                tmp_str_list[6] = tmp_str_list[5] + tmp_list[6][i_6]
                tmp_list[6][6], tmp_list[6][i_6] = tmp_list[6][i_6], tmp_list[6][6]
                if len(tmp_str_list[6]) == n:
                  pattern_set.add(tmp_str_list[6])
                  continue

                for i_7 in range(7,n):
                  tmp_list[7] = tmp_list[6][:]
                  tmp_str_list[7] = tmp_str_list[6] + tmp_list[7][i_7]
                  tmp_list[7][7], tmp_list[7][i_7] = tmp_list[7][i_7], tmp_list[7][7]
                  if len(tmp_str_list[7]) == n:
                    pattern_set.add(tmp_str_list[7])
                    continue

                  for i_8 in range(8,n):
                    tmp_list[8] = tmp_list[7][:]
                    tmp_str_list[8] = tmp_str_list[7] + tmp_list[8][i_8]
                    tmp_list[8][8], tmp_list[8][i_8] = tmp_list[8][i_8], tmp_list[8][8]
                    if len(tmp_str_list[8]) == n:
                      pattern_set.add(tmp_str_list[8])
                      continue

                    for i_9 in range(9,n):
                      tmp_list[9] = tmp_list[8][:]
                      tmp_str_list[9] = tmp_str_list[8] + tmp_list[9][i_9]
                      tmp_list[9][9], tmp_list[9][i_9] = tmp_list[9][i_9], tmp_list[9][9]
                      if len(tmp_str_list[9]) == n:
                        pattern_set.add(tmp_str_list[9])
                        continue

  # ic(len(list(pattern_set)))

  ans = 0

  for pattern in pattern_set:
    # ic(pattern)
    if not FindPalindrome(pattern, k):
      ans += 1

  print(ans)


if __name__ == "__main__":
  main()