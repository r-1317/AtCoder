#!/bin/bash
NUM="04"
# 最大何ジョブまで並列実行するかを指定
MAX_JOBS=6

for i in $(seq -w 0000 0099); do
  python3 a${NUM}.py < in/${i}.txt > out${NUM}/out${NUM}_${i}.txt &
  # バックグラウンドジョブがMAX_JOBSに達したら待機
  if (( $(jobs -r | wc -l) >= MAX_JOBS )); then
    wait -n
  fi
done

# 残りのジョブが終わるまで待機
wait