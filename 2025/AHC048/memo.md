# AHC048

## 概要
- 絵の具を混ぜて最適な色に近いものを作る
- $E(D) \risingdotseq 1445$

## 01の方針
- ビジュアライザを見た感じ、同系色の色ばかり
- 微調整で行けるのか？

## 01の方針
- まずは最も近い色の絵の具をそのまま提出

## 01提出
- 提出前の相対スコア: 0(未提出)
- 提出前順位: 361/398(未提出)
- 提出日時: 2025-05-31 10:25:27
- 絶対スコア: 109690905
- 相対スコア: 2,900,274,487
- 順位: 186/399

## 今後の方針
- 区画を大きめに区分けして、最大2つまで足して最適な色を作る
- 最大の足す数はDによって変えてもいいかも
- 4*4で25枠

## 02の方針
- 4*4の25枠を作る
- 最大2つまで足して最適な色を作る
- 枠が足りない場合は絵の具を減らす
- まずはサイズ5から
  - 行けそうなら4
- ビームサーチやchokudaiサーチも使えそう
- 1枠目しか使われない
- 混ざった色のほうが近いのは入力生成方法を見たらわかる
- 最初からいっぱい混ぜておく
- ランダム初期化は有無を見たほうが良い

## 02提出(ランダム初期化なし)
- 提出前の相対スコア: 2,028,043,875
- 提出前順位: 257/496
- 提出日時: 2025-05-31 16:31:35
- 絶対スコア: 109690905
- 相対スコア: 1,852,915,772
- 順位: 257/496

## 02を踏まえて(ランダム初期化なし)
- 01と全く同じ

## 02提出(ランダム初期化あり)
- 提出前の相対スコア: 1,676,762,627 
- 提出前順位: 273/519
- 提出日時: 2025-05-31 17:42:01
- 絶対スコア: 91553952
- 相対スコア: 2,041,416,258
- 順位: 262/520

## 02を踏まえて(ランダム初期化あり)
- 思ったより変わらない
- ウェルは多いほうがいいのか？
- コストの評価にミスがあった
- paletteの更新をしていなかった
- ウェルサイズは2がベスト？
  - それ以下は計算量がきつい

## 02提出(修正, サイズ2)
- WA
- TLEも

## 対処
- 原因がわかった
  - 絵の具が埋まってたときの破棄する数の計算が間違っていた
### C++に変換
- ローカルではコンパイルできない
- AtCoderではいけてるっぽい
- 結果が若干違う
  - 少しだけ良くなっている

## 02提出(再修正, C++)
- 提出前の相対スコア: 1,520,933,098
- 提出前順位: 295/588
- 提出日時: 2025-05-31 21:29:45
- 絶対スコア: 36436641
- 相対スコア: 7,273,552,366
- 順位: 47/588

## 02を踏まえて(再修正, C++)
- 凄まじい躍進
- このまま維持したい
- 精度は概ね文句なし
- コストの大部分は絵の具の量によるもの
- 最初に全マス埋める必要もない
- 半分だけとか、それ以下とか
- 絵の具のコストによって決まる？

## 今後の方針
- 初期の絵の具絵を減らす方針で行く
- 初期状態ごとの制度を確認した後、Dによって分ける
### 初期状態の種類
- 2*2の枠に、2色のみ入れる
  - 色の制度が厳しい？
- 4*4の枠に少量の絵の具を入れる
  - 絵の具の消費量は $\frac{1}{4}$ になる
  - 後半になると一度の調整での振れ幅が狭くなる
  - 精度に悪影響を及ぼすか、そうでもないか
- 2*2の枠の数を減らす。1枠の絵の具の量は3または2
  - これが最適だったら嬉しい
  - 101段階で調節できるので
- まずは3に減らして実行
  - 3に減らしても精度に悪影響はないはず
- ターン毎に絵の具を追加しないという選択肢
  - chokudaiサーチ等ではロスにならないと思うのでその必要はないのでは
- 900あたりからは何もしないも解禁？

