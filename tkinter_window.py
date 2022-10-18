from typing import Tuple, List, Dict
import tkinter as tk
from tkinter import ttk, filedialog
from dataloader import *
import os
import subprocess

def window_opener(total_data_tuple: Tuple[Dict[str,List[Dict[str,str]]]]):
    """
    Takes all information and organizes it into a window GUI
    :param total_data_tuple: Contains all the sorted data for both BNK and WEM files.
    :return: Window/None
    """

    def getFolderPathFoobar():
        file = filedialog.askopenfilename()
        program_directories(file, 0)

    def getFolderPathHex():
        file = filedialog.askopenfilename()
        program_directories(file, 1)

    def getFolderPathText():
        file = filedialog.askopenfilename(filetypes = (("Text files", "*.txt"),
        ('All files', '*.*')))
        program_directories(file, 2)
        with open("program_directories_settings.txt", "r") as settings:
            all_settings = settings.readlines()
            path_extra = all_settings[2]
            path_list = path_extra.split("=")
            path_raw = path_list[1]
            path = path_raw.strip()
        total_data = wem_opener(path)
        total_bnk = bnk_opener(path)
        sorted_data = retrieve_categories(total_data, total_bnk)
        main_window.destroy()
        window_opener(sorted_data)


    #Separates wem and bnk data from tuple
    total_wem_data = total_data_tuple[0]
    total_bnk_data = total_data_tuple[1]

    #Gets categories for each form of data if they exist
    if (total_wem_data == None and total_bnk_data == None):
        category_selections_wem = ["Empty."]
        category_selections_bnk = ["Empty."]
    elif (total_wem_data == None):
        category_selections_bnk = list(total_bnk_data.keys())
        category_selections_wem = ["Empty."]

    elif(total_bnk_data == None):
        category_selections_wem = list(total_wem_data.keys())
        category_selections_bnk = ["Empty."]

    else:
        category_selections_wem = list(total_wem_data.keys())

        category_selections_bnk = list(total_bnk_data.keys())





    # TODO =====> Creates Window <===== ===== #
    main_window = tk.Tk()
    main_window.geometry("800x600")
    main_window.minsize(800,600)
    main_window.maxsize(800, 600)
    main_window.configure(bg="dark gray")

    # TODO =====> Creates Top Label <===== ===== #
    audio_sorter_name = tk.Label(main_window, text="HiddenBoi's Audio Sorter and Converter for Punch-Out!! Wii", font=("Arial", 20), bg="dark grey")
    audio_sorter_name.pack(side="top", pady=10)

    informational_label = tk.Label(main_window, text="Please ensure that your .wav and .bnk files are in the same directory as the notes files you are looking through, or else your files will not play or open properly.", wraplength=800, font=["Arial", 13], bg="dark grey")
    informational_label.pack(side="top", pady=10)

    # TODO =====> Frames <===== ===== #
    left_frame = tk.Frame(main_window, height=500, width=475)
    left_frame.propagate(False)
    left_frame.pack(side="left", expand=True, padx=20, pady=10)

    right_frame = tk.Frame(main_window, bg="pink", height=500, width=225)
    right_frame.propagate(False)
    right_frame.pack(side="right", expand=True, padx=20, pady=10)



    def direct_set():
        """
        Opens file in foobar2000.
        :return: None
        """
        with open("program_directories_settings.txt", "r") as direct:
            lines = direct.readlines()
            chosen = lines[0]
            chosen_list = chosen.split("=")
            directory_foo = chosen_list[1].strip()
            dir_cont = lines[2]
            dir_cont_list = dir_cont.split("=")
            dir_cont_list_further = dir_cont_list[1].strip()
            dir_cont_last_split = dir_cont_list_further.split("/")
            dir_cont_last_split.pop(-1)
            directory_content =  "/".join(dir_cont_last_split)

        if (notebook_parent.index("current") == 0):
            fileName = file_list_box.get("active")
            selected_index = category_selections_wem.index(selected.get())
            for files in total_wem_data[category_selections_wem[selected_index]]:
                if fileName in files["Name"]:
                    ext = files["Generated audio file"]
                    ext_save = ext.split(".")
                    ext_save[1] = "wem"
                    extension = ".".join(ext_save)
                    final_dir = directory_content + "/" + extension
                else:
                    pass
            subprocess.Popen([directory_foo, final_dir])

        else:
            renamer = dir_cont_list_further.split(".")
            renamer[1] = "bnk"
            final_dir = ".".join(renamer)
            subprocess.Popen([directory_foo, final_dir])


    def hex_opener():
        """
        Opens file in HxD or other hex editor
        :return: None
        """
        with open("program_directories_settings.txt", "r") as direct:
            lines = direct.readlines()
            chosen = lines[1]
            chosen_list = chosen.split("=")
            directory_hex = chosen_list[1].strip()
            dir_cont = lines[2]
            dir_cont_list = dir_cont.split("=")
            dir_cont_list_further = dir_cont_list[1].strip()
            dir_cont_last_split = dir_cont_list_further.split("/")
            dir_cont_last_split.pop(-1)
            directory_content =  "/".join(dir_cont_last_split)

        if (notebook_parent.index("current") == 0):
            fileName = file_list_box.get("active")
            selected_index = category_selections_wem.index(selected.get())
            for files in total_wem_data[category_selections_wem[selected_index]]:
                if fileName in files["Name"]:
                    ext = files["Generated audio file"]
                    ext_save = ext.split(".")
                    ext_save[1] = "wem"
                    extension = ".".join(ext_save)
                    final_dir = directory_content + "/" + extension
                else:
                    pass
            subprocess.Popen([directory_hex, final_dir])

        else:
            renamer = dir_cont_list_further.split(".")
            renamer[1] = "bnk"
            final_dir = ".".join(renamer)
            subprocess.Popen([directory_hex, final_dir])


    def replace_Dsp():
        print("replace the dsp")



    play_foobar = tk.Button(right_frame, text="Play file in Foobar2000/VGMStream", height=3, width=35, command=direct_set)
    open_in_hex = tk.Button(right_frame, text="Open in a Hex Editor", height=3, width=35, command=hex_opener)
    replace_dsp = tk.Button(right_frame, text="Replace DSP", height=3, width=35, command=replace_Dsp)

    open_in_hex.pack(side="bottom")
    replace_dsp.pack(side="bottom")
    play_foobar.pack(side="bottom")





    # TODO =====> Menu <===== ===== #
    #Menu containing opbtions for user to pick from if they want to change their program directories
    variable = "Options"
    #Create menubar
    menubar = tk.Menu(main_window)


    #Create menu
    # create a menubar
    menubar = tk.Menu(main_window)
    main_window.config(menu = menubar)

    # create a menu
    file_menu = tk.Menu(menubar, tearoff = False)

    # add a menu item to the menu
    file_menu.add_command(label = "Change Foobar2000 Directory", command=getFolderPathFoobar)
    file_menu.add_command(label = "Change Hex Editor Directory", command=getFolderPathHex)
    file_menu.add_command(label = "Change Text File", command=getFolderPathText)

    # add the File menu to the menubar
    menubar.add_cascade(label = "Options", menu = file_menu)




    # TODO =====> Tabs/Notebook <===== ===== #

    #Tabs for bnk vs wem (notebook)
    notebook_parent = ttk.Notebook(left_frame)

    #Creates tabs
    tab1 = ttk.Frame(notebook_parent)
    tab2 = ttk.Frame(notebook_parent)

    notebook_parent.add(tab1, text="WEM Files")
    notebook_parent.add(tab2, text="BNK Files")


    # TODO =====> Listboxes to select categories <===== ===== #
    file_list_box = tk.Listbox(tab1, height=30, width=75, selectmode="single")
    file_list_box_bnk = tk.Listbox(tab2, height=30, width=75, selectmode="single")

    # TODO =====> File Information in Frames WEM <===== ===== #

    def on_field_change(index, value, op):
        """
        Updates wem listbox depending on selected category.
        :param index:
        :param value:
        :param op:
        :return:
        """
        file_list_box.config(state="normal")
        file_list_box.delete(0, "end")
        selected_index = category_selections_wem.index(selected.get())
        for files in total_wem_data[category_selections_wem[selected_index]]:
            file_list_box.insert("end", files["Name"])
        if total_wem_data[category_selections_wem[selected_index]] == []:
            file_list_box.insert("end", "There are no files in this category! Please select another one.")
            file_list_box.config(state="disabled")
    def on_field_change_bnk(index, value, op):
        """
        Updates bnk listbox depending on selected category.
        :param index:
        :param value:
        :param op:
        :return:
        """
        file_list_box_bnk.config(state="normal")
        file_list_box_bnk.delete(0, "end")
        try:
            selected_index = category_selections_bnk.index(selected_bnk.get())
            for files in total_bnk_data[category_selections_bnk[selected_index]]:
                file_list_box_bnk.insert("end", files["Name"])
            if total_bnk_data[category_selections_bnk[selected_index]] == []:
                file_list_box_bnk.insert("end", "There are no files in this category! Please select another one.")
                file_list_box_bnk.config(state="disabled")
        except:
            file_list_box_bnk.insert("end", "That category does not exist!")
            file_list_box_bnk.config(state="disabled")



    #Keep track of changes for wem
    selected = tk.StringVar()
    selected.trace("w", on_field_change)

    #keep track of chagnes for bnk
    selected_bnk = tk.StringVar()
    selected_bnk.trace("w", on_field_change_bnk)


    #Combobox/dropdown
    category_box = ttk.Combobox(tab1, values=category_selections_wem, width=20, textvariable=selected, )
    category_box.set(category_selections_wem[0])

    category_box_bnk = ttk.Combobox(tab2, values=category_selections_bnk, width=20, textvariable=selected_bnk)
    category_box_bnk.set(category_selections_bnk[0])

    # TODO =====> File Information WEM <===== ===== #
    def onselect(evt):
        """
        Changes information on right side showing info about selected text file.
        :param evt: Change in selection
        :return: None
        """
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        try:
            #Gets index of current selection in listbox
            index = int(w.curselection()[0])

            #Collects specific info but makes variables shorter because I named them very long
            category_index = category_selections_wem.index(selected.get())
            dict_text = total_wem_data[category_selections_wem[category_index]]
            get_info = dict_text[index]

            #get list of keys
            keys_in_info = list(get_info.keys())
            text_display = ""

            #Creates text to be displayed
            for keys in keys_in_info:
                text_key = str(keys)
                text_value = str(get_info[keys])
                text_display = text_display + text_key + ": \n" + text_value + "\n" + "\n"

            #updates text box
            file_information["state"] = "normal"
            file_information.delete(0.0, "end")
            file_information.insert(0.0, f"{text_display}")
            file_information["state"] = "disabled"

        except:
            pass

    file_list_box.bind('<<ListboxSelect>>', onselect)



    # TODO =====> File Information BNK <===== ===== #
    def onselect_bnk(evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        try:
            #Gets index of current selection in listbox
            index = int(w.curselection()[0])

            #Collects specific info but makes variables shorter because I named them very long
            category_index = category_selections_bnk.index(selected_bnk.get())
            dict_text = total_bnk_data[category_selections_bnk[category_index]]
            get_info = dict_text[index]

            #get list of keys
            keys_in_info = list(get_info.keys())
            text_display = ""

            #Creates text to be displayed
            for keys in keys_in_info:
                text_key = str(keys)
                text_value = str(get_info[keys])
                text_display = text_display + text_key + ": " + text_value + "\n" + "\n"

            #updates text box
            file_information["state"] = "normal"
            file_information.delete(0.0, "end")
            file_information.insert(0.0, f"{text_display}")
            file_information["state"] = "disabled"

        except:
            pass

    file_list_box_bnk.bind('<<ListboxSelect>>', onselect_bnk)

    file_information = tk.Text(right_frame, height=20, state="disabled")

    # TODO =====> Packing All Items <===== ===== #
    #pack locations
    category_box.pack(side="top", anchor="nw")
    category_box_bnk.pack(side="top", anchor="nw")

    #scrollbar.pack(side="right")
    file_list_box.pack(anchor="nw")
    file_list_box_bnk.pack(anchor="nw")

    notebook_parent.pack(expand=1, fill="both")

    file_information.pack(side="top")

    #Main window loop
    main_window.mainloop()

