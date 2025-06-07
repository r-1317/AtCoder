import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 巡回左シフト
def rotate(s_list, start_index, end_index):
  rotated_part = s_list[start_index:end_index + 1]
  head = rotated_part[0]
  rotated_part = rotated_part[1:] + [head]
  return s_list[:start_index] + rotated_part + s_list[end_index + 1:]

def main():
  t = int(input())
  for _ in range(t):
    n = int(input())
    s_list = list(input())

    start_index = 0
    for i in range(n-1):
      if ord(s_list[i]) > ord(s_list[i+1]):
        start_index = i
        break

    end_index = n - 1
    for i in range(start_index, n-1):
      if ord(s_list[start_index]) < ord(s_list[i+1]):
        end_index = i
        break

    rotated_list = rotate(s_list, start_index, end_index)
    ic(rotated_list)
    print(*rotated_list, sep='')


if __name__ == "__main__":
  main()