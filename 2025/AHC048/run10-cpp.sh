#!/bin/bash
for i in $(seq 0 99); do
  file=$(printf "%04d" $i)
  echo "Running test case: ${file}"
  start=$(date +%s.%N)
  ./a10.out < in/${file}.txt > out10/out10_${file}.txt
  end=$(date +%s.%N)
  elapsed=$(echo "$end - $start" | bc)
  echo "Execution time for ${file}: ${elapsed} seconds"
done
