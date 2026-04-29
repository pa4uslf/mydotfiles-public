#!/bin/bash
path="$1"
path="${path/#$HOME/~}"
threshold=25

if [ ${#path} -le $threshold ]; then
    echo "$path"
    exit 0
fi

IFS='/' read -ra parts <<< "$path"
result_parts=()
count=${#parts[@]}

for ((i=0; i<count-1; i++)); do
    part="${parts[$i]}"
    if [ -z "$part" ]; then
        result_parts+=("")
    elif [ "$part" = "~" ]; then
        result_parts+=("~")
    else
        result_parts+=("${part:0:1}")
    fi
done

[ $count -gt 0 ] && result_parts+=("${parts[$((count-1))]}")

result=$(IFS='/'; echo "${result_parts[*]}")
echo "$result"
