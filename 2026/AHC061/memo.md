# AHC061

## 00提出
- 提出前の相対スコア: 
- 提出前順位: /
- 提出日時: 
- 絶対スコア: 
- 相対スコア: 
- 順位: /

## はじめに
- 開始直後に空白を提出してみよう
- ワンチャンshortestとれる

## 空白の提出
- 提出前の相対スコア: 0(未提出)
- 提出前順位: (見てない。おそらく全員同率1位)
- 提出日時: 2026-02-13 19:00:05
- 絶対スコア: 0
- 相対スコア: 0
- 順位: 1/3
---
- 最速は取れなかったと思う
- 同じこと考えている人が5人くらいいた

## 最初の方針
- 自分以外のNPC的なのがいるのか
  - 珍しい
- ~~AIの行動は完全に予測できる~~
  - 非公開の変数があるっぽい
- もしかして非公開変数予測ゲーだったりする?
  - 流石にないか
- なんか強化学習とかが強そうな気もする
- 条件付きでビジュアライザの画像を公開してもいいのか
- ビジュアライザを見ると、相手の動作を封鎖したら強そう
- とりあえず手動操作をしてゲームの戦略を掴む
### 手動操作
- 近くにある価値の高いマスを優先して取る
- 相手が近くにいるなら防衛に向かう
- 分断が強い? 
- 攻撃しても駒の位置は変わらないか
- 分断された領土は防衛できない
- 一撃で分断されないように
- 自分の領土で囲った空マスには誰も手出しできない
- レベル1が2つよりもレベル2を1つのほうが強そう
- 普通にCPが強いな
- 手動で勝てないなら何もわからん
- ここから追記
- 領土保全が大事な気がする
- 国境はすべて複数レベルがいい
---
- むずくね
  - 難しいのは皆同じはず
- MiniMaxかな
- 知識科学概論のやつ見返すか
- あんまわからん
- プレイヤーの数が多いからMiniMaxは使えない?
- とりあえずスコアで貪欲するか?

## 01の方針
- 手番ごとにスコアで貪欲
  - やっぱ最高得点のCPとの比率にしよう
- 盤面は3つに分けよう
- 他プレイヤーはその場から動かないものとする

## 01提出
- 提出前の相対スコア: 0
- 提出前順位: 405/441
- 提出日時: 2026-02-14 14:03:44
- 絶対スコア: 11758690
- 相対スコア: 46,814,511,307
- 順位: 160/441

## 01を踏まえて
- 上位陣もCP相手に圧勝と言うわけではないのか
- いや割と圧勝してるか
- そういえばlogスケールで評価されるんだった
- 同率がいないのは意外
### この後どうするか
- わりと強化学習くらいしか案がない
- でも強化学習やったことない
- N固定なのでやりやすそう
- 入力
  - 自分の領土2値(100個)
  - 他人の領土2値(100個)
    - 誰のとかはこだわらなくてもいいだろうか
    - 人数ごとに対応が違うの困るから
  - 他人の駒が置いてあるエリア2値(100個)
  - 各マスの価値(100個)
  - 各マスのレベル/上限レベル(100個)
- 出力
  - 次に移動するマスのone-hotベクトル(100個)
- 別のファイルに書こう
- copilotがすごくうまいことやってくれた
```
python train01.py --epocs xxx
python export_g01.py --model tmp_best2.model.json --out g-xxx.py
```
- 1エポック1時間くらいかな
- ABCまでにはギリ学習終わるか
- 提出まで行けるかな
- メモ: `python export_g01.py --model trained_best.model.json --out g-01-0214T2058.py`
  - 01はエポック数
- ギリ終わった
- 提出ファイルのの書き出しまでしてからABC
- ABCは解けそうな問題は解けたので、20分くらい残してAHCに戻る
- 0000.txtでテスト
- 普通に弱すぎるな
- 学習が足りないのか?
- 評価関数も無理がある
### v2
- rustは並列処理が強いと聞いた
- copilotに任せる
- 質問とかしてくれるのか
  - いいね
```
cargo run -q --bin train02 -- --start 0 --end 1 --generations 2 --eval-cases 1 --parents 2 --children 4 --threads 2 --save-model /tmp/ahc061_train02_test.model.json
```
- 0215T1059
  - ` cargo run -q --bin train02 --save-model ../v2-models/0215T1059.json`
  - 一向に表示が変わらないので中断
- 0215T1108
  - `cargo run -q --bin train02 -- --start 0 --end 999 --epochs 10 --eval-cases 1 --parents 10 --children 100 --threads 8 --save-model /tmp/0215T1108.model.json`
- いうほど速くないな
- 隠れ層を増やしたからかな
- まあでも、そこそこ速い
- 数時間で終わりそう
- 違う、これやっと1周したところか
  - あと9周あるのか
