# A - Mixing on the Palette


## ストーリー 

高橋画伯は、新作の水彩画シリーズに取り組んでいる。
彼の作品は繊細な色使いが評価されており、色の調合には特にこだわっている。
あなたは高橋画伯のアシスタントとして、彼が求める色をその場で調合して提供するという重要な役目を担っている。

使用する絵の具は高価であるため、出来るだけ無駄なく色を作ることが求められる。
幸い、これから必要となる色のリストが事前に渡されている。
できるだけ正確に、かつできるだけ少ない無駄でそれらの色を順番通りに作成してほしい。

## 問題文

絵の具の色は、シアン $(C)$、マゼンタ $(M)$、イエロー $(Y)$からなる三次元ベクトル $(C, M, Y)$ で表される。

<p><svg width="400" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="400" height="150" fill="rgb(255,255,255)" stroke="black"></rect>
  <rect x="40" y="50" width="40" height="40" fill="rgb(0,255,255)" stroke="black"></rect>
  <text x="60" y="40" text-anchor="middle" font-size="18">v₁ = 4</text>
  <text x="60" y="120" text-anchor="middle" font-size="18">p₁ = (1, 0, 0)</text>
  <text x="95" y="72" font-size="30">+</text>
  <rect x="140" y="45.5" width="49" height="49" fill="rgb(255,0,255)" stroke="black"></rect>
  <text x="164.5" y="35" text-anchor="middle" font-size="18">v₂ = 6</text>
  <text x="164.5" y="120" text-anchor="middle" font-size="18">p₂ = (0, 1, 0)</text>
  <text x="210" y="72" font-size="30">=</text>
  <rect x="260" y="29.5" width="70.7" height="70.7" fill="rgb(153,102,255)" stroke="black"></rect>
  <text x="295.35" y="20" text-anchor="middle" font-size="18">v₁ + v₂ = 10</text>
  <text x="295.35" y="125" text-anchor="middle" font-size="18">
    p = (0.4, 0.6, 0)
  </text>
</svg></p>

色 $p_1 = (C_1, M_1, Y_1)$ の絵の具を $v_1$ グラム、色 $p_2 = (C_2, M_2, Y_2)$ の絵の具を $v_2$ グラム混ぜると、色 $\frac{v_1 \cdot p_1 + v_2 \cdot p_2}{v_1 + v_2}$ の絵の具が $v_1 + v_2$ グラム得られる。

$K$ 種類のチューブ絵の具を所持しており、$i$ 番目のチューブの色は $(C^{\mathrm{own}}_i, M^{\mathrm{own}}_i, Y^{\mathrm{own}}_i)$ である。各チューブから絵の具を 1 グラム使うごとに、コスト $D$ がかかる。これらのチューブを用いて、$H$ 種類の色を順番に 1 グラムずつ作成し、画伯に渡したい。$i$ 番目に作るべき色は$(C^{\mathrm{target}}_i, M^{\mathrm{target}}_i, Y^{\mathrm{target}}_i)$ である。作成の順番は固定で、変更することはできない。

絵の具を混ぜるパレットは $N \times N$ の格子状のマス目で構成されている。

左上のマスの座標を $(0,0)$ とし、下方向に $i$、右方向に $j$ マス進んだ位置の座標を $(i,j)$ とする

各マスは、上下左右の隣接マスとの間に出し入れ可能な仕切りを備えている。 これらの仕切りの初期状態は、自由に設定してよい。

隣接するマスの間の仕切りが下がっている場合、それらのマスは **連結** であると呼ぶ。 連結なマス同士をたどって到達可能なマスの集合を **ウェル** と定義する。 

各ウェルには高々1色の絵の具しか入れられず、$k$ マスからなるウェルには最大で $k$ グラムの絵の具を入れることができる。 初期状態ではどのウェルにも絵の具は入っていない。

あなたは以下の操作を、最大で $T$ ターンまで行うことができる：

1. 任意のマスとチューブを 1 つずつ選び、そのマスが属するウェルに、チューブから 1 グラムの絵の具を出す。ただし、ウェルの残り容量を $w$ とすると、実際に混ざるのは $\min(w, 1)$ グラムであり、残りの $1 - \min(w, 1)$ グラムは混ざらずに即座に廃棄される。
2. 任意のマスを選び、そのマスの属するウェルから 1 グラムの絵の具を取り出して画伯に渡す。ただし、そのウェルの絵の具が 1 グラムに満たないようなマスを選択することはできない。
3. 任意のマスを選び、そのマスの属するウェルから 1 グラムの絵の具を廃棄する。1 グラムに満たない場合は、すべて廃棄される。
4. 隣接する 2 マス $s, t$ を選び、仕切りを出し入れする。

   * 仕切りを引っ込めたことにより 2 つのウェルが合併された場合、絵の具は混ざって 1 色になる。
   * 仕切りを出したことにより 1 つのウェルが 2 つに分割された場合、容量に比例する形で絵の具も分割される。すなわち、分割前の絵の具量が $v$、$s$ 側の容量が $v\_s$、$t$ 側の容量が $v\_t$ のとき、$s$ 側に残る絵の具量は $v \times \frac{v\_s}{v\_s + v\_t}$、$t$ 側には $v \times \frac{v\_t}{v\_s + v\_t}$ となる。

