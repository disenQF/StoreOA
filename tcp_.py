#!/usr/bin/python3
# coding: utf-8
'''
发送端 目的端

发送 接收

应用  http ftp dns smtp

表示

会话

传输 tcp udp

网络 ip icmp arp

链路 mac

物理
'''
import socket


sock = socket.socket()

sock.bind(('0.0.0.0',8080))
sock.listen(5)
while True:
    conn,addr = sock.accept()
    data = conn.recv(2048)
    print(str(data,encoding='utf-8'))
    conn.send(b'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n <h3>hello</h3>')
    conn.close()