- 一晩放置するしかないか
- 8個並列で1週100分くらいか
- 60週するとなると800コア時間かかるか
- 普通にスコア低くない?
- うまく行かないっぽい
- あまり希望が持てないので中断
- 思い切って親の数を減らすか?
- 0215T1353
  - `cargo run -q --bin train02 -- --start 0 --end 999 --epochs 1 --eval-cases 1 --parents 4 --children 32 --mutation-sigma 0.05 --threads 8 --save-model /tmp/0215T1353.model.json`
  - `python export-g02.py --model /tmp/0215T1353.model.json --out v2-codes/g02-0215T135.py`
- 中間層の次元数を変更できるように
- 例: `cargo run -q --bin train02 -- --hidden-dim 800 --in-dir ../in --start 0 --end 999 --threads 8`
- 軽量で世代数だけ重ねるか
- 0215T1442
  - `cargo run -q --bin train02 -- --start 0 --end 999 --epochs 20 --eval-cases 1 --parents 4 --children 32 --hidden-dim 30 --mutation-sigma 0.02 --threads 8 --save-model ../v2-models/0215T1442.model.json`
  - `python export-g02.py --model v2-models/0215T1442.model.json --out v2-codes/g02-0215T1442.py`
- 世代を経るごとに伸びているようには思える
- これを実際に使えるようにするにはかなりの計算量が必要なのでは
- ほぼ動かない
- 遺伝的アルゴリズムは失敗か?
  - 上手い人がやれば強いのだろう
- best_fitには意味がない
  - 最後の世代で最も評価の高かったものを出力するように変更
- もう一度同じことをする
- 0215T1553
  - `cargo run -q --bin train02 -- --start 0 --end 999 --epochs 20 --eval-cases 1 --parents 4 --children 32 --hidden-dim 30 --mutation-sigma 0.02 --threads 8 --save-model ../v2-models/0215T1553.model.json`
  - `python export-g02.py --model v2-models/0215T1553.model.json --out v2-codes/g02-0215T1553.py`
- わずかながら伸びた
- これ学習するのきついな
  - どこまで伸びるかもわからんし
- hidden-dim=200でどれだけかかるか
- 0215T1706
  - `cargo run -q --bin train02 -- --start 0 --end 999 --epochs 1 --eval-cases 1 --parents 4 --children 32 --hidden-dim 200 --mutation-sigma 0.02 --threads 8 --save-model ../v2-models/0215T1706.model.json`
  - `python export-g02.py --model v2-models/0215T1706.model.json --out v2-codes/g02-0215T1706.py`
  - `cargo run -r --bin tester python3 ../v2-codes/g02-0215T1706.py < in/0000.txt > result.txt`
- 200だと1エポックあたり12-13分くらいか
- これノートPCの方だともっと早くならんか
  - CPUがcore i7 12700H なので
- Rustのインストールからやるか
- 0215T1810
  - `cargo run -q --bin train02 -- --start 0 --end 999 --epochs 1 --eval-cases 1 --parents 4 --children 32 --hidden-dim 200 --mutation-sigma 0.02 --threads 18 --save-model ../v2-models/0215T1810.model.json`
  - `python export-g02.py --model v2-models/0215T1810.model.json --out v2-codes/g02-0215T1810.py`
  - `cargo run -r --bin tester python3 ../v2-codes/g02-0215T1810.py < in/0000.txt > result.txt`
- 別にそんな早くない?
- 10分くらい
- 思ったほどの差はなかった
- CPU使用率が低いままだったな
- 途中で中断できるように適宜保存するように変更しよう
  - した
- 1エポック12分換算で、60エポックは12時間くらい
- とりあえず300エポック回すか
  - 途中で止められるわけだし
- 0215T2000
  - `cargo run -q --bin train02 -- --start 0 --end 999 --epochs 300 --eval-cases 1 --parents 4 --children 32 --hidden-dim 200 --mutation-sigma 0.02 --threads 12 --save-model ../v2-models/0215T2000.model.json`
  - `python export-g02.py --model v2-models/0215T2000.model.json --out v2-codes/g02-0215T2000.py`
  - `cargo run -r --bin tester python3 ../v2-codes/g02-0215T2000.py < in/0000.txt > result.txt`
- スレッド数を12にしても普通に動く
- 学校から帰ってきた段階で90エポック
  - そこで打ち切り

