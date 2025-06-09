#!/bin/bash
sum=0
for i in $(seq 0 99); do
  file=$(printf "%04d" $i)
  out=$(./a04-test.out < in/${file}.txt)
  sum=$((sum + out))
done
# echo $sum
printf "Total sum: %'d\n" $sum