## 03の方針
- 基本は02
- 1枠あたりの絵の具の初期量を3に減らす
  - 精度は悪くならないはず
- 今回からローカルでのテストを導入

## 03提出(枠あたり3)
- 提出前の相対スコア: 6,817,027,916
- 提出前順位: 59/656
- 提出日時: 2025-06-01 09:31:25
- 絶対スコア: 29958325
- 相対スコア: 7,004,842,853
- 順位: 55/656

## 03を踏まえて
- そこまで変わらなかった
- 何故かローカルだとC++がめっちゃ遅い
  - コンパイル時に `-O2` オプションをつけることで解決した
- 次は2色
- その前にスコアの総和をとる

### 03総スコア
- 54,453,686

## 04の方針
- 基本は03
- 先程4色から3色に減らした部分を、2色に減らす
### 04総スコア
- 50,207,944
- 後半の絵の具不足が目立つ
- ランダムでもいいかな
- 保留: 04のランダム
- その前に枠を大きくする

## 05の方針
- 基本は04
- 枠を4*4にし、絵の具は1/4
### 05総スコア
- 51,825,472
- やはり絵の具不足
- こちらもランダムかな

## 06の方針
- 基本は04
- コストが同じならば $(\frac{1}{ウェル数})^{\frac{1}{ウェル数}}$ の確率で遷移
- 一度遷移が起きたら遷移しない
- それでは上の方にたまりすぎている
- 一度遷移が起きたら確率を半分にする
- +0.2が丁度いいかな
- 乗算のほうがいいのだろうけど
### 06総コスト
- 44,315,680
- 07とどちらがいいか
- 枠の数を減らす方式が強かったら+0.2の値を1とかにする

## 07の方針
- 基本は05
- 遷移確率を06と同様に設定
### 07の総スコア
- 38,687,604
- とても良い
- 提出する価値がある

## 07提出
- 提出前の相対スコア: 6,992,588,316
- 提出前順位: 59/681
- 提出日時: 2025-06-01 13:37:42
- 絶対スコア: 19813720
- 相対スコア: 6,796,558,318 
- 順位: 64/681

## 07を踏まえて
- 奇妙なことが起きた
- 絶対スコアは大幅に改善されたのに相対スコアが若干減った
- 念の為06も提出しよう

## 今後の方針
- 終盤にはパージを許可してもいいかな
- パージを許可する時期はD値によって決まる
  - この想定と逆だったかな

## 06提出
- 提出前の相対スコア: 6,813,070,823
- 提出前順位: 66/685
- 提出日時: 2025-06-01 14:10:28
- 絶対スコア: 23966268
- 相対スコア: 7,187,300,530 
- 順位: 58/685

## 08の方針
- 基本は06
- 常にパージを許可
- j = 0を許可
- 予想通り、初期にすべてを使い果たしてしまう
  - 150~200くらいで
### 総スコア
- 108,871,673

## 09の方針
- 基本は07
- 常にパージを許可
- 100もたない
### 09総スコア
- 112,222,713

## 10の方針
- 基本は08
- 最後の850回目くらいからパージを許可
- ここの値は要調整
### 10総スコア
**lim = 850**
- 31,931,989
**lim = 800**
- 33,655,199
**lim = 900**
- 34,439,273
**lim = 825**
- 32,341,608
**lim = 875**
- 32,763,568
**lim = 840**
- 31,927,759
**lim = 860**
- 32,131,352
**lim = 845**
- 31,911,336

## 11の方針
- 基本は09
- 08 -> 10のような変更
### 11総スコア
**lim = 925**
- 31,454,219
**lim = 900**
- 29,917,317
**lim = 950**
- 33,743,730
**lim = 875**
- 31,452,107
**lim = 895**
- 30,187,326
**lim = 905**
- 29,996,222

## 10,11のまとめ
- 10は845、11は900が最適に近い
- 2つとも実行して良かったほうを使えないかな

