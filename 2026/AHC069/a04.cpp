#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <set>
#include <string>
#include <utility>
#include <vector>

using namespace std;

namespace {

constexpr int N = 50;
constexpr int M = 1000;
constexpr double COEF = 0.5;
constexpr int BEAM_WIDTH = 1;
constexpr double POND_BOUNDARY_WEIGHT = 0.0;
constexpr int SIZE = N * N;

using Region = vector<int>;

struct GroupInfo {
    int s;
    int t;
    int p;
    long long v;
    double c = 0.0;
    Region pos;
};

struct BeamState {
    double perimeter;
    int distance_sum;
    Region cells;
    Region frontier;
};

struct CandidateState {
    double perimeter;
    int distance_sum;
    long long serial;
    Region cells;
    Region frontier;
};

struct Placement {
    vector<Region> moves;
    Region region;
    bool found = false;
};

array<vector<int>, SIZE> build_neighbors() {
    array<vector<int>, SIZE> neighbors;
    for (int x = 0; x < N; ++x) {
        for (int y = 0; y < N; ++y) {
            const int cell = x * N + y;
            if (x > 0) neighbors[cell].push_back(cell - N);
            if (x + 1 < N) neighbors[cell].push_back(cell + N);
            if (y > 0) neighbors[cell].push_back(cell - 1);
            if (y + 1 < N) neighbors[cell].push_back(cell + 1);
        }
    }
    return neighbors;
}

const array<vector<int>, SIZE> NEIGHBORS = build_neighbors();

double compactness(const Region& region, int p) {
    array<unsigned char, SIZE> included{};
    for (const int cell : region) included[cell] = 1;

    int perimeter = 0;
    for (const int cell : region) {
        const int x = cell / N;
        const int y = cell % N;
        perimeter += (x == 0 || !included[cell - N]);
        perimeter += (x + 1 == N || !included[cell + N]);
        perimeter += (y == 0 || !included[cell - 1]);
        perimeter += (y + 1 == N || !included[cell + 1]);
    }
    return 4.0 * sqrt(static_cast<double>(p)) / perimeter;
}

double expected_v(int s, int t, int p) {
    return p * pow(static_cast<double>(t - s), 0.9);
}

long long rounded_payment(long long v, double coefficient) {
    return static_cast<long long>(static_cast<double>(v) * coefficient + 0.5);
}

long long release_groups(vector<GroupInfo>& groups,
                         array<int, SIZE>& owner,
                         int current_time) {
    long long released_money = 0;
    for (auto& group : groups) {
        if (group.pos.empty() || group.t >= current_time) continue;
        for (const int cell : group.pos) owner[cell] = -1;
        released_money += rounded_payment(group.v, group.c);
        group.pos.clear();
    }
    return released_money;
}

Region set_union_with_cell(const Region& cells, int cell) {
    Region result;
    result.reserve(cells.size() + 1);
    const auto it = lower_bound(cells.begin(), cells.end(), cell);
    result.insert(result.end(), cells.begin(), it);
    result.push_back(cell);
    result.insert(result.end(), it, cells.end());
    return result;
}

bool contains(const Region& sorted_region, int cell) {
    return binary_search(sorted_region.begin(), sorted_region.end(), cell);
}

Region find_region(
    int p,
    int movable,
    const array<unsigned char, SIZE>& grass,
    const array<int, SIZE>& flat_owner,
    const array<double, SIZE>& weighted_cell_perimeter,
    const array<unsigned char, SIZE>* forbidden = nullptr) {
    array<unsigned char, SIZE> allowed{};
    for (int cell = 0; cell < SIZE; ++cell) {
        allowed[cell] = grass[cell] &&
                        (forbidden == nullptr || !(*forbidden)[cell]) &&
                        (flat_owner[cell] == -1 || flat_owner[cell] == movable);
    }

    // Python 版と同じく、左上から調べた最初の p マス以上の連結成分だけを探索する。
    array<unsigned char, SIZE> seen_component{};
    for (int start = 0; start < SIZE; ++start) {
        if (!allowed[start] || seen_component[start]) continue;

        vector<int> component{start};
        seen_component[start] = 1;
        for (size_t head = 0; head < component.size(); ++head) {
            const int cell = component[head];
            for (const int next : NEIGHBORS[cell]) {
                if (allowed[next] && !seen_component[next]) {
                    seen_component[next] = 1;
                    component.push_back(next);
                }
            }
        }
        if (static_cast<int>(component.size()) < p) continue;

        Region initial_frontier;
        for (const int next : NEIGHBORS[start]) {
            if (allowed[next]) initial_frontier.push_back(next);
        }
        sort(initial_frontier.begin(), initial_frontier.end());

        vector<BeamState> beam{{weighted_cell_perimeter[start],
                                0,
                                Region{start},
                                move(initial_frontier)}};
        const int start_x = start / N;
        const int start_y = start % N;
        long long serial = 0;

        for (int selected_count = 1; selected_count < p; ++selected_count) {
            vector<CandidateState> candidates;
            set<Region> used;

            for (const auto& state : beam) {
                for (const int cell : state.frontier) {
                    Region new_cells = set_union_with_cell(state.cells, cell);
                    if (!used.insert(new_cells).second) continue;

                    int adjacent = 0;
                    for (const int next : NEIGHBORS[cell]) {
                        adjacent += contains(state.cells, next);
                    }
                    const double new_perimeter =
                        state.perimeter + weighted_cell_perimeter[cell] -
                        2 * adjacent;

                    Region new_frontier = state.frontier;
                    new_frontier.erase(
                        lower_bound(new_frontier.begin(), new_frontier.end(), cell));
                    for (const int next : NEIGHBORS[cell]) {
                        if (!allowed[next] || contains(new_cells, next)) continue;
                        const auto it = lower_bound(new_frontier.begin(),
                                                    new_frontier.end(), next);
                        if (it == new_frontier.end() || *it != next) {
                            new_frontier.insert(it, next);
                        }
                    }

                    const int cell_x = cell / N;
                    const int cell_y = cell % N;
                    const int new_distance_sum =
                        state.distance_sum + abs(cell_x - start_x) +
                        abs(cell_y - start_y);

                    ++serial;
                    candidates.push_back({new_perimeter,
                                          new_distance_sum,
                                          serial,
                                          move(new_cells),
                                          move(new_frontier)});
                }
            }

            if (candidates.empty()) break;
            stable_sort(candidates.begin(), candidates.end(),
                        [](const CandidateState& lhs,
                           const CandidateState& rhs) {
                            if (lhs.perimeter != rhs.perimeter) {
                                return lhs.perimeter < rhs.perimeter;
                            }
                            if (lhs.distance_sum != rhs.distance_sum) {
                                return lhs.distance_sum < rhs.distance_sum;
                            }
                            return lhs.serial < rhs.serial;
                        });

            beam.clear();
            const int next_width =
                min(BEAM_WIDTH, static_cast<int>(candidates.size()));
            beam.reserve(next_width);
            for (int i = 0; i < next_width; ++i) {
                beam.push_back({candidates[i].perimeter,
                                candidates[i].distance_sum,
                                move(candidates[i].cells),
                                move(candidates[i].frontier)});
            }
        }

        if (!beam.empty() && static_cast<int>(beam.front().cells.size()) == p) {
            const auto best = min_element(
                beam.begin(), beam.end(),
                [](const BeamState& lhs, const BeamState& rhs) {
                    if (lhs.perimeter != rhs.perimeter) {
                        return lhs.perimeter < rhs.perimeter;
                    }
                    return lhs.distance_sum < rhs.distance_sum;
                });
            return best->cells;
        }
    }
    return {};
}

Placement find_best_placement(
    const array<unsigned char, SIZE>& grass,
    const array<int, SIZE>& owner,
    const array<double, SIZE>& weighted_cell_perimeter,
    vector<GroupInfo>& groups,
    double r) {
    Placement result;
    result.moves.resize(groups.size());
    GroupInfo& new_group = groups.back();

    Region region = find_region(new_group.p, -1, grass, owner,
                                weighted_cell_perimeter);
    if (!region.empty()) {
        new_group.pos = region;
        result.region = move(region);
        result.found = true;
        return result;
    }

    vector<int> active;
    for (int i = 0; i + 1 < static_cast<int>(groups.size()); ++i) {
        if (!groups[i].pos.empty()) active.push_back(i);
    }
    stable_sort(active.begin(), active.end(), [&](int lhs, int rhs) {
        const long long lhs_cost =
            max(rounded_payment(groups[lhs].v, r), 1LL);
        const long long rhs_cost =
            max(rounded_payment(groups[rhs].v, r), 1LL);
        return lhs_cost < rhs_cost;
    });

    long long best_gain = -1;
    int best_group = -1;
    Region best_destination;
    Region best_region;

    const int candidates_to_try = min(32, static_cast<int>(active.size()));
    for (int k = 0; k < candidates_to_try; ++k) {
        const int i = active[k];
        Region candidate = find_region(new_group.p, i, grass, owner,
                                       weighted_cell_perimeter);
        if (candidate.empty()) continue;

        bool uses_group = false;
        for (const int cell : candidate) {
            if (owner[cell] == i) {
                uses_group = true;
                break;
            }
        }
        if (!uses_group) continue;

        array<unsigned char, SIZE> blocked{};
        for (const int cell : candidate) blocked[cell] = 1;
        Region destination =
            find_region(groups[i].p, i, grass, owner,
                        weighted_cell_perimeter, &blocked);
        if (destination.empty()) continue;

        const long long income = rounded_payment(
            new_group.v, compactness(candidate, new_group.p));
        const long long cost = max(rounded_payment(groups[i].v, r), 1LL);
        if (cost > income) continue;

        const long long gain = income - cost;
        if (gain > best_gain) {
            best_gain = gain;
            best_group = i;
            best_destination = move(destination);
            best_region = move(candidate);
        }
    }

    if (best_group == -1) return result;

    result.moves[best_group] = move(best_destination);
    new_group.pos = best_region;
    result.region = move(best_region);
    result.found = true;
    return result;
}

long long move_groups(array<int, SIZE>& owner,
                      vector<GroupInfo>& groups,
                      const vector<Region>& moves,
                      double r) {
    vector<int> moved;
    for (int i = 0; i < static_cast<int>(moves.size()); ++i) {
        if (!moves[i].empty()) moved.push_back(i);
    }
    cout << moved.size() << '\n';

    for (const int i : moved) {
        for (const int cell : groups[i].pos) owner[cell] = -1;
    }

    long long move_cost = 0;
    for (const int i : moved) {
        GroupInfo& group = groups[i];
        for (const int cell : moves[i]) owner[cell] = i;
        group.pos = moves[i];
        const double new_c = compactness(group.pos, group.p);
        group.c = min(group.c, new_c);
        move_cost += max(rounded_payment(group.v, r), 1LL);

        cout << i << '\n';
        for (const int cell : group.pos) {
            cout << cell / N << ' ' << cell % N << '\n';
        }
    }
    return move_cost;
}

}  // namespace

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int input_n, input_m;
    double r;
    cin >> input_n >> input_m >> r;

    array<unsigned char, SIZE> grass{};
    for (int x = 0; x < N; ++x) {
        string row;
        cin >> row;
        for (int y = 0; y < N; ++y) {
            grass[x * N + y] = (row[y] == '.');
        }
    }

    array<double, SIZE> weighted_cell_perimeter;
    weighted_cell_perimeter.fill(4.0);
    for (int x = 0; x < N; ++x) {
        for (int y = 0; y < N; ++y) {
            const int cell = x * N + y;
            int pond_sides = 0;
            if (x > 0 && !grass[cell - N]) ++pond_sides;
            if (x + 1 < N && !grass[cell + N]) ++pond_sides;
            if (y > 0 && !grass[cell - 1]) ++pond_sides;
            if (y + 1 < N && !grass[cell + 1]) ++pond_sides;
            weighted_cell_perimeter[cell] -=
                pond_sides * (1.0 - POND_BOUNDARY_WEIGHT);
        }
    }

    array<int, SIZE> owner;
    owner.fill(-1);
    vector<GroupInfo> groups;
    groups.reserve(M);
    long long money = 0;

    for (int i = 0; i < M; ++i) {
        int group_id, s, t, p;
        long long v;
        cin >> group_id >> s >> t >> p >> v;
        groups.push_back({s, t, p, v, 0.0, {}});

        money += release_groups(groups, owner, s);
        money += release_groups(groups, owner, s);

        if (static_cast<double>(v) < expected_v(s, t, p) * COEF) {
            cout << 0 << '\n' << "No\n";
            cout.flush();
            continue;
        }

        Placement placement = find_best_placement(
            grass, owner, weighted_cell_perimeter, groups, r);
        if (placement.found) {
            money -= move_groups(owner, groups, placement.moves, r);
            cout << "Yes\n";
            for (const int cell : placement.region) {
                owner[cell] = i;
                cout << cell / N << ' ' << cell % N << '\n';
            }
            groups.back().c = compactness(placement.region, p);
        } else {
            cout << 0 << '\n' << "No\n";
        }
        cout.flush();
    }

    return 0;
}
