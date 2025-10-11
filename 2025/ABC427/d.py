import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

truns = "ABABABABABABABABABABABABABABABABABABABABABABABABABABABABABAB"

def main():
  T = int(input())

  for _ in range(T):
    N, M, K = map(int, input().split())
    S = input()
    adj_list = [[] for _ in range(N)]
    reverced_adj_list = [[] for _ in range(N)]
    for _ in range(M):
      u, v = map(int, input().split())
      u -= 1
      v -= 1
      adj_list[u].append(v)
      reverced_adj_list[v].append(u)

    dp_list = [[""]*N for _ in range(K*2 + 1)]
    for j in range(N):
      dp_list[K*2][j] = S[j]

    for i in range(K*2 - 1, -1, -1):
      t = truns[i]
      # ic(t)
      for j in range(N):
        flag = False
        for a in adj_list[j]:
          if dp_list[i+1][a] == t:
            flag = True
            break
        dp_list[i][j] = t if flag else truns[i+1]
  
    ans = ""
    if dp_list[0][0] == "A":
      ans = "Alice"
    else:
      ans = "Bob"
    print(ans)
    ic(ans)

    # ic(dp_list)

if __name__ == "__main__":
  main()