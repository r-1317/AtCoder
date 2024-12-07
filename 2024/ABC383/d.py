import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# https://qiita.com/takayg1/items/3769ab4cc62a231f4259
def eratosthenes_sieve(n):
  is_prime = [True]*(n + 1)
  is_prime[0] = is_prime[1] = False
  for p in range(2, n + 1):
    if is_prime[p]:
      for q in range(2*p, n + 1, p):
        is_prime[q] = False
  return is_prime

def main():
  n = int(input())
  ans = 0

  prime_list = []

  is_prime_list = eratosthenes_sieve(10**6)

  for i in range(10**6):
    if is_prime_list[i]:
      prime_list.append(i)

  ic(len(prime_list))

  for prime in prime_list:
    if prime**8 <= n:
      ans += 1

  for i in range(len(prime_list)):
    for j in range(i+1, len(prime_list)):
      if prime_list[i]**2 * prime_list[j]**2 <= n:
        ans += 1
      else:
        break

  print(ans)

if __name__ == "__main__":
  main()