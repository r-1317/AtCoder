# AHC043

## 概要
- 鉄道網を作る
- 家・職場からマンハッタン距離2以内に駅があれば、家と職場のマンハッタン距離の資金が手に入る
- 敷いた線路は変更できない

## 最初の方針
- 初期資産の関係上、最初は駅2つから
- 路線を継ぎ足していく
- 動的計画法で最短経路を求める
  - スタート・ゴールともに異なるのでBFSでいいのでは
  - 平均858.5マスの訪問(多分)

## 01の方針
- まずは1本だけ
- 現在の資金で建てられる最長の路線を作る
- x軸、y軸の順番で敷く

## 01提出
- 提出前の相対スコア: 0(未提出)
- 提出前順位: 565位(未提出)
- 絶対スコア: 0(TLE)
- 相対スコア: 1,410,446,265
- 順位: 224位

## 01を踏まえて
- TLE
- 想定外
- 再提出したら治るかな
- Mが1600のケースで試したが79ms
- 1位は私の35倍のスコア
- 再提出する

## 01提出(2回目)
- 提出前の相対スコア: 1,410,446,265
- 提出前順位: 230位
- 絶対スコア: 0(TLE)
- 相対スコア: 1,410,446,265
- 順位: 230位

## 01を踏まえて(2回目)
- またTLE
- 偶然ではない
- 原因がわからない
- 手元のケースで1秒以上かかるものを探す
- o3-mini-highに
```
以下のようなshellスクリプトを作成してください。

- `python3でa01.py`を実行
- 標準入力をin/xxxx.txtから読み込む
  - xxxxには0000から0999までの数が入る
- a01.pyの実行時間を計測
- 実行時間が1秒を超えた場合、xxxxをtime.txtの1番下の行に追加する
```
- ハングアップしていた
- 再提出

## 01提出(3回目)
- 提出前の相対スコア: 1,405,912,225
- 提出前順位: 233位
- 絶対スコア: 2008706
- 相対スコア: 1,468,990,809
- 順位: 219位

## 01を踏まえて(3回目)
- 治った
- 実行時間は81msと、かなり余裕がある

## 02の方針
- 2本目に挑戦
- 1本目を敷き、資金が溜まり次第2本目
- 交差はなし
- どうやって決めよう
- 下が最も高いものと上が最も低いもの
  - それでも被るなら諦めて1つだけ
- 工事のqueueを作成し、毎ターンのシミュレーション
- 資金が溜まり次第次のマスに建設

## 02提出(1回目)
- 提出前の相対スコア: 1,361,004,504
- 提出前順位: 559位
- 絶対スコア: 547130	
- 相対スコア: 312,266,276
- 順位: 962位

## 02を踏まえて
- とても下がった
- 普通に効率が悪い
- 相対スコアの比較のために01を再提出しておく
- 2本敷いたら良いというものでもない

## 03の方針
- まずは初期資金で建設できる通勤経路を列挙
- その中で、家同士・職場同士の距離が最も近いものとの距離が最も小さいものを選ぶ
  - 01みたいに距離が長いものでもいいかも
- 2以内なら-5000とか
- 2以内なら追加の駅なし
- 線路上ならそこを駅に
- 当てはまらないなら駅まで線路を敷く

## 03提出(1回目)
- 提出前の相対スコア: 1,339,575,329
- 提出前順位: 656位
- 絶対スコア: 2218080
- 相対スコア: 1,293,125,957
- 順位: 671位

## 03を踏まえて
- 絶対スコアは少しだけ上がった
- 何故か相対スコアと順位は下がった
  - 上位層の提出とタイミングが被った？
- 距離が最も近いよりも01みたいに単体のマンハッタン距離が長いもので試す。

## 04の方針
- 基本は03と同じ
- 最初の住民は、01で選ぶ住民にする。
- 01と同じ結果も残し、最終的な資金が多かったほうを採用
### 実装完了
- 01の結果のほうが得点が良いことがほとんど

## 04提出(1回目)
- 提出前の相対スコア: 1,285,895,329
- 提出前順位: 690位
- 絶対スコア: 2008706
- 相対スコア: 1,332,688,584
- 順位: 677位

## 04を踏まえて(1回目)
- 01と全く同じ絶対スコア
- 相対スコアと順位は上がった
- 上位陣が不得意なケースで勝ってる？

## 05の方針
- 1本で2つの通勤経路を結べるなら、その中で最も収入の多いものを採用
  - それでも01のほうがよかったら、そちらを採用
- 

## 05提出(1回目)
- 提出前の相対スコア: 1,331,254,100
- 提出前順位: 679位
- 絶対スコア: 2048235
- 相対スコア: 1,266,137,656
- 順位: 695位

## 05を踏まえて(1回目)
- 01よりは絶対スコアは若干伸びた
- 03よりは少ない
- やはり順位は下がった
- よく見たら建設シミュレーションに渡す変数が違っていた
- 修正と再提出

## 05提出(2回目)
- 提出前の相対スコア: 1,263,372,891
- 提出前順位: 736位
- 絶対スコア: 2008706
- 相対スコア: 1,329,021,146
- 順位: 722位

## 05を踏まえて(2回目)
- 絶対スコアは下がり、相対スコアは上がった。
- 01と全く同じ絶対スコア

## 06の方針
- すべての路線に対し、ギリギリまで寄せた位置に駅を置く
- そのすべての資金をシミュレートし、最も多かったものを採用

## 06提出(1回目)
- 提出前の相対スコア: 1,329,021,146
- 提出前順位: 723位
- 絶対スコア: 2224359
- 相対スコア: 1,466,081,105
- 順位: 633位

## 06を踏まえて(1回目)
- かなり伸びた
- 特に順位