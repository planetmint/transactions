# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

from transactions.types.assets.compose import Compose
from pytest import raises

example_compose_tx = {
    "inputs": [
        {
            "owners_before": ["E9iwLjakBJtWGWvRRwi39L3z341pmq8X4GuJyZPZ3x1T"],
            "fulfills": {
                "transaction_id": "ee9b031b61a3b7eaa63728ace4a4e08d21e69ba38d0cb90596aec198b970926b",
                "output_index": 0,
            },
            "fulfillment": "pGSAIMNj_qX5E_xk428K0Oc4Ik1MNn_ln_u-jIggdg-ynOXmgUDO4j5R1yMeFLf68JGfjygzmR48wZm0k6-VNt6a3vhlANfoXWrnJnoRKVPBPm2fcrio0NafT7MCWxZEXqoFovgO",
        }
    ],
    "outputs": [
        {
            "public_keys": ["5V4AANHTSLdQH1mEA1pohW3jMduY9xMJ1voos7gRfMQF"],
            "condition": {
                "details": {
                    "type": "ed25519-sha-256",
                    "public_key": "5V4AANHTSLdQH1mEA1pohW3jMduY9xMJ1voos7gRfMQF",
                },
                "uri": "ni:///sha-256;M3l9yVs7ItjP-lxT7B2ta6rpRa-GHt6TBSYpy8l-IS8?fpt=ed25519-sha-256&cost=131072",
            },
            "amount": "3000",
        }
    ],
    "operation": "COMPOSE",
    "metadata": "QmRBri4SARi56PgB2ALFVjHsLhQDUh4jYbeiHaU94vLoxd",
    "assets": [
        {"data": "QmW5GVMW98D3mktSDfWHS8nX2UiCd8gP1uCiujnFX4yK8n"},
        {"id": "6b569a4c4e7a97ea4c3b8ef072620d8f6131c1929e2058cc484f003c9459baf4"},
        {"id": "3e2a2c5eef5e6a0c4e1e5f8d0dc1d3d9b4f035592a9788f8bfa7d59f86d123d3"}
    ],
    "version": "3.0",
    "id": "3e2a2c5eef5e6a0c4e1e5f8d0dc1d3d9b4f035592a9788f8bfa7d59f86d123d3",
}

# Test scenarios

# Test valid compose 1 input same owner
def test_valid_compose_single_input_same_owner():
    return 

# Test valid compose 1 input different owner
def test_valid_compose_single_input_different_owner():
    return 

# Test valid compose 2 inputs same owner
def test_valid_compose_two_input_same_owner():
    return

# Test valid compose 2 inputs different owner
def test_valid_compose_two_input_different_owner():
    return 

# Test more asset_ids than input_txid
def test_asset_input_missmatch():
    return

# Test more than one new asset
def test_invalid_number_of_new_assets():
    return

# Test consuming not owned assets => needs to be tested as acceptance/integration test
def test_consuming_not_owned_assets():
    return