### v3
- 入力層と評価値を変更
- 詳細は`GA-plan-v3.md`
```
v3の加点重みをCLI引数化しました（デフォルトは元のまま）
--rw-level-up（default 1.0）
--rw-occupy（default 1.2）
--rw-attack-capture（default 2.0）
--rw-attack-damage（default 0.8）
--rw-lose-cell（default -0.7）
clapの都合で --rw-lose-cell -0.9 だと -0.9 をオプション扱いして落ちるので、--rw-lose-cell=-0.9 の形式で渡してください。
```
- 0216T1800
  - `cargo run -q --bin train03 -- --start 0 --end 999 --epochs 300 --eval-cases 1 --parents 4 --children 32 --hidden-dim 200 --mutation-sigma 0.02 --threads 12 --save-model ../v3-models/0216T1800.model.json`
  - `python ../export-g03.py --model v3-models/progresxxx-0216T1800.model.json --out v3-codes/g03-progresxxx-0216T1800.py`
  - `cargo run -r --bin tester python3 ../v3-codes/g03-progresxxx-0216T1800.py < in/0000.txt > result.txt`

## 次の案を練る
- CPの内部パラメータ$wa_{p}$から$wd_{p}$の最適なものを探る
  - 焼きなましとかでいけると思う

### v3修正
- v3の方のファイルに記載
```
--eval-cases のデフォルトを 20 にしました
使い方例
cargo run --release --bin train03 -- --start 0 --end 999 --epochs 50 --eval-cases 20 --hidden-dim 600 --save-model ../trained_best_v3.model.json
```

- 0216T1830
  - `cargo run -q --bin train03 -- --start 0 --end 999 --epochs 300 --eval-cases 20 --parents 4 --children 32 --hidden-dim 200 --threads 12 --save-model ../v3-models/0216T1830.model.json`
  - `python ../export-g03.py --model ../v3-models/progressxxx-0216T1830.model.json --out ../v3-codes/g03-progressxxx-0216T1830.py`
  - `cargo run -r --bin tester python3 ../v3-codes/g03-progressxxx-0216T1830.py < in/0000.txt > result.txt`

- 020の段階でテスト
- 上がってはいるが、微妙
  - 明日帰ってからまた見るか
- 帰ってきたので試す
  - 27865
- ランダムより悪くない?
- 一旦GAから離れるか
- 追記: 更に1晩経ってもあんま変わらん

## 次の案を練る
- ChatGPTに有力な案を聞いてみる
- CPのパラメータがわかれば強いよな
- 途中までやってパラメータ予測できないかな
- ランダムの行動があるから厳しいか
- 平均的なパターンを計算してモンテカルロ法とか

## 02の方針
- 基本は01
- 自分もCPと同じような規則に基づいて行動する
- ランダム確率はは0とする
- やっぱ中断
- 再開
```
`task_a.md` に記載されている問題について、自分の操作するプレイヤー0も問題文中にあるAIと同じように行動するという解法に取り組んでいます。
そこで、ハイパーパラメータである $wa_{p}$, $wb_{p}$, $wc_{p}$, $wd_{p}$, $\epsilon_{p}$ の最適値を求めたいと考えています。
`in/0000.txt`から`in/0099.txt`の100ケースの得点の総和で評価値として、各パラメータを都度ランダムに設定して試行する山登り法で最適値に近い値を求めたいです。
指定された秒数が経過するまでその試行を繰り返し、試行回数と最適なパラメータを出力するプログラムを`tools`ディレクトリ内に`optimize01.rs`として作成してでださい。
AIの挙動については、`tools`ディレクトリ内の`lib.rs`等を参考にしてください。
```
- `lib.rs`変えよった
- `cargo run -r --bin optimize01 -- --sec 0.2`
- 1, 1, 0.3, 0.3, 0.5が強いのかな
- `cargo run -r --bin optimize01 -- --sec 120 --threads 10`
  - 12にするとCPU使用率がすべて100%に張り付く
  - 怖いから10にしよう
  - それでもなんか怖いので8にした
- 8並列で15分
```
# スコア計算の重み（今回は固定値）
A = 0.3967478050685961
B = 0.5197709763452972
C = 0.07427911229835994
D = 0.04794619663421519

# ランダムに移動する確率
Epsilon = 0.04096090055043922
```
- sum_score: 11581250
- 参考までに、01は 10712635

## 02提出
- 提出前の相対スコア: 41,166,464,020 
- 提出前順位: 477/925
- 提出日時: 2026-02-18 21:51:54
- 絶対スコア: 10573371
- 相対スコア: 40,631,679,70
- 順位: 491/925

## 02を踏まえて
- 下がった?
- 今日もPC回して最適値を探るか
- とりあえず9時間回す
- スレッド数は6にしておこう
  - 夜うるさくてもあれだし

```
trials 1911719
best_sum_score 11586713
wa 0.33170512098053534
wb 0.42828729584957725
wc 0.068163596687858
wd 0.03158541924602543
eps 0.038333012831001996
elapsed 32400.095s threads 6
```

## 03の方針
- 基本は01
- 相手が皆動かない前提でN手のシミュレーション
- 最も高スコアになれそうな
- 中断