## 10提出
- 提出前の相対スコア: 7,249,149,802
- 提出前順位: 63/708
- 提出日時: 2025-06-01 16:25:12
- 絶対スコア: 16936059
- 相対スコア: 7,913,643,513
- 順位: 56/708

## 11提出
- 提出前の相対スコア: 7,885,834,466
- 提出前順位: 55/710
- 提出日時: 2025-06-01 16:55:35
- 絶対スコア: 14693649
- 相対スコア: 7,896,276,408
- 順位: 55/710

## 10,11を踏まえて
- そこまでの変化はない
- 色を追加する際に捨てられる絵の具のコストが馬鹿にならないのでは

## 12の方針
- 基本は10
- 色を追加する際に絵の具を捨てたら追加と同じコストを足す
- 一時的にlimitはなし
- 遷移確率も調整しないと
### 12総スコア
**lim = 10000**
- 45,171,010
**lim = 0**
- 109,779,321
**lim = 850**
- 30,943,130
**lim = 830**
- 29,827,464
**lim = 820**
- 29,357,64
**lim = 810**
- 29,045,225
**lim = 800**
- 29,040,266
**lim = 805**
- 29,029,575
- やはり原因は色の制度か

## 13の方針
- 基本は11
- 色を追加する際に絵の具を捨てたら追加と同じコストを足す
### 13総スコア
**lim = 900**
- 29,882,494
**lim = 850**
- 33,111,890
**lim = 875**
- 31,418,145
**lim = 925**
- 31,577,453
**lim = 890**
- 30,478,331
**lim = 910**
- 30,463,934
**lim = 895**
- 30,114,941
**lim = 905**
- 30,131,836
**lim = 903**
- 30,009,753
**lim = 897**
- 30,027,385
**lim = 902**
- 29,951,571
**lim = 898**
- 29,976,395
**lim = 901**
- 29,917,296
**lim = 899**
- 29,933,375

## 12,13のまとめ
- 12は805、13は900が最適に近い

## 12提出
- 提出前の相対スコア: 7,602,416,921
- 提出前順位: 60/738
- 提出日時: 2025-06-01 20:23:44
- 絶対スコア: 15083982
- 相対スコア: 7,854,509,362
- 順位: 55/378

## 12を踏まえて
- 絶対スコアはやや悪化したが、相対スコアは伸びた。

## 13提出
- 提出前の相対スコア: 7,793,066,975
- 提出前順位: 57/745
- 提出日時: 2025-06-01 21:08:40
- 絶対スコア: 14473843
- 相対スコア: 7,731,897,522
- 順位: 57/745

## 13を踏まえて
- 絶対スコアはやや改善したが、相対スコアはわずかに悪化した。

## 今後の方針
- 13をchokudaiサーチ
- 組み合わせが少ないから
- 12もやってもいいかも
- 評価関数を変えようかな
- 向こうn件との色の一致度
  - 別にその時点で一致している必要はない

## 14の方針
- 基本は13
- chokudaiサーチ
- chokudaiサーチを実装するに当たり、追加しない選択肢の実装を改める必要がある。
- ランダムな配置もなくなる
- 一旦C++のコードもリセットするかも
-  `[visited(bool),total_tmp_cost, diff, add_count, [palette], [tmp_ans_list], 前の状態のindex]`
- 状態はIDをkeyとした辞書で管理
- 配列のほうが良さそう
- やはり絵の具が上の方に溜まる
- ランダムに微小な数をたそう
  - 0から0.001
  - 大きすぎるかな
- ~~C++に変換したらMLE~~
- メモリ確保のミスだった
### 14総コスト
- 30,357,366
- 13と比べても下がっていない

## 14提出
- 提出前の相対スコア: 4,947,213,191
- 提出前順位: 156/1021
- 提出日時: 2025-06-06 14:57:56
- 絶対スコア: 14835374
- 相対スコア: 4,830,028,339
- 順位: 157/1021

## 14を踏まえて
- 若干下がった
- bost_limitを2段階ではなく線形にする
- 10回に1回の周期にしたほうが良いのでは
  - やっぱなし