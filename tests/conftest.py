# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

import pytest
import random

from base58 import b58decode
from planetmint_cryptoconditions import ThresholdSha256, Ed25519Sha256
from ipld import marshal, multihash
from transactions.types.assets.create import Create

USER_PRIVATE_KEY = "8eJ8q9ZQpReWyQT5aFCiwtZ5wDZC4eDnCen88p3tQ6ie"
USER_PUBLIC_KEY = "JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE"

USER2_PRIVATE_KEY = "F86PQPiqMTwM2Qi2Sda3U4Vdh3AgadMdX3KNVsu5wNJr"
USER2_PUBLIC_KEY = "GDxwMFbwdATkQELZbMfW8bd9hbNYMZLyVXA3nur2aNbE"

USER3_PRIVATE_KEY = "4rNQFzWQbVwuTiDVxwuFMvLG5zd8AhrQKCtVovBvcYsB"
USER3_PUBLIC_KEY = "Gbrg7JtxdjedQRmr81ZZbh1BozS7fBW88ZyxNDy7WLNC"

CC_FULFILLMENT_URI = (
    "pGSAINdamAGCsQq31Uv-08lkBzoO4XLz2qYjJa8CGmj3B1EagUDlVkMAw2CscpCG4syAboKKh"
    "Id_Hrjl2XTYc-BlIkkBVV-4ghWQozusxh45cBz5tGvSW_XwWVu-JGVRQUOOehAL"
)
CC_CONDITION_URI = "ni:///sha-256;" "eZI5q6j8T_fqv7xMROaei9_tmTMk4S7WR5Kr4onPHV8" "?fpt=ed25519-sha-256&cost=131072"

ASSET_DEFINITION = [{"data": "QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4"}]

DATA = "QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4"


@pytest.fixture
def user_priv():
    return USER_PRIVATE_KEY


@pytest.fixture
def user_pub():
    return USER_PUBLIC_KEY


@pytest.fixture
def user2_priv():
    return USER2_PRIVATE_KEY


@pytest.fixture
def user2_pub():
    return USER2_PUBLIC_KEY


@pytest.fixture
def user3_priv():
    return USER3_PRIVATE_KEY


@pytest.fixture
def user3_pub():
    return USER3_PUBLIC_KEY


@pytest.fixture
def ffill_uri():
    return CC_FULFILLMENT_URI


@pytest.fixture
def cond_uri():
    return CC_CONDITION_URI


@pytest.fixture
def user_Ed25519(user_pub):
    return Ed25519Sha256(public_key=b58decode(user_pub))


@pytest.fixture
def user_user2_threshold(user_pub, user2_pub):
    user_pub_keys = [user_pub, user2_pub]
    threshold = ThresholdSha256(threshold=len(user_pub_keys))
    for user_pub in user_pub_keys:
        threshold.add_subfulfillment(Ed25519Sha256(public_key=b58decode(user_pub)))
    return threshold


@pytest.fixture
def user2_Ed25519(user2_pub):
    return Ed25519Sha256(public_key=b58decode(user2_pub))


@pytest.fixture
def user_input(user_Ed25519, user_pub):
    from transactions.common.transaction import Input

    return Input(user_Ed25519, [user_pub])


@pytest.fixture
def user_user2_threshold_output(user_user2_threshold, user_pub, user2_pub):
    from transactions.common.transaction import Output

    return Output(user_user2_threshold, [user_pub, user2_pub])


@pytest.fixture
def user_user2_threshold_input(user_user2_threshold, user_pub, user2_pub):
    from transactions.common.transaction import Input

    return Input(user_user2_threshold, [user_pub, user2_pub])


@pytest.fixture
def user_output(user_Ed25519, user_pub):
    from transactions.common.transaction import Output

    return Output(user_Ed25519, [user_pub])


@pytest.fixture
def user2_output(user2_Ed25519, user2_pub):
    from transactions.common.transaction import Output

    return Output(user2_Ed25519, [user2_pub])


@pytest.fixture
def asset_definition():
    return ASSET_DEFINITION


@pytest.fixture
def data():
    return DATA


@pytest.fixture
def utx(user_input, user_output):
    from transactions.common.transaction import Transaction

    return Transaction(Transaction.CREATE, [{"data": None}], [user_input], [user_output])


@pytest.fixture
def tx(utx, user_priv):
    return utx.sign([user_priv])


@pytest.fixture
def transfer_utx(user_output, user2_output, utx):
    from transactions.common.transaction import Input, TransactionLink, Transaction

    user_output = user_output.to_dict()
    input = Input(utx.outputs[0].fulfillment, user_output["public_keys"], TransactionLink(utx.id, 0))
    return Transaction("TRANSFER", [{"id": utx.id}], [input], [user2_output])


@pytest.fixture
def transfer_tx(transfer_utx, user_priv):
    return transfer_utx.sign([user_priv])