操作 2 は、**ちょうど $H$ 回**行わなければならない。$H$ 回に満たない、または超過した場合は、`WA` となる。

### 計算誤差について

絵の具の量は分数値となるため、操作 2 における「1 グラム以上」の判定を厳密に行うことが難しい。  
そのため、ジャッジプログラムでは絵の具量を倍精度浮動小数（double）で管理し、操作 2 の可否判定および取り出し量を、内部値 $v$（グラム）に基づいて以下のように処理する。

- **操作可否の判定**

  - $v < 1 - 10^{-6}$ の場合：「1 グラム未満」と見なされ、操作 2 は実行できない。
  - $v \geq 1 - 10^{-6}$ の場合：「1 グラム以上」と見なされ、操作 2 を実行できる。

- **取り出し量の決定**

  - $v \geq 1$ の場合：ちょうど 1 グラムを取り出す。
  - $1 - 10^{-6} \leq v < 1$ の場合：ウェル内の絵の具をすべて取り出す。

なお、配布ツールもジャッジプログラムと**完全に同一の挙動**をするように実装されている。

## 得点

$i$ 番目に画伯に渡した絵の具の色を $(C_i^\mathrm{made}, M_i^\mathrm{made}, Y_i^\mathrm{made})$ としたとき、誤差 $E$ を以下で定義する：

$$
E = \sum_{i=0}^{H-1} \sqrt{(C_i^\mathrm{target} - C_i^\mathrm{made})^2 + (M_i^\mathrm{target} - M_i^\mathrm{made})^2 + (Y_i^\mathrm{target} - Y_i^\mathrm{made})^2}
$$

操作 1 を行った回数を $V$ としたとき、以下の絶対スコアが得られる：

$$
1 + D \cdot (V - H) + \mathrm{round}(10^4 \times E)
$$

**絶対スコアは小さければ小さいほど良い。**

各テストケース毎に、$\mathrm{round}(10^9\times \frac{\text{全参加者中の最小絶対スコア}}{\text{自身の絶対スコア}})$ の**相対評価スコア**が得られ、その和が提出の得点となる。

最終順位はコンテスト終了後に実施されるより多くの入力に対するシステムテストにおける得点で決定される。  
暫定テスト、システムテストともに、一部のテストケースで不正な出力や制限時間超過をした場合、そのテストケースの相対評価スコアは0点となり、そのテストケースにおいては「全参加者中の最小絶対スコア」の計算から除外される。  
システムテストは**CE（コンパイルエラー）以外の結果を得た一番最後の提出**に対してのみ行われるため、最終的に提出する解答を間違えないよう注意せよ。

