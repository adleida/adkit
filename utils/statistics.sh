#!/bin/bash

log_file=$1
flag=(True ERROR timeout)
all_count=`less $log_file | grep case_name | wc -l`

count_array=()
percentage_array=()

echo 'statistics start, please wait ..'
for each_flag in ${flag[@]}
do
    count=`less $log_file | grep $each_flag | wc -l`
    count_array=("${count_array[@]}" $count)
    percentage=$(echo "scale=3; $count / $all_count * 100" | bc)
    percentage_array=("${percentage_array[@]}" $percentage)
done

echo 'done'

# echo ${count_array[*]}
# echo ${percentage_array[*]}
timeout_on_error=$(echo "scale=3; ${count_array[2]} / ${count_array[1]} * 100" | bc)

echo -e "| \t  | count     | percentage(%) | remark         |"
echo -e "| all     | $all_count    | \t      | all case count |"
echo -e "| True    | ${count_array[0]}    | ${percentage_array[0]}        | True / all     |"
echo -e "| error   | ${count_array[1]}     | ${percentage_array[1]}         | Error / all    |"
echo -e "| timeout | ${count_array[2]}     | ${percentage_array[2]}         | timeout / all  |"
echo -e "| timeout | ${count_array[2]}     | $timeout_on_error        | timeout / Error|"
