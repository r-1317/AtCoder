#include <bits/stdc++.h>
using namespace std;

static const int MAXN = 20;
static const int MAXK = 10;
static const int MAXSTATE = (1 << MAXK) * MAXN * MAXN;

int N, M, K;
vector<string> c;

struct XorShift {
    uint64_t x;

    XorShift() {
        x = chrono::steady_clock::now().time_since_epoch().count();
        x ^= 0x9e3779b97f4a7c15ULL;
    }

    uint64_t next() {
        x ^= x << 7;
        x ^= x >> 9;
        return x;
    }

    int nextInt(int n) {
        return (int)(next() % n);
    }

    double nextDouble() {
        return (next() >> 11) * (1.0 / 9007199254740992.0);
    }
};

XorShift rng;

struct Timer {
    chrono::steady_clock::time_point st;

    Timer() {
        st = chrono::steady_clock::now();
    }

    double elapsed() const {
        auto now = chrono::steady_clock::now();
        return chrono::duration<double>(now - st).count();
    }
};

struct Door {
    int d, i, j, g;
};

struct Sw {
    int i, j, s;
};

struct Solution {
    vector<Door> doors;
    vector<Sw> switches;
};

struct Edge {
    int d, i, j;
};

vector<Edge> allEdges;
vector<Edge> openEdges;
vector<pair<int, int>> openCells;

int edgeCode(int d, int i, int j) {
    return d * N * N + i * N + j;
}

int edgeCode(const Edge& e) {
    return edgeCode(e.d, e.i, e.j);
}

bool edgeUsed(const Solution& sol, int code, int skip = -1) {
    for (int idx = 0; idx < (int)sol.doors.size(); idx++) {
        if (idx == skip) continue;
        const auto& e = sol.doors[idx];
        if (edgeCode(e.d, e.i, e.j) == code) return true;
    }
    return false;
}

bool cellUsed(const Solution& sol, int i, int j, int skip = -1) {
    for (int idx = 0; idx < (int)sol.switches.size(); idx++) {
        if (idx == skip) continue;
        if (sol.switches[idx].i == i && sol.switches[idx].j == j) {
            return true;
        }
    }
    return false;
}

Edge edgeBetween(pair<int, int> a, pair<int, int> b) {
    int i1 = a.first, j1 = a.second;
    int i2 = b.first, j2 = b.second;

    if (i1 + 1 == i2 && j1 == j2) return {0, i1, j1};
    if (i2 + 1 == i1 && j1 == j2) return {0, i2, j2};
    if (j1 + 1 == j2 && i1 == i2) return {1, i1, j1};
    return {1, i2, j2};
}

void buildEdges() {
    allEdges.clear();
    openEdges.clear();
    openCells.clear();

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (c[i][j] == '.') {
                openCells.push_back({i, j});
            }
        }
    }

    for (int i = 0; i + 1 < N; i++) {
        for (int j = 0; j < N; j++) {
            Edge e{0, i, j};
            allEdges.push_back(e);
            if (c[i][j] == '.' && c[i + 1][j] == '.') {
                openEdges.push_back(e);
            }
        }
    }

    for (int i = 0; i < N; i++) {
        for (int j = 0; j + 1 < N; j++) {
            Edge e{1, i, j};
            allEdges.push_back(e);
            if (c[i][j] == '.' && c[i][j + 1] == '.') {
                openEdges.push_back(e);
            }
        }
    }
}

