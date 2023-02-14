# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

from copy import deepcopy
from typing import Optional
from cid import is_cid

from transactions.common.transaction import Transaction
from transactions.common.input import Input
from transactions.common.output import Output
from transactions.common.schema import validate_transaction_schema
from transactions.common.exceptions import SchemaValidationError


class Decompose(Transaction):
    OPERATION = "DECOMPOSE"
    ALLOWED_OPERATIONS = (OPERATION,)

    @classmethod
    def validate_decompose(
        cls, inputs: list[Input], recipients: list[tuple[list[str], int]], new_assets: list[str], asset_ids: list[str]
    ):
        if not isinstance(inputs, list):
            raise TypeError("`inputs` must be a list instance")

        if len(asset_ids) != 1:
            raise ValueError("`assets` must contain exactly one item")

        if len(new_assets) < 1:
            raise ValueError("decompose must create at least one new `asset`")

        outputs = []
        recipient_pub_keys = []
        for recipient in recipients:
            if not isinstance(recipient, tuple) or len(recipient) != 2:
                raise ValueError(
                    ("Each `recipient` in the list must be a" " tuple of `([<list of public keys>]," " <amount>)`")
                )
            pub_keys, amount = recipient
            if len(pub_keys) != 1:
                raise ValueError("decompose transactions only allow for one recipient")
            recipient_pub_keys.append(pub_keys[0])
            outputs.append(Output.generate(pub_keys, amount))

        if len(set(recipient_pub_keys)) != 1:
            raise ValueError("decompose transactions only allow for one recipient")

        owners_before = []
        for i in inputs:
            if len(i.owners_before) == 1:
                owners_before.append(i.owners_before[0])
            else:
                raise ValueError("decompose transactions only allow for one owner_before")

        if set(recipient_pub_keys) != set(owners_before):
            raise ValueError("recipient/owners_before missmatch")

        return (deepcopy(inputs), outputs)

    @classmethod
    def validate_schema(cls, tx):
        validate_transaction_schema(tx)

    @classmethod
    def generate(
        cls,
        inputs: list[Input],
        recipients: list[tuple[list[str], int]],
        assets: list[str],
        metadata: Optional[dict] = None,
    ):
        asset_ids = []
        new_assets = []
        for asset in assets:
            if is_cid(asset):
                new_assets.append(asset)
            else:
                asset_ids.append(asset)
        (inputs, outputs) = Decompose.validate_decompose(inputs, recipients, new_assets, asset_ids)
        new_assets = [{"data": cid} for cid in new_assets]
        asset_ids = [{"id": id} for id in asset_ids]
        decompose = cls(cls.OPERATION, new_assets + asset_ids, inputs, outputs, metadata)
        cls.validate_schema(decompose.to_dict())
        return decompose
