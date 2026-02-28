#!/usr/bin/env python3
"""AHC061: GAでニューラルネットワークのパラメータを最適化する学習スクリプト。

このスクリプトは `tools/src/lib.rs` のゲーム進行・AI行動決定を Python に移植し、
プレイヤー0をニューラルネットワークで行動させたときの絶対スコアを評価値として
遺伝的アルゴリズム(GA)でネットワーク重みを最適化します。

注意/前提
- 入力形式は `tools/src/lib.rs::parse_input` に準拠します。
  in/*.txt には AI 内部パラメータ(wa,wb,wc,wd,eps) と乱数列 r が含まれます。
- ここでの学習はローカル用です。AtCoder提出用(Main.py)ではそれらは読めません。

計画(GA-plan.md)のデフォルト値は非常に計算量が大きいので、
CLI オプションで世代数や評価ケース数を調整できるようにしています。
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

import numpy as np


@dataclass(frozen=True)
class InputData:
    N: int
    M: int
    T: int
    U: int
    V: np.ndarray  # (N,N) int
    xy: List[Tuple[int, int]]  # len M
    wa: np.ndarray  # (M-1,) float
    wb: np.ndarray
    wc: np.ndarray
    wd: np.ndarray
    eps: np.ndarray
    r: np.ndarray  # (M-1, 2T) float


@dataclass
class State:
    pos: List[Tuple[int, int]]  # len M
    owner: np.ndarray  # (N,N) int, -1..M-1
    level: np.ndarray  # (N,N) int, 0..U
    selected: List[Tuple[int, int]]  # len M

    @staticmethod
    def new(input_data: InputData) -> "State":
        owner = np.full((input_data.N, input_data.N), -1, dtype=np.int32)
        level = np.zeros((input_data.N, input_data.N), dtype=np.int32)
        pos = list(input_data.xy)
        selected = list(pos)
        for p, (x, y) in enumerate(pos):
            owner[x, y] = p
            level[x, y] = 1
        return State(pos=pos, owner=owner, level=level, selected=selected)


def parse_input_file(path: Path) -> InputData:
    data = path.read_text().strip().split()
    it = iter(data)

    def next_int() -> int:
        return int(next(it))

    def next_float() -> float:
        return float(next(it))

    N = next_int()
    M = next_int()
    T = next_int()
    U = next_int()

    V = np.zeros((N, N), dtype=np.int32)
    for i in range(N):
        for j in range(N):
            V[i, j] = next_int()

    xy: List[Tuple[int, int]] = []
    for _ in range(M):
        xy.append((next_int(), next_int()))

    wa = np.zeros(M - 1, dtype=np.float64)
    wb = np.zeros(M - 1, dtype=np.float64)
    wc = np.zeros(M - 1, dtype=np.float64)
    wd = np.zeros(M - 1, dtype=np.float64)
    eps = np.zeros(M - 1, dtype=np.float64)
    for i in range(M - 1):
        wa[i] = next_float()
        wb[i] = next_float()
        wc[i] = next_float()
        wd[i] = next_float()
        eps[i] = next_float()

    r = np.zeros((M - 1, 2 * T), dtype=np.float64)
    for tt in range(T):
        for i in range(M - 1):
            r[i, 2 * tt] = next_float()
            r[i, 2 * tt + 1] = next_float()

    return InputData(N=N, M=M, T=T, U=U, V=V, xy=xy, wa=wa, wb=wb, wc=wc, wd=wd, eps=eps, r=r)


def _dirs4() -> Tuple[Tuple[int, int], ...]:
    return ((0, 1), (1, 0), (0, -1), (-1, 0))


def get_candidates(input_data: InputData, state: State, player: int) -> List[Tuple[int, int]]:
    """`tools/src/lib.rs::get_candidates` を移植。

    BFS は「自分の領土上」からのみ拡張するが、隣接マス自体は候補として追加される。
    また、他プレイヤーの駒がいるマスは候補から除外される。
    """

    N = input_data.N
    visited = [[False] * N for _ in range(N)]
    q: List[Tuple[int, int]] = []

    sx, sy = state.pos[player]
    q.append((sx, sy))
    visited[sx][sy] = True

    reachable: List[Tuple[int, int]] = []
    dirs = _dirs4()

    while q:
        x, y = q.pop(0)

        ok = True
        for i in range(input_data.M):
            if i != player and state.pos[i] == (x, y):
                ok = False
                break
        if ok:
            reachable.append((x, y))

        if state.owner[x, y] == player:
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny))

    return reachable


def is_valid_move(input_data: InputData, state: State, player: int, target: Tuple[int, int]) -> bool:
    x, y = target
    if x < 0 or x >= input_data.N or y < 0 or y >= input_data.N:
        return False
    for i in range(input_data.M):
        if i != player and state.pos[i] == target:
            return False
    candidates = get_candidates(input_data, state, player)
    return target in candidates


def decide_ai_move(input_data: InputData, state: State, ai_idx: int, turn: int) -> Tuple[int, int]:
    """`tools/src/lib.rs::decide_ai_move` を移植。"""

    player_id = ai_idx + 1
    candidates = get_candidates(input_data, state, player_id)

    scores: List[float] = []
    for (x, y) in candidates:
        owner = int(state.owner[x, y])
        level = int(state.level[x, y])
        value = float(input_data.V[x, y])

        if owner == -1:
            score = value * float(input_data.wa[ai_idx])
        elif owner == player_id:
            if level < input_data.U:
                score = value * float(input_data.wb[ai_idx])
            else:
                score = 0.0
        else:
            if level == 1:
                score = value * float(input_data.wc[ai_idx])
            else:
                score = value * float(input_data.wd[ai_idx])
        scores.append(score)

    eps = float(input_data.eps[ai_idx])
    r1 = float(input_data.r[ai_idx, 2 * (turn % input_data.T)])
    r2 = float(input_data.r[ai_idx, 2 * (turn % input_data.T) + 1])

    if r1 < eps:
        idx = int(math.floor(r2 * len(candidates)))
        idx = min(idx, len(candidates) - 1)
        return candidates[idx]

    max_score = max(scores) if scores else float("-inf")
    tolerance = 1e-9 * max(abs(max_score), 1.0)
    best = [i for i in range(len(candidates)) if scores[i] >= max_score - tolerance]
    idx = int(math.floor(r2 * len(best)))
    idx = min(idx, len(best) - 1)
    return candidates[best[idx]]


def update_state(input_data: InputData, state: State, moves: Sequence[Tuple[int, int]]) -> State:
    """`tools/src/lib.rs::update_state` を移植。"""

    if len(moves) != input_data.M:
        raise ValueError("moves length mismatch")

    new_state = State(
        pos=list(state.pos),
        owner=state.owner.copy(),
        level=state.level.copy(),
        selected=list(moves),
    )

    for i in range(input_data.M):
        if not is_valid_move(input_data, state, i, moves[i]):
            x, y = moves[i]
            if x >= input_data.N or y >= input_data.N or x < 0 or y < 0:
                raise ValueError(f"Player {i} attempted to move to out-of-bounds position ({x}, {y})")
            raise ValueError(
                f"Player {i} attempted invalid move from {state.pos[i]} to {moves[i]}"
            )

    temp_pos = list(moves)

    move_counts: dict[Tuple[int, int], int] = {}
    for mv in moves:
        move_counts[mv] = move_counts.get(mv, 0) + 1

    collected = [False] * input_data.M
    for i in range(input_data.M):
        target_pos = temp_pos[i]
        if move_counts[target_pos] >= 2:
            owner = int(new_state.owner[target_pos[0], target_pos[1]])
            if i != owner:
                collected[i] = True

    for i in range(input_data.M):
        if collected[i]:
            continue

        x, y = temp_pos[i]
        owner = int(new_state.owner[x, y])

        if owner == -1:
            new_state.owner[x, y] = i
            new_state.level[x, y] = 1
        elif owner == i:
            if int(new_state.level[x, y]) < input_data.U:
                new_state.level[x, y] += 1
        else:
            new_state.level[x, y] -= 1
            if int(new_state.level[x, y]) == 0:
                new_state.owner[x, y] = i
                new_state.level[x, y] = 1
            else:
                collected[i] = True

    for i in range(input_data.M):
        if collected[i]:
            temp_pos[i] = state.pos[i]

    new_state.pos = temp_pos
    return new_state


def _round_half_up_pos(x: float) -> int:
    # Rust の f64::round は 0 以上であれば「0.5以上切り上げ」。
    return int(math.floor(x + 0.5))


def calc_absolute_score(input_data: InputData, state: State) -> int:
    scores = [0] * input_data.M
    for i in range(input_data.N):
        for j in range(input_data.N):
            owner = int(state.owner[i, j])
            if owner >= 0:
                scores[owner] += int(input_data.V[i, j]) * int(state.level[i, j])

    s0 = scores[0]
    sa = max(scores[1:]) if input_data.M > 1 else 0
    if sa <= 0:
        return 0
    raw = 1e5 * math.log2(1.0 + (s0 / sa))
    return _round_half_up_pos(raw)


def sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -60.0, 60.0)
    return 1.0 / (1.0 + np.exp(-x))


class SimpleNN:
    """500 -> 200 -> 100 の 1-hidden-layer NN。"""

    INPUT_DIM = 500
    HIDDEN_DIM = 200
    OUTPUT_DIM = 100

    def __init__(self, W1: np.ndarray, b1: np.ndarray, W2: np.ndarray, b2: np.ndarray):
        self.W1 = W1
        self.b1 = b1
        self.W2 = W2
        self.b2 = b2

    @staticmethod
    def num_params() -> int:
        return (
            SimpleNN.HIDDEN_DIM * SimpleNN.INPUT_DIM
            + SimpleNN.HIDDEN_DIM
            + SimpleNN.OUTPUT_DIM * SimpleNN.HIDDEN_DIM
            + SimpleNN.OUTPUT_DIM
        )

    @staticmethod
    def from_genome(genome: np.ndarray) -> "SimpleNN":
        g = genome.astype(np.float32, copy=False)
        offset = 0

        W1 = g[offset : offset + SimpleNN.HIDDEN_DIM * SimpleNN.INPUT_DIM].reshape(
            (SimpleNN.HIDDEN_DIM, SimpleNN.INPUT_DIM)
        )
        offset += SimpleNN.HIDDEN_DIM * SimpleNN.INPUT_DIM

        b1 = g[offset : offset + SimpleNN.HIDDEN_DIM]
        offset += SimpleNN.HIDDEN_DIM

        W2 = g[offset : offset + SimpleNN.OUTPUT_DIM * SimpleNN.HIDDEN_DIM].reshape(
            (SimpleNN.OUTPUT_DIM, SimpleNN.HIDDEN_DIM)
        )
        offset += SimpleNN.OUTPUT_DIM * SimpleNN.HIDDEN_DIM

        b2 = g[offset : offset + SimpleNN.OUTPUT_DIM]
        offset += SimpleNN.OUTPUT_DIM

        if offset != len(g):
            raise ValueError("Genome length mismatch")

        return SimpleNN(W1=W1, b1=b1, W2=W2, b2=b2)

    def forward(self, x: np.ndarray) -> np.ndarray:
        # x: (500,)
        h = sigmoid(self.W1 @ x + self.b1)
        y = self.W2 @ h + self.b2
        return y


def _to_base64_f16(arr: np.ndarray) -> str:
    b = np.asarray(arr, dtype=np.float16, order="C").tobytes(order="C")
    return base64.b64encode(b).decode("ascii")


def save_model_base64_json(path: Path, nn: SimpleNN, meta: dict) -> None:
    payload = {
        "format": "ahc061-nn-f16-b64-v1",
        "meta": meta,
        "layers": {
            "W1": {
                "shape": list(nn.W1.shape),
                "dtype": "float16",
                "order": "C",
                "b64": _to_base64_f16(nn.W1),
            },
            "b1": {
                "shape": list(nn.b1.shape),
                "dtype": "float16",
                "order": "C",
                "b64": _to_base64_f16(nn.b1),
            },
            "W2": {
                "shape": list(nn.W2.shape),
                "dtype": "float16",
                "order": "C",
                "b64": _to_base64_f16(nn.W2),
            },
            "b2": {
                "shape": list(nn.b2.shape),
                "dtype": "float16",
                "order": "C",
                "b64": _to_base64_f16(nn.b2),
            },
        },
    }
    path.write_text(json.dumps(payload, ensure_ascii=False))


def build_features(input_data: InputData, state: State, player: int = 0) -> np.ndarray:
    N = input_data.N

    # 現在スコア（領土合計）を計算し、相手をスコア降順に並べる
    cur_scores = [0] * input_data.M
    for i in range(N):
        for j in range(N):
            owner = int(state.owner[i, j])
            if owner >= 0:
                cur_scores[owner] += int(input_data.V[i, j]) * int(state.level[i, j])

    opponents = list(range(input_data.M))
    opponents.remove(player)
    opponents.sort(key=lambda p: cur_scores[p], reverse=True)
    rank_of: dict[int, int] = {p: idx for idx, p in enumerate(opponents)}

    my_territory = np.zeros(N * N, dtype=np.float32)
    other_territory = np.zeros(N * N, dtype=np.float32)
    other_piece = np.zeros(N * N, dtype=np.float32)
    value_feat = np.zeros(N * N, dtype=np.float32)
    level_feat = np.zeros(N * N, dtype=np.float32)

    occupied_by_other = set(state.pos[p] for p in range(input_data.M) if p != player)

    idx = 0
    for x in range(N):
        for y in range(N):
            owner = int(state.owner[x, y])

            if owner == player:
                my_territory[idx] = 1.0
            elif owner in rank_of:
                rnk = rank_of[owner]
                other_territory[idx] = 1.0 - (rnk / float(input_data.M))

            if (x, y) in occupied_by_other:
                other_piece[idx] = 1.0

            value_feat[idx] = float(input_data.V[x, y]) / 1e5
            level_feat[idx] = float(state.level[x, y]) / float(input_data.U)
            idx += 1

    feats = np.concatenate([my_territory, other_territory, other_piece, value_feat, level_feat])
    if feats.shape[0] != 500:
        raise AssertionError(feats.shape)
    return feats


def choose_move_by_nn(input_data: InputData, state: State, nn: SimpleNN) -> Tuple[int, int]:
    candidates = get_candidates(input_data, state, 0)
    if not candidates:
        raise RuntimeError("No candidates")

    x = build_features(input_data, state, player=0)
    y = nn.forward(x)  # (100,)

    # 候補の中で出力最大を選ぶ
    best = None
    best_val = float("-inf")
    for (cx, cy) in candidates:
        idx = input_data.N * cx + cy
        val = float(y[idx])
        if val > best_val:
            best_val = val
            best = (cx, cy)
        elif val == best_val and best is not None:
            # 安定化: 同値なら座標が小さい方
            if (cx, cy) < best:
                best = (cx, cy)

    assert best is not None
    return best


def simulate_game(input_data: InputData, genome: np.ndarray) -> int:
    nn = SimpleNN.from_genome(genome)
    state = State.new(input_data)

    for turn in range(input_data.T):
        my_move = choose_move_by_nn(input_data, state, nn)
        moves = [my_move]
        for i in range(1, input_data.M):
            moves.append(decide_ai_move(input_data, state, ai_idx=i - 1, turn=turn))
        state = update_state(input_data, state, moves)

    return calc_absolute_score(input_data, state)


def make_initial_population(rng: np.random.Generator, pop_size: int, sigma: float) -> np.ndarray:
    # (pop_size, P)
    P = SimpleNN.num_params()
    return rng.normal(loc=0.0, scale=sigma, size=(pop_size, P)).astype(np.float32)


def crossover_uniform(rng: np.random.Generator, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    mask = rng.random(a.shape[0]) < 0.5
    child = a.copy()
    child[mask] = b[mask]
    return child


def mutate_gaussian(rng: np.random.Generator, genome: np.ndarray, rate: float, sigma: float) -> np.ndarray:
    g = genome.copy()
    mask = rng.random(g.shape[0]) < rate
    if np.any(mask):
        g[mask] += rng.normal(loc=0.0, scale=sigma, size=int(mask.sum())).astype(np.float32)
    return g


def eval_population(
    inputs: Sequence[InputData],
    population: np.ndarray,
    case_indices: Sequence[int],
) -> np.ndarray:
    fitness = np.zeros(population.shape[0], dtype=np.float64)
    for ci in case_indices:
        inp = inputs[ci]
        for i in range(population.shape[0]):
            fitness[i] += simulate_game(inp, population[i])
    fitness /= float(len(case_indices))
    return fitness


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-dir", type=str, default="in")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=999)

    # GA-plan.md の値（ただし現実的には重いので調整推奨）
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--parents", type=int, default=10)
    parser.add_argument("--children", type=int, default=100)
    parser.add_argument("--mutation-rate", type=float, default=0.002)

    # 実行時間を調整するための追加パラメータ
    parser.add_argument("--generations", type=int, default=None, help="指定時は epochs とは独立に世代数を固定")
    parser.add_argument("--eval-cases", type=int, default=1, help="1世代の評価に使うケース数")
    parser.add_argument("--init-sigma", type=float, default=0.05)
    parser.add_argument("--mutation-sigma", type=float, default=0.02)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--save", type=str, default="trained_best.npz")
    parser.add_argument(
        "--save-b64",
        type=str,
        default=None,
        help="float16+base64 の重みを JSON でも保存する（未指定なら --save から派生）",
    )

    args = parser.parse_args()

    in_dir = Path(args.in_dir)
    paths = [in_dir / f"{i:04}.txt" for i in range(args.start, args.end + 1)]
    missing = [p for p in paths if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing input files. Example: {missing[0]}")

    inputs = [parse_input_file(p) for p in paths]
    num_cases = len(inputs)

    generations = args.generations
    if generations is None:
        # GA-plan.md: 世代数 = EPOCH*1000(テストケースの数)
        generations = args.epochs * num_cases

    pop_size = args.parents + args.children
    rng = np.random.default_rng(args.seed)

    population = make_initial_population(rng, pop_size=pop_size, sigma=args.init_sigma)

    best_genome = population[0].copy()
    best_fit = float("-inf")

    for gen in range(generations):
        # 評価ケース: 連番で回す（必要ならeval-casesで複数個）
        start_ci = gen % num_cases
        case_indices = [(start_ci + k) % num_cases for k in range(args.eval_cases)]

        fitness = eval_population(inputs, population, case_indices)
        order = np.argsort(-fitness)

        if float(fitness[order[0]]) > best_fit:
            best_fit = float(fitness[order[0]])
            best_genome = population[order[0]].copy()

        if gen % 10 == 0 or gen == generations - 1:
            print(
                f"gen={gen:6d}  best_fit={best_fit:.2f}  "
                f"cur_best={float(fitness[order[0]]):.2f}  "
                f"avg={float(np.mean(fitness)):.2f}  cases={case_indices}",
                flush=True,
            )

        parents = population[order[: args.parents]]

        # 次世代生成（エリート維持 + 交叉・突然変異）
        next_population = np.empty_like(population)
        next_population[: args.parents] = parents

        for i in range(args.children):
            pa = parents[int(rng.integers(0, args.parents))]
            pb = parents[int(rng.integers(0, args.parents))]
            child = crossover_uniform(rng, pa, pb)
            child = mutate_gaussian(rng, child, rate=args.mutation_rate, sigma=args.mutation_sigma)
            next_population[args.parents + i] = child

        population = next_population

    # 保存
    nn_best = SimpleNN.from_genome(best_genome)
    np.savez_compressed(
        args.save,
        genome=best_genome.astype(np.float32),
        W1=nn_best.W1.astype(np.float32),
        b1=nn_best.b1.astype(np.float32),
        W2=nn_best.W2.astype(np.float32),
        b2=nn_best.b2.astype(np.float32),
        best_fit=best_fit,
    )
    print(f"saved: {args.save} (best_fit={best_fit:.2f})")

    save_b64 = args.save_b64
    if save_b64 is None:
        save_path = Path(args.save)
        if save_path.suffix.lower() == ".npz":
            save_b64 = str(save_path.with_suffix(".model.json"))
        else:
            save_b64 = str(save_path) + ".model.json"

    save_model_base64_json(
        Path(save_b64),
        nn_best,
        meta={
            "best_fit": float(best_fit),
            "input_dim": SimpleNN.INPUT_DIM,
            "hidden_dim": SimpleNN.HIDDEN_DIM,
            "output_dim": SimpleNN.OUTPUT_DIM,
        },
    )
    print(f"saved: {save_b64} (float16+base64)")


if __name__ == "__main__":
    main()
