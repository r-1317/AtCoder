
# 操作の実行
def operation(ans,tk_position,tk_angle):

  #マスの色の変更
  if ans[tk_position[0]][tk_position[1]] == ".":  # 足元が「.」(白)か否か

    ans[tk_position[0]][tk_position[1]] = "#"  # 足元を「#」(黒)にする
    tk_angle = change_angle(tk_angle,True)  # 時計回りに90°回転する

    # print(ans[tk_position[0]][tk_position[1]])  # デバッグ

  else:  # 足元が「#」(黒)だっ場合

    ans[tk_position[0]][tk_position[1]] = "."  # 足元を「.」(白)にする
    tk_angle = change_angle(tk_angle,False)  # 反時計回りに90°回転する

    # print("黒to白")  # デバッグ

  # print(ans)  # デバッグ
  return ans, tk_angle  # 戻り値



# 向きの変更
def change_angle(tk_angle,deg):
  #総当り
  if tk_angle == [1,0]:  # 上向きの場合
    if deg:  # 90°
      tk_angle = [0,1]  # 右向き
    else:  # -90°
      tk_angle = [0,-1]  # 左向き

  elif tk_angle == [0,1]:  # 右向きの場合
    if deg:  # 90°
      tk_angle = [-1,0]  # 下向き
    else:  # -90°
      tk_angle = [1,0]  # 上向き

  elif tk_angle == [-1,0]:  # 下向きの場合
    if deg:  # 90°
      tk_angle = [0,-1]  # 左向き
    else:  # -90°
      tk_angle = [0,1]  # 右向き

  elif tk_angle == [0,-1]:  # 左向きの場合
    if deg:  # 90°
      tk_angle = [1,0]  # 上向き
    else:  # -90°
      tk_angle = [-1,0]  # 下向き

  # print(f"tk_angle: {tk_angle}")  # デバッグ
  return tk_angle  # 戻り値


# マスの移動
def tk_move(tk_position, tk_angle, height, width):

  tk_position[0] = (tk_position[0] - tk_angle[0]) % height  # 縦

  tk_position[1] = (tk_position[1] + tk_angle[1]) % width  # 横

  # print(f"  座標: {tk_position}")  # デバッグ
  return tk_position

# 解答の出力
def print_ans(ans, height, width):

  for i in range(height):

    for j in range(width):
      print(ans[i][j], end="")

    print("")

  print("")


def main():
  height, width, n = map(int, input().split())
  tk_angle = [1,0]  # 高橋君の向き(H,W)
  tk_position = [0,0]  # 高橋君の座標(0オリジン)
  ans = [["."]*width for _ in range(height)]  # 解答の初期化

  # 繰り返し開始
  for i in range(n):
    ans, tk_angle = operation(ans,tk_position,tk_angle)  # 操作の実行
    
    tk_position = tk_move(tk_position, tk_angle, height, width)  # 移動

  # 解答の出力
  print_ans(ans, height, width)


if __name__ == "__main__":
  main()