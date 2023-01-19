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


class Compose(Transaction):
    OPERATION = "COMPOSE"
    ALLOWED_OPERATIONS = (OPERATION,)

    @classmethod
    def validate_compose(
      cls,
      inputs: list[Input],
      recipients: list[tuple[list[str], int]],
      new_assets: list[str],
      asset_ids: list[str]
    ):
        if not isinstance(inputs, list):
            raise TypeError("`inputs` must be a list instance")
        if len(inputs) == 0:
            raise ValueError("`inputs` must contain at least one item")
        if not isinstance(recipients, list):
            raise TypeError("`recipients` must be a list instance")

        if len(new_assets) != 1:
            raise ValueError("`assets` must contain only one new asset")

        input_tx_ids = []
        for input in inputs:
            if input.fulfills:
                input_tx_ids.append(input.fulfills.txid)
            else:
                raise ValueError("`inputs` must fulfill another transaction")

        if set(asset_ids) != set(input_tx_ids):
            raise ValueError("consumed `asset_ids` must be represented in `input.fulfills`")

        outputs = []
        for recipient in recipients:
            if not isinstance(recipient, tuple) or len(recipient) != 2:
                raise ValueError(
                    ("Each `recipient` in the list must be a" " tuple of `([<list of public keys>]," " <amount>)`")
                )
            pub_keys, amount = recipient
            outputs.append(Output.generate(pub_keys, amount))
        
        return (deepcopy(inputs), outputs)

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
        (inputs, outputs) = Compose.validate_compose(inputs, recipients, new_assets, asset_ids)
        new_assets = [{"data": cid} for cid in new_assets]
        asset_ids = [{"id": id} for id in asset_ids]
        return cls(cls.OPERATION, new_assets + asset_ids, inputs, outputs, metadata)