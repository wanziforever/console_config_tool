#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
handle all the form import and dynamic generation
"""

import urwid as uw
import time
import sqlite3
#import forms.dbBaseConfigForm
from forms.dbProfileForm import dbProfileForm
from forms.networkMangementForm import networkManagementForm
from forms.dbUserConfigForm import dbUserConfigForm
from forms.shareStorageForm import shareStorageForm
from forms.fenseDeviceForm import fenseDeviceForm

class Form(uw.Overlay):
    pass


def get_form(widget):
    # the background parameter uw.SolidFill(u'/') not work, don't know why!!
    return Form(widget, uw.SolidFill(u'/'),
                align="center", width=('relative', 80), valign='middle',
                height=('relative', 80), min_width=24, min_height=8,
                left=2, right=2, top=3, bottom=3)


def example_form():
    network_id = uw.Edit("network id: ")
    network_name = uw.Edit("network name: ")
    network_type = uw.Edit("type: ")
    div = uw.Divider()
    text = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    button = uw.Button(text)

    pile = uw.Pile([
        network_id,
        network_name,
        network_type,
        div,
        button
        ])

    return uw.Filler(pile)

class Form(object):
    def __init__(self, menuitem):
        self._id = menuitem.get_formid()
        self._title = menuitem.get_title()

    def gen_view(self):
        """import the view form script file and generate a form view"""
        # here just simply use an exmaple
        if self._id == "baseConfig":
            form = dbProfileForm()
            return form.show_form()

        return example_form()


