## 目標など
- 水パフォ、もしくは青パフォ
- 200位以内に入りたい

## 課題
- どのような順路で移動するか
- 配列Aをどのように決めるか
- WAになる
  - main_02の配列Aの出力だと思う
- TLEする
  - near_listの要素数を減らそう

### 何故かREになる(解決済み)
- ~~icecreamの問題か？~~(違った)
- next_posがループしてpath_listが埋まったっぽい

## 案など
- next_city候補の2番目をすでに通っていたらそちらを採用する
  - 信号操作の短縮が見込める(多分)
  - 遠回りになり、逆に信号操作が増えるかも？

- 一部の都市を通行止めにする (優先度低め)
  - 通る都市が少なく、信号操作が少なくなりそう
  - かなりの都市を通行止めにする必要があり、遠回りになりそう
  - あまり効果は見込めなさそう(多分)

- 幹線道路の制定 (採用)
  - 幹線道路というより路線バスに近いかも
  - 通る道のパターンができると、信号操作がかなり楽になりそう
  - どうやって効率的な幹線道路を制定するのか？
    - 放射状・碁盤の目など
    - 環状なら作りやすそう
    - 田の字でも良さそう
    - 米の字が簡単で効果ありそう
    - まずは十字からで、その次に米の字にしたい
  - かなり難しそう

- ブロック毎に信号を点灯させる
  - 路線バスの派生
  - どのようにブロックを作るか

- 中心から螺旋状の路線を伸ばす
  - 駅の重複なしで広範囲をカバーできる
  - 場合によってはかなり遠回りになりそう

- 一本道ですべての都市をつなぐ
  - 螺旋の派生
  - 螺旋で良い気がする
  - 非効率な気がする


### 路線バス方式(幹線道路)について
- 想像以上に効果があった。
- 路線が多ければ多いほど良さそう
  - l_bにもよるが、コスト3か4くらいで端から端まで横断できそうな感じだった。
  - ほとんどコストなしと見て良さそう。
- なので、四方八方に路線を伸ばす方針で行きたい。
- 十字にはできたので、次は米の字を作りたい
  - 簡略化のため、必ず一度中心を通るようにしたい。
- 一部のケースでREになる
- 基本的は米の字の路線で、配列Aにすべての都市が入らないようであれば螺旋
- 螺旋を使って最寄り駅へ移動
  - 配列Aが足りなくなりそう
- 米の字にできた。

## 次の案など
- 上位陣は目的地1つあたりコスト2くらいで済ませている。
- 駅までの徒歩移動がネック
- 碁盤の目に路線を並べ、いい感じに乗り換えできるようにする
  - どうやって乗り換えできるようにするか
- 降りる駅を求めるとき、移動を計算するときの道順が逆になっているため、反転に対応する
- 路線に入っていない区間でも、もっと効率的に移動したい。
- 配列Aの徒歩の部分の並べ方を改良したい。
- 配列Aにない都市のうち、直前の都市から最も近いものを新たに配列Aに追加する (採用)
  - どこを開始地点にするか
    - 中心?角?
    - ひとまず中心でやる
  - 目的地のリストにあることが最優先
  - 次に直前の都市とつながっていること
  - その中で、直前の都市とのユークリッド距離が最も小さいものを選ぶ
  - 旧式のほうが良い場合は、そちらに変更する
- よく通る通路を優先してもいいかも

### 04以降の課題
- 1つだけWAになる
  - 手元のテストケース100件のうち、main_01に移行するケースが1つもなかった。
    - 01への移行がうまく行っていないのか？
    - すべて試して、ビジュアライザでエラーが出るか確認しよう

## 次の案など
- やはり上位陣には敵わない
  - 200位以内には入りたい
- WAの原因を探る
- 予測コストの精度を上げる
- 経路の探索にダイクストラ法を用いる
  - ダイクストラ法わからん
  - NumPyとかSciPyとかでなんとかなるやろ
  - ワーシャルフロイド法に変更
  - 幅優先探索で良いらしい

### 05以降の課題
- めっちゃ遅い
  - NumPyとSciPyのせいだと思う
- BFSにしたら解決した。

## 次の案など
- 路線はfind_pathのままの方がいいかも？
  - 07で採用
  - 逆効果だった。