### テストケース数
- 暫定テスト: 50個  
- システムテスト: 2000個、コンテスト終了後に [seeds.txt](https://img.atcoder.jp/ahc048/seeds.txt) (sha256=e93b5367e87f49c8fe325dbeb0f8daa331d23481c1eb533ff032c7978e39ae04) を公開

### 相対評価システムについて
暫定テスト、システムテストともに、**CE 以外の結果を得た一番最後の提出のみが順位表に反映**される。  
相対評価スコアの計算に用いられる各テストケース毎の全参加者中の最小絶対スコアの算出においても、順位表に反映されている最終提出のみが用いられる。

順位表に表示されているスコアは相対評価スコアであり、新規提出があるたびに、相対評価スコアが再計算される。  
一方、提出一覧から確認出来る各提出のスコアは各テストケース毎の絶対スコアをそのまま足し合わせたものであり、相対評価スコアは表示されない。  
最新以外の提出の、現在の順位表における相対評価スコアを知るためには、再提出が必要である。  
不正な出力や制限時間超過をした場合、提出一覧から確認出来るスコアは0となるが、順位表には正解したテストケースに対する相対スコアの和が表示されている。

### 実行時間について
実行時間には多少のブレが生じます。  
また、システムテストでは同時に大量の実行を行うため、暫定テストに比べて数%程度実行時間が伸びる現象が確認されています。  
そのため、実行時間制限ギリギリの提出がシステムテストで**TLE（実行時間制限超過）**となる可能性があります。  
プログラム内で時間を計測して処理を打ち切るか、実行時間に余裕を持たせるようお願いします。

## 入力

入力は以下の形式で標準入力から与えられる。

$$
N K H T D\\
C_0^{\mathrm{own}} M_0^{\mathrm{own}} Y_0^{\mathrm{own}}\\
⋮\\
C_{K-1}^{\mathrm{own}} M_{K-1}^{\mathrm{own}} Y_{K-1}^{\mathrm{own}}\\
C_0^{\mathrm{target}} M_0^{\mathrm{target}} Y_0^{\mathrm{target}}\\
⋮\\
C_{H-1}^{\mathrm{target}} M_{H-1}^{\mathrm{target}} Y_{H-1}^{\mathrm{target}}\\
$$

- パレットのサイズ $N$ は、すべてのテストケースで $N = 20$ に固定されている。
- チューブ絵の具の種類数 $K$ は、$4 \leq K \leq 20$ を満たす。
- 作成すべき色の数 $H$ は、すべてのテストケースで $H = 1000$ に固定されている。
- 操作可能な最大ターン数 $T$ は、$4000 \leq T \leq 64000$ を満たす。
- チューブから絵の具を 1 グラム出す際のコスト $D$ は、$10 \leq D \leq 10000$ を満たす。

## 出力

まず、初期状態における仕切りの配置を、以下の形式で標準出力に出力せよ

$$
v_{0,0} ⋯ v_{0,N-2}\\
⋮\\
v_{N-1,0} ⋯ v_{N-1,N-2}\\
h_{0,0} ⋯ h_{0,N-1}\\
⋮\\
h_{N-2,0} ⋯ h_{N-2,N-1}\\
$$

* \$v\_{i,j}\$ は、マス \$(i, j)\$ とマス \$(i, j+1)\$ の間の縦の仕切りの状態を表す。\$v\_{i,j} = 0\$ の場合、仕切りは下がっており、\$v\_{i,j} = 1\$ の場合、仕切りは出ている。
* \$h\_{i,j}\$ は、マス \$(i, j)\$ とマス \$(i+1, j)\$ の間の横の仕切りの状態を表す。\$h\_{i,j} = 0\$ の場合、仕切りは下がっており、\$h\_{i,j} = 1\$ の場合、仕切りは出ている。

次に、最大で \$T\$ 行の操作を出力せよ。
\$t\$ 行目には、\$t\$ ターン目に行う操作を、以下の形式で出力する。

* マス \$(i, j)\$ の属するウェルにチューブ \$k\$（\$0 \leq k \leq K-1\$）から絵の具を 1 グラム追加する場合：

$$
1 i j k
$$

* マス \$(i, j)\$ の属するウェルから 1 グラムの絵の具を取り出して画伯に渡す場合：

$$
2 i j
$$

* マス \$(i, j)\$ の属するウェルから 1 グラムの絵の具を取り出して廃棄する場合：

$$
3 i j
$$

* マス \$(i\_1, j\_1)\$ とその隣接マス \$(i\_2, j\_2)\$ の間の仕切りを出し入れする場合：

$$
4 i_1 j_1 i_2 j_2
$$


## 入力生成方法

- $\mathrm{rand}(L,U)$: $L$ 以上 $U$ 以下の整数値を一様ランダムに生成する。
- $\mathrm{rand\_double}(L,U)$: $L$ 以上 $U$ 以下の実数値を一様ランダムに生成する。

### $N$, $K$, $H$, $T$, $D$ の生成

- $N = 20$
- $K = \mathrm{rand}(4,20)$
- $H = 1000$
- $T = \mathrm{round}(4000 \times 2^{\mathrm{rand\_double}(0,4)})$
- $D = \mathrm{round}(10^{\mathrm{rand\_double}(1,4)})$

### チューブ絵の具 $(C^{\mathrm{own}}, M^{\mathrm{own}}, Y^{\mathrm{own}})$ の生成

各 $i$ に対して、以下のように独立に生成する。

- $C_i^{\mathrm{own}} = \mathrm{rand}(0,10^5) \times 10^{-5}$
- $M_i^{\mathrm{own}} = \mathrm{rand}(0,10^5) \times 10^{-5}$
- $Y_i^{\mathrm{own}} = \mathrm{rand}(0,10^5) \times 10^{-5}$


#### 目標色 $(C^{\mathrm{target}}, M^{\mathrm{target}}, Y^{\mathrm{target}})$ の生成

各 $i$ に対して、以下の手順で独立に生成する。

1. $K$ 個の値 $x_0, \dots, x_{K-1}$ を、$x_k = -\ln \mathrm{rand\_double}(0, 1)$ により生成する。ここで $\ln$ は自然対数である。

2. 正規化：$x_k' = x_k \Big/ \sum_{j=0}^{K-1} x_j$ とする。

3. 次の式により、目標色の各成分を生成する：

$$
C_i^{\mathrm{target}}=\mathrm{round}\left(10^5\times \sum_{k=0}^{K-1}x_k' C_k^\mathrm{own}\right)\times 10^{-5}
$$

$$
M_i^{\mathrm{target}}=\mathrm{round}\left(10^5\times \sum_{k=0}^{K-1}x_k' M_k^\mathrm{own}\right)\times 10^{-5}
$$

$$
Y_i^{\mathrm{target}}=\mathrm{round}\left(10^5\times \sum_{k=0}^{K-1}x_k' Y_k^\mathrm{own}\right)\times 10^{-5}
$$
