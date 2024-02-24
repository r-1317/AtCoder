
# メイン処理
def main():

  n = int(input())  # カードの枚数
  a_list = list(map(int, input().split()))  # カードの数字
  Alice_sum = 0  # Aliceの合計得点
  Bob_sum = 0  # Bobの合計得点

  # ゲーム開始
  for _ in range(int(n/2)):  # nが奇数なら1枚残る

    # Aliceの番
    tmp = a_list.index(max(a_list))  # 最大値のインデックス

    Alice_sum += a_list[tmp]  # 最大のカードを追加

    a_list[tmp] = 0  # 取ったカードを0にする

    # Bobの番
    tmp = a_list.index(max(a_list))  # 最大値のインデックス

    Bob_sum += a_list[tmp]  # 最大のカードを追加

    a_list[tmp] = 0  # 取ったカードを0にする

  # 奇数1枚余るので、Aliceが取る
  tmp = a_list.index(max(a_list))  # 最大値のインデックス

  Alice_sum += a_list[tmp]  # 最大のカードを追加

  a_list[tmp] = 0  # 取ったカードを0にする

  #回答の出力
  print(Alice_sum - Bob_sum)

if __name__ == "__main__":
  main()