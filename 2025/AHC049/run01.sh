#!/bin/bash

NUM = "01"

for i in $(seq 0 99); do
  file=$(printf "%04d" $i)
  echo "Running test case: ${file}"
  start=$(date +%s.%N)
  pypy3 a01.py < in/${file}.txt > out01/out01_${file}.txt
  end=$(date +%s.%N)
  elapsed=$(echo "$end - $start" | bc)
  echo "Execution time for ${file}: ${elapsed} seconds"
done
