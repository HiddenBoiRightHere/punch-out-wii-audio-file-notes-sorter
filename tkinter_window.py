from typing import Tuple, List, Dict
import tkinter as tk
from tkinter import ttk

def window_opener(total_data_tuple: Tuple[Dict[str,List[Dict[str,str]]]]):
    """
    makes window of alllll data
    :param total_data_tuple:
    :return: window
    """

    #Separates wem and bnk data from tuple
    total_wem_data = total_data_tuple[0]
    total_bnk_data = total_data_tuple[1]

    #Gets categories for each form of data if they exist
    if (total_wem_data == None):
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
    main_window.configure(bg="dark gray")

    # TODO =====> Creates Top Label <===== ===== #
    audio_sorter_name = tk.Label(main_window, text="HiddenBoi's Audio Sorter and Converter for Punch-Out!! Wii", font=("Arial", 15), bg="dark grey")
    audio_sorter_name.pack(side="top", pady=10)

    # TODO =====> Frames <===== ===== #
    left_frame = tk.Frame(main_window, height=500, width=475)
    left_frame.propagate(False)
    left_frame.pack(side="left", expand=True, padx=20, pady=10)

    right_frame = tk.Frame(main_window, bg="pink", height=500, width=225)
    right_frame.propagate(False)
    right_frame.pack(side="right", expand=True, padx=20, pady=10)


    # TODO =====> File Information and Conversion Buttons <===== ===== #
    file_information = tk.Label(right_frame, text="This is your file information")
    file_information.pack(side="top")



    play_foobar = tk.Button(right_frame, text="Play file in Foobar2000/VGMStream", height=3, width=35)
    open_in_hex = tk.Button(right_frame, text="Open in a Hex Editor", height=3, width=35)
    replace_dsp = tk.Button(right_frame, text="Replace DSP", height=3, width=35)

    play_foobar.pack(side="bottom")
    open_in_hex.pack(side="bottom")
    replace_dsp.pack(side="bottom")



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
    file_menu.add_command(label = "Change Foobar2000 Directory")
    file_menu.add_command(label = "Change VGAudio Directory")
    file_menu.add_command(label = "Change DSP Converter Directory")
    file_menu.add_command(label = "Change Hex Editor Directory")

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

    # TODO =====> Combobox <===== ===== #
    #Combobox/dropdown
    category_box = ttk.Combobox(tab1, values=category_selections_wem, width=20)
    category_box.set(category_selections_wem[0])




    # TODO =====> BNK Combobox <===== ===== #
    category_box_bnk = ttk.Combobox(tab2, values=category_selections_bnk, width=20)
    category_box_bnk.set(category_selections_bnk[0])

    # TODO =====> File Information in Frames WEM <===== ===== #

    file_list_box = tk.Listbox(tab1, height=30, width = 75)
    for files in total_wem_data[category_selections_wem[0]]:
            file_list_box.insert("end", files["Name"])




    # TODO =====> Scrollbar <===== ===== #
    #Scrollbar
    scrollbar = tk.Scrollbar(master=tab1, width=15)




    # TODO =====> Packing All Items <===== ===== #
    #pack locations


    category_box.pack(side="top", anchor="nw")
    category_box_bnk.pack(side="top", anchor="nw")

    #scrollbar.pack(side="right")
    file_list_box.pack(anchor="nw")

    notebook_parent.pack(expand=1, fill="both")


    #Main window loop
    main_window.mainloop()

