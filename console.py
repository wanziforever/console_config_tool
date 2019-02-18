#!/usr/bin/env python
# encoding: utf-8

"""
handle the main console constructor and rendering. the whole console will
draw a layout frame, including the toppest header, lowest footer, and the body
in the middle, body part will have a main window and a main interactor.
the main window is used to show the menu and form, main window is a simple
place holder with nothing actuall widget, and console logic will control
when to show menu or to show form by replacing the placeholder's original_widget
main interactor is mainly controled by user, parsing the user input and do
layout or console level work, including the menu/form switch, menu navigation.

the menus and forms navigation will use a path algorithom, the menu manager will
build a console model for menu and form information including all the item with
path information like following:
1: submenu aaaa
2: submenu bbb
1.1: form cccc
1.2: form dddd

so the path is the string concated with the index and '.', each time, user
input a index, an switcher will record it and make new a new path base on
the path which currerntly is located in. for exmaple, if you are in the submenu
aaaa, you currently will see the sub items form cccc, and form dddd, and your
current path is '1', when user enter 2, a new path '1.2' will be generated
and user will navigated to form 1.2 dddd. now the form dddd view will in front
of you.
"""

import urwid as uw
from log import log

class MenuView(uw.ListBox):
    """show menu item information in the menu view
    
    :type rows: list of tuple
    :param rows: member is a tuple (index, menu_title_text)
    """
    def __init__(self, rows):
        body = uw.SimpleListWalker(self._wrap_rows(rows))
        super(MenuView, self).__init__(body)

    def _wrap_rows(self, rows):
        """the text cannot directly add to listbox, use Text widget wrap
        :type rows: list of tuple
        :param rows: member is a tuple (index, menu_title_text)
        """
        return [uw.Text("%-3s%s" % (str(index)+".", txt)) for index, txt in rows]

    def change_items(self, rows):
        """change the menu content which is showed on the console
        urwid.Text list cannot directly add to listbox, use
        simpleListWalker wrap

        :type rows: list of tuple
        :param rows: member is a tuple (index, menu_title_text)
        """
        self.body = uw.SimpleListWalker(self._wrap_rows(rows))
        

class MenuViewControler(object):
    """menu view controler, normally the content of the menu change is
    triggered by a key press by user navigation operation. provide a do
    method to accept the uplevel controler command and do view navigation
    """
    def __init__(self, model):
        self._view = None
        self._model = model

    def get_view(self):
        if self._view is not None:
            return self._view

        return self._view

    def do(self, path):
        menu = self._model.find_by_path(path)
        if menu is None:
            return False
        rows = [(index, item.get_title()) for index, item in menu.get_items()]
        if not self._view:
            self._view = MenuView(rows)
        else:
            self._view.change_items(rows)
        return True


class FormViewControler(object):
    """form view controler, mainly use to cordinate the form generator to
    retrieve the form base on the specified path
    """
    def __init__(self, model):
        self._view = None
        self._model = model

    def get_view(self):
        return self._view

    def do(self, path):
        form = self._model.find_by_path(path)
        log(form)
        if form is None:
            return False

        self._view = form.gen_view()
        return True


class ViewSwitcher(object):
    """a status control object, control the switcher between menu view and form
    view, the switcher will consider the current status (current path located)
    and determine the next view. switcher will also in charge of generated
    new paths.
    """
    menu_upward = ['U', 'u']
    root_menu = ['', 'root']
    def __init__(self, menuctl, formctl):
        self._current_path = ''
        self._menuctl = menuctl
        self._formctl = formctl

    def startup_view(self):
        self._current_path = path = 'root'
        self._menuctl.do(path)
        return self._menuctl

    def do(self, cmd):
        """accept the uplevel controler command"""
        path = ""
        if cmd in self.menu_upward:
            if self._current_path not in self.root_menu:
                tokens = self._current_path.split(".")
                if len(tokens) <= 1:
                    path = "root"
                else:
                    path = ".".join(tokens[-1])
                
        else:
            if self._current_path in self.root_menu:
                path = cmd
            else:
                path = self._current_path + "." + cmd
        
        if self._menuctl.do(path):
            self._current_path = path
            return self._menuctl

        if self._formctl.do(path):
            self._current_path = path
            return self._formctl

        return None


