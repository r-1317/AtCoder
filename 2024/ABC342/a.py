import statistics as st

def main():
  s = (input())
  same = st.mode(s[:3])


  for i in range(len(s)):
    if s[i] != same:
      print(i+1)


if __name__ == "__main__":
  main()