vector<pair<int, int>> findInitialPath() {
    static int par[MAXN][MAXN];
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            par[i][j] = -1;
        }
    }

    queue<pair<int, int>> q;
    q.push({0, 0});
    par[0][0] = -2;

    const int di[4] = {-1, 1, 0, 0};
    const int dj[4] = {0, 0, -1, 1};

    while (!q.empty()) {
        auto [i, j] = q.front();
        q.pop();

        if (i == N - 1 && j == N - 1) break;

        for (int dir = 0; dir < 4; dir++) {
            int ni = i + di[dir];
            int nj = j + dj[dir];

            if (ni < 0 || ni >= N || nj < 0 || nj >= N) continue;
            if (c[ni][nj] == '#') continue;
            if (par[ni][nj] != -1) continue;

            par[ni][nj] = i * N + j;
            q.push({ni, nj});
        }
    }

    vector<pair<int, int>> path;
    int ci = N - 1;
    int cj = N - 1;

    while (!(ci == 0 && cj == 0)) {
        path.push_back({ci, cj});
        int p = par[ci][cj];
        int pi = p / N;
        int pj = p % N;
        ci = pi;
        cj = pj;
    }

    path.push_back({0, 0});
    reverse(path.begin(), path.end());
    return path;
}

Solution makeInitialSolution(const vector<pair<int, int>>& path) {
    Solution sol;
    sol.doors.reserve(M);
    sol.switches.resize(K);

    int L = (int)path.size() - 1;
    int gateCount = min({K, M, L});

    vector<char> usedDoor(2 * N * N, 0);
    vector<char> pathDoor(2 * N * N, 0);
    vector<char> usedCell(N * N, 0);

    for (int eidx = 0; eidx < L; eidx++) {
        Edge e = edgeBetween(path[eidx], path[eidx + 1]);
        pathDoor[edgeCode(e)] = 1;
    }

    vector<char> usedPathIndex(max(1, L), 0);

    for (int k = 0; k < gateCount; k++) {
        int base = (long long)(k + 1) * L / (gateCount + 1);
        if (base >= L) base = L - 1;

        int eidx = base;
        while (eidx < L && usedPathIndex[eidx]) eidx++;
        if (eidx == L) {
            eidx = base;
            while (eidx >= 0 && usedPathIndex[eidx]) eidx--;
        }

        usedPathIndex[eidx] = 1;

        auto swCell = path[eidx];
        sol.switches[k] = {swCell.first, swCell.second, k};
        usedCell[swCell.first * N + swCell.second] = 1;

        Edge e = edgeBetween(path[eidx], path[eidx + 1]);
        Door door{e.d, e.i, e.j, 2 * k + 1}; // 初期閉、スイッチ k で開く
        sol.doors.push_back(door);
        usedDoor[edgeCode(e)] = 1;
    }

    for (int k = gateCount; k < K; k++) {
        for (int t = 0; t < 10000; t++) {
            auto [i, j] = openCells[rng.nextInt((int)openCells.size())];
            int code = i * N + j;
            if (!usedCell[code]) {
                sol.switches[k] = {i, j, k};
                usedCell[code] = 1;
                break;
            }
        }
    }

    int guard = 0;
    while ((int)sol.doors.size() < M && guard < 200000) {
        guard++;

        const vector<Edge>& pool =
            (!openEdges.empty() && rng.nextInt(100) < 85) ? openEdges : allEdges;

        Edge e = pool[rng.nextInt((int)pool.size())];
        int code = edgeCode(e);

        if (usedDoor[code]) continue;
        if (pathDoor[code]) continue;

        int type = rng.nextInt(K);
        int parity = (rng.nextInt(100) < 80 ? 1 : 0); // 閉扉を多めに置く
        Door door{e.d, e.i, e.j, 2 * type + parity};

        sol.doors.push_back(door);
        usedDoor[code] = 1;
    }

    for (const Edge& e : allEdges) {
        if ((int)sol.doors.size() >= M) break;

        int code = edgeCode(e);
        if (usedDoor[code]) continue;

        Door door{e.d, e.i, e.j, 0};
        sol.doors.push_back(door);
        usedDoor[code] = 1;
    }

    return sol;
}

