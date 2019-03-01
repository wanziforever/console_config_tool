#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urwid
import socket, fcntl, struct
import re
from IPy import IP

class HighgoButton(urwid.Button):
    button_left = urwid.Text('[')
    button_right = urwid.Text(']')


def hg_button(*args, **kwargs):
    b = HighgoButton(*args, **kwargs)
    b = urwid.AttrMap(b, '', 'highlight')
    b = urwid.Padding(b, left=1, right=1)
    return b


class networkMgrForm():

    networkInfo ={}
    def getNetworkInfo(self):
        with open('/proc/net/route', 'r') as f:
            for line in f:
                m = re.match('(\S+)\s+(\S+)\s+(\S+)\s+.*', line)
                if m.group(1) != 'Iface':  # and m.group(2) != '00000000':# and m.group(3) == '00000000':
                    interface = m.group(1)
                    gateway = '.'.join([
                        str(int(m.group(3)[6:8], 16)),
                        str(int(m.group(3)[4:6], 16)),
                        str(int(m.group(3)[2:4], 16)),
                        str(int(m.group(3)[0:2], 16))
                    ])
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', interface))[20:24])
                    netmask = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s', interface))[20:24])
                    subnet = IP(ip).make_net(netmask)
                    strinterface =(str)(interface)
                    # filter all the virtual networks
                    if strinterface[0:5] != 'virbr':
                        self.networkInfo[interface] = subnet
                    # print(" interface =" + str(interface) +";ip ="+(str)(ip)+" netmask = " + (str)(netmask))


    def onSave(self):
        print ("save")

    def onCancel(self):
        print("cancel")

    def show_form(self):

        rows = []
        # 标题配置
        title = urwid.Text(('title', u"网卡信息配置"), 'center', 'any')
        rows.append(title)
        secondLevelTitle = urwid.Text(('underline', u"请选择网卡类型"), 'left', 'any')
        rows.append(secondLevelTitle)
        rows.append(urwid.Divider())

        # 获取网络信息，并将结果写入字典networkInfo中
        self.getNetworkInfo()

        # 假设最多有10组网卡信息
        typeGroup = [[], [], [], [], [], [], [], [], [], []]  # 最多10组
        empty = urwid.Text(" ")  # 设置空行，美化页面配置

        i = 0
        for item, value in self.networkInfo.items():
            if i==0:
             rows.append(urwid.Columns([urwid.Text("网卡"+(str)(i+1)+"："+(str)(item)),
                                       urwid.Text("子网"+(str)(i+1)+"："+(str)(value)),
                                       empty,
                                       urwid.Columns([urwid.Text("*请选择类型："), urwid.RadioButton(typeGroup[i], u"Public", state=True),
                                                      urwid.RadioButton(typeGroup[i], u"Private")])]))
            else:
                rows.append(urwid.Columns([urwid.Text("网卡" +(str)(i+1)+"：" + (str)(item)),
                                           urwid.Text("子网" +(str)(i+1)+"："+ (str)(value)),
                                           empty,
                                           urwid.Columns([urwid.Text("*请选择类型："), urwid.RadioButton(typeGroup[i], u"Public"),
                                                          urwid.RadioButton(typeGroup[i], u"Private", state=True)])]))
            i = i + 1

        rows.append(urwid.Divider())
        rows.append(urwid.Divider())
        rows.append(urwid.Columns([urwid.Text(" "),
                                   urwid.Text(" "),
                                   urwid.Text(" "),
                                   urwid.Text(" "),
                                   urwid.Text(" "),
                                   urwid.Text(" "),
                       hg_button('保存', on_press=self.onSave()),
                       hg_button('取消', on_press=self.onCancel()),
                       ]))

        pile = urwid.Pile(rows)
        return urwid.Filler(pile)
