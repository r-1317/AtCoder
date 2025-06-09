#!/bin/bash
for i in $(seq 0 99); do
  file=$(printf "%04d" $i)
  echo "Running test case: ${file}"
  start=$(date +%s.%N)
  ./a07.out < in/${file}.txt > out07/out07_${file}.txt
  end=$(date +%s.%N)
  elapsed=$(echo "$end - $start" | bc)
  echo "Execution time for ${file}: ${elapsed} seconds"
done
