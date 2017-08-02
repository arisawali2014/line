# coding: utf-8

"""
:copyright: (c) 2014 by Taehoon Kim.
:license: BSD, see LICENSE for more details.

このライブラリはTaehoon Kim氏が開発し、Sh1maが改良したライブラリです。
"""


from line import LineClient, PollManager
from LineThrift.ttypes import Message

try:
    client = LineClient(authToken="")
    print("{}: Login Success".format(client.profile.displayName))
except Exception as e:
    print(e)
fetch = PollManager(client)

def sendMessage(text, to, _from, toType=0, contentMetadata=0):

    msg = Message()

    if to[0] == "c":

        msg.to = to
        msg._from = _from
        msg.toType = 2

    elif to[0] == "u":
        msg.to = _from
        msg._from = to
        msg.toType = 0

    if contentMetadata:
        msg.contentMetadata = contentMetadata

    msg.text = text

    client.sendMessage(msg)

def RECEIVE_MESSAGE(op):

    msg = op.message
    # print(msg)
    print(
    " TO: {}\n".format(msg.to),
    "FROM: {}\n".format(msg._from),
    "TEXT: {}\n".format(msg.text),
    "CONTENT TYPE: {}\n".format(msg.contentType),
    "METADATA: {}\n".format(msg.contentMetadata),
    "TYPE: {}\n".format(msg.toType),
    "MESSAGE ID: {}\n".format(msg.id),
    "DATE: {}\n\n".format(msg.createdTime)
    )

    if msg.contentType != 0:
        pass

    else:
        text = msg.text
        to = msg.to
        _from = msg._from

        sendMessage(msg.text, to, _from)

fetch.addFunction(26, RECEIVE_MESSAGE)

while True:

    fetch.start()
