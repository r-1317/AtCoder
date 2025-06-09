#!/bin/bash
for i in $(seq 0 99); do
  file=$(printf "%04d" $i)
  pypy3 a02.py < in/${file}.txt > out/out_${file}.txt
done
