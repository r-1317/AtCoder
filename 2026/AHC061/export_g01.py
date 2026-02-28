#!/usr/bin/env python3
"""train01.py が出力した *.model.json から、提出用の g01.py を生成する。

生成物は numpy 不要で、float16+base64 埋め込み重みを起動時にデコードして推論する。

Usage:
  python3 export_g01.py --model tmp_best2.model.json --out g01.py
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
    ap.add_argument("--out", type=str, default="g01.py")
    args = ap.parse_args()

    model_path = Path(args.model)
    out_path = Path(args.out)

    payload = json.loads(model_path.read_text())
    if payload.get("format") != "ahc061-nn-f16-b64-v1":
        raise ValueError("Unexpected model format")

    layers = payload["layers"]
    W1 = layers["W1"]
    b1 = layers["b1"]
    W2 = layers["W2"]
    b2 = layers["b2"]

    # 形状は g01.py 側でもチェックする
    meta = payload.get("meta", {})

    lines: list[str] = []
    lines.append(f"# Generated from {model_path.name}\n")
    lines.append(f"# format: {payload.get('format')}\n\n")
    lines.append("import base64\n")
    lines.append("import math\n")
    lines.append("import struct\n")
    lines.append("import sys\n\n\n")

    lines.append(f"MODEL_META = {json.dumps(meta, ensure_ascii=False)}\n\n")
    lines.append(f"W1_SHAPE = {W1['shape']}\n")
    lines.append(f"b1_SHAPE = {b1['shape']}\n")
    lines.append(f"W2_SHAPE = {W2['shape']}\n")
    lines.append(f"b2_SHAPE = {b2['shape']}\n\n")

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
        """
def readints():
    return list(map(int, sys.stdin.readline().split()))


def sigmoid(x: float) -> float:
    if x < -60.0:
        return 0.0
    if x > 60.0:
        return 1.0
    return 1.0 / (1.0 + math.exp(-x))


def decode_f16_list(b64: str, expected_len: int) -> list[float]:
    raw = base64.b64decode(b64)
    out = [0.0] * expected_len
    i = 0
    for (v,) in struct.iter_unpack('<e', raw):
        if i >= expected_len:
            break
        out[i] = float(v)
        i += 1
    if i != expected_len:
        raise ValueError(f"decode length mismatch: got={i} expected={expected_len}")
    return out


def get_candidates(N: int, M: int, pos: list[tuple[int,int]], owner: list[list[int]], player: int) -> list[tuple[int,int]]:
    visited = [[False] * N for _ in range(N)]
    q: list[tuple[int,int]] = []
    sx, sy = pos[player]
    visited[sx][sy] = True
    q.append((sx, sy))

    reachable: list[tuple[int,int]] = []
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))

    qi = 0
    while qi < len(q):
        x, y = q[qi]
        qi += 1

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


def build_features(N: int, M: int, U: int, V: list[list[int]], pos: list[tuple[int,int]], owner: list[list[int]], level: list[list[int]]) -> list[float]:
    scores = [0] * M
    for x in range(N):
        for y in range(N):
            o = owner[x][y]
            if o >= 0:
                scores[o] += V[x][y] * level[x][y]

    opponents = [p for p in range(M) if p != 0]
    opponents.sort(key=lambda p: scores[p], reverse=True)
    rank_of = {p: i for i, p in enumerate(opponents)}

    occupied_other = set(pos[p] for p in range(1, M))

    feats = [0.0] * (5 * N * N)
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
            feats[300 + idx] = V[x][y] / 1e5
            feats[400 + idx] = level[x][y] / float(U)
            idx += 1
    return feats


def nn_forward(x: list[float], W1: list[float], b1: list[float], W2: list[float], b2: list[float]) -> list[float]:
    in_dim = 500
    hid_dim = 200
    out_dim = 100
    h = [0.0] * hid_dim
    for i in range(hid_dim):
        base = i * in_dim
        s = b1[i]
        for j in range(in_dim):
            s += W1[base + j] * x[j]
        h[i] = sigmoid(s)

    y = [0.0] * out_dim
    for i in range(out_dim):
        base = i * hid_dim
        s = b2[i]
        for j in range(hid_dim):
            s += W2[base + j] * h[j]
        y[i] = s
    return y


def choose_move(N: int, M: int, U: int, V: list[list[int]], pos: list[tuple[int,int]], owner: list[list[int]], level: list[list[int]],
                W1: list[float], b1: list[float], W2: list[float], b2: list[float]) -> tuple[int,int]:
    candidates = get_candidates(N, M, pos, owner, 0)
    if not candidates:
        return pos[0]
    feats = build_features(N, M, U, V, pos, owner, level)
    out = nn_forward(feats, W1, b1, W2, b2)

    best = candidates[0]
    best_val = -1e100
    for (x, y0) in candidates:
        idx = N * x + y0
        v = out[idx]
        if v > best_val:
            best_val = v
            best = (x, y0)
        elif v == best_val and (x, y0) < best:
            best = (x, y0)
    return best


def main():
    N, M, T, U = map(int, sys.stdin.readline().split())
    V = [readints() for _ in range(N)]
    pos = [tuple(readints()) for _ in range(M)]

    if W1_SHAPE != [200, 500] or b1_SHAPE != [200] or W2_SHAPE != [100, 200] or b2_SHAPE != [100]:
        raise ValueError('Unexpected shapes')

    W1 = decode_f16_list(W1_B64, 200 * 500)
    b1 = decode_f16_list(b1_B64, 200)
    W2 = decode_f16_list(W2_B64, 100 * 200)
    b2 = decode_f16_list(b2_B64, 100)

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


if __name__ == '__main__':
    main()
"""
    )

    out_path.write_text("".join(lines))
    print(f"wrote: {out_path}")


if __name__ == "__main__":
    main()
