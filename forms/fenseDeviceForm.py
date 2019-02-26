#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urwid
class fenseDeviceForm():

    def show_form(self):

        # 节点
        node = urwid.Edit(("bold", "节点:  "), multiline=False, edit_pos=0, wrap='space')
        cssnode = urwid.AttrMap(node, 'reverse')
        nodeEdit = urwid.Columns([(50, cssnode)])

        #换行分隔符
        div = urwid.Divider()

        # IP
        ip = urwid.Edit(("bold", "IP:    "), multiline=False, edit_pos=0, wrap='space')
        cssip = urwid.AttrMap(ip, 'reverse')
        ipEdit = urwid.Columns([(50, cssip)])

        # 用户
        user = urwid.Edit(("bold", "用户:  "), multiline=False, edit_pos=0, wrap='space')
        cssuser = urwid.AttrMap(user, 'reverse')
        userEdit = urwid.Columns([(50, cssuser)])

        # 密码
        passwd = urwid.Edit(("bold", "密码:  "), multiline=False, edit_pos=0, wrap='space')
        csspasswd = urwid.AttrMap(passwd, 'reverse')
        passwdEdit = urwid.Columns([(50, csspasswd)])



        # button
        save = urwid.Button("保存")
        cancel = urwid.Button("取消")
        urwid.connect_signal(save, 'click', self.on_save_clicked)
        urwid.connect_signal(cancel, 'click', self.on_cancel_clicked)

        pile = urwid.Pile([
            nodeEdit,
            div,
            ipEdit,
            div,
            userEdit,
            div,
            passwdEdit,
            save,
            cancel
        ])
        return urwid.Filler(pile)

    def on_cancel_clicked(self, button):
        raise urwid.ExitMainLoop()

    def on_save_clicked(self, button):
        print("保存成功")
