#!/bin/bash

pytest onion/ --cov --cov-report term-missing > test.out

grep -A 100 "coverage" test.out > test.sum

if [[ -f "test.out" ]]; then
  rm test.out
fi

cat test.sum
