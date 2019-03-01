#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urwid
import time
from Database import Database

class dbProfileForm():

    def show_form(self):

        title =urwid.Text(('title', u"数据库信息配置"), 'center', 'any')
        #csstitle = urwid.AttrMap(title, 'chars')

        secondLevelTitle =urwid.Text(('underline', u"以下所有配置项都会作为数据库启动参数，修改参数需要重新启动数据库"), 'left', 'any')
        #csssecondLevelTitle = urwid.AttrMap(secondLevelTitle, 'chars')

        # text for installation path which was given by installation.
        self.pathdir = urwid.Text("*安装目录：")
        div = urwid.Divider()

        # edit box with reverse for data path
        self.datadir = urwid.Edit(("bold", "*数据目录:    "), multiline=False, edit_pos=0, wrap='space')
        cssdatadir = urwid.AttrMap(self.datadir, 'reverse')
        datadirEdit = urwid.Columns([(50, cssdatadir)])

        # edit box for port
        self.port = urwid.Edit(("bold", "*端口号:      "), multiline=False, edit_pos=0, wrap='space')
        cssport = urwid.AttrMap(self.port, 'reverse')
        portEdit = urwid.Columns([(50, cssport)])

        # checkBox
        self.arch_chk = urwid.CheckBox("*开启归档", False, False)

        # edit box for log
        self.log = urwid.Edit(("bold", "运行日志:     "), multiline=False, edit_pos=0, wrap='space')
        csslog = urwid.AttrMap(self.log, 'reverse')
        logEdit = urwid.Columns([(50, csslog)])

        self.get_db_record()

        # empty
        empty = urwid.Text("    ")

        # button
        save = urwid.Button("保存")
        urwid.AttrMap(save, None, focus_map='reversed')
        cancel = urwid.Button("取消")
        urwid.connect_signal(save, 'click', self.on_save_clicked)
        urwid.connect_signal(cancel, 'click', self.on_cancel_clicked)
        btns = urwid.Columns([save, cancel])

        pile = urwid.Pile([
            title,
            secondLevelTitle,
            div,
            self.pathdir,
            div,
            datadirEdit,
            div,
            portEdit,
            div,
            self.arch_chk,
            div,
            logEdit,
            btns,

        ])
        return urwid.Filler(pile)

    def on_cancel_clicked(self, button):
        raise urwid.ExitMainLoop()

    def on_save_clicked(self, button):
        # setup db connection
        sqlite = Database()

        #get the values of arch check box
        if self.arch_chk.get_state() == True:
            flag = 1
        else:
            flag = 0

        # check if there is record in db or not. if number of records is 0, then insert. otherwise update the existing records
        counter = sqlite.readDB("select count(*) from dbProfile")
        if (counter[0][0] == 0 or counter[0][0] > 1):
            print("！！！！！！！！！！！数据异常！！！！！！！！！！！！！")
            return

        else:
            sql = 'update dbProfile set dataDir ="' + self.datadir.get_edit_text() +\
                  '", portNum =' + self.port.get_edit_text() + \
                  ', archStatus = '+ str(flag) + \
                  ', logFile ="' + self.log.get_edit_text() + '"'
                  #+', time = "'+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) +'"'
        sqlite.executeDB(sql)
        sqlite.closeConn()
        print("保存成功!======="+sql)

    def get_db_record(self):
        sqlite = Database()
        sql = "select installDir,dataDir,portnum,archstatus,logFile from dbProfile limit 0,1"
        datarows = sqlite.readDB(sql)
        _dataPath = datarows[0][1]
        _logPath = datarows[0][4]

        # handle if the data is none.
        if datarows[0][1] == None:
            _dataPath = ""

        if datarows[0][4] == None:
            _logPath = ""
        self.pathdir.set_text("*安装路径：    "+str(datarows[0][0]))
        self.datadir.set_edit_text(""+str(_dataPath))
        self.port.set_edit_text(""+str(datarows[0][2]))

        if datarows[0][3] == 0:
            self.arch_chk.set_state(False)
        else:
            self.arch_chk.set_state(True)

        self.log.set_edit_text("" + str(_logPath))
        sqlite.closeConn()
