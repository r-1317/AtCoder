/*
================  Original Python3 code (verbatim)  ================
import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

D_LIST = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIR_LIST = ["v", "^", ">", "<"]

def main():
  h, w = map(int, input().split())
  s_list = [list(input()) for _ in range(h)]

  grid = [["#"]*(w+2) for _ in range(h+2)]

  for i in range(h):
    for j in range(w):
      grid[i+1][j+1] = s_list[i][j]
  # ic(grid)

  ic("------------")

  bfs_list = [[[10**9, ""] for _ in range(w+2)] for _ in range(h+2)]

  queue = []
  for i in range(h+2):
    for j in range(w+2):
      if grid[i][j] == "E":
        bfs_list[i][j] = [0, "E"]
        queue.append((i, j))
      elif grid[i][j] == "#":
        bfs_list[i][j] = [0, "#"]

  while queue:
    x, y = queue.pop(0)
    for i in range(4):
      dx, dy = D_LIST[i]
      nx, ny = x + dx, y + dy
      if grid[nx][ny] == "#":
        continue
      if bfs_list[nx][ny][0] > bfs_list[x][y][0] + 1:
        bfs_list[nx][ny][0] = bfs_list[x][y][0] + 1
        bfs_list[nx][ny][1] = DIR_LIST[i]
        queue.append((nx, ny))
  
  for i in range(1, h+1):
    for j in range(1, w+1):
      print(bfs_list[i][j][1], end="")
    print()

if __name__ == "__main__":
  main()
=====================================================================
*/

#include <bits/stdc++.h>
using namespace std;

// FAILED: os.path.basename(__file__) != "Main.py"  (Python-specific environment detection)
// FAILED: icecream (debug-print helper)            (no direct C++ equivalent)

const int INF = 1'000'000'000;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int h, w;
    if (!(cin >> h >> w)) return 0;
    vector<string> s_list(h);
    for (int i = 0; i < h; ++i) cin >> s_list[i];

    /* ---- Build grid with a 1-cell thick wall (#) border ---- */
    vector<vector<char>> grid(h + 2, vector<char>(w + 2, '#'));
    for (int i = 0; i < h; ++i)
        for (int j = 0; j < w; ++j)
            grid[i + 1][j + 1] = s_list[i][j];

    /* ---- BFS distance + direction table ---- */
    vector<vector<pair<int, char>>> bfs(h + 2,
        vector<pair<int, char>>(w + 2, {INF, ' '}));

    vector<pair<int, int>> queue;            // list-style queue (pop(0) → erase(begin))
    for (int i = 0; i < h + 2; ++i) {
        for (int j = 0; j < w + 2; ++j) {
            if (grid[i][j] == 'E') {
                bfs[i][j] = {0, 'E'};
                queue.push_back({i, j});
            } else if (grid[i][j] == '#') {
                bfs[i][j] = {0, '#'};
            }
        }
    }

    const int dx[4]   = {-1, 1, 0, 0};
    const int dy[4]   = { 0, 0,-1, 1};
    const char dir_l[4] = {'v', '^', '>', '<'};   // corresponds to D_LIST indices

    /* ---- BFS (vector + erase to match Python pop(0) complexity) ---- */
    while (!queue.empty()) {
        auto [x, y] = queue.front();
        queue.erase(queue.begin());                // O(N) just like Python list.pop(0)

        for (int k = 0; k < 4; ++k) {
            int nx = x + dx[k], ny = y + dy[k];
            if (grid[nx][ny] == '#') continue;
            if (bfs[nx][ny].first > bfs[x][y].first + 1) {
                bfs[nx][ny].first  = bfs[x][y].first + 1;
                bfs[nx][ny].second = dir_l[k];
                queue.push_back({nx, ny});
            }
        }
    }

    /* ---- Output only the original H×W inner area ---- */
    for (int i = 1; i <= h; ++i) {
        for (int j = 1; j <= w; ++j) cout << bfs[i][j].second;
        cout << '\n';
    }
    return 0;
}
