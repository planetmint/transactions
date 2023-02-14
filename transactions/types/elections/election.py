# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

from uuid import uuid4
from typing import Optional

from transactions.common.transaction import Transaction
from transactions.common.schema import validate_transaction_schema, SchemaValidationError


class Election(Transaction):
    """Represents election transactions.

    To implement a custom election, create a class deriving from this one
    with OPERATION set to the election operation, ALLOWED_OPERATIONS
    set to (OPERATION,), CREATE set to OPERATION.
    """

    OPERATION: Optional[str] = None
    # Election Statuses:
    ONGOING: str = "ongoing"
    CONCLUDED: str = "concluded"
    INCONCLUSIVE: str = "inconclusive"
    # Vote ratio to approve an election
    ELECTION_THRESHOLD = 2 / 3

    @classmethod
    def validate_election(self, tx_signers, recipients, assets, metadata):
        if not isinstance(tx_signers, list):
            raise TypeError("`tx_signers` must be a list instance")
        if not isinstance(recipients, list):
            raise TypeError("`recipients` must be a list instance")
        if len(tx_signers) == 0:
            raise ValueError("`tx_signers` list cannot be empty")
        if len(recipients) == 0:
            raise ValueError("`recipients` list cannot be empty")
        if not isinstance(assets, list) and len(assets) != 1:
            raise TypeError("`assets` must be a list containing exactly on element")
        if not (metadata is None or isinstance(metadata, str)):
            # add check if metadata is ipld marshalled CID string
            raise TypeError("`metadata` must be a CID string or None")

        return True

    @classmethod
    def generate(cls, initiator, voters, election_data, metadata=None):
        # Break symmetry in case we need to call an election with the same properties twice
        uuid = uuid4()
        election_data[0]["data"]["seed"] = str(uuid)

        Election.validate_election(initiator, voters, election_data, metadata)
        (inputs, outputs) = Transaction.complete_tx_i_o(initiator, voters)
        election = cls(cls.OPERATION, election_data, inputs, outputs, metadata)
        cls.validate_schema(election.to_dict())
        return election

    @classmethod
    def validate_schema(cls, tx):
        """Validate the election transaction. Since `ELECTION` extends `CREATE` transaction, all the validations for
        `CREATE` transaction should be inherited
        """
        try:
            validate_transaction_schema(tx)
        except KeyError:
            raise SchemaValidationError()
