/*
Original Python Code:

import sys


h, w = map(int, input().split())
s_list = [list(input()) for _ in range(h)]

grid = [["#"] * (w+2) for _ in range(h+2)]

for i in range(h):
  for j in range(w):
    grid[i+1][j+1] = s_list[i][j]

dp_list = [[[10**9] * (w+2) for _ in range(h+2)] for _ in range(2)]  # 0: 縦方向で来た, 1: 横方向で来た

for i in range(h+2):
  for j in range(w+2):
    if grid[i][j] == "S":
      start = (i, j)
    elif grid[i][j] == "G":
      goal = (i, j)

queue = [(start[0], start[1], 0), (start[0], start[1], 1)]

dp_list[0][start[0]][start[1]] = 0
dp_list[1][start[0]][start[1]] = 0

i = 0
ans = -1

while queue:
  i += 1
  prev_queue = queue
  queue = []
  while prev_queue:
    x, y, direction = prev_queue.pop(0)
    if direction == 0:  # 前の手が縦方向。つまり、今は横方向
      for dx in (-1, 1):
        if grid[x+dx][y] == "#":
          continue
        elif grid[x+dx][y] == "G":
          ans = i
          print(ans)
          sys.exit()
        elif i < dp_list[1][x+dx][y]:
          dp_list[1][x+dx][y] = i
          queue.append((x+dx, y, 1))
    else:  # 前の手が横方向。つまり、今は縦方向
      for dy in (-1, 1):
        if grid[x][y+dy] == "#":
          continue
        elif grid[x][y+dy] == "G":
          ans = i
          print(ans)
          sys.exit()
        elif i < dp_list[0][x][y+dy]:
          dp_list[0][x][y+dy] = i
          queue.append((x, y+dy, 0))

print(ans)
*/

#include <iostream>
#include <vector>
#include <queue>
#include <tuple>
#include <cstdlib>
using namespace std;

int main() {
    int h, w;
    cin >> h >> w;
    vector<vector<char>> s_list(h, vector<char>(w));
    for (int i = 0; i < h; ++i) {
        for (int j = 0; j < w; ++j) {
            cin >> s_list[i][j];
        }
    }

    vector<vector<char>> grid(h + 2, vector<char>(w + 2, '#'));
    for (int i = 0; i < h; ++i) {
        for (int j = 0; j < w; ++j) {
            grid[i + 1][j + 1] = s_list[i][j];
        }
    }

    vector<vector<vector<int>>> dp_list(2, vector<vector<int>>(h + 2, vector<int>(w + 2, 1e9)));

    pair<int, int> start, goal;
    for (int i = 0; i < h + 2; ++i) {
        for (int j = 0; j < w + 2; ++j) {
            if (grid[i][j] == 'S') {
                start = {i, j};
            } else if (grid[i][j] == 'G') {
                goal = {i, j};
            }
        }
    }

    queue<tuple<int, int, int>> q;
    q.emplace(start.first, start.second, 0);
    q.emplace(start.first, start.second, 1);

    dp_list[0][start.first][start.second] = 0;
    dp_list[1][start.first][start.second] = 0;

    int i = 0;
    int ans = -1;

    while (!q.empty()) {
        ++i;
        int size = q.size();
        for (int k = 0; k < size; ++k) {
            auto [x, y, direction] = q.front();
            q.pop();
            if (direction == 0) {
                for (int dx : {-1, 1}) {
                    if (grid[x + dx][y] == '#') continue;
                    if (grid[x + dx][y] == 'G') {
                        cout << i << endl;
                        return 0;
                    }
                    if (i < dp_list[1][x + dx][y]) {
                        dp_list[1][x + dx][y] = i;
                        q.emplace(x + dx, y, 1);
                    }
                }
            } else {
                for (int dy : {-1, 1}) {
                    if (grid[x][y + dy] == '#') continue;
                    if (grid[x][y + dy] == 'G') {
                        cout << i << endl;
                        return 0;
                    }
                    if (i < dp_list[0][x][y + dy]) {
                        dp_list[0][x][y + dy] = i;
                        q.emplace(x, y + dy, 0);
                    }
                }
            }
        }
    }

    cout << ans << endl;
    return 0;
}
