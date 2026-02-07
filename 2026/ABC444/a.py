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
  N = int(input())
  N_set_list = list(set(list(str(N))))

  print("Yes" if len(N_set_list) == 1 else "No")

if __name__ == "__main__":
  main()