int calcT(const Solution& sol) {
    static int doorH[MAXN][MAXN];
    static int doorV[MAXN][MAXN];
    static int swCell[MAXN][MAXN];

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            doorH[i][j] = -1;
            doorV[i][j] = -1;
            swCell[i][j] = -1;
        }
    }

    for (const auto& e : sol.doors) {
        if (e.d == 0) {
            doorH[e.i][e.j] = e.g;
        } else {
            doorV[e.i][e.j] = e.g;
        }
    }

    for (const auto& s : sol.switches) {
        swCell[s.i][s.j] = s.s;
    }

    static int seen[1 << MAXK][MAXN][MAXN];
    static int dist[1 << MAXK][MAXN][MAXN];
    static int stamp = 1;
    static int que[MAXSTATE];

    stamp++;
    if (stamp == INT_MAX) {
        memset(seen, 0, sizeof(seen));
        stamp = 1;
    }

    auto isOpen = [&](int g, int mask) -> bool {
        if (g == -1) return true;
        int k = g / 2;
        int parity = g & 1;
        return ((mask >> k) & 1) == parity;
    };

    int head = 0;
    int tail = 0;

    seen[0][0][0] = stamp;
    dist[0][0][0] = 0;
    que[tail++] = 0;

    const int di[4] = {-1, 1, 0, 0};
    const int dj[4] = {0, 0, -1, 1};

    int NN = N * N;

    while (head < tail) {
        int v = que[head++];

        int mask = v / NN;
        int rem = v % NN;
        int i = rem / N;
        int j = rem % N;

        int d = dist[mask][i][j];

        if (i == N - 1 && j == N - 1) {
            return d;
        }

        for (int dir = 0; dir < 4; dir++) {
            int ni = i + di[dir];
            int nj = j + dj[dir];

            if (ni < 0 || ni >= N || nj < 0 || nj >= N) continue;
            if (c[ni][nj] == '#') continue;

            int g = -1;

            if (di[dir] == 1) {
                g = doorH[i][j];
            } else if (di[dir] == -1) {
                g = doorH[ni][nj];
            } else if (dj[dir] == 1) {
                g = doorV[i][j];
            } else {
                g = doorV[ni][nj];
            }

            if (!isOpen(g, mask)) continue;

            if (seen[mask][ni][nj] != stamp) {
                seen[mask][ni][nj] = stamp;
                dist[mask][ni][nj] = d + 1;
                que[tail++] = mask * NN + ni * N + nj;
            }
        }

        int s = swCell[i][j];
        if (s != -1) {
            int nmask = mask ^ (1 << s);

            if (seen[nmask][i][j] != stamp) {
                seen[nmask][i][j] = stamp;
                dist[nmask][i][j] = d + 1;
                que[tail++] = nmask * NN + i * N + j;
            }
        }
    }

    return 0;
}

void moveSwitch(Solution& sol) {
    int idx = rng.nextInt(K);

    if (rng.nextInt(100) < 60) {
        int i = sol.switches[idx].i;
        int j = sol.switches[idx].j;

        vector<pair<int, int>> cand;
        const int di[4] = {-1, 1, 0, 0};
        const int dj[4] = {0, 0, -1, 1};

        for (int dir = 0; dir < 4; dir++) {
            int ni = i + di[dir];
            int nj = j + dj[dir];

            if (ni < 0 || ni >= N || nj < 0 || nj >= N) continue;
            if (c[ni][nj] == '#') continue;
            if (cellUsed(sol, ni, nj, idx)) continue;

            cand.push_back({ni, nj});
        }

        if (!cand.empty()) {
            auto [ni, nj] = cand[rng.nextInt((int)cand.size())];
            sol.switches[idx].i = ni;
            sol.switches[idx].j = nj;
            return;
        }
    }

    for (int t = 0; t < 200; t++) {
        auto [i, j] = openCells[rng.nextInt((int)openCells.size())];

        if (!cellUsed(sol, i, j, idx)) {
            sol.switches[idx].i = i;
            sol.switches[idx].j = j;
            return;
        }
    }
}

