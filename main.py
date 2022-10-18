import tkinter

from dataloader import *
from tkinter_window import *



def getFolderPathFoobar():
    """
    Gets folder path for Foobar2000 or VGMStream
    :return: None
    """
    file = filedialog.askopenfilename()
    program_directories(file, 0)


def getFolderPathHex():
    """
    Gets folder path for a hex editor.
    :return: None
    """
    file = filedialog.askopenfilename()
    program_directories(file, 1)


def getFolderPathText():
    """
    Gets folder path for the text notes to look at.
    :return: None
    """
    file = filedialog.askopenfilename(filetypes = (("Text files", "*.txt"),
        ('All files', '*.*')))
    program_directories(file, 2)


def getFolderPathTextFixer():
    """
    Gets folder path for the text notes to look at.
    :return: None
    """
    file = filedialog.askopenfilename()
    program_directories(file, 2)

def close_window():
    """
    Closes the "first time" starting window and starts main window.
    :return: None
    """
    #read directory
    with open("program_directories_settings.txt", "r") as settings:
        all_settings = settings.readlines()
        path_extra = all_settings[2]
        path_list = path_extra.split("=")
        path_raw = path_list[1]
        path = path_raw.strip()
    total_data = wem_opener(path)
    total_bnk = bnk_opener(path)
    sorted_data = retrieve_categories(total_data, total_bnk)
    set_dir.destroy()
    window_opener(sorted_data)




def opening_processing():
    """
    Starts the program.
    :return: None
    """
    with open("program_directories_settings.txt", "r") as settings:
        all_settings = settings.readlines()
        path_extra = all_settings[2]
        path_list = path_extra.split("=")
        path_raw = path_list[1]
        path = path_raw.strip()
    try:
        total_data = wem_opener(path)
        total_bnk = bnk_opener(path)
        sorted_data = retrieve_categories(total_data, total_bnk)
        window_opener(sorted_data)
    except:
        fail = tk.Tk()
        def startagain():
            """
            Sends user back through restart process with updated information.
            :return:
            """
            fail.destroy()
            opening_processing()

        message = tk.Label(text="Something is wrong with your file. Please check the program_directories_settings.txt file, the contents of your current .txt file, or select a new file using the button below.")
        message.pack()
        fix_button = tk.Button(text="Select new notes .txt file", command=getFolderPathText)
        fix_button.pack()
        continue_button = tk.Button(text="Continue", command=startagain)
        continue_button.pack()
        fail.mainloop()

# When you open the program for the first time, set the directories for Foobar2000 and a hex editor.
with open("program_directories_settings.txt", "r") as settings_file:
    settings_info = settings_file.readlines()
if settings_info[3] == "First Run = True":
    print("First time")
    settings_info[3] = "First Run = False"
    with open("program_directories_settings.txt", "w") as setter:
        setter.writelines(settings_info)
    set_dir = tk.Tk()

    foobar_button = ttk.Button(set_dir, text="Set Foobar2000/VGMStream Directory", command=getFolderPathFoobar)
    foobar_button.grid(row=0, column=2)

    hex_editor_button = ttk.Button(set_dir, text="Set Hex Editor Directory", command=getFolderPathHex)
    hex_editor_button.grid(row=1, column=2)

    set_text_button = ttk.Button(set_dir, text="Set text file to be opened.", command=getFolderPathText)
    set_text_button.grid(row=2, column=2)

    close_button = ttk.Button(set_dir, text="Continue", command=close_window)
    close_button.grid(row=3, column=2)

    set_dir.mainloop()
else:
    opening_processing()


