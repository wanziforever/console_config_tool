#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urwid
import socket, fcntl, struct
import re
from IPy import IP
from Database import Database
'''
显示当前网卡信息，读取数据库信息并展示，用户可以点击保存。
'''
class networkInfoForm():
    current_page = 1
    total_item_count = 1

    # 下一页
    def next(self, button):
        if (self.current_page + 1) >= self.total_item_count:
            self.current_page = self.total_item_count
        else:
            self.current_page = self.current_page + 1
        self.show_current_row_data()

    # 上一页
    def previous(self, button):
        if (self.current_page - 1) <= 1:
            self.current_page = 1
        else:
            self.current_page = self.current_page - 1
        self.show_current_row_data()

    # 首页
    def first(self, button):
        self.current_page = 1
        self.show_current_row_data()

    # 最后一页
    def last(self, button):
        self.current_page = self.total_item_count
        self.show_current_row_data()

    def show_current_row_data(self):
        self.tip.set_text(["当前是第",
                           ("redfont", str(self.current_page)),
                           "条记录，一共",
                           ("redfont", str(self.total_item_count)),
                           '条记录，点击"上一条"、"下一条"浏览更多记录'])
        self.txtnetworkName.set_text("网卡:    " + (str)(self.datarows[self.current_page - 1][0]))
        self.txtsubnet.set_text("子网:    " + (str)(self.datarows[self.current_page - 1][1]))
        self.txtnetworktype.set_text("类型:    " + (str)(self.datarows[self.current_page - 1][2]))

    def cancel(self,button):
        raise urwid.ExitMainLoop()

    def show_form(self):

        # 标题配置
        title = urwid.Text(('title', u"网卡信息配置表单（只读信息）"), 'center', 'any')
        div = urwid.Divider()

        # get the existing information
        sqlite = Database()
        self.datarows = sqlite.readDB("select networkName, subnet, networkType from networkinfo")
        sqlite.closeConn()
        self.total_item_count = len (self.datarows)

        self.tip = urwid.Text(["当前是第",
                               ("redfont", str(self.current_page)),
                               "条记录，一共",
                               ("redfont", str(self.total_item_count)),
                               '条记录，点击"上一条"、"下一条"浏览更多记录'])
        self.txtnetworkName = urwid.Text("网卡:    " + (str)(self.datarows[0][0]))
        self.txtsubnet = urwid.Text("子网:    " + (str)(self.datarows[0][1]))
        self.txtnetworktype = urwid.Text("类型:    " + (str)(self.datarows[0][2]))


        prebtn = urwid.Button("上一条")
        nextbtn = urwid.Button("下一条")
        cancelbtn = urwid.Button("取消")
        lastbtn = urwid.Button("最后一页")
        firstbtn = urwid.Button("第一页")
        urwid.connect_signal(prebtn, 'click', self.previous)
        urwid.connect_signal(nextbtn, 'click', self.next)
        urwid.connect_signal(lastbtn, 'click', self.last)
        urwid.connect_signal(firstbtn, 'click', self.first)
        urwid.connect_signal(cancelbtn, 'click', self.cancel)
        empty = urwid.Text(" ")
        btns = urwid.GridFlow ([prebtn, nextbtn, cancelbtn],10,1,1,"left")

        pile = urwid.Pile([title,
                           div,
                           self.tip,
                           div,
                           self.txtnetworkName,
                           self.txtsubnet,
                           self.txtnetworktype,
                           div,
                           btns])
        return urwid.Filler(pile)
