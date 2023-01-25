# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

from transactions.types.assets.compose import Compose
from pytest import raises


# Test valid compose 1 input same owner
def test_valid_compose_single_input_same_owner(signed_create_tx, user_pub):
    inputs = signed_create_tx.to_inputs()
    assets = [signed_create_tx.id, "QmW5GVMW98D3mktSDfWHS8nX2UiCd8gP1uCiujnFX4yK8n"]
    compose_tx = Compose.generate(inputs, [([user_pub], 1)], assets)

    assert compose_tx
    assert len(compose_tx.outputs) == 1
    assert user_pub in compose_tx.outputs[0].public_keys
    
    from transactions.common.transaction import Transaction
    from transactions.common.schema import validate_transaction_schema
    dict = compose_tx.to_dict()
    Transaction.from_dict(dict)
    validate_transaction_schema(dict)
    

# Test valid compose 1 input different owner
def test_valid_compose_single_input_different_owner(signed_create_tx, user2_pub):
    inputs = signed_create_tx.to_inputs()
    assets = [signed_create_tx.id, "QmW5GVMW98D3mktSDfWHS8nX2UiCd8gP1uCiujnFX4yK8n"]
    compose_tx = Compose.generate(inputs, [([user2_pub], 1)], assets)
    assert compose_tx
    assert len(compose_tx.outputs) == 1
    assert user2_pub in compose_tx.outputs[0].public_keys

# Test valid compose 2 inputs same owner
def test_valid_compose_two_input_same_owner(signed_create_tx, signed_create_tx_2, user_pub):
    inputs = signed_create_tx.to_inputs() + signed_create_tx_2.to_inputs()
    assets = [signed_create_tx.id, signed_create_tx_2.id, "QmW5GVMW98D3mktSDfWHS8nX2UiCd8gP1uCiujnFX4yK8n"]
    compose_tx = Compose.generate(inputs, [([user_pub], 1)], assets)
    assert compose_tx
    assert len(compose_tx.outputs) == 1
    assert user_pub in compose_tx.outputs[0].public_keys

# Test valid compose 2 inputs different owner
def test_valid_compose_two_input_different_owner(signed_create_tx, signed_create_tx_2, user2_pub):
    inputs = signed_create_tx.to_inputs() + signed_create_tx_2.to_inputs()
    assets = [signed_create_tx.id, signed_create_tx_2.id, "QmW5GVMW98D3mktSDfWHS8nX2UiCd8gP1uCiujnFX4yK8n"]
    compose_tx = Compose.generate(inputs, [([user2_pub], 1)], assets)
    assert compose_tx
    assert len(compose_tx.outputs) == 1
    assert user2_pub in compose_tx.outputs[0].public_keys

# Test more asset_ids than input_txid
def test_asset_input_missmatch(signed_create_tx, signed_create_tx_2, user_pub):
    inputs = signed_create_tx.to_inputs()
    assets = [signed_create_tx.id, signed_create_tx_2.id, "QmW5GVMW98D3mktSDfWHS8nX2UiCd8gP1uCiujnFX4yK8n"]
    with raises(ValueError):
        Compose.generate(inputs, [([user_pub], 1)], assets)

# Test more than one new asset
def test_invalid_number_of_new_assets(signed_create_tx, user_pub):
    inputs = signed_create_tx.to_inputs()
    assets = [signed_create_tx.id, "QmW5GVMW98D3mktSDfWHS8nX2UiCd8gP1uCiujnFX4yK8n", "QmW5GVMW98D3mktSDfWHS8nX2UiCd8gP1uCiujnFX4yK8n"]
    with raises(ValueError):
        Compose.generate(inputs, [([user_pub], 1)], assets)
