#!/bin/bash
NUM="07"
# 最大何ジョブまで並列実行するかを指定
MAX_JOBS=12
# 警告を出す実行時間のしきい値（秒）。環境変数でも変更できる。
WARNING_THRESHOLD_SECONDS=${WARNING_THRESHOLD_SECONDS:-1.9}
WARNING_THRESHOLD_US=$(awk -v seconds="$WARNING_THRESHOLD_SECONDS" 'BEGIN { printf "%.0f", seconds * 1000000 }')

for i in $(seq -w 0000 0099); do
  (
    start_us=${EPOCHREALTIME/./}
    ./a${NUM}.out < in/${i}.txt > out${NUM}/out${NUM}_${i}.txt
    status=$?
    end_us=${EPOCHREALTIME/./}
    elapsed_us=$((end_us - start_us))
    if (( elapsed_us > WARNING_THRESHOLD_US )); then
      printf '\033[33m警告: ケース %s の実行時間は %d.%06d 秒です（%s 秒超）\033[0m\n' \
        "$i" "$((elapsed_us / 1000000))" "$((elapsed_us % 1000000))" \
        "$WARNING_THRESHOLD_SECONDS" >&2
    fi
    exit "$status"
  ) &
  # バックグラウンドジョブがMAX_JOBSに達したら待機
  if (( $(jobs -r | wc -l) >= MAX_JOBS )); then
    wait -n
  fi
done

# 残りのジョブが終わるまで待機
wait
