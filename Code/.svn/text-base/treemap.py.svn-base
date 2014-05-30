import main_form
import media
import stdlib
# i decide to present only the files so, if there is an empty folder, it will
# be a small line on the map.
# please read the help file (help.txt) for more information

def get_start_up_open_folder():
    '''()-> string

    Return the path of chosen folder
    '''

    folder_name = media.choose_folder()
    path = folder_name
    return path

if __name__ == "__main__":

    # show opening dialog
    path = get_start_up_open_folder()
    # if there is a chosen folder
    while path:
        # start the GUI
        main = main_form.MainForm(path)
        path = main.show_dialog()
