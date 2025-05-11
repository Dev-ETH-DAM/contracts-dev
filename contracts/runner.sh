#!/bin/bash

source /root/.bashrc

# Run the command and capture its JSON output
json_output=$(forge create src/SubContract.sol:SubContract --evm-version paris --json --rpc-url https://testnet.sapphire.oasis.dev --private-key 951ce0377a4cec5d2312b45396784ca75227098d414f704b25b601a33af96e27 --constructor-args "Sample_1" 0xF4906b5F6D8D6f0f0512187C826729f027ADcb4B 00eac11dbccf10c68be35adf2fcf5ed09fecace79c)

# Extract the 'transaction' object using jq
transaction=$(echo "$json_output" | jq '.transaction')

curl -s --json '${transaction}' \
    --unix-socket /run/rofl-appd.sock \
    http://localhost/rofl/v1/txs/sign-submit 