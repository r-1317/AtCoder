n = int(input())
a_list = list(map(int, input().split()))
ans_list = [0]*n
for i in range(n):
  while a_list[i] %2 == 0:
    a_list[i] /= 2
    ans_list[i] += 1

print(min(ans_list))