from icecream import ic
# ic.disable()

# def is_cubic(K):
#   x = K**(1/3)  # x^3 = K

#   # x^3 が K であるか
#   if int(x)**3 == K or (int(x)+1)**3 == K:
#     return True
#   else:
#     return False

# 回文数であるか
def is_palindromic(K):
  K_obverse = str(K)
  K_reverse = K_obverse[::-1]

  if K_obverse == K_reverse:
    return True
  else:
    return False

def main():

  n = int(input())
  ans = 0

  for x in range(1, 1000001):
    
    K  = x**3

    # K が n 以下であるか
    if K <= n:

      # K が回文数であるか
      if is_palindromic(K) :
        ans = K
    
    # K が n 以下でないなら終了
    else:
      break

  print(ans)
  # ic(x)


if __name__ == "__main__":
  main()