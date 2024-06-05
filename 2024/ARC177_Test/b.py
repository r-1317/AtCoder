import os

if os.path.basename(__file__) != "Main.py":
  from icecream import ic
else:
  def ic(*args):
    return None

ic.disable() if os.path.basename(__file__) != "Main.py" else None

def main():
  n = int(input())
  t_str = input()

  ans = ""
  tmp_list = ("0", "1")
  tmp = tmp_list[0]
  q_dict = {"0": "A", "1": "B"}

  ic(q_dict[tmp])

  for i in range(n-1, -1, -1):
    if t_str[i] != tmp:
      ans += (q_dict[tmp])*(i+1)
      tmp = tmp_list[(tmp_list.index(tmp)+1)%2]

  print(len(ans))
  print(ans)


if __name__ == "__main__":
  main()