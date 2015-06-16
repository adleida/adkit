#!/bin/bash

echo start generating ..
less $1 | grep case_escaped_time | cut -d : -f 5 > test_avgtime.out
echo done.

awk 'BEGIN{sum=max=0; min=9999}{sum+=$1; max=$1>max?$1:max; min=$1>min?min:$1;}END{printf "SUM: %f\nMAX: %f\nMIN: %f\nAVG: %f\n", sum, max, min, sum/NR}' test_avgtime.out
