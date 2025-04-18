# AHC044

## 概要
- 掃除当番の頻度を決める
- Lが500000と非常に多い
  - 途中までで切り上げてもいいかな

## 01の方針
- 理想の掃除回数を重みとして、aiとbiをランダムに割り当てる

## 01提出
提出前スコア: 0 (未提出)
提出前順位: 457位
スコア: 92,156,008
順位: 370位

## 01を踏まえて
- 順位が悪い
- 112,722,738点の人が多い
- 番号が若い順だろうか
- 一旦試す

## 02の方針
- 番号が若い順

## 02提出
提出前スコア: 92,156,008
提出前順位: 498位
スコア: 112,722,734
順位: 318位

## 02を踏まえて
- スコアと順位が上がった
- 納得できない

## 03の方針
- aiは02でbiは01

## 03提出
提出前スコア: 112,722,734
提出前順位: 344位
スコア: 108836824
順位: 349位

## 03を踏まえて
- 普通に悪かった

## これからの方針
- 山登り -> 焼きなまし
- 試行回数は1万週(仮)

## 04の方針
- 最初はランダムに割当て
- aかbから10個選び、ランダムに変える
- 前より良かったら採用
- これを時間ギリギリまで繰り返す
- 結果が良くないので中断
- 想定通りに動くようになったったので提出
  - 10個のところは200にした。

## 04提出
- TLE
- 攻めすぎた
- 05のほうが良さそうなので05の提出を優先


## 05の方針
- ノルマが多い順にソート
- aはソートした順
- bは一定の区間ごとに先頭の社員を入れる
  - ほかはaと同じ

## 05提出
提出前スコア: 112,722,734
提出前順位: 651位
スコア: 135,445,910 
順位: 304位

## 05を踏まえて
- かなりの躍進

## 06の方針
- 基本は05と同じ
- 先頭を0にする
- 05のほうが良さそう

## 07の方針
- dを定数から変えたい
- dを毎回減らす
- 変数xとdx

## 07提出(1回目　x=35, dx=8)
提出前スコア: 135,445,910
提出前順位: 359位
スコア: 138,203,938
順位: 292位

## 07を踏まえて
- 順位がそこそこ上がった

## 次の方針
- 2つある
  - xとdxを山登り
  - 最初に戻る位置を乱択or山登り
- どちらも計算量が重要
- c++への変換は必須
- ひとまず07をc++に変換し、計算量の様子を見る
  - 3ms
- かなり高速
- これなら両方ともいけそう

## 08の方針
- xとdxを山登り
- 範囲を指定して総当りできそうな計算量
- xを20から50まで
- dxを4から16まで
- c++に変換し、提出

## 08提出
提出前スコア: 138,203,938
提出前順位: 389位
スコア: 138,834,244
順位: 362位

## 08を踏まえて
- 07提出時点の順位あたりまで巻き返せた

## 09の方針
- 最初に戻る位置を乱択or山登り
- ビームサーチでもいいのでは
  - 無理そう
- 08の最適解の折り返し地点をそれぞれ±1して総当り
- +1に変更
- c++に変換し、確認していないが提出

## 09提出
提出前スコア: 138,834,244
提出前順位: 416位
スコア: 138,855,296
順位: 418位

## 09を踏まえて
- ごく僅かにスコアが上がった
- やらないよりはマシ