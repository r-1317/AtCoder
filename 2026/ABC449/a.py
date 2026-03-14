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
  D = int(input())

  print((D*0.5)**2*3.14159265358979323846264)

if __name__ == "__main__":
  main()