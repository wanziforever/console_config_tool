#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from menumgr import parse_menu_document
from console import Console

# main start
if __name__ == "__main__":
    menumgr = parse_menu_document("menu.xml")
    menumgr.build()
    #menumgr.show_path_info()
 
    menu_model = menumgr.get_menu_model()
    form_model = menumgr.get_form_model()
    
    purog_console = Console()
    purog_console.set_menu_model(menu_model)
    purog_console.set_form_model(form_model)
    purog_console.startup()

