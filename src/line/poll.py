# coding: utf-8

"""
:copyright: (c) 2014 by Taehoon Kim.
:license: BSD, see LICENSE for more details.

このライブラリはTaehoon Kim氏が開発し、Sh1maが改良したライブラリです。
"""


from LineThrift.ttypes import OpType


class PollManager:
    """Polling Manage class"""

    def __init__(self, client):

        self.client = client
        self.functions = {}

    def fetchOperation(self, revision, count=1):
        """operationを取得"""

        return self.client._client_in.fetchOperations(revision, count)

    def addFunction(self, operationType, functionName):
        """処理を追加する"""

        self.functions[operationType] = functionName

    def start(self):

        try:
            operations = self.fetchOperation(self.client.revision)
        except EOFError:
            return
        except KeyboardInterrupt:
            exit()
        except:
            return

        for op in operations:

            #print op
            if op.type in self.functions.keys():
                self.functions[op.type](op)

            self.client.revision = max(op.revision, self.client.revision)