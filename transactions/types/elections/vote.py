# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

from transactions.types.assets.transfer import Transfer
from transactions.common.transaction import VOTE
from transactions.common.schema import (
    _validate_schema,
    TX_SCHEMA_COMMON,
    TX_SCHEMA_TRANSFER,
    TX_SCHEMA_VOTE,
    TX_SCHEMA_COMMON_2_0,
    TX_SCHEMA_TRANSFER_2_0,
)


class Vote(Transfer):
    OPERATION = VOTE
    # NOTE: This class inherits TRANSFER txn type. The `TRANSFER` property is
    # overriden to re-use methods from parent class
    TRANSFER = OPERATION
    ALLOWED_OPERATIONS = (OPERATION,)
    # Custom validation schema
    TX_SCHEMA_CUSTOM = TX_SCHEMA_VOTE

    @classmethod
    def generate(cls, inputs, recipients, election_ids, metadata=None):
        (inputs, outputs) = cls.validate_transfer(inputs, recipients, election_ids, metadata)
        election_vote = cls(cls.OPERATION, [{"id": id} for id in election_ids], inputs, outputs, metadata)
        cls.validate_schema(election_vote.to_dict())
        return election_vote

    @classmethod
    def validate_schema(cls, tx):
        """Validate the validator election vote transaction. Since `VOTE` extends `TRANSFER`
        transaction, all the validations for `CREATE` transaction should be inherited
        """
        try:
            if tx["version"] == "3.0":
                _validate_schema(TX_SCHEMA_COMMON, tx)
                _validate_schema(TX_SCHEMA_TRANSFER, tx)
            else:
                _validate_schema(TX_SCHEMA_COMMON_2_0, tx)
                _validate_schema(TX_SCHEMA_TRANSFER_2_0, tx)
        except KeyError:
            raise SchemaValidationError()
        _validate_schema(cls.TX_SCHEMA_CUSTOM, tx)
