import sys


def build_row_belts(n: int):
	belts = []
	belt_pos = []
	for r in range(0, n, 2):
		cells = []
		for c in range(n):
			cells.append((r, c))
		for c in range(n - 1, -1, -1):
			cells.append((r + 1, c))
		pos_map = {cell: idx for idx, cell in enumerate(cells)}
		belts.append(cells)
		belt_pos.append(pos_map)
	return belts, belt_pos


def build_col_belt(n: int, col: int):
	cells = []
	for r in range(n):
		cells.append((r, col))
	for r in range(n - 1, -1, -1):
		cells.append((r, col + 1))
	pos_map = {cell: idx for idx, cell in enumerate(cells)}
	return cells, pos_map


def rotate_belt(grid, pos_of_box, cells, d):
	l = len(cells)
	values = [grid[i][j] for i, j in cells]
	if d == 1:
		shifted = [values[-1]] + values[:-1]
	else:
		shifted = values[1:] + [values[0]]
	for (i, j), val in zip(cells, shifted):
		grid[i][j] = val
		if val != -1:
			pos_of_box[val] = (i, j)


def choose_rotation(cur_idx, targets, l):
	best_steps = None
	best_dir = 1
	for tgt in targets:
		forward = (tgt - cur_idx) % l
		backward = (cur_idx - tgt) % l
		if best_steps is None or forward < best_steps:
			best_steps = forward
			best_dir = 1
		if backward < best_steps:
			best_steps = backward
			best_dir = -1
	return best_steps, best_dir


def main():
	data = sys.stdin.read().strip().split()
	if not data:
		return
	it = iter(data)
	n = int(next(it))
	grid = [[0] * n for _ in range(n)]
	pos_of_box = [(-1, -1) for _ in range(n * n)]
	for i in range(n):
		for j in range(n):
			v = int(next(it))
			grid[i][j] = v
			pos_of_box[v] = (i, j)

	row_belts, row_pos = build_row_belts(n)
	col_belt, col_pos = build_col_belt(n, n // 2)

	belts = row_belts + [col_belt]
	belt_pos = row_pos + [col_pos]

	ops = []
	exit_cell = (0, n // 2)
	max_ops = 100000
	target = 0

	while target < n * n and len(ops) < max_ops:
		pos = pos_of_box[target]
		if pos == (-1, -1):
			target += 1
			continue

		i, j = pos
		row_idx = i // 2
		row_cells = belts[row_idx]
		row_map = belt_pos[row_idx]
		cur_idx = row_map[(i, j)]

		r = row_idx * 2
		candidates = [
			row_map[(r, n // 2)],
			row_map[(r, n // 2 + 1)],
			row_map[(r + 1, n // 2)],
			row_map[(r + 1, n // 2 + 1)],
		]
		steps, direction = choose_rotation(cur_idx, candidates, len(row_cells))

		for _ in range(steps):
			if len(ops) >= max_ops:
				break
			rotate_belt(grid, pos_of_box, row_cells, direction)
			ops.append((row_idx, direction))
			if grid[exit_cell[0]][exit_cell[1]] == target:
				grid[exit_cell[0]][exit_cell[1]] = -1
				pos_of_box[target] = (-1, -1)
				target += 1
				break

		if pos_of_box[target - 1] == (-1, -1):
			continue

		pos = pos_of_box[target]
		i, j = pos
		col_idx = len(belts) - 1
		col_cells = belts[col_idx]
		col_map = belt_pos[col_idx]
		cur_idx = col_map[(i, j)]
		tgt_idx = col_map[exit_cell]
		steps, direction = choose_rotation(cur_idx, [tgt_idx], len(col_cells))

		for _ in range(steps):
			if len(ops) >= max_ops:
				break
			rotate_belt(grid, pos_of_box, col_cells, direction)
			ops.append((col_idx, direction))
			if grid[exit_cell[0]][exit_cell[1]] == target:
				grid[exit_cell[0]][exit_cell[1]] = -1
				pos_of_box[target] = (-1, -1)
				target += 1
				break

		if pos_of_box[target] == (-1, -1):
			target += 1

	out = []
	out.append(str(len(belts)))
	for cells in belts:
		line = [str(len(cells))]
		for i, j in cells:
			line.append(str(i))
			line.append(str(j))
		out.append(" ".join(line))

	out.append(str(len(ops)))
	for m, d in ops:
		out.append(f"{m} {d}")

	sys.stdout.write("\n".join(out))


if __name__ == "__main__":
	main()
