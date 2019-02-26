#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urwid
class networkManagementForm():


    def show_form(self):

        rows = []
        # edit box with underline for installation path
        editbox = urwid.Edit(("bold", "网卡:  "), multiline=False, edit_pos=0, wrap='space')
        csseditbox = urwid.AttrMap(editbox, 'reverse')
        pathEdit=urwid.Columns([(50, csseditbox)])
        div = urwid.Divider()


        # edit box with reverse for data path
        editbox = urwid.Edit(("bold", "子网:  "), multiline=False, edit_pos=0, wrap='space')
        csseditbox2 = urwid.AttrMap(editbox, 'reverse')
        dataEdit=urwid.Columns([(50, csseditbox2)])


        # edit box for port
        editbox = urwid.Edit(("bold", "类型:  "), multiline=False, edit_pos=0, wrap='space')
        csseditbox3 = urwid.AttrMap(editbox, 'reverse')
        portEdit=urwid.Columns([(50, csseditbox3)])



        # button
        save = urwid.Button("保存")
        cancel = urwid.Button("取消")
        urwid.connect_signal(save, 'click', self.on_save_clicked)
        urwid.connect_signal(cancel, 'click', self.on_cancel_clicked)

        pile = urwid.Pile([
            pathEdit,
            div,
            dataEdit,
            div,
            portEdit,
            div,
            save,
            cancel
        ])
        return urwid.Filler(pile)




    def on_cancel_clicked(self, button):
        raise urwid.ExitMainLoop()

    def on_save_clicked(self, button):
        print("保存成功")
