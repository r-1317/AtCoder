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
  N, M = map(int, input().split())
  a_list = list(map(int, input().split()))

  total_len = sum(a_list)
  total_mod = total_len % M

  ans = 0
  current_mod = 0
  mod_list = [0]*M
  mod_idx_list = [-1]*N

  # まずは1週
  for i in range(N):
    ic(i, mod_list[current_mod])
    ans += mod_list[current_mod]
    mod_list[current_mod] += 1
    mod_idx_list[i] = current_mod
    current_mod = (current_mod + a_list[i]) % M
    ic(mod_list)

  # 2週目で答えを出す
  for i in range(N):
    # mod_list[(total_mod + current_mod) % M] -= 1
    mod_list[mod_idx_list[i]] -= 1
    ic(i, mod_list[current_mod])
    ans += mod_list[current_mod]
    current_mod = (current_mod + a_list[i]) % M
    ic(mod_list)

  print(ans)

if __name__ == "__main__":
  main()