#!/bin/bash

# 0000～0999までループ
for i in $(seq -w 0000 0999); do
    # 各ファイルを標準入力として実行し、
    # 標準出力は破棄し、標準エラー出力のみを変数errに格納
    err=$(python3 a01.py < "in/${i}.txt" 2>&1 1>/dev/null)
    
    # errが空でなければ、error_log.txtに追記
    if [ -n "$err" ]; then
        # error_log.txtが空でなければ、追記する前に改行を追加（必要に応じて）
        # ※ ここでは必ず改行して区切りを明確にするため、エラー出力の末尾に改行を含むと仮定
        echo "$err" >> error_log.txt
        echo "==========" >> error_log.txt
    fi
done
