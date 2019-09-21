#!/usr/bin/python
# -*- coding: utf-8 -*-

import ssl
import socket



if __name__ == '__main__':

    ctx = ssl.create_default_context()
    sock = ctx.wrap_socket(socket.socket(),server_hostname="games.wanmei.com")
    sock.connect(("games.wanmei.com",443))
    cert = sock.getpeercert()

    print cert







