from icecream import ic

def main():
  keyboard_inf = "wbwbwwbwbwbw"*18
  w, b = map(int, input().split())

  length = w+b

  flag = False

  for i in range(12):
    keyboad = keyboard_inf[i:length+i]
    num_w = keyboad.count("w")
    num_b = keyboad.count("b")

    # ic(keyboad)
    # ic(num_w)
    # ic(num_b)

    if w == num_w and b == num_b:
      flag = True
      break

  if flag:
    print("Yes")
  else:
    print("No")


if __name__ == "__main__":
  main()