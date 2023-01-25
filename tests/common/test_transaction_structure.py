# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

"""All tests of transaction structure. The concern here is that transaction
structural / schematic issues are caught when reading a transaction
(ie going from dict -> transaction).
"""
import json
import pytest
import hashlib as sha3

from unittest.mock import MagicMock
from transactions.common.exceptions import AmountError, SchemaValidationError, ThresholdTooDeep
from transactions.common.transaction import Transaction
from transactions.common.utils import _fulfillment_to_details, _fulfillment_from_details
from ipld import marshal, multihash

################################################################################
# Helper functions


def validate(tx):
    if isinstance(tx, Transaction):
        tx = tx.to_dict()
    Transaction.from_dict(tx, False)


def validate_raises(tx, exc=SchemaValidationError):
    with pytest.raises(exc):
        validate(tx)


# We should test that validation works when we expect it to
def test_validation_passes(signed_create_tx):
    Transaction.from_dict(signed_create_tx.to_dict(), False)


################################################################################
# ID


def test_tx_serialization_hash_function(signed_create_tx):
    tx = signed_create_tx.to_dict()
    tx["id"] = None
    payload = json.dumps(tx, skipkeys=False, sort_keys=True, separators=(",", ":"))
    assert sha3.sha3_256(payload.encode()).hexdigest() == signed_create_tx.id


def test_tx_serialization_with_incorrect_hash(signed_create_tx):
    from transactions.common.exceptions import InvalidHash

    tx = signed_create_tx.to_dict()
    tx["id"] = "a" * 64
    with pytest.raises(InvalidHash):
        Transaction.validate_id(tx)


def test_tx_serialization_with_no_hash(signed_create_tx):
    from transactions.common.exceptions import InvalidHash

    tx = signed_create_tx.to_dict()
    del tx["id"]
    with pytest.raises(InvalidHash):
        Transaction.from_dict(tx, False)


################################################################################
# Operation


def test_validate_invalid_operation(create_tx, alice):
    create_tx.operation = "something invalid"
    signed_tx = create_tx.sign([alice.private_key])
    validate_raises(signed_tx)


################################################################################
# Metadata


def test_validate_fails_metadata_empty_dict(create_tx, alice):
    create_tx.metadata = multihash(marshal({"a": 1}))
    signed_tx = create_tx.sign([alice.private_key])
    validate(signed_tx)

    create_tx._id = None
    create_tx.fulfillment = None
    create_tx.metadata = None
    signed_tx = create_tx.sign([alice.private_key])
    validate(signed_tx)

    create_tx._id = None
    create_tx.fulfillment = None
    create_tx.metadata = {}
    signed_tx = create_tx.sign([alice.private_key])
    validate_raises(signed_tx)


################################################################################
# Asset


def test_transfer_asset_schema(user_sk, signed_transfer_tx):
    from transactions.common.transaction import Transaction

    tx = signed_transfer_tx.to_dict()
    validate(tx)
    tx["id"] = None
    tx["assets"][0]["data"] = {}
    tx = Transaction.from_dict(tx).sign([user_sk]).to_dict()
    validate_raises(tx)
    tx["id"] = None
    del tx["assets"][0]["data"]
    tx["assets"][0]["id"] = "b" * 63
    tx = Transaction.from_dict(tx).sign([user_sk]).to_dict()
    validate_raises(tx)


def test_create_tx_no_asset_id(create_tx, alice):
    create_tx.assets[0]["id"] = "b" * 64
    signed_tx = create_tx.sign([alice.private_key])
    validate_raises(signed_tx)


def test_create_tx_asset_type(create_tx, alice):
    create_tx.assets[0]["data"] = multihash(marshal({"a": ""}))
    signed_tx = create_tx.sign([alice.private_key])
    validate(signed_tx)


def test_create_tx_no_asset_data(create_tx):
    tx_body = create_tx.to_dict()
    del tx_body["assets"][0]["data"]
    tx_serialized = json.dumps(tx_body, skipkeys=False, sort_keys=True, separators=(",", ":"))
    tx_body["id"] = sha3.sha3_256(tx_serialized.encode()).hexdigest()
    validate_raises(tx_body)


################################################################################
# Inputs


def test_no_inputs(create_tx, alice):
    create_tx.inputs = []
    signed_tx = create_tx.sign([alice.private_key])
    validate_raises(signed_tx)


def test_create_single_input(create_tx, alice):
    from transactions.common.transaction import Transaction

    tx = create_tx.to_dict()
    tx["inputs"] += tx["inputs"]
    tx = Transaction.from_dict(tx).sign([alice.private_key]).to_dict()
    validate_raises(tx)
    tx["id"] = None
    tx["inputs"] = []
    tx = Transaction.from_dict(tx).sign([alice.private_key]).to_dict()
    validate_raises(tx)


def test_create_tx_no_fulfills(create_tx, alice):
    from transactions.common.transaction import Transaction

    tx = create_tx.to_dict()
    tx["inputs"][0]["fulfills"] = {"transaction_id": "a" * 64, "output_index": 0}
    tx = Transaction.from_dict(tx).sign([alice.private_key]).to_dict()
    validate_raises(tx)


def test_transfer_has_inputs(user_sk, signed_transfer_tx):
    signed_transfer_tx.inputs = []
    signed_transfer_tx._id = None
    signed_transfer_tx.sign([user_sk])
    validate_raises(signed_transfer_tx)


################################################################################
# Outputs


def test_low_amounts(user_sk, create_tx, signed_transfer_tx, alice):
    for sk, tx in [(alice.private_key, create_tx), (user_sk, signed_transfer_tx)]:
        tx.outputs[0].amount = 0
        tx._id = None
        tx.sign([sk])
        validate_raises(tx, AmountError)
        tx.outputs[0].amount = -1
        tx._id = None
        tx.sign([sk])
        validate_raises(tx)


def test_high_amounts(create_tx, alice):
    # Should raise a SchemaValidationError - don't want to allow ridiculously
    # large numbers to get converted to int
    create_tx.outputs[0].amount = 10**21
    create_tx.sign([alice.private_key])
    validate_raises(create_tx)
    # Should raise AmountError
    create_tx.outputs[0].amount = 9 * 10**18 + 1
    create_tx._id = None
    create_tx.sign([alice.private_key])
    validate_raises(create_tx, AmountError)
    # Should pass
    create_tx.outputs[0].amount -= 1
    create_tx._id = None
    create_tx.sign([alice.private_key])
    validate(create_tx)


################################################################################
# Conditions


def test_handle_threshold_overflow():
    cond = {
        "type": "ed25519-sha-256",
        "public_key": "a" * 43,
    }
    for i in range(1000):
        cond = {
            "type": "threshold-sha-256",
            "threshold": 1,
            "subconditions": [cond],
        }
    with pytest.raises(ThresholdTooDeep):
        _fulfillment_from_details(cond)


def test_unsupported_condition_type():
    from planetmint_cryptoconditions.exceptions import UnsupportedTypeError

    with pytest.raises(UnsupportedTypeError):
        _fulfillment_from_details({"type": "a"})

    with pytest.raises(UnsupportedTypeError):
        _fulfillment_to_details(MagicMock(type_name="a"))


################################################################################
# Version


def test_validate_version(create_tx, alice):
    create_tx.version = "3.0"
    create_tx.sign([alice.private_key])
    validate(create_tx)

    create_tx.version = "0.10"
    create_tx._id = None
    create_tx.sign([alice.private_key])
    validate_raises(create_tx)

    create_tx.version = "110"
    create_tx._id = None
    create_tx.sign([alice.private_key])
    validate_raises(create_tx)
