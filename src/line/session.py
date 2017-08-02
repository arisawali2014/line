# coding: utf-8

"""
:copyright: (c) 2014 by Taehoon Kim.
:license: BSD, see LICENSE for more details.

このライブラリはTaehoon Kim氏が開発し、Sh1maが改良したライブラリです。
"""


# from thrift.transport import TTransport
# from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol

from LineThrift import TalkService
from LineThrift import ChannelService
from LineThrift import CallService

class SessionManager:

    def __init__(self, url, headers):

        self.host = url
        self.headers = headers

    def TalkSession(self, isopen=True):

        self.transport = THttpClient.THttpClient(self.host)
        self.transport.setCustomHeaders(self.headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._client  = TalkService.Client(self.protocol)
        
        if isopen:
            self.transport.open()

        return self._client

    def ChannelSession(self, isopen=True):

        self.transport = THttpClient.THttpClient(self.host)
        self.transport.setCustomHeaders(self.headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._client  = ChannelService.Client(self.protocol)
        
        if isopen:
            self.transport.open()

        return self._client

    def CallSession(self, isopen=True):

        self.transport = THttpClient.THttpClient(self.host)
        self.transport.setCustomHeaders(self.headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._client  = CallService.Client(self.protocol)
        
        if isopen:
            self.transport.open()

        return self._client