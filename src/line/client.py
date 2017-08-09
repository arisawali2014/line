# coding: utf-8

"""
:copyright: (c) 2014 by Taehoon Kim.
:license: BSD, see LICENSE for more details.

このライブラリはTaehoon Kim氏が開発し、Sh1maが改良したライブラリです。
"""


import requests
from .login import LoginManager

from LineThrift.ttypes import MIDType
from LineThrift.ttypes import MediaType
from LineThrift.ttypes import ContentType
from LineThrift.ttypes import OpType

class LineClient(LoginManager):


    """
    本体です。
    client = LineClient(email, password) # email login
    or
    client = LineClient(authToken="your authToken") # token login
    or
    client = LineClient() # URL login

    authTokenの取得方法
    ログインした状態で、
    print(client.authToken)
    """

    def __init__(self, mail=None, password=None, authToken=None):

        LoginManager.__init__(self)

        if not (authToken or mail and password):
            url = self.getQrCode()
            print("AUTH URL: line://au/q/{}".format(self.getQrCode()))

            self.urlLogin(self.vr)
            self.startSession()

        if authToken:
            self.authToken = self.headers['X-Line-Access'] = authToken

            self.tokenLogin()
            self.startSession()

        if mail and password:
            self.email = mail
            self.password = password

            self.mailLogin()
            self.startSession()

        self.profile = self.getProfile()
        self.group = self.getGroupIdsJoined()


    """プロフィール関係"""

    def getProfile(self):
        """プロフィールを取得(typeはProfile)"""

        return self._client.getProfile()

    def updateProfile(self, profile, seq=0):
        """プロフィールを更新(typeはProfile)"""

        return self._client.updateProfile(seq, profile)

    def _reissueUserTicket(self, expirationTime=100, maxUseCount=100):
        """ユーザーチケットを再発行"""

        return self._client.reissueUserTicket(expirationTime,maxUseCount)


    """コンタクト関係"""

    def getAllContactIds(self):
        """全ての友達のmidを取得(list)"""

        return self._client.getAllContactIds()

    def getBlockedContactIds(self):
        """ブロックしたユーザのmidを取得(list)"""

        return self._client.getBlockedContactIds()

    def getContacts(self, ids):
        """ids引数(list)で渡したmidのユーザ情報を取得"""

        if type(ids) != list:
            raise Exception("[!]:ids引数は必ずlistで渡してください")

        return self._client.getContacts(ids)

    def getContact(self, id):
        """id引数(string)で渡したmidのユーザ情報を取得"""

        if type(id) != str:
            raise Exception("[!]:id引数は必ずstringで渡してください")

        return self._client.getContact(id)

    def findContactByUserTicket(self, ticketId):
        """ticket(ユーザurlのpath)からユーザ情報を取得する"""

        return self._client.findContactByUserTicket(ticketId)

    def findContactByUserid(self, userid):
        """ユーザidからユーザ情報を取得する"""

        return self._client.findContactByUserid(userid)

    def findAndAddContactsByMid(self, mid, seq=0):
        """midからユーザ情報を取得し、追加する"""

        return self._client.findAndAddContactsByMid(seq, mid)

    def findAndAddContactsByUserid(self, userid, seq=0):
        """ユーザidからユーザ情報を取得し、追加する"""

        return self._client.findAndAddContactsByUserid(seq, userid)

    def findContactsByPhone(self, phones):
        """電話番号からユーザ情報を取得する"""

        return self._client.findContactsByPhone(phones)

    def findAndAddContactsByPhone(self, phones, seq=0):
        """電話番号からユーザ情報を取得し、追加する"""

        return self._client.findAndAddContactsByPhone(seq, phones)

    def findContactsByEmail(self, emails):
        """メールアドレスからユーザ情報を取得する"""

        return self._client.findContactsByEmail(emails)

    def findAndAddContactsByEmail(self, emails, seq=0):
        """メールアドレスからユーザ情報を取得し、追加する"""

        return self._client.findAndAddContactsByEmail(seq, emails)


    """トークルーム関係"""

    def createRoom(self, ids, seq=0):
        """トークルームを作成する"""

        if type(ids) != list:
            raise Exception("[!]:ids引数は必ずlistで渡してください")

        return self._client.createRoom(seq, ids)

    def getRoom(self, id):
        """idからトークルームを取得する"""

        return self._client.getRoom(id)

    def inviteIntoRoom(self, roomId, contactIds=[]):
        """contactsIdsのmidのユーザをトークルームに招待する"""

        return self._client.inviteIntoRoom(0, roomId, contactIds)

    def leaveRoom(self, id):
        """idのトークルームから退出する"""

        return self._client.leaveRoom(0, id)


    """グループ関係"""

    def createGroup(self, name, ids, seq=0):
        """グループを作成"""

        return self._client.createGroup(seq, name, ids)

    def getGroups(self, ids):
        """グループを取得(list)"""

        if type(ids) != list:
            raise Exception("[!]:ids引数は必ずlistで渡してください")

        return self._client.getGroups(ids)

    def getGroup(self, groupId):
        """グループを取得(string)"""

        if type(ids) != str:
            raise Exception("[!]:ids引数は必ずstringで渡してください")

        return self._client.getGroup(groupId)

    def getGroupIdsJoined(self):
        """参加済みグループidを取得"""

        return self._client.getGroupIdsJoined()

    def getGroupIdsInvited(self):
        """招待されているグループidを取得"""

        return self._client.getGroupIdsInvited()

    def acceptGroupInvitation(self, groupId, seq=0):
        """グループに参加"""

        return self._client.acceptGroupInvitation(seq, groupId)

    def acceptGroupInvitationByTicket(self, GroupMid, ticketId, seq=0):
        """グループチケット(グループurlのパス)からグループに参加"""

        return self._client.acceptGroupInvitationByTicket(seq, GroupMid, ticketId)

    def rejectGroupInvitation(self, groupId, seq=0):
        """グループ招待を拒否"""

        return self._client.rejectGroupInvitation(seq, groupId)

    def kickoutFromGroup(self, groupId, contactIds=[], seq=0):
        """グループメンバーを退会"""

        return self._client.kickoutFromGroup(seq, groupId, contactIds)

    def cancelGroupInvitation(self, groupId, contactIds=[], seq=0):
        """グループ招待をキャンセル"""

        return self._client.cancelGroupInvitation(seq, groupId, contactIds)

    def inviteIntoGroup(self, groupId, contactIds=[], seq=0):
        """グループに招待"""

        return self._client.inviteIntoGroup(seq, groupId, contactIds)

    def leaveGroup(self, id):
        """グループを退会"""

        return self._client.leaveGroup(0, id)

    def findGroupByTicket(self, ticketId):
        """グループチケットからグループ情報を取得"""

        return self._client.findGroupByTicket(ticketId)

    def reissueGroupTicket(self, groupMid):
        """グループチケットを発行する"""

        return self._client.reissueGroupTicket(groupMid)

    def updateGroup(self, group, seq=0):
        """グループを更新(typeはGroup)"""

        return self._client.updateGroup(seq, group)


    """POLL関係"""

    def fetchOperation(self, revision, count=50):
        """operationを取得"""

        return self._client_in.fetchOperations(revision, count)

    """その他"""

    def getRecentMessages(self, id, count=1):

        return self._client.getRecentMessages(id, count)

    def sendMessage(self, message, seq=0):

        return self._client.sendMessage(seq, message)

    def issueChannelToken(self, channelId="1341209850"):

        return self._client_ch.issueChannelToken(channelId)

    def getMessageBoxCompactWrapUp(self, id):

        return self._client.getMessageBoxCompactWrapUp(id)

    def getMessageBoxCompactWrapUpList(self, start=1, count=50):

        return self._client.getMessageBoxCompactWrapUpList(start, count)

    def getSettings(self):

        return self._client.getSettings()

    def updateSettings(self, settings, seq=0):

        return self._client.updateSettings(seq, settings)

    def getGroupCall(self, ChatMid):

        return self._client_cl.getGroupCall(ChatMid)

    def acquireGroupCallRoute(self, groupId, mediaType=MediaType.AUDIO):

        return self._client_cl.acquireGroupCallRoute(groupId, mediaType)

    def post_content(self, url, data=None, files=None):
        return self._session.post(url, headers=self.headers, data=data, files=files)
