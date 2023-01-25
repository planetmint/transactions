# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

from transactions.types.assets.decompose import Decompose
from transactions.common.transaction import Transaction
from transactions.common.schema import validate_transaction_schema
from pytest import raises


# Test valid transaction
def test_valid_decompose(signed_create_tx, user_pub):
    inputs = signed_create_tx.to_inputs()
    assets = [signed_create_tx.id]
    decompose_tx = Decompose.generate(inputs, [([user_pub], 1)], assets)
    assert decompose_tx
    assert len(decompose_tx.outputs) == 1
    assert user_pub in decompose_tx.outputs[0].public_keys

# Test more than one asset
def test_invalida_number_of_assets(signed_create_tx, signed_create_tx_2, user_pub):
    inputs = signed_create_tx.to_inputs()
    assets = [signed_create_tx.id, signed_create_tx_2]
    with raises(ValueError):
        Decompose.generate(inputs, [([user_pub], 1)], assets)

# Test more than one recipient
def test_invalid_number_of_recipients(signed_create_tx, user_pub, user2_pub):
    inputs = signed_create_tx.to_inputs()
    assets = [signed_create_tx.id]
    with raises(ValueError):
        Decompose.generate(inputs, [([user_pub, user2_pub], 1)], assets)
    with raises(ValueError):
        Decompose.generate(inputs, [([user_pub], 1), ([user2_pub], 1)], assets)

# Test not matching owners_before and recipients
def test_invalid_recipient(signed_create_tx, user2_pub):
    inputs = signed_create_tx.to_inputs()
    assets = [signed_create_tx.id]
    with raises(ValueError):
        Decompose.generate(inputs, [([user2_pub], 1)], assets)

# Test Transaction.from_dict
def test_from_dict(signed_create_tx, user_pub):
    inputs = signed_create_tx.to_inputs()
    assets = [signed_create_tx.id]
    decompose_tx = Decompose.generate(inputs, [([user_pub], 1)], assets)
    decompose_dict = decompose_tx.to_dict()
    validate_transaction_schema(decompose_dict)
    Transaction.from_dict(decompose_dict)
    