class MainPanelControler(object):
    """main panel view control, use view switcher to determine which view
    to show, manager the main panel widget.
    """
    def __init__(self, main_panel, menuctl, formctl):
        self._main_panel = main_panel
        self._viewswitcher = ViewSwitcher(menuctl, formctl)
        self._current_ctl = None

    def switch_view(self, newctl):
        if newctl is None:
            return
        if newctl == self._current_ctl:
            return
        self._current_ctl = newctl
        self._main_panel.original_widget = newctl.get_view()

    def do(self, cmd):
        newctl = self._viewswitcher.do(cmd)
        self.switch_view(newctl)

    def get_view(self):
        return self._main_panel

    def startup_view(self):
        ctl = self._viewswitcher.startup_view()
        self.switch_view(ctl)


class ConsoleControler(object):
    """top level controler, accept the user key press, and transfer comamnd
    to every sub controlers
    """
    console_exit = ['Q', 'q']
    
    def __init__(self):
        self._mainctl = None

    def set_main_panel_controler(self, ctl):
        self._mainctl = ctl

    def do(self, cmd):
        if cmd in self.console_exit:
            raise uw.ExitMainLoop()
        
        if not self._mainctl.do(cmd):
            return

        # someother sub controler do one by one ...
    

def get_header():
    """frame header"""
    txt = (u'Highgo Purog瀚高集群软件V2.0 配置工具')
    return uw.Text(txt, align="center")


def get_footer():
    """frame footer"""
    txt = (u'Press u to upward, q to quit')
    return uw.Text(txt)


class MainPanel(uw.WidgetPlaceholder):
    """control how to show the form and menu"""
    def __init__(self, *args):
        super(MainPanel, self).__init__(uw.SolidFill('^'))
        
    def show_form(self, form):
        self.original_widget = form

    def show_menu(self, menu):
        """use a unified interface to set the menu with padding"""
        self.original_widget = uw.Padding(menu, left=2)

    
def get_main_panel():
    #return uw.WidgetPlaceholder(uw.SolidFill())
    #menu = get_menu(menuitems)
    return MainPanel()


class MainInteractor(uw.Edit):
    """the main interactor interface to user, handle the key press, and send
    it to top controler
    """
    def __init__(self, *args):
        self._controler = None
        super(MainInteractor, self).__init__(*args)
    
    def keypress(self, size, key):
        if key == 'enter':
            self._controler.do(self.get_edit_text())
            self.set_edit_text("")

        super(MainInteractor, self).keypress(size, key)

    def set_controler(self, control):
        self._controler = control


class Console(object):
    def __init__(self):
        self._controler = ConsoleControler()
        self._loop = None
        self._menu_model = None
        self._form_model = None
        self._menuctl = None
        self._formctl = None
        self._mainctl = None
        self._maininteractor = None
        self._frame = None

    def set_menu_model(self, model):
        self._menu_model = model

    def set_form_model(self, model):
        self._form_model = model

    def _make_layout(self):
        pile = uw.Pile(
        [
            (1, uw.SolidFill()),
            self._mainctl.get_view(),
            uw.Filler(self._maininteractor, valign="bottom"),
            ((1, uw.SolidFill('-')))

        ])
        self._frame = uw.Frame(pile, header=get_header(),
                               footer=get_footer())

    def _run(self):
        self._loop = uw.MainLoop(self._frame)
        #main.show_menu(menu)
        self._loop.run()

    def startup(self):
        """related resource creation and do assignment"""
        self._menuctl = MenuViewControler(self._menu_model)
        self._formctl = FormViewControler(self._form_model)
        self._mainctl = MainPanelControler(get_main_panel(),
                                           self._menuctl,
                                           self._formctl)
        self._maininteractor = MainInteractor("choice: ")
        self._maininteractor.set_controler(self._controler)
        self._controler.set_main_panel_controler(self._mainctl)

        self._make_layout()

        # for startup, firstly swith to menu view
        #self._mainctl.switch_view(self._menuctl)
        self._mainctl.startup_view()
        
        self._run()
        

if __name__ == "__main__":
    pass
