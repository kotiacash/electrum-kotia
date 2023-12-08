# -*- coding: utf-8 -*-
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2018 The Electrum developers
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json
import sys

from .util import inv_dict, all_subclasses
from . import bitcoin


def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            r = json.loads(f.read())
    except Exception:
        r = default
    return r


GIT_REPO_URL = "https://github.com/kotiacash/electrum-kot"
GIT_REPO_ISSUES_URL = "https://github.com/kotiacash/electrum-kot/issues"
BIP39_WALLET_FORMATS = read_json('bip39_wallet_formats.json', [])


class AbstractNet:

    NET_NAME: str
    TESTNET: bool
    WIF_PREFIX: int
    ADDRTYPE_P2PKH: int
    ADDRTYPE_P2SH: int
    GENESIS: str
    BIP44_COIN_TYPE: int

    @classmethod
    def max_checkpoint(cls) -> int:
        checkpoints = [int(k) for k, v in cls.CHECKPOINTS.items() if v != 0] or [0, ]
        return max(0, max(checkpoints))

    @classmethod
    def rev_genesis_bytes(cls) -> bytes:
        return bytes.fromhex(bitcoin.rev_hex(cls.GENESIS))


# Kotia
class BitcoinMainnet(AbstractNet):

    NET_NAME = "mainnet"
    TESTNET = False
    WIF_PREFIX = 0x99
    ADDRTYPE_P2PKH = 25
    ADDRTYPE_P2SH = 85
    SEGWIT_HRP = "kot"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "000008e4586479cd9dc5832b262414a60f152381e371cf7940ffe9f5aa4b80a0"
    DEFAULT_PORTS = {'s': '50001'}
    DEFAULT_SERVERS = read_json('servers.json', {})
    CHECKPOINTS = read_json('checkpoints.json', {})
    COINBASE_MATURITY = 20

    POW_LIMIT = 0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    POS_LIMIT = 0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    POS_LIMITV2 = 0x000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffff
    LAST_POW_BLOCK = 1000000
    FIRST_POSV1RF_BLOCK = 0
    FIRST_POSV2_BLOCK = 0
    FIRST_POSV3_BLOCK = 0
    FIRST_POSV3_1_BLOCK_TIME = sys.maxsize

    XPRV_HEADERS = {
        'standard':    0x0488ade4,  # xprv
        'p2wpkh-p2sh': 0x049d7878,  # yprv
        'p2wsh-p2sh':  0x0295b005,  # Yprv
        'p2wpkh':      0x04b2430c,  # zprv
        'p2wsh':       0x02aa7a99,  # Zprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x0488b21e,  # xpub
        'p2wpkh-p2sh': 0x049d7cb2,  # ypub
        'p2wsh-p2sh':  0x0295b43f,  # Ypub
        'p2wpkh':      0x04b24746,  # zpub
        'p2wsh':       0x02aa7ed3,  # Zpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 10
    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = []


# Kotia
class BitcoinTestnet(AbstractNet):

    NET_NAME = "testnet"
    TESTNET = False
    WIF_PREFIX = 0xef
    ADDRTYPE_P2PKH = 111
    ADDRTYPE_P2SH = 196
    SEGWIT_HRP = "tkot"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "000008e4586479cd9dc5832b262414a60f152381e371cf7940ffe9f5aa4b80a0"
    DEFAULT_PORTS = {'t': '51001', 's': '51002'}
    DEFAULT_SERVERS = read_json('servers_testnet.json', {})
    CHECKPOINTS = read_json('checkpoints_testnet.json', {})
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 0
    COINBASE_MATURITY = 10

    POW_LIMIT = 0x0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    POS_LIMIT = 0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    POS_LIMITV2 = 0x000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffff
    LAST_POW_BLOCK = 0x7fffffff
    FIRST_POSV1RF_BLOCK = 38425
    FIRST_POSV2_BLOCK = 319002
    FIRST_POSV3_BLOCK = 872456
    FIRST_POSV3_1_BLOCK_TIME = 1667779200

    XPRV_HEADERS = {
        'standard':    0x04358394,  # tprv
        'p2wpkh-p2sh': 0x044a4e28,  # uprv
        'p2wsh-p2sh':  0x024285b5,  # Uprv
        'p2wpkh':      0x045f18bc,  # vprv
        'p2wsh':       0x02575048,  # Vprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x043587cf,  # tpub
        'p2wpkh-p2sh': 0x044a5262,  # upub
        'p2wsh-p2sh':  0x024289ef,  # Upub
        'p2wpkh':      0x045f1cf6,  # vpub
        'p2wsh':       0x02575483,  # Vpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 1
    LN_REALM_BYTE = 1
    LN_DNS_SEEDS = [  # TODO investigate this again
        #'test.nodes.lightning.directory.',  # times out.
        #'lseed.bitcoinstats.com.',  # ignores REALM byte and returns mainnet peers...
    ]


# Kotia
class BitcoinRegtest(BitcoinTestnet):

    NET_NAME = "regtest"
    SEGWIT_HRP = "blrt"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "0000724595fb3b9609d441cbfb9577615c292abf07d996d3edabc48de843642d"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


# Bitcoin
class BitcoinSimnet(BitcoinTestnet):

    NET_NAME = "simnet"
    WIF_PREFIX = 0x64
    ADDRTYPE_P2PKH = 0x3f
    ADDRTYPE_P2SH = 0x7b
    SEGWIT_HRP = "sb"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "683e86bd5c6d110d91b94b97137ba6bfe02dbbdb8e3dff722a669b5d69d77af6"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


# Bitcoin
class BitcoinSignet(BitcoinTestnet):

    NET_NAME = "signet"
    BOLT11_HRP = "tbs"
    GENESIS = "00000008819873e925422c1ff0f99f7cc9bbb232af63a077a480a3633bee1ef6"
    DEFAULT_SERVERS = read_json('servers_signet.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


NETS_LIST = tuple(all_subclasses(AbstractNet))

# don't import net directly, import the module instead (so that net is singleton)
net = BitcoinMainnet

def set_signet():
    global net
    net = BitcoinSignet

def set_simnet():
    global net
    net = BitcoinSimnet

def set_mainnet():
    global net
    net = BitcoinMainnet

def set_testnet():
    global net
    net = BitcoinTestnet

def set_regtest():
    global net
    net = BitcoinRegtest