@pytest.fixture(scope="session")
def dummy_transaction():
    return {
        "assets": [{"data": None}],
        "id": 64 * "a",
        "inputs": [
            {
                "fulfillment": "dummy",
                "fulfills": None,
                "owners_before": [58 * "a"],
            }
        ],
        "metadata": None,
        "operation": "CREATE",
        "outputs": [
            {
                "amount": "1",
                "condition": {
                    "details": {"public_key": 58 * "b", "type": "ed25519-sha-256"},
                    "uri": "dummy",
                },
                "public_keys": [58 * "b"],
            }
        ],
        "version": "3.0",
    }


@pytest.fixture
def unfulfilled_transaction():
    return {
        "assets": [{"data": "QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4"}],
        "id": None,
        "inputs": [
            {
                # XXX This could be None, see #1925
                # https://github.com/planetmint/planetmint/issues/1925
                "fulfillment": {
                    "public_key": "JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE",
                    "type": "ed25519-sha-256",
                },
                "fulfills": None,
                "owners_before": ["JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE"],
            }
        ],
        "metadata": None,
        "operation": "CREATE",
        "outputs": [
            {
                "amount": "1",
                "condition": {
                    "details": {
                        "public_key": "JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE",
                        "type": "ed25519-sha-256",
                    },
                    "uri": "ni:///sha-256;49C5UWNODwtcINxLgLc90bMCFqCymFYONGEmV4a0sG4?fpt=ed25519-sha-256&cost=131072",
                },
                "public_keys": ["JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE"],
            }
        ],
        "version": "1.0",
    }


@pytest.fixture
def fulfilled_transaction():
    return {
        "assets": [{"data": "QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4"}],
        "id": None,
        "inputs": [
            {
                "fulfillment": (
                    "pGSAIP_2P1Juh-94sD3uno1lxMPd9EkIalRo7QB014pT6dD9g"
                    "UANRNxasDy1Dfg9C2Fk4UgHdYFsJzItVYi5JJ_vWc6rKltn0k"
                    "jagynI0xfyR6X9NhzccTt5oiNH9mThEb4QmagN"
                ),
                "fulfills": None,
                "owners_before": ["JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE"],
            }
        ],
        "metadata": None,
        "operation": "CREATE",
        "outputs": [
            {
                "amount": "1",
                "condition": {
                    "details": {
                        "public_key": "JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE",
                        "type": "ed25519-sha-256",
                    },
                    "uri": "ni:///sha-256;49C5UWNODwtcINxLgLc90bMCFqCymFYONGEmV4a0sG4?fpt=ed25519-sha-256&cost=131072",
                },
                "public_keys": ["JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE"],
            }
        ],
        "version": "1.0",
    }


# TODO For reviewers: Pick which approach you like best: parametrized or not?
@pytest.fixture(
    params=(
        {
            "id": None,
            "fulfillment": {"public_key": "JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE", "type": "ed25519-sha-256"},
        },
        {
            "id": None,
            "fulfillment": (
                "pGSAIP_2P1Juh-94sD3uno1lxMPd9EkIalRo7QB014pT6dD9g"
                "UANRNxasDy1Dfg9C2Fk4UgHdYFsJzItVYi5JJ_vWc6rKltn0k"
                "jagynI0xfyR6X9NhzccTt5oiNH9mThEb4QmagN"
            ),
        },
        {
            "id": "7a7c827cf4ef7985f08f4e9d16f5ffc58ca4e82271921dfbed32e70cb462485f",
            "fulfillment": (
                "pGSAIP_2P1Juh-94sD3uno1lxMPd9EkIalRo7QB014pT6dD9g"
                "UANRNxasDy1Dfg9C2Fk4UgHdYFsJzItVYi5JJ_vWc6rKltn0k"
                "jagynI0xfyR6X9NhzccTt5oiNH9mThEb4QmagN"
            ),
        },
    )
)
def tri_state_transaction(request):
    tx = {
        "assets": [{"data": "QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4"}],
        "id": None,
        "inputs": [
            {"fulfillment": None, "fulfills": None, "owners_before": ["JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE"]}
        ],
        "metadata": None,
        "operation": "CREATE",
        "outputs": [
            {
                "amount": "1",
                "condition": {
                    "details": {
                        "public_key": "JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE",
                        "type": "ed25519-sha-256",
                    },
                    "uri": "ni:///sha-256;49C5UWNODwtcINxLgLc90bMCFqCymFYONGEmV4a0sG4?fpt=ed25519-sha-256&cost=131072",
                },
                "public_keys": ["JEAkEJqLbbgDRAtMm8YAjGp759Aq2qTn9eaEHUj2XePE"],
            }
        ],
        "version": "3.0",
    }
    tx["id"] = request.param["id"]
    tx["inputs"][0]["fulfillment"] = request.param["fulfillment"]
    return tx


@pytest.fixture
def user_sk():
    return USER_PRIVATE_KEY


@pytest.fixture
def user_pk():
    return USER_PUBLIC_KEY


@pytest.fixture
def alice():
    from transactions.common.crypto import generate_key_pair

    return generate_key_pair()


