import os

if os.path.basename(__file__) == "Main.py":
  def ic(*args):
    return None
else:
  from icecream import ic

if os.path.basename(__file__) != "Main.py":
  # ic.disable()
  pass

def main():
  pass

if __name__ == "__main__":
  main()