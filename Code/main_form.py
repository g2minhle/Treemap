import win_form
import button
import label
import stdlib
import media
import systemIO
import display_unit
import key_handler


class MainForm(win_form.WinForm):

    def __init__(self, path):
        '''(MainForm, string) -> NoneType

        Construct the main form

        self : the form
        path : the path of the folder
        '''

        win_form.WinForm.__init__(self, stdlib.Point(1024, 650))
        self.file_system_info = systemIO.DirectoryInfo(path)
        self.selecting = None
        self.path = ""
        self.set_up_GUI()

    def _set_up_buttons(self):
        '''(MainForm) -> NoneType

        Construct all buttons of the form

        self : the form
        '''

        button_text = ["Exit", "Refresh", "Load folder"]
        button_function = [self.halt, \
                           self.refresh, \
                           self.open_folder]
        self.buttons = []
        for i in range(0, 3):
            bt = button.Button(stdlib.Point(914 - 110 * i, 600), \
                               button_text[i])
            bt.mouse_click = button_function[i]
            self.buttons.append(bt)

    def _set_up_labels(self):
        '''(MainForm) -> NoneType

        Construct all the labels

        self : the form
        '''

        self.lb_start_up = label.Label(stdlib.Point(30, 580), "Start up : ")
        self.lb_start_up.text = "Start up : " + self.file_system_info.path
        self.lb_selected = label.Label(stdlib.Point(30, 560), "Selected : ")
        self.lb_hovering = label.Label(stdlib.Point(30, 540), "Hovering : ")

    def _set_up_key_handler(self):
        '''(MainForm) -> NoneType

        Construct the key handler of the form

        self : the form
        '''

        self.key_handler = key_handler.KeyHandler()
        self.key_handler.key_handle = self.key

    def _set_up_map(self):
        '''(MainForm) -> NoneType

        Construct the map of the form

        self : the form
        '''

        self.display_unit = display_unit.DisplayUnit(stdlib.Point(10, 10), \
                                                stdlib.Point(1004, 510), \
                                                self, \
                                                [self.file_system_info])
        # setup function respond for treemap
        self.display_unit.mouse_hover = self.hover
        self.display_unit.mouse_click = self.click
        self.display_unit.no_focus = self.no_focus

    def _add_controls(self):
        '''(MainForm) -> NoneType

        Add all the controls into the form

        self : the form
        '''

        for i in range(0, 3):
            self.add_control(self.buttons[i])
        self.add_control(self.lb_start_up)
        self.add_control(self.lb_selected)
        self.add_control(self.lb_hovering)
        self.add_control(self.key_handler)
        self.add_control(self.display_unit)

    def set_up_GUI(self):
        '''(MainForm) -> NoneType

        Construct all controls of the form

        self : the form
        '''

        self._set_up_buttons()
        self._set_up_labels()
        self._set_up_key_handler()
        self._set_up_map()
        self._add_controls()

    def show_dialog(self):
        '''(WinForm) -> string

        Return the path of chosen folder

        self : the form
        '''

        win_form.WinForm.show_dialog(self)
        return self.path

    def refresh(self, obj):
        '''(WinForm, list) -> NoneType

        Process when user does not hover on any display unit

        self : the form
        obj : nothing
        '''

        self.path = self.file_system_info.path
        self.close()

    def no_focus(self, obj):
        '''(WinForm, list) -> NoneType

        Process when user does not hover on any display unit

        self : the form
        obj : nothing
        '''

        self.lb_hovering.Text("Hovering : ")

    def hover(self, obj):
        '''(WinForm, list) -> NoneType

        Process when user hover mouse on a display unit

        self : the form
        obj : nothing
        '''

        if obj:
            self.lb_hovering.Text("Hovering : " + obj[0].path)

    def click(self, obj):
        '''(WinForm, list) -> NoneType

        Process when user click on a display unit

        self : the form
        obj : the selected unit
        '''

        if obj:
            self.lb_selected.Text("Selected : " + obj[0].path)
            self._deselected()
            self.selecting = obj[0].display_unit
            self._set_selected()

    def _set_selected(self):
        '''(WinForm, list) -> NoneType

        Set the newly selected item in active stage

        self : the form
        '''

        if self.selecting:
            self.selecting.border = True
            self.selecting.draw()
            self.lb_selected.Text("Selected : " +\
                                  self.selecting.file_system_info.path)

    def _deselected(self):
        '''(WinForm, list) -> NoneType

        Set the current selected item back to normal stage

        self : the form
        '''

        if self.selecting:
            self.selecting.border = False
            self.selecting.draw()

    def key(self, obj):
        '''(WinForm, list) -> NoneType

        Process key press event

        self : the form
        obj : the selected unit
        '''

        if obj and self.selecting:
            self._deselected()
            # get file info
            selecting = self.selecting.file_system_info
            # process when user press up - go up 1 level
            if obj[0] in stdlib.UP:
                # only go up when there is a parent
                if selecting.parent:
                    selecting = selecting.parent
            # process when user press down - down up 1 level
            elif obj[0] in stdlib.DOWN:
                # only go down when it is a directory
                # and it is not empty
                if selecting.typ == stdlib.DIRECTORY:
                    if selecting.size:
                        selecting = selecting.children[0]
            # process when user press right - go to next child
            elif obj[0] in stdlib.RIGHT:
                if selecting.next:
                    selecting = selecting.next
            # process when user press right - go to previous child
            elif obj[0] in stdlib.LEFT:
                if selecting.previous:
                    selecting = selecting.previous
            # get display unit
            self.selecting = selecting.display_unit
            self._set_selected()

    def halt(self, obj):
        '''(MainForm, list) -> NoneType

        Close the current form

        self : the form
        obj : nothing
        '''

        self.close()

    def open_folder(self, obj):
        '''(MainForm, list) -> NoneType

        Ask for a new folder

        self : the form
        obj : nothing
        '''

        folder_name = media.choose_folder()
        if folder_name:
            self.path = folder_name
            self.close()
