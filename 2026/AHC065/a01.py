import os
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None


def build_vertical_belts(n: int):
  belts = []
  for k in range(n // 2):
    c0 = 2 * k
    c1 = 2 * k + 1
    belt = []
    for r in range(n):
      belt.append((r, c0))
    for r in range(n - 1, -1, -1):
      belt.append((r, c1))
    belts.append(belt)
  return belts


def build_horizontal_belt(n: int):
  belt = []
  for c in range(n):
    belt.append((0, c))
  for c in range(n - 1, -1, -1):
    belt.append((1, c))
  return belt


def rotate_belt(belt, belt_id, direction, grid, pos, ops):
  values = [grid[i][j] for i, j in belt]
  if direction == 1:
    values = [values[-1]] + values[:-1]
  else:
    values = values[1:] + values[:1]
  for (i, j), v in zip(belt, values):
    grid[i][j] = v
    if v >= 0:
      pos[v] = (i, j)
  ops.append((belt_id, direction))


def main():
  data = sys.stdin.read().strip().split()
  if not data:
    return
  it = iter(data)
  n = int(next(it))
  grid = [[0] * n for _ in range(n)]
  for i in range(n):
    for j in range(n):
      grid[i][j] = int(next(it))

  belts = build_vertical_belts(n)
  belts.append(build_horizontal_belt(n))
  horizontal_id = len(belts) - 1

  belt_index = []
  for belt in belts:
    idx = {}
    for k, cell in enumerate(belt):
      idx[cell] = k
    belt_index.append(idx)

  pos = [(-1, -1)] * (n * n)
  for i in range(n):
    for j in range(n):
      pos[grid[i][j]] = (i, j)

  exit_cell = (0, n // 2)
  exit_idx = belt_index[horizontal_id][exit_cell]
  ops = []
  limit_ops = 100000

  for box_id in range(n * n):
    if pos[box_id] == (-1, -1):
      continue
    if pos[box_id] == exit_cell:
      grid[exit_cell[0]][exit_cell[1]] = -1
      pos[box_id] = (-1, -1)
      continue

    i, j = pos[box_id]
    vb = j // 2
    belt = belts[vb]
    L = len(belt)
    cur_idx = belt_index[vb][(i, j)]
    c0 = 2 * vb
    c1 = 2 * vb + 1
    candidates = [(0, c0), (0, c1), (1, c0), (1, c1)]

    best = None
    for cell in candidates:
      target_idx = belt_index[vb][cell]
      diff = (target_idx - cur_idx) % L
      steps_v = diff if diff <= L - diff else L - diff
      dir_v = 1 if diff <= L - diff else -1

      cur_h_idx = belt_index[horizontal_id][cell]
      diff_h = (exit_idx - cur_h_idx) % len(belts[horizontal_id])
      steps_h = diff_h if diff_h <= len(belts[horizontal_id]) - diff_h else len(belts[horizontal_id]) - diff_h
      dir_h = 1 if diff_h <= len(belts[horizontal_id]) - diff_h else -1

      total = steps_v + steps_h
      if best is None or total < best[0]:
        best = (total, steps_v, dir_v, steps_h, dir_h, cell)

    if best is None:
      break

    total, steps_v, dir_v, steps_h, dir_h, cell = best
    if len(ops) + steps_v + steps_h > limit_ops:
      break

    for _ in range(steps_v):
      rotate_belt(belt, vb, dir_v, grid, pos, ops)

    for _ in range(steps_h):
      rotate_belt(belts[horizontal_id], horizontal_id, dir_h, grid, pos, ops)

    if pos[box_id] == exit_cell:
      grid[exit_cell[0]][exit_cell[1]] = -1
      pos[box_id] = (-1, -1)

  out_lines = []
  out_lines.append(str(len(belts)))
  for belt in belts:
    parts = [str(len(belt))]
    for i, j in belt:
      parts.append(str(i))
      parts.append(str(j))
    out_lines.append(" ".join(parts))

  out_lines.append(str(len(ops)))
  for m, d in ops:
    out_lines.append(f"{m} {d}")

  sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
  main()