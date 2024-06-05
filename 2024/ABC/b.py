import os

if os.path.basename(__file__) != "Main.py":
  from icecream import ic
else:
  def ic(*args):
    return None

# ic.disable() if os.path.basename(__file__) != "Main.py" else None

def main():
  pass

if __name__ == "__main__":
  main()