@pytest.fixture
def bob():
    from transactions.common.crypto import generate_key_pair

    return generate_key_pair()


@pytest.fixture
def carol():
    from transactions.common.crypto import generate_key_pair

    return generate_key_pair()


@pytest.fixture
def merlin():
    from transactions.common.crypto import generate_key_pair

    return generate_key_pair()


@pytest.fixture
def create_tx(alice, user_pk):
    name = f"I am created by the create_tx fixture. My random identifier is {random.random()}."
    assets = [{"data": multihash(marshal({"name": name}))}]
    return Create.generate([alice.public_key], [([user_pk], 1)], assets=assets)


@pytest.fixture
def signed_create_tx(alice, create_tx):
    return create_tx.sign([alice.private_key])


@pytest.fixture
def signed_transfer_tx(signed_create_tx, user_pk, user_sk):
    from transactions.types.assets.transfer import Transfer

    inputs = signed_create_tx.to_inputs()
    tx = Transfer.generate(inputs, [([user_pk], 1)], asset_ids=[signed_create_tx.id])
    return tx.sign([user_sk])


@pytest.fixture
def signed_2_0_create_tx():
    return {
        "inputs": [
            {
                "owners_before": ["5V4AANHTSLdQH1mEA1pohW3jMduY9xMJ1voos7gRfMQF"],
                "fulfills": None,
                "fulfillment": "pGSAIEKelMEu8AzcA9kcDLrsEXhSpZG-lf2c9CuZpzZU_ONkgUBMztcnweWqwHVfVk9Y-IRgfdh864yXYTrTKzSMy6uvNjQeLtGzKxz4gjb01NUu6WLvZBAvr0Ws4glfxKiDLjkP",
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
        "operation": "CREATE",
        "metadata": "QmRBri4SARi56PgB2ALFVjHsLhQDUh4jYbeiHaU94vLoxd",
        "asset": {"data": "QmW5GVMW98D3mktSDfWHS8nX2UiCd8gP1uCiujnFX4yK8n"},
        "version": "2.0",
        "id": "3e2a2c5eef5e6a0c4e1e5f8d0dc1d3d9b4f035592a9788f8bfa7d59f86d123d3",
    }


@pytest.fixture
def signed_2_0_create_tx_assets():
    return {
        "inputs": [
            {
                "owners_before": ["5V4AANHTSLdQH1mEA1pohW3jMduY9xMJ1voos7gRfMQF"],
                "fulfills": None,
                "fulfillment": "pGSAIEKelMEu8AzcA9kcDLrsEXhSpZG-lf2c9CuZpzZU_ONkgUBMztcnweWqwHVfVk9Y-IRgfdh864yXYTrTKzSMy6uvNjQeLtGzKxz4gjb01NUu6WLvZBAvr0Ws4glfxKiDLjkP",
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
        "operation": "CREATE",
        "metadata": "QmRBri4SARi56PgB2ALFVjHsLhQDUh4jYbeiHaU94vLoxd",
        "assets": {"data": "QmW5GVMW98D3mktSDfWHS8nX2UiCd8gP1uCiujnFX4yK8n"},
        "version": "2.0",
        "id": "3e2a2c5eef5e6a0c4e1e5f8d0dc1d3d9b4f035592a9788f8bfa7d59f86d123d3",
    }


@pytest.fixture
def signed_2_0_transfer_tx():
    return {
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
                "public_keys": ["CfQjBk7RSsZt2xMfdV7axSxwrUT9ujEZqECMKHjdaB53"],
                "condition": {
                    "details": {
                        "type": "ed25519-sha-256",
                        "public_key": "CfQjBk7RSsZt2xMfdV7axSxwrUT9ujEZqECMKHjdaB53",
                    },
                    "uri": "ni:///sha-256;xQo74kd_tmP_DXe8r5kuVwa6rDUlsqClkTG5FS8W5k0?fpt=ed25519-sha-256&cost=131072",
                },
                "amount": "50",
            },
            {
                "public_keys": ["E9iwLjakBJtWGWvRRwi39L3z341pmq8X4GuJyZPZ3x1T"],
                "condition": {
                    "details": {
                        "type": "ed25519-sha-256",
                        "public_key": "E9iwLjakBJtWGWvRRwi39L3z341pmq8X4GuJyZPZ3x1T",
                    },
                    "uri": "ni:///sha-256;sy10qWh8LW4JxhlHBZ1oYZo-t2DjY90YVy2BsGg-K3M?fpt=ed25519-sha-256&cost=131072",
                },
                "amount": "2950",
            },
        ],
        "operation": "TRANSFER",
        "metadata": "QmTjWHzypFxE8uuXJXMJQJxgAEKjoWmQimGiutmPyJ6CAB",
        "asset": {"id": "ee9b031b61a3b7eaa63728ace4a4e08d21e69ba38d0cb90596aec198b970926b"},
        "version": "2.0",
        "id": "6b569a4c4e7a97ea4c3b8ef072620d8f6131c1929e2058cc484f003c9459baf4",
    }
