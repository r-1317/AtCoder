#!/usr/bin/env python3
"""train02.rs が出力した *.model.json (int8+scale+base64) から、提出用の g02.py を生成する。

Usage:
  python3 export-g02.py --model trained_best_v2.model.json --out g02.py

生成物:
- numpy を使って推論（行列積）を高速化
- 重みは int8 + layerごとの scale を base64 埋め込みし、起動時に復元

注意:
- AtCoder で numpy が利用できる前提（AHCでは通常可）
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _chunk_string(s: str, width: int = 120) -> str:
    return "\n".join(s[i : i + width] for i in range(0, len(s), width))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, required=True)
    ap.add_argument("--out", type=str, default="g02.py")
    args = ap.parse_args()

    model_path = Path(args.model)
    out_path = Path(args.out)

    payload = json.loads(model_path.read_text())
    if payload.get("format") != "ahc061-nn-i8-b64-v2":
        raise ValueError(f"Unexpected model format: {payload.get('format')}")

    layers = payload["layers"]
    W1 = layers["W1"]
    b1 = layers["b1"]
    W2 = layers["W2"]
    b2 = layers["b2"]

    meta = payload.get("meta", {})

    lines: list[str] = []
    lines.append(f"# Generated from {model_path.name}\n")
    lines.append(f"# format: {payload.get('format')}\n\n")

    lines.append("import base64\n")
    lines.append("import sys\n")
    lines.append("from collections import deque\n")
    lines.append("\n")
    lines.append("import numpy as np\n")
    lines.append("\n\n")

    lines.append(f"MODEL_META = {json.dumps(meta, ensure_ascii=False)}\n\n")

    lines.append(f"W1_SHAPE = {W1['shape']}\n")
    lines.append(f"b1_SHAPE = {b1['shape']}\n")
    lines.append(f"W2_SHAPE = {W2['shape']}\n")
    lines.append(f"b2_SHAPE = {b2['shape']}\n\n")

    lines.append(f"W1_SCALE = {float(W1['scale'])}\n")
    lines.append(f"b1_SCALE = {float(b1['scale'])}\n")
    lines.append(f"W2_SCALE = {float(W2['scale'])}\n")
    lines.append(f"b2_SCALE = {float(b2['scale'])}\n\n")

    lines.append('W1_B64 = """\n')
    lines.append(_chunk_string(W1["b64"]))
    lines.append('\n"""\n\n')

    lines.append('b1_B64 = """\n')
    lines.append(_chunk_string(b1["b64"]))
    lines.append('\n"""\n\n')

    lines.append('W2_B64 = """\n')
    lines.append(_chunk_string(W2["b64"]))
    lines.append('\n"""\n\n')

    lines.append('b2_B64 = """\n')
    lines.append(_chunk_string(b2["b64"]))
    lines.append('\n"""\n\n')

    lines.append(
        r"""

def readints():
    return list(map(int, sys.stdin.readline().split()))


def sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -60.0, 60.0)
    return 1.0 / (1.0 + np.exp(-x))


def decode_i8_layer(b64: str, expected_len: int, scale: float) -> np.ndarray:
    raw = base64.b64decode(b64)
    arr = np.frombuffer(raw, dtype=np.int8)
    if arr.size != expected_len:
        raise ValueError(f"decode length mismatch: got={arr.size} expected={expected_len}")
    # 復元: float = (q/127) * scale
    return (arr.astype(np.float32) / 127.0) * np.float32(scale)


def get_candidates(N: int, M: int, pos: list[tuple[int, int]], owner: list[list[int]], player: int) -> list[tuple[int, int]]:
    visited = [[False] * N for _ in range(N)]
    q = deque()
    sx, sy = pos[player]
    visited[sx][sy] = True
    q.append((sx, sy))

    reachable: list[tuple[int, int]] = []
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))

    while q:
        x, y = q.popleft()

        ok = True
        for i in range(M):
            if i != player and pos[i] == (x, y):
                ok = False
                break
        if ok:
            reachable.append((x, y))

        if owner[x][y] == player:
            for dx, dy in dirs:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny))

    return reachable


def build_features(N: int, M: int, U: int, V: np.ndarray, pos: list[tuple[int, int]], owner: list[list[int]], level: list[list[int]]) -> np.ndarray:
    owner_np = np.asarray(owner, dtype=np.int32)
    level_np = np.asarray(level, dtype=np.int32)

    scores = [0] * M
    vl = V * level_np
    for p in range(M):
        scores[p] = int(np.sum(vl[owner_np == p], dtype=np.int64))

    opponents = [p for p in range(M) if p != 0]
    opponents.sort(key=lambda p: scores[p], reverse=True)
    rank_of = {p: i for i, p in enumerate(opponents)}

    occupied_other = set(pos[p] for p in range(1, M))

    feats = np.zeros(5 * N * N, dtype=np.float32)
    idx = 0
    for x in range(N):
        for y in range(N):
            o = owner[x][y]
            feats[idx] = 1.0 if o == 0 else 0.0
            if o in rank_of:
                rnk = rank_of[o]
                feats[100 + idx] = 1.0 - (rnk / float(M))
            else:
                feats[100 + idx] = 0.0
            feats[200 + idx] = 1.0 if (x, y) in occupied_other else 0.0
            feats[300 + idx] = float(V[x, y]) / 1e5
            feats[400 + idx] = float(level[x][y]) / float(U)
            idx += 1

    return feats


def choose_move(
    N: int,
    M: int,
    U: int,
    V: np.ndarray,
    pos: list[tuple[int, int]],
    owner: list[list[int]],
    level: list[list[int]],
    W1: np.ndarray,
    b1: np.ndarray,
    W2: np.ndarray,
    b2: np.ndarray,
) -> tuple[int, int]:
    candidates = get_candidates(N, M, pos, owner, 0)
    if not candidates:
        return pos[0]

    x = build_features(N, M, U, V, pos, owner, level)  # (500,)

    # NN forward (numpy)
    h = sigmoid(W1 @ x + b1)  # (H,)
    y = W2 @ h + b2  # (100,)

    best = candidates[0]
    best_val = -1e100
    for (cx, cy) in candidates:
        out_idx = N * cx + cy
        v = float(y[out_idx])
        if v > best_val:
            best_val = v
            best = (cx, cy)
        elif v == best_val and (cx, cy) < best:
            best = (cx, cy)

    return best


def main():
    N, M, T, U = map(int, sys.stdin.readline().split())
    V_list = [readints() for _ in range(N)]
    V = np.asarray(V_list, dtype=np.float32)
    pos = [tuple(readints()) for _ in range(M)]

    # 形状チェック
    hid_dim = int(W1_SHAPE[0])
    if W1_SHAPE != [hid_dim, 500] or b1_SHAPE != [hid_dim] or W2_SHAPE != [100, hid_dim] or b2_SHAPE != [100]:
        raise ValueError("Unexpected shapes")

    W1 = decode_i8_layer(W1_B64, hid_dim * 500, W1_SCALE).reshape((hid_dim, 500))
    b1 = decode_i8_layer(b1_B64, hid_dim, b1_SCALE)
    W2 = decode_i8_layer(W2_B64, 100 * hid_dim, W2_SCALE).reshape((100, hid_dim))
    b2 = decode_i8_layer(b2_B64, 100, b2_SCALE)

    # 入力側の dtype を合わせる（@ の結果を float32 に寄せる）
    W1 = np.asarray(W1, dtype=np.float32)
    b1 = np.asarray(b1, dtype=np.float32)
    W2 = np.asarray(W2, dtype=np.float32)
    b2 = np.asarray(b2, dtype=np.float32)

    owner = [[-1] * N for _ in range(N)]
    level = [[0] * N for _ in range(N)]
    for p, (x, y) in enumerate(pos):
        owner[x][y] = p
        level[x][y] = 1

    for _turn in range(T):
        mv = choose_move(N, M, U, V, pos, owner, level, W1, b1, W2, b2)
        print(mv[0], mv[1], flush=True)

        _tx = [tuple(readints()) for _ in range(M)]
        pos = [tuple(readints()) for _ in range(M)]
        owner = [readints() for _ in range(N)]
        level = [readints() for _ in range(N)]


if __name__ == "__main__":
    main()
"""
    )

    out_path.write_text("".join(lines))
    print(f"wrote: {out_path}")


if __name__ == "__main__":
    main()
