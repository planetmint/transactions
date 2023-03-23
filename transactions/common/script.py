# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

import json
import base58
from zenroom import zencode_exec
from json.decoder import JSONDecodeError


class Script(object):
    def __init__(self, code, inputs, outputs):
        self.code = code
        self.inputs = inputs
        self.outputs = outputs

    @classmethod
    def from_dict(cls, data: dict):
        return Script(
            json.loads(base58.b58decode(data["code"])),
            json.loads(base58.b58decode(data["inputs"])),
            json.loads(base58.b58decode(data["outputs"])),
        )

    def to_dict(self):
        return {
            "code": base58.b58encode(json.dumps(self.code)),
            "inputs": base58.b58encode(json.dumps(self.inputs)),
            "outputs": base58.b58encode(json.dumps(self.outputs)),
        }

    def validate(self) -> bool:
        result = zencode_exec(self.code, data=self.inputs)

        if len(result.output) == 0 and len(result.logs) > 0:
            return False

        try:
            result = json.loads(result.output)
            # output tag is only defined if zenroom returns a type (int, string, ...)
            # in case a 'variable' is returned, the output will look like follows: 'variable':'value'
            # that's the cause for the KeyError catch
            try:
                result["output"]
            except KeyError:
                return result == self.outputs
            else:
                return result["output"] == self.outputs
        except JSONDecodeError:
            return False
