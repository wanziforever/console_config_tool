#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urwid
import time
from Database import Database

class dbUserConfigForm():

    def show_form(self):

        # 超级用户输入框
        self.dbUser = urwid.Edit(("bold", "超级用户:      "), multiline=False, edit_pos=0, wrap='space')
        cssdbuser = urwid.AttrMap(self.dbUser, 'reverse')
        dbUserEdit = urwid.Columns([(50, cssdbuser)])

        #换行分隔符
        div = urwid.Divider()

        # 用户密码输入框
        self.dbPasswd = urwid.Edit(("bold", "用户密码:      "), multiline=False, edit_pos=0, wrap='space')
        cssbPasswd = urwid.AttrMap(self.dbPasswd, 'reverse')
        dbPasswdEdit = urwid.Columns([(50, cssbPasswd)])

        # 确认密码输入框
        self.dbPasswdConfirm = urwid.Edit(("bold", "确认密码:      "), multiline=False, edit_pos=0, wrap='space')
        cssDbPasswdConfirm = urwid.AttrMap(self.dbPasswdConfirm, 'reverse')
        cssDbPasswdConfirmEdit = urwid.Columns([(50, cssDbPasswdConfirm)])

        # 流复制用户名
        self.repUser = urwid.Edit(("bold", "流复制用户名:  "), multiline=False, edit_pos=0, wrap='space')
        cssrepUser = urwid.AttrMap(self.repUser, 'reverse')
        repUserEdit = urwid.Columns([(50, cssrepUser)])

        # 用户密码输入框
        self.repUserPasswd = urwid.Edit(("bold", "用户密码:      "), multiline=False, edit_pos=0, wrap='space')
        cssrepUserPasswd = urwid.AttrMap(self.repUserPasswd, 'reverse')
        repUserPasswdEdit = urwid.Columns([(50, cssrepUserPasswd)])

        # 确认密码输入框
        self.repUserPasswdConfirm = urwid.Edit(("bold", "确认密码:      "), multiline=False, edit_pos=0, wrap='space')
        cssrepUserPasswdConfirm = urwid.AttrMap(self.repUserPasswdConfirm, 'reverse')
        repUserPasswdConfirmEdit = urwid.Columns([(50, cssrepUserPasswdConfirm)])

        self.get_db_record()

        # button
        save = urwid.Button("保存")
        cancel = urwid.Button("取消")
        urwid.connect_signal(save, 'click', self.on_save_clicked)
        urwid.connect_signal(cancel, 'click', self.on_cancel_clicked)

        pile = urwid.Pile([
            dbUserEdit,
            div,
            dbPasswdEdit,
            cssDbPasswdConfirmEdit,
            div,
            repUserEdit,
            div,
            repUserPasswdEdit,
            repUserPasswdConfirmEdit,
            save,
            cancel
        ])
        return urwid.Filler(pile)

    def on_cancel_clicked(self, button):
        raise urwid.ExitMainLoop()

    def on_save_clicked(self, button):
        # setup db connection
        sqlite = Database()

        # check if there is record in db or not. if number of records is 0, then insert. otherwise update the existing records
        counter = sqlite.readDB("select count(*) from dbconfig")
        if (counter[0][0] == 0 or counter[0][0] > 1):
            print("！！！！！！！！！！！数据异常！！！！！！！！！！！！！")
            return
        else:
            sql = 'update dbconfig set userName ="' + self.dbUser.get_edit_text() \
                  + '", passwd ="' + self.dbPasswd.get_edit_text() \
                  + '", repUserName = "' + self.repUser.get_edit_text() \
                  + '",repPasswd ="'+ self.repUserPasswd.get_edit_text() \
                  +'", time = "' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '"'
        sqlite.executeDB(sql)
        sqlite.closeConn()
        print("保存成功!=======" + sql)



    def get_db_record(self):
        sqlite = Database()
        sql = "select userName,passwd,repUserName,repPasswd from dbconfig limit 0,1"
        datarows = sqlite.readDB(sql)
        self.dbUser.set_edit_text(""+str(datarows[0][0]))
        self.dbPasswd.set_edit_text(""+str(datarows[0][1]))
        self.dbPasswdConfirm.set_edit_text(""+str(datarows[0][1]))
        self.repUser.set_edit_text(""+str(datarows[0][2]))
        self.repUserPasswd.set_edit_text(""+str(datarows[0][3]))
        self.repUserPasswdConfirm.set_edit_text(""+str(datarows[0][3]))
        sqlite.closeConn()