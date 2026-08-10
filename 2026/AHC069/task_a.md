### ストーリー

日本橋公園は美しい芝生と豊かな池を擁する行楽客に人気の公園である。押し寄せる利用希望者を効率よく公園の中に配置して多くの利用料を得よう。

### 問題文

$N \times N$ のマス目で表される公園があり、各マスは芝生か池のいずれかである。最も左上のマスを $(0, 0)$ とし、そこから下に $x$、右に $y$ 移動したマスを $(x, y)$ と呼ぶ。

公園に、ピクニックをしたい $M$ 個のグループがやってくる。グループは $0, 1, \ldots, M - 1$ と番号づけられており、番号の順に公園へ到着する。各グループ $i$ には、到着時刻 $S_i$・退去時刻 $T_i$（$S_i < T_i$）・人数 $P_i$・基本支払額 $V_i$ が定められている。

あなたはこの公園の管理者で、各グループに対して利用を許可して領域を割り当てるか、利用を断るかを決める。利用を許可する場合は利用料を得られる。最終的な所持金をできるだけ大きくすることが目的である。

所持金は最初 $0$ である。利用を許可したグループは、退去するまでの間、割り当てられた領域を占有する。領域を占有しているグループを「利用中」と呼ぶ。

#### 処理の流れ

グループ $i$ が到着するたびに、次の順で処理を行う。

1. $i > 0$ の場合、$S_{i - 1} < T_j < S_i$ であって利用を許可していたグループ $j$ は、グループ $i-1$ の処理を行った後から現在までの間に公園を退去済みであり、その領域は解放されて空いている。
   - 退去したグループについて、利用料が所持金に加算される。利用料の計算方法は後述する。
2. （任意）利用中のグループのうちいくつかを、コストを払って公園内の別の場所へ移動させる。払ったコストの分だけ所持金が減る。所持金は負になる場合もある。
3. グループ $i$ に利用を許可して公園内の領域を割り当てるか、利用を断るかを決める。割り当てる場合はどの領域を占有するかを決める。
   - 割り当てられた領域は時刻 $T_i$ までの間グループ $i$ に占有される。ただし後でグループ $i$ が移動させられた場合は、移動の内容に従って占有する領域が変化する。

最後にグループ $M-1$ に対して上記の処理を行った後、残っている利用中のグループはすべて退去し、それぞれについて利用料が所持金に加算される。

#### 割り当てる領域の条件

グループ $i$ に割り当てる領域は、次の条件を満たす芝生マス $P_i$ 個の集合でなければならない。

- 上下左右に連結である。
  - すなわち、領域内のどの 2 つのマスも、領域内で上下左右の移動を繰り返すことで互いに行き来できる。
- その時点で利用中である他のグループが占有しているマスを含まない。

#### グループの移動

到着したグループの利用を許可するか断るかを決める前に、利用中のグループを公園内の別の場所へ移動させることができる。グループ $j$ を 1 回移動させるごとに、所持金が $\max(\mathrm{round}(V_j \times R), 1)$ だけ減る。ここで、$\mathrm{round}(x)$ は $x$ を四捨五入した値、すなわち $x + 0.5$ 以下の最大の整数とする。

複数のグループをまとめて移動させる場合は、**移動するすべてのグループがいったん領域を空けたのち、それぞれが指定した位置へ配置される**、という形で同時に行われる。このため、ふたつのグループの位置を入れ替えるような移動も可能である。移動後の各領域も、「割り当てる領域の条件」（芝生 $P_j$ マスが連結し、移動後の状態で他の利用中グループと重ならない）を満たす必要がある。

#### コンパクト度と利用料

割り当てた領域がコンパクトであるほど、グループは多くの利用料を支払う。コンパクト度 $C$ を以下で定める。

- $P$ マスの領域に対して、領域外および公園の外との境界線の長さの合計が $L$ であるとき、コンパクト度 $C$ を $C = \frac{4\sqrt{P}}{L}$ とする。

$0 < C \le 1$ である。領域が軸平行な正方形に近いほど $C$ は $1$ に近づき、細長い形や穴のある形であるほど $C$ は小さくなる。

利用中のグループ $i$ が退去するとき、グループのコンパクト度を $C_i$ として、$\mathrm{round}(V_i \times C_i)$ が利用料として所持金に加算される。利用を断ったグループからは利用料を得られない。

ここで $C_i$ は、そのグループが滞在中に占めたすべての位置（最初に配置した位置と、移動した場合は各移動後の位置）におけるコンパクト度の最小値とする。

例えば人数 $P_i = 4$ のグループを、最初に $2 \times 2$ の正方形（境界線の長さ $L = 8$ なので $C = 1$）に配置し、その後 $1 \times 4$ の細長い形（$L = 10$ なので $C = 0.8$）へ移動させたとする。このとき $C_i$ は両者の最小値をとり、$C_i = 0.8$ となる。

