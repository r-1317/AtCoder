# AHC041

## 最初の方針
- ランダムに複数の根を選び、そこから高さ10までBFS
- 最も良かった根付き木を採用(貪欲法)
- ビームサーチやChokudaiサーチもありかも
- すべての頂点を根にして試す
  - 1回だけなら計算量の問題もないだろう
  - 初回だけやっても大した意味なさそう
- やっぱり100とかにする
### 100の場合の計算量
  - 1回に1つだけ選ぶので、1000回繰り返す
  - 辺の数は頂点の数の3倍までなので、頂点一つを探索すると、平均2つの新たな頂点が見つかる(多分)(未検証)
  - なので1回あたりの平均は最大で10230(おそらく)
    - 196830だった
  - それを毎回100回やると、9.8513415×10¹²
    - あかんやん
- 新規頂点の平均の数は本当にそうなのか?

## 01の方針
- BFSでは高さが出せる頂点を先にとってしまうのでは
- 高いところから攻める
- まず、未探索の頂点の中で最も美しさが高いものを基準に深さ5までBFSした木を作成
  - 高得点は得られないかもしれないが、安定のため
- 次に、その木の葉の中で美しさが最低のものを根とし、深さ10までBFS
- この方法では、少ない計算量で安定した得点が取れるのではないか
  - 上位を狙うのは厳しいかも
- 大変だったので中断

## 02の方針
- 美しさが最も低いものを根にBFS
- これを未探索の頂点がなくなるまで繰り返す

## 02提出
提出前スコア: 0 (未提出)
提出前順位: 729位くらい (不正確)
スコア: 56112269
順位: 392位だったと思う (記録忘れ)

## 02を踏まえて
- 意外と木の数が少ない
- サンプルケース0の場合、6本
- 最初の方針でも良さそう

## 03の方針
- 最初の方針の100回バージョンをとりあえず作る
  - chokudaiサーチでも良さそうだが、まずは貪欲法
- これ最初が一番計算量多い
- 100とかの数をxと呼ぶ
- よく考えたら探索する頂点の数が1000を超える訳がない
- x = 1000(全探索)でもいけるのでは
- 未探索なのに認識されないバグがある
- その点も根として、とりあえず提出

## 03提出 (1回目  バグ未修正)
提出前スコア: 56,112,269
提出前順位: 530位
スコア: 57,150,564
順位: 495位

## 03を踏まえて(1回目)
- あんま変わらん
- まずはバグ修正
- chokudaiサーチの実装を優先してもいいかも
- やっぱバグ修正を優先
- 数分でなんか動く状態になった

## 03提出(2回目  バグ修正済み)
提出前スコア: 57,150,564
提出前順位: 519位
スコア: 0(TLE)
順位: 523位

## 03を踏まえて(2回目)
- まさかのTLE
- 真面目にバグ修正をする
- 15分くらいを限度にする

## 03提出(3回目  TLEが偶然であったか確かめるため、同じコードをもう一投)
- やっぱりTLE
- もう諦めてchokudaiサーチを実装する
- やっぱやめる

## 04の方針
- 木の組み換え
- すべての葉に対し、今の高さよりも高くなることができるなら、親を変える
- 変えられる葉がなくなるまで続ける
- 木の選び方を頂点の数に変えてもいいかも
  - まずは変えずに提出

## 04提出 (1回目  評価方法03のまま)
提出前スコア: 57,150,564
提出前順位: 630位
スコア: 0(WAとRE)
順位: 632	位

## 04を踏まえて(1回目)
- ACが1件もなかった
- 手元のテストで誤って04を実行していた
- 根なしの木があるらしい
- 新たな親を葉リストから除外するのを忘れていた。

## 04提出 (2回目  評価方法03のまま  バグ修正?)
提出前スコア: 57,150,564
提出前順位: 657位
スコア: 64,473,765
順位: 492位

## 04を踏まえて(2回目)
- まあまあの結果
- 木の選び方を頂点の数に変える

## 05の方針
- 基本的に04と同じ
- 木の選び方を頂点の数に変更

## 05提出 (1回目)
提出前スコア: 64,473,765
提出前順位: 507位
スコア: 64,411,186
順位: 507位

## 05を踏まえて
- 悪化している
- 時間的に厳しいが、04のchokudaiサーチを実装
- やっぱやめる

## 06の方針
- 04の良かったBFSの上位n個に対して木の組み換えを行う
- まずはn=2
- バグがある
- 治らないままコンテストが終了した。

## 振り返り
- どうやらDFSが良いらしい
- 葉でなくても組み換えできる
- 上位陣の解法を見ていると、意外と頂点数がある
  - 少なければ良いというものでもないのか

  ## 07の方針
- 深さDまで美しさの小さい順に貪欲でたどる
- そこからはBFS

## 07提出 (1回目)
- 1つだけRE

## 08の方針
- 07の貪欲を04に移植
- Dを増やすほど時間がかかる
  - 訪問する頂点数は少なくなるはず(未検証)
  - 直感に反する
- test0で試した結果、D=5が一番よかった
  - 本来はサンプル増やすべき

## 08提出
スコア: 70,783,919
延長戦順位: 250位

## 08を踏まえて
- Perf 1718くらい
- なかなか良い結果