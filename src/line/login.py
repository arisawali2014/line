# coding: utf-8

"""
:copyright: (c) 2014 by Taehoon Kim.
:license: BSD, see LICENSE for more details.

このライブラリはTaehoon Kim氏が開発し、Sh1maが改良したライブラリです。
"""


import rsa
import requests
import simplejson as json

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol

from LineThrift import TalkService
from LineThrift import ChannelService
from LineThrift import CallService
from LineThrift.ttypes import TalkException
from LineThrift.ttypes import IdentityProvider

from .session import SessionManager

class LoginManager(object):


    def __init__(self):

        self.HOST = "https://gm2.line.naver.jp"

        #ログイン関連
        self.SESSION_URL = self.HOST + "/authct/v1/keys/line"
        self.LOGIN_URL   = self.HOST + "/api/v4/TalkService.do"

        #セッション関連
        self.EXEC_URL = self.HOST + "/S4"
        self.POLL_URL = self.HOST + "/P4"
        self.CALL_URL = self.HOST + "/V4"

        #認証用
        self.CERT_URL = self.HOST + "/Q"
        self._session = requests.session()

        self.revision    = None
        self.certificate = ""

        #PC名
        self.com_name = "in9lude"

        self.headers = {}
        self.headers["User-Agent"] = "DESKTOP:MAC:10.12.4-UNKNOWN(5.1.1)"
        self.headers["X-Line-Application"] = "DESKTOPMAC\t5.1.1\tMAC\t10.12.4-UNKNOWN"
            

    def mailLogin(self):

        j = self.get_json(self.SESSION_URL)

        session_key = j['session_key']

        message = (
            chr(len(session_key)) + session_key +
            chr(len(self.email)) + self.email +
            chr(len(self.password)) + self.password).encode('utf-8')

        keyname, n, e = j['rsa_key'].split(",")
        pub_key       = rsa.PublicKey(int(n,16), int(e,16))
        crypto        = rsa.encrypt(message, pub_key).encode('hex')

        self._client = SessionManager(self.LOGIN_URL, self.headers).TalkSession(isopen=False)

        try:
            with open(self.email + ".crt", 'r') as f:
                self.certificate = f.read()
        except:
            self.certificate = ""

        result = self._client.loginWithIdentityCredentialForCertificate(
                IdentityProvider.LINE, keyname, crypto, True, "127.0.0.1",
                self.com_name, self.certificate)

        if result.type == 1:
            self.certificate = result.certificate
            self.authToken = self.headers['X-Line-Access'] = result.authToken

            self.startSession()
            return self._client

        elif result.type == 2:
            result = "require QR code"
            self.raise_error(result)

        elif result.type == 3:
            self.headers['X-Line-Access'] = result.verifier
            self._pinCode = result.pinCode

            print("PINCODE:  {}".format(self._pinCode))

            j = self.get_json(self.CERT_URL)
            self.verifier = j['result']['verifier']

            result = self._client.loginWithVerifierForCertificate(self.verifier)

            if result.type == 1:

                if result.certificate is not None:
                    with open(self.email+".crt",'w') as f:
                        f.write(result.certificate)
                    self.certificate = result.certificate

                if result.authToken is not None:
                    self.authToken = self.headers['X-Line-Access'] = result.authToken

                    self.startSession()
                    return self._client

                else:
                    return False
            else:
                raise Exception("ERROR: LOGIN FAILED")
        else:
            self.authToken = self.headers['X-Line-Access'] = result.authToken

            self.startSession()
            return self._client

    def tokenLogin(self):

        self._client  = SessionManager(self.EXEC_URL, self.headers).TalkSession(isopen=False)

        self.startSession()
        return self._client

    def getQrCode(self):

        self._client  = SessionManager(self.LOGIN_URL, self.headers).TalkSession(isopen=False)

        msg = self._client.getAuthQrcode(True, self.com_name)
        self.vr = msg.verifier

        return self.vr

    def urlLogin(self, vr):

        self.headers['X-Line-Access'] = vr

        j = self.get_json(self.CERT_URL)
        self.verifier = j['result']['verifier']

        msg = self._client.loginWithVerifierForCertificate(self.verifier)
        if msg.type == 1:
            if msg.certificate is not None:
                self.certificate = msg.certificate
            if msg.authToken is not None:
                self.authToken = self.headers['X-Line-Access'] = msg.authToken

            self.startSession()
            return self._client

        else:
            raise Exception("ERROR: LOGIN FAILED")

    def getLastOpRevision(self):
        return self._client_in.getLastOpRevision()

    def logout(self):
        """セッションを破棄する"""

        return self._client.logoutSession(self.authToken)

    def startSession(self):
        self._client = SessionManager(self.EXEC_URL, self.headers).TalkSession()
        self._client_in = SessionManager(self.POLL_URL, self.headers).TalkSession()
        self._client_ch = SessionManager(self.EXEC_URL, self.headers).ChannelSession()
        self._client_cl = SessionManager(self.EXEC_URL, self.headers).CallSession()
        self.revision = self._client_in.getLastOpRevision()

    def get_json(self, url):
        """Get josn from given url with saved session and headers"""
        return json.loads(self._session.get(url, headers=self.headers).text)
