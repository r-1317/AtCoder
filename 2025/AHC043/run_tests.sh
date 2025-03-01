#!/bin/bash

# 0000～0999までループ
for i in $(seq -w 0000 0999); do
    input_file="in/${i}.txt"
    
    # 入力ファイルが存在しない場合はスキップ
    if [ ! -f "$input_file" ]; then
        echo "Warning: $input_file not found. Skipping."
        continue
    fi

    # 開始時刻（秒単位・小数点以下も取得）
    start=$(date +%s.%N)
    
    # 標準入力としてファイルを渡して実行
    python3 a01.py < "$input_file" > /dev/null
    
    # 終了時刻
    end=$(date +%s.%N)
    
    # 実行時間を計算
    elapsed=$(echo "$end - $start" | bc)
    
    # 1秒超えた場合、time.txtにxxxxを追記
    if (( $(echo "$elapsed > 1" | bc -l) )); then
        echo "$i" >> time.txt
    fi
done
