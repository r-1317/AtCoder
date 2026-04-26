import sys


def main() -> None:
  input = sys.stdin.readline

  r = int(input())
  departures = [list(map(int, input().split())) for _ in range(r)]
  sidings = [[] for _ in range(r)]

  turns = []

  # 1) Move all cars from departure i to siding i in one turn.
  first_turn = []
  for i in range(r):
    k = len(departures[i])
    if k > 0:
      moved = departures[i][-k:]
      departures[i] = departures[i][:-k]
      sidings[i] = moved + sidings[i]
      first_turn.append((0, i, i, k))
  turns.append(first_turn)

  # 2) Move cars one by one from sidings to target departures (by tens digit).
  #    Order inside departures is ignored in this phase.
  total_cars = 10 * r
  for _ in range(total_cars):
    src = -1
    for j in range(r):
      if sidings[j]:
        src = j
        break

    car = sidings[src][0]
    sidings[src] = sidings[src][1:]

    dst = car // 10
    departures[dst].append(car)
    turns.append([(1, dst, src, 1)])

  # 3) For each departure line, reorder by moving cars to sidings by ones digit,
  #    then restore from siding 0..r-1.
  for dep in range(r):
    # Move out 10 cars from tail one by one.
    for _ in range(10):
      car = departures[dep].pop()
      sid = car % 10
      sidings[sid] = [car] + sidings[sid]
      turns.append([(0, dep, sid, 1)])

    # Move back in siding index order.
    for sid in range(r):
      car = sidings[sid][0]
      sidings[sid] = sidings[sid][1:]
      departures[dep].append(car)
      turns.append([(1, dep, sid, 1)])

  # Output
  print(len(turns))
  for ops in turns:
    print(len(ops))
    for t, i, j, k in ops:
      print(t, i, j, k)

if __name__ == "__main__":
  main()