def main():
  s = input()

  letter_1 = s[0].isupper()
  other_letter = s[1:].islower()

  if letter_1 and other_letter:
    print("Yes")
  elif len(s) == 1 and letter_1:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()