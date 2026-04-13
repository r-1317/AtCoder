import os
import time

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

K = 1000
TIME_LIMIT = 1.8


class BeamState:
  __slots__ = ("pos", "col", "foods", "matches", "score", "node_id")

  def __init__(self, pos, col, foods, matches, score, node_id):
    self.pos = pos
    self.col = col
    self.foods = foods
    self.matches = matches
    self.score = score
    self.node_id = node_id


def score_of(length: int, matches: int, turns: int) -> int:
  return 10000 * (length + matches) - turns


def reconstruct_ops(parents, moves, node_id: int):
  ops = []
  cur = node_id
  while cur > 0:
    ops.append(moves[cur])
    cur = parents[cur]
  ops.reverse()
  return ops

def main():
  N, M, C = map(int, input().split())
  desired = tuple(map(int, input().split()))

  board = [0] * (N * N)
  for i in range(N):
    row = list(map(int, input().split()))
    base = i * N
    for j, v in enumerate(row):
      board[base + j] = v

  # Directions are fixed to keep deterministic behavior.
  dirs = [(-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")]
  neighbors = [[] for _ in range(N * N)]
  for r in range(N):
    for c in range(N):
      idx = r * N + c
      cand = []
      for dr, dc, ch in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < N and 0 <= nc < N:
          cand.append((nr * N + nc, ch))
      neighbors[idx] = cand

  init_pos = (4 * N, 3 * N, 2 * N, 1 * N, 0)
  init_col = (1, 1, 1, 1, 1)
  init_foods = tuple(board)
  init_matches = 5
  init_score = score_of(5, 5, 0)

  parents = [-1]
  moves = [""]

  beam = [BeamState(init_pos, init_col, init_foods, init_matches, init_score, 0)]

  best_node = 0
  best_score = init_score
  turn = 0
  start_time = time.perf_counter()

  while beam and (time.perf_counter() - start_time) < TIME_LIMIT:
    next_cands = []
    next_turn = turn + 1

    for st in beam:
      pos = st.pos
      col = st.col
      foods = st.foods
      k = len(col)
      head = pos[0]
      neck = pos[1]

      for nh, mv in neighbors[head]:
        if nh == neck:
          continue

        moved_pos = (nh,) + pos[:-1]
        food_color = foods[nh]

        if food_color != 0:
          # Eat first; this turn never includes biting by problem statement.
          food_list = list(foods)
          food_list[nh] = 0
          new_foods = tuple(food_list)
          new_pos = (nh,) + pos
          new_col = col + (food_color,)
          new_matches = st.matches
          if k < M and food_color == desired[k]:
            new_matches += 1
        else:
          bite_h = -1
          for h in range(1, k - 1):
            if moved_pos[h] == nh:
              bite_h = h
              break

          if bite_h != -1:
            new_pos = moved_pos[:bite_h + 1]
            new_col = col[:bite_h + 1]
            food_list = list(foods)
            for p in range(bite_h + 1, k):
              food_list[moved_pos[p]] = col[p]
            new_foods = tuple(food_list)

            upto = min(len(new_col), M)
            mcnt = 0
            for i in range(upto):
              if new_col[i] == desired[i]:
                mcnt += 1
            new_matches = mcnt
          else:
            new_pos = moved_pos
            new_col = col
            new_foods = foods
            new_matches = st.matches

        new_len = len(new_col)
        new_score = score_of(new_len, new_matches, next_turn)

        node_id = len(parents)
        parents.append(st.node_id)
        moves.append(mv)

        if new_score > best_score:
          best_score = new_score
          best_node = node_id

        next_cands.append((new_score, node_id, new_pos, new_col, new_foods, new_matches))

    if not next_cands:
      break

    next_cands.sort(key=lambda x: x[0], reverse=True)
    if len(next_cands) > K:
      next_cands = next_cands[:K]

    beam = [
      BeamState(pos, col, foods, matches, score, node_id)
      for score, node_id, pos, col, foods, matches in next_cands
    ]

    turn = next_turn

  ans = reconstruct_ops(parents, moves, best_node)
  print("\n".join(ans))

if __name__ == "__main__":
  main()