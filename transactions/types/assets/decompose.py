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
        new_assets: list[str],
        asset_ids: list[str]
    ):
        return
    
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
        return