#!/bin/zsh

num_process=10 # The number of processes to collect data
max_total_tokens=500000 # Set maximum numbers of tokens to collect data
api_key=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 # Set your openai api key
for ((i=0; i<$num_process; i++))
do
    python3 collect.py $api_key $max_total_tokens $i $num_process quora &
done