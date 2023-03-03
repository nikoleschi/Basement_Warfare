import os
import tkinter
import tkinter.filedialog
import mimetypes


def prompt_file(initial_dir):
    dialog = tkinter.Tk()
    dialog.withdraw()
    file_name = tkinter.filedialog.askopenfilename(parent=dialog, initialdir=initial_dir)
    dialog.destroy()
    return file_name


def get_file_type(file_path):
    return mimetypes.guess_type(file_path)[0]


def get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


def get_dirname(file_path):
    return os.path.dirname(file_path)


def get_current_directory():
    return os.getcwd()