void swapSwitchTypesByPositions(Solution& sol) {
    int a = rng.nextInt(K);
    int b = rng.nextInt(K);
    if (a == b) return;

    swap(sol.switches[a].i, sol.switches[b].i);
    swap(sol.switches[a].j, sol.switches[b].j);
}

void changeDoorType(Solution& sol) {
    int idx = rng.nextInt((int)sol.doors.size());
    sol.doors[idx].g = rng.nextInt(2 * K);
}

void moveDoor(Solution& sol) {
    int idx = rng.nextInt((int)sol.doors.size());

    for (int t = 0; t < 200; t++) {
        const vector<Edge>& pool =
            (!openEdges.empty() && rng.nextInt(100) < 85) ? openEdges : allEdges;

        Edge e = pool[rng.nextInt((int)pool.size())];
        int code = edgeCode(e);

        if (!edgeUsed(sol, code, idx)) {
            sol.doors[idx].d = e.d;
            sol.doors[idx].i = e.i;
            sol.doors[idx].j = e.j;
            return;
        }
    }

    for (const Edge& e : allEdges) {
        int code = edgeCode(e);
        if (!edgeUsed(sol, code, idx)) {
            sol.doors[idx].d = e.d;
            sol.doors[idx].i = e.i;
            sol.doors[idx].j = e.j;
            return;
        }
    }
}

void mutate(Solution& sol) {
    int cnt = 1;

    if (rng.nextInt(100) < 7) {
        cnt += 1 + rng.nextInt(3);
    }

    for (int rep = 0; rep < cnt; rep++) {
        int r = rng.nextInt(100);

        if (r < 25) {
            moveSwitch(sol);
        } else if (r < 35) {
            swapSwitchTypesByPositions(sol);
        } else if (r < 60) {
            changeDoorType(sol);
        } else if (r < 85) {
            moveDoor(sol);
        } else {
            moveDoor(sol);
            changeDoorType(sol);
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> M >> K;
    c.resize(N);
    for (int i = 0; i < N; i++) {
        cin >> c[i];
    }

    buildEdges();

    auto path = findInitialPath();

    Solution cur = makeInitialSolution(path);
    int curScore = calcT(cur);

    if (curScore == 0) {
        for (auto& e : cur.doors) {
            e.g = 0;
        }
        curScore = calcT(cur);
    }

    Solution best = cur;
    int bestScore = curScore;

    Timer timer;

    // const double TIME_LIMIT = 1.85;
    const double TIME_LIMIT = 1.95;
    // double startTemp = max(10.0, curScore * 0.30);
    // double endTemp = 0.50;
    double startTemp = max(15.0, curScore * 0.30);
    double endTemp = 0.20;

    while (timer.elapsed() < TIME_LIMIT) {
        double t = timer.elapsed() / TIME_LIMIT;
        double temp = startTemp * pow(endTemp / startTemp, t);

        Solution nxt = cur;
        mutate(nxt);

        int nxtScore = calcT(nxt);

        if (nxtScore == 0) {
            continue;
        }

        int diff = nxtScore - curScore;

        bool accept = false;
        if (diff >= 0) {
            accept = true;
        } else {
            double prob = exp((double)diff / temp);
            if (rng.nextDouble() < prob) {
                accept = true;
            }
        }

        if (accept) {
            cur = std::move(nxt);
            curScore = nxtScore;

            if (curScore > bestScore) {
                best = cur;
                bestScore = curScore;
            }
        }
    }

    cout << best.doors.size() << '\n';
    for (const auto& e : best.doors) {
        cout << e.d << ' ' << e.i << ' ' << e.j << ' ' << e.g << '\n';
    }

    cout << best.switches.size() << '\n';
    for (const auto& s : best.switches) {
        cout << s.i << ' ' << s.j << ' ' << s.s << '\n';
    }

    return 0;
}