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
  S = input()

  box_index_list = []
  for i in range(len(S)):
    if S[i] == "#":
      box_index_list.append(i+1)

  ic(box_index_list)

  for i in range(len(box_index_list)//2):
    print(f"{box_index_list[i*2]},{box_index_list[(i*2+1)]}")

if __name__ == "__main__":
  main()