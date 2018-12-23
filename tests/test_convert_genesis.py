import pytest

from genesis_blockchain_tools.convert.genesis import (
    address_to_wallet, wallet_to_address,
    key_id_to_wallet, wallet_to_key_id
)

def test_address_to_wallet():
    fns = (address_to_wallet, key_id_to_wallet)
    for i in range(0, len(fns)):
        assert fns[0](-7129004159526005831) == '1131-7739-9141-8354-5785'
        assert fns[0](-7129004159526005831, use_delims=False) == '11317739914183545785'
        assert fns[0](3496019374267252370) == '0349-6019-3742-6725-2370'
        assert fns[0](7822345485898532948) == '0782-2345-4858-9853-2948'


def test_wallet_to_address():
    fns = (wallet_to_address, wallet_to_key_id)
    for i in range(0, len(fns)):
        assert fns[0]('1131-7739-9141-8354-5785') == -7129004159526005831
        assert fns[0]('11317739914183545785') == -7129004159526005831
        assert fns[0]('0349-6019-3742-6725-2370') == 3496019374267252370
        assert fns[0]('0782-2345-4858-9853-2948') == 7822345485898532948
        assert fns[0]('07822345485898532948') == 7822345485898532948
        assert fns[0]('7822345485898532948') == 7822345485898532948

