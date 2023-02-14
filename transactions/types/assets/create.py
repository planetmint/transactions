# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

from typing import Optional
from cid import is_cid

from transactions.common.transaction import Transaction
from transactions.common.input import Input


class Create(Transaction):
    OPERATION = "CREATE"
    ALLOWED_OPERATIONS = (OPERATION,)

    @classmethod
    def validate_create(
        cls,
        tx_signers: list[str],
        recipients: list[tuple[list[str], int]],
        assets: Optional[list[dict]],
        metadata: Optional[dict],
    ):
        if not isinstance(tx_signers, list):
            raise TypeError("`tx_signers` must be a list instance")
        if not isinstance(recipients, list):
            raise TypeError("`recipients` must be a list instance")
        if len(tx_signers) == 0:
            raise ValueError("`tx_signers` list cannot be empty")
        if len(recipients) == 0:
            raise ValueError("`recipients` list cannot be empty")
        if not assets is None:
            if not isinstance(assets, list) and len(assets) != 1:
                raise TypeError("`assets` must be a list of length 1 or None")
            if "data" in assets[0]:
                if assets[0]["data"] is not None and not is_cid(assets[0]["data"]):
                    raise TypeError("`asset.data` must be a CID string or None")
        if not (metadata is None or is_cid(metadata)):
            raise TypeError("`metadata` must be a CID string or None")

        return True

    @classmethod
    def generate(
        cls,
        tx_signers: list[str],
        recipients: list[tuple[list[str], int]],
        metadata: Optional[dict] = None,
        assets: Optional[list] = [{"data": None}],
        inputs: Optional[list[Input]] = None,
    ):
        """A simple way to generate a `CREATE` transaction.

        Note:
            This method currently supports the following Cryptoconditions
            use cases:
                - Ed25519
                - ThresholdSha256

            Additionally, it provides support for the following Planetmint
            use cases:
                - Multiple inputs and outputs.

        Args:
            tx_signers (:obj:`list` of :obj:`str`): A list of keys that
                represent the signers of the CREATE Transaction.
            recipients (:obj:`list` of :obj:`tuple`): A list of
                ([keys],amount) that represent the recipients of this
                Transaction.
            metadata (dict): The metadata to be stored along with the
                Transaction.
            assets (:obj:`list` of :obj:`dict`): The metadata associated with the asset that will
                be created in this Transaction.

        Returns:
            :class:`~planetmint.common.transaction.Transaction`
        """

        Create.validate_create(tx_signers, recipients, assets, metadata)
        (generated_inputs, outputs) = Transaction.complete_tx_i_o(tx_signers, recipients)
        inputs = inputs if inputs is not None else generated_inputs
        return cls(cls.OPERATION, assets, inputs, outputs, metadata)
