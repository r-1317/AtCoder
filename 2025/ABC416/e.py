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
  adj_matrix = [[0] * N for _ in range(N)]
  for _ in range(M):
    u, v, c = map(int, input().split())
    adj_matrix[u - 1][v - 1] = c
    adj_matrix[v - 1][u - 1] = c

  

if __name__ == "__main__":
  main()