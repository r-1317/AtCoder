from icecream import ic

def main():
  n, m = map(int, input().split())
  a_list = list(map(int, input().split()))
  x_list = [list(map(int, input().split())) for _ in range(n)]

  for i in range(n):
    for j in range(m):
      a_list[j] -= x_list[i][j]

  # ic(a_list)

  flag = True

  for i in range(m):
    if 0 < a_list[i]:
      flag = False

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()