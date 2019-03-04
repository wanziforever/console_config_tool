#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urwid
import socket, fcntl, struct
import re
from IPy import IP
from Database import Database

class HighgoButton(urwid.Button):
    button_left = urwid.Text('[')
    button_right = urwid.Text(']')


def hg_button(*args, **kwargs):
    b = HighgoButton(*args, **kwargs)
    b = urwid.AttrMap(b, '', 'highlight')
    b = urwid.Padding(b, left=1, right=1)
    return b

'''
显示当前网卡信息，动态读取并展示，用户可以点击保存。

首次打开，动态读取的数据会自动写入数据库。第一条记录为public，后面的所有记录为private

如果数据库中有记录，不会再次写入数据库，只会根据动态读取数据进行显示，第一条为Public，后面的为Private。用户修改点击保存后，才会录入数据库。
'''
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
        # setup db connection
        sqlite = Database()
        # check if there is record in db or not. if number of records is 0, then insert. otherwise update the existing records
        sql = 'delete from networkinfo'
        sqlite.executeDB(sql)
        i = 0
        for item, value in self.networkInfo.items():
            if self.radioButtonPub[i].state == True:
                sql = 'insert into networkinfo (networkName, subnet, networkType) values ("' + (str)(item) + \
                          '", "' + (str)(value) + \
                          '", "'+'Public")'
            else:
                sql = 'insert into networkinfo (networkName, subnet, networkType) values ("' + (str)(item) + \
                      '", "' + (str)(value) + \
                      '", "' + 'Private")'
            sqlite.executeDB(sql)
        sqlite.closeConn()

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
        self.typeGroup = [[], [], [], [], [], [], [], [], [], []]  # 最多10组
        empty = urwid.Text(" ")  # 设置空行，美化页面配置

        # setup db connection
        sqlite = Database()
        i = 0
        for item, value in self.networkInfo.items():
            if i == 0:
                sql = 'insert into networkinfo (networkName, subnet, networkType) values ("' + (str)(item) + \
                        '", "' + (str)(value) + \
                        '", "Public")'
            else:
                sql = 'insert into networkinfo (networkName, subnet, networkType) values ("' + (str)(item) + \
                          '", "' + (str)(value) + \
                          '",  "Private")'
            i = i + 1
            sqlite.executeDB(sql)
        sqlite.closeConn()

        self.radioButtonPri = [None, None, None, None]
        self.radioButtonPub = [None, None, None, None]
        i = 0
        for item, value in self.networkInfo.items():
            if i == 0:
                self.radioButtonPub[i] = urwid.RadioButton(self.typeGroup[i], u"Public", state=True)
                self.radioButtonPri[i] = urwid.RadioButton(self.typeGroup[i], u"Private")
                rows.append(urwid.Columns([urwid.Text("网卡"+(str)(i+1)+"："+(str)(item)),
                                       urwid.Text("子网"+(str)(i+1)+"："+(str)(value)),
                                       empty,
                                       urwid.Columns([urwid.Text("*请选择类型："), self.radioButtonPub[i],
                                                      self.radioButtonPri[i]])]))
            else:
                self.radioButtonPub[i] = urwid.RadioButton(self.typeGroup[i], u"Public")
                self.radioButtonPri[i] = urwid.RadioButton(self.typeGroup[i], u"Private", state=True)
                rows.append(urwid.Columns([urwid.Text("网卡" +(str)(i+1)+"：" + (str)(item)),
                                           urwid.Text("子网" +(str)(i+1)+"："+ (str)(value)),
                                           empty,
                                           urwid.Columns([urwid.Text("*请选择类型："), self.radioButtonPub[i],
                                                          self.radioButtonPri[i]])]))
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
