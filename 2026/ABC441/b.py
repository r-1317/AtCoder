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
  takahashi_set = set(list(input()))
  aoki_set = set(list(input()))
  Q = int(input())

  for _ in range(Q):
    w_list = list(input())
    lang = "Unknown"
    for c in w_list:
      is_takahashi = c in takahashi_set
      is_aoki = c in aoki_set
      if is_takahashi and is_aoki:
        continue
      if is_takahashi:
        lang = "Takahashi"
        break
      elif is_aoki:
        lang = "Aoki"

    ic(lang)
    print(lang)

if __name__ == "__main__":
  main()