#!/usr/bin/env bash
export HOME=~
set -eux pipefail
mkdir -p ~/.kotia
cat > ~/.kotia/kotia.conf <<EOF
regtest=1
txindex=1
printtoconsole=1
rpcuser=doggman
rpcpassword=donkey
rpcallowip=127.0.0.1
zmqpubrawblock=tcp://127.0.0.1:28332
zmqpubrawtx=tcp://127.0.0.1:28333
fallbackfee=0.0002
[regtest]
rpcbind=0.0.0.0
rpcport=18554
EOF
rm -rf ~/.kotia/regtest
bitcoind -regtest &
sleep 6
kotia-cli createwallet test_wallet
addr=$(kotia-cli getnewaddress)
kotia-cli generatetoaddress 150 $addr
tail -f ~/.kotia/regtest/debug.log
