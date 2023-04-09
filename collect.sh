#!/bin/zsh

num_process=10 # The number of processes to collect data
max_total_tokens=500000 # Set maximum numbers of tokens to collect data
api_key=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 # Set your openai api key
for ((i=0; i<5; i++))
do
    python3 collect.py $api_key $max_total_tokens $i $num_process quora &
done