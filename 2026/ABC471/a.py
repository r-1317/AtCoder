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
  A, B = map(int, input().split())

  if A + B == 9 or A - B == 9 or A * B == 9 or (A // B == 9 and A % B == 0):
    print("Nine")
  else:
    print("Nein")

if __name__ == "__main__":
  main()