### 得点

全てのグループの退去時刻が過ぎた時点での所持金を $X$ とすると、$\max(X, 0)$ が絶対スコアとなる。絶対スコアは大きい方が良い。

各テストケースごとに、$\mathrm{round}(10^9 \times \left(\frac{\text{自身の絶対スコア}}{\text{全参加者中の最大絶対スコア}}\right))$ の**相対評価スコア**が得られ、その和が提出の得点となる。

最終順位はコンテスト終了後に実施されるより多くの入力に対するシステムテストにおける得点で決定される。暫定テスト、システムテストともに、一部のテストケースで不正な出力や制限時間超過をした場合、そのテストケースの相対評価スコアは 0 点となり、そのテストケースにおいては「全参加者中の最大絶対スコア」の計算から除外される。システムテストは **CE 以外の結果を得た一番最後の提出**に対してのみ行われるため、最終的に提出する解答を間違えないよう注意せよ。

#### テストケース数

- 暫定テスト: 50 個
- システムテスト: 2000 個、コンテスト終了後に [seeds.txt](https://img.atcoder.jp/ahc069/seeds.txt) (sha256=`f63752a346a388e810574d22c9ee271f4f77d0b5f9e353084f2c335417c96482`) を公開

#### 相対評価システムについて

暫定テスト・システムテストともに、CE 以外の結果を得た一番最後の提出のみが順位表に反映される。  
相対評価スコアの計算に用いられる各テストケース毎の全参加者中の最大絶対スコアの算出についても、順位表に反映されている最終提出のみが用いられる。

順位表に表示されているスコアは相対評価スコアであり、新規提出があるたびに、相対評価スコアが再計算される。一方、提出一覧から確認できる各提出のスコアは各テストケースごとの絶対スコアをそのまま足し合わせたものであり、相対評価スコアは表示されない。最新以外の提出について、現在の順位表における相対評価スコアを知るためには、再提出が必要である。不正な出力や制限時間超過をした場合、提出一覧から確認できるスコアは 0 となるが、順位表には正解したテストケースに対する相対スコアの和が表示される。

#### 実行時間について

実行時間には多少のブレが生じる。また、システムテストでは同時に大量の実行を行うため、暫定テストに比べて数 % 程度実行時間が伸びる現象が確認されている。そのため、実行時間制限ギリギリの提出がシステムテストで TLE となる可能性がある。プログラム内で時間を計測して処理を打ち切るか、実行時間に余裕を持たせることを推奨する。

### 入出力

本問題はインタラクティブ形式である。

最初に、問題のパラメタと公園の形状が標準入力から与えられる。

$$
N\ M\ R \\
\mathrm{row}_0 \\
\vdots \\
\mathrm{row}_{N-1}
$$

- $1$ 行目：公園の大きさ $N$、グループ数 $M$、移動コスト係数 $R$。
- 続く $N$ 行：公園の形状。各行は `.`（芝生）と `#`（池）からなる長さ $N$ の文字列 $\mathrm{row}_i$ である。$\mathrm{row}_i$ の $j$ 文字目が、マス $(i, j)$ が芝生か池かを表す。

続いて、$M$ 個のグループについて到着順に、次の「グループ情報の入力」「移動の出力」「到着したグループの取り扱いの出力」を繰り返す。

**出力の後には改行をし、更に標準出力を flush しなければならない。**そうしない場合、TLE となる可能性がある。

#### グループ情報の入力

到着したグループの情報が 1 行で与えられる（$i$ は $0, 1, \ldots, M - 1$ の順）。

$$
i\ S_i\ T_i\ P_i\ V_i
$$

#### 移動の出力

まず、移動させるグループの数 $A_i$ を出力する。$A_i$ の値は $0$ 以上、現在利用中のグループ数以下で、移動を行わない場合は `0` を出力する。

$$
A_i
$$

続けて、移動させる各グループについて、グループ番号 $j$ と移動後の $P_j$ 個のマスの座標 $(z_0, w_0), \ldots, (z_{P_j - 1}, w_{P_j - 1})$ を以下の形式で出力する。これを $A_i$ 回繰り返す。

$$
j \\
z_0\ w_0 \\
\vdots \\
z_{P_j - 1}\ w_{P_j - 1}
$$

ひとつの移動の中で同じグループを複数回指定してはならない。

#### 到着したグループの取り扱いの出力

到着したグループの利用を許可する場合は、`Yes` に続けて割り当てる $P_i$ 個のマスの座標 $(x_0, y_0), \ldots, (x_{P_i - 1}, y_{P_i - 1})$ を以下の形式で出力する。

$$
\mathtt{Yes} \\
x_0\ y_0 \\
\vdots \\
x_{P_i - 1}\ y_{P_i - 1}
$$

利用を断る場合は、`No` を出力する。

$$
\mathtt{No}
$$

[例を見る](https://img.atcoder.jp/ahc069/AdcJXWH4.html?lang=ja&seed=0&output=sample)

#### 制約

- $N = 50$
- $M = 1000$
- $0.001 \le R \le 0.1$
- $0 \le S_i < T_i \le 100000$
- $S_i < S_{i + 1}\ (0 \le i < M - 1)$
- $2 \times M$ 個の値 $S_0, S_1, \ldots, S_{M - 1}, T_0, T_1, \ldots, T_{M - 1}$ は互いに異なる。
- $4 \le P_i \le 150$
- $0 < V_i \le 10^8$
- $S_i, T_i, P_i, V_i$ は整数である。
- $R$ は小数点以下 $3$ 桁まで与えられる。

### サンプルプログラム（Python）

Python での解答例を示す。このプログラムでは、上の行から順に現在利用中でない芝生のマスを探し、最初に見つかったマスから幅優先探索をして $P_i$ 個のマスを訪問できたらグループに割り当てる。$P_i$ 個の連結した領域が見つからない場合は利用を拒否する。

```python
import math
import sys
from collections import deque

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class GroupInfo:
    def __init__(self, s, t, p, v):
        self.s = s        # 到着時刻
        self.t = t        # 退去時刻
        self.p = p        # 人数
        self.v = v        # 基本支払額
        self.c = None     # コンパクト度（配置後に設定）
        self.pos = None   # 占有マスの座標 [(行, 列), ...]（配置後に設定）


def find_region(grid, owner, n, p):
    """
    上の行から順に最初の空き芝生マスを探し、そこから BFS で p マス集める。
    p マス集められれば座標リストを、集められなければ None を返す。
    """

    # 最初の空き芝生マスを探す
    start = None
    for x in range(n):
        for y in range(n):
            if grid[x][y] == "." and owner[x][y] == -1:
                start = (x, y)
                break
        if start is not None:
            break
    if start is None:
        return None

    # start から BFS。取り出したマスを順に領域へ加え、p 個に達したら止める。
    visited = [[False] * n for _ in range(n)]
    visited[start[0]][start[1]] = True
    queue = deque([start])
    region = []
    while queue and len(region) < p:
        x, y = queue.popleft()
        region.append((x, y))
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] \
                    and grid[nx][ny] == "." and owner[nx][ny] == -1:
                visited[nx][ny] = True
                queue.append((nx, ny))

    return region if len(region) == p else None


def compactness(region, p):
    """コンパクト度を返す。"""
    cells = set(region)
    perimeter = 0
    for (x, y) in region:
        for dx, dy in DIRS:
            if (x + dx, y + dy) not in cells:
                perimeter += 1
    return 4 * math.sqrt(p) / perimeter


def main():
    n, m, r = input().split()
    n, m = int(n), int(m)
    grid = [input() for _ in range(n)]

    # owner[x][y]: そのマスを占有しているグループ番号。空きは -1。
    owner = [[-1] * n for _ in range(n)]
    # これまで到着した全グループ
    groups = []

    for i in range(m):
        _gi, s, t, p, v = map(int, input().split())
        group = GroupInfo(s, t, p, v)
        groups.append(group)

        # 退去時刻が現在時刻 s より前のグループを解放する
        for g in groups:
            if g.pos is not None and g.t < s:
                for (x, y) in g.pos:
                    owner[x][y] = -1
                g.pos = None

        # 移動は行わない
        print(0)

        region = find_region(grid, owner, n, p)
        if region is not None:
            # 割り当てる: owner を更新し、コンパクト度と占有マスを記録する
            for (x, y) in region:
                owner[x][y] = i
            group.pos = region
            group.c = compactness(region, p)
            print("Yes")
            for (x, y) in region:
                print(x, y)
        else:
            # 拒否
            print("No")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
```

### 入力生成方法

$x$ 以上 $y$ 以下の整数を一様ランダムに返す関数を $\mathrm{rand}(x, y)$、$x$ 以上 $y$ 以下の実数を一様ランダムに返す関数を $\mathrm{randf}(x, y)$ で表す。また、$\mathrm{gauss}(\mu, \sigma)$ を平均 $\mu$、標準偏差 $\sigma$ のガウス分布から値を返す関数とする。

#### $R$ の生成

$R = \mathrm{rand}(1, 100) \times 0.001$ とする。

#### 公園の形状の生成

まず、公園のすべてのマスを芝生とする。

$\mathrm{num\_cluster} = \mathrm{round}(2^{\mathrm{randf}(1.0, 8.0)})$ とし、互いに異なる $\mathrm{num\_cluster}$ 個のマスを一様ランダムに選んで池に変更する。

$\mathrm{num\_pond} = \mathrm{rand}(0, 900 - \mathrm{num\_cluster})$ とし、以下の操作を $\mathrm{num\_pond}$ 回繰り返し行う。

- 芝生のマスであって、池のマスに隣接しているものから一様ランダムに一つを選び、池に変更する。

生成された公園では、芝生のマスの全てが上下左右に連結しているとは限らないことに注意せよ。

#### グループの情報の生成

$P_i = \mathrm{round}(\mathrm{randf}(2.0, \sqrt{150.0})^2)$ とする。

$S_i, T_i$ は次のように決める。

1. $\theta = \mathrm{rand}(2000, 8000)$ とする。
2. $0 \le i < M$ を満たす $i$ に対して順に、次のように $s_i, t_i$ を定める。
   1. $l_i$ を、$\lambda = 1/\theta$ の指数分布から発生させた値を最も近い整数に丸めたものとする。
   2. $l_i \ge 100000$ の場合、$l_i$ の生成からやり直す。
   3. $s_i = \mathrm{rand}(0, 100000 - 1 - l_i)$ とする。
   4. $t_i = s_i + l_i + 1$ とする。
   5. $s_i, t_i$ がすでに生成した $s_j, t_j\ (0 \le j < i)$ と重複していた場合、$l_i$ の生成からやり直す。
3. $(s_i, t_i)\ (0 \le i < M)$ を $s_i$ 昇順にソートしたものを $(S_0, T_0), (S_1, T_1), \ldots, (S_{M-1}, T_{M-1})$ とする。

$V_i$ は次のように決める。

1. $V_i = \mathrm{round}(P_i \times (T_i - S_i)^{0.9} \times 2^{\mathrm{gauss}(0.0, 0.8)})$ とする。
2. $V_i$ が $0$ の場合は $V_i = 1$ とする。
3. $V_i > 10^8$ の場合は $V_i = 10^8$ とする。

### ツール(入力ジェネレータ・ビジュアライザ)

- [Web 版](https://img.atcoder.jp/ahc069/AdcJXWH4.html?lang=ja): ローカル版より高性能でアニメーション表示が可能です。
- [ローカル版](https://img.atcoder.jp/ahc069/AdcJXWH4.zip): 使用するには [Rust 言語](https://www.rust-lang.org/ja) のコンパイル環境をご用意下さい。
  - [Windows 用のコンパイル済みバイナリ](https://img.atcoder.jp/ahc069/AdcJXWH4_windows.zip): Rust 言語の環境構築が面倒な方は代わりにこちらをご利用下さい。

コンテスト期間中に、ビジュアライズ結果の共有や、解法・考察に関する言及は禁止されています。ご注意下さい。

### 生成AIの利用に関して

現行の [AtCoder Heuristic Contest 生成 AI 利用ルール－20250616 版](https://info.atcoder.jp/entry/ahc-llm-rules-ja) では、AI エージェントに解答プログラムを実行させ、その実行結果に基づく改善を自動的に繰り返させることを禁止しています。

一方、最新の生成 AI では、ChatGPT のような対話型サービスと、Codex のような AI エージェントとの区別が曖昧になっています。対話型サービスであっても、利用者が明示的に指示していない場合に、内部でテストケースの生成、解答プログラムの実行、および実行結果に基づく改善を自動的に繰り返すことがあります。

一部の参加者は、このような挙動を防ぐため、生成 AI に対して禁止事項を明示しています。参加者間の公平性を確保し、現行ルールの趣旨を徹底するため、本コンテストで生成 AI を利用する場合は、以下の指示文を各チャットの冒頭に入力するか、各生成 AI ツールが提供するカスタム指示、プロジェクト指示、または自動的に読み込む指示ファイル（例：`AGENTS.md`、`CLAUDE.md` など）に設定しなければなりません。

```text
I am currently participating in an AtCoder Heuristic Contest, and I will use this generative AI to assist in developing my solution.

When using this generative AI, the "AtCoder Heuristic Contest Generative AI Usage Rules - Version 20250616" apply.

https://info.atcoder.jp/entry/ahc-llm-rules-en

Most importantly, after running the solution program, you must not modify or improve the solution, its approach, or its code based on the execution results unless the user gives a new explicit instruction to do so.

You may run the solution program and report its execution results, logs, scores, or other observations. After reporting them, you must stop and wait for a new instruction from the user before making any improvement based on those results.

Here, "solution program" refers to any program created or being created for the purpose of solving this contest problem, regardless of whether it was created by the user or by generative AI, and regardless of whether it is still in progress or already complete.
```
