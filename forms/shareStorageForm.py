#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urwid
class shareStorageForm():

    def show_form(self):

        # 共享磁盘
        shareDisk = urwid.Edit(("bold", "共享磁盘:      "), multiline=False, edit_pos=0, wrap='space')
        cssShareDisk = urwid.AttrMap(shareDisk, 'reverse')
        shareDiskEdit = urwid.Columns([(50, cssShareDisk)])

        #换行分隔符
        div = urwid.Divider()

        # 共享目录
        shareDir = urwid.Edit(("bold", "共享目录:      "), multiline=False, edit_pos=0, wrap='space')
        cssshareDir = urwid.AttrMap(shareDir, 'reverse')
        shareDirEdit = urwid.Columns([(50, cssshareDir)])

        # button
        save = urwid.Button("保存")
        cancel = urwid.Button("取消")
        urwid.connect_signal(save, 'click', self.on_save_clicked)
        urwid.connect_signal(cancel, 'click', self.on_cancel_clicked)

        pile = urwid.Pile([
            shareDiskEdit,
            div,
            shareDirEdit,
            div,
            shareDirEdit,
            save,
            cancel
        ])
        return urwid.Filler(pile)

    def on_cancel_clicked(self, button):
        raise urwid.ExitMainLoop()

    def on_save_clicked(self, button):
        print("保存成功")
