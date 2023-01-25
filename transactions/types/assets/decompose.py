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
from transactions.common.schema import _validate_schema, TX_SCHEMA_COMMON, TX_SCHEMA_DECOMPOSE
from transactions.common.exceptions import SchemaValidationError


class Decompose(Transaction):
    OPERATION = "DECOMPOSE"
    ALLOWED_OPERATIONS = (OPERATION,)
    TX_SCHEMA_CUSTOM = TX_SCHEMA_DECOMPOSE
    
    @classmethod
    def validate_decompose(
        cls,
        inputs: list[Input],
        recipients: list[tuple[list[str], int]],
        assets: list[str]
    ):
        if not isinstance(inputs, list):
            raise TypeError("`inputs` must be a list instance")
        if len(inputs) != 1:
            raise ValueError("`inputs` must contain exactly one item")
        
        if len(assets) != 1:
            raise ValueError("`assets` must contain exactly one item")
        
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
        
        if len(set(recipient_pub_keys)) != 0:
            raise ValueError("decompose transactions only allow for one recipient")
        
        return (deepcopy(inputs), outputs)
    
    @classmethod
    def validate_schema(cls, tx):
        try:
            _validate_schema(TX_SCHEMA_COMMON, tx)
            _validate_schema(cls.TX_SCHEMA_CUSTOM, tx)
        except KeyError:
            raise SchemaValidationError()
        
    @classmethod
    def generate(
        cls,
        inputs: list[Input],
        recipients: list[tuple[list[str], int]],
        assets: list[str],
        metadata: Optional[dict] = None,
    ):
        (inputs, outputs) = Decompose.validate_decompose(inputs, recipients, assets)
        decompose = cls(cls.OPERATION, assets, inputs, outputs, metadata)
        cls.validate_schema(decompose.to_dict())
        return decompose