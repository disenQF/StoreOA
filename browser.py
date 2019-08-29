#!/usr/bin/python3
# coding: utf-8

import socket

browser = socket.socket()
browser.connect(('www.baidu.com', 80))

# 发送请求
browser.send(b'GET / HTTP/1.1\r\nHost:www.baidu.com\r\nUser-Agent:IE10\r\n\r\n')

# 接收响应数据
msg = browser.recv(2048)
print(msg.decode(encoding='utf-8'))