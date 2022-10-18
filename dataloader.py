from typing import List, Tuple, Dict
import tkinter as tk


def wem_opener(path: str) -> List[Dict[str, str]]:
    """
    Opens the file and creates something, perhaps a list of dictionaries, which can be used elsewhere to sort through
    data.
    :param path: File path string.
    :return: List of dictionaries containing ID, Name, Audio Source File, Generated Audio File, Wwise object path, and notes
    """
    #Opens file
    with open(path) as file:
        #Creates empty list to store all information from file
        holding_list: list = []
        final_list: list = []

        #For loop to traverse through file
        for elements in file:

            #Appends all elements into holding list
            holding_list.append(elements)

            #Locates index of where the important information begins
            if "Streamed Audio" in elements:
                set_index = len(holding_list)

        #begins using try except to make sure the data is in the file at all
        try:

            #Obtains keys for dictionary. While all notes are the same, this is used to account for any spelling mistakes
            #or changes made by user
            dict_keys_raw = holding_list[set_index - 1].rstrip()
            dict_keys_split = dict_keys_raw.split("\t")
            dict_keys_split.pop(0)


            #creates list of dictionaries
            for all_items in holding_list[set_index:-1]:
                #resets dictionary
                dict_template = {}

                #strips current thing
                values = all_items.strip()
                split_values = values.split("\t")

                #Creates keys each time
                for keys in dict_keys_split:
                    dict_template[keys] = ""

                #assigns values to dictionary
                for things in range(0,5):
                    dict_template[dict_keys_split[things]] = split_values[things]

                #appends dictionary into list
                final_list.append(dict_template)
            return final_list

        except:
            return None


def bnk_opener(path: str) -> List[Dict[str,str]]:
    """
    Retrieves all bnk file information if available, and places it in a list of dictionaries.
    :param path: File path string.
    :return: List of dictionaries containing ID, Name, Audio Source File, Wwise object path, and notes.
    """
    with open(path) as file:
        #Creates empty list to store all information from file
        holding_list: list = []
        final_list: list = []
        #For loop to traverse through file
        for elements in file:

            #Appends all elements into holding list
            holding_list.append(elements)

            #Locates index of where the important information begins
            if "In Memory Audio" in elements:
                set_index = len(holding_list)
            if "Streamed Audio" in elements:
                set_stop = len(holding_list)


        #begins using try except to make sure the data is in the file at all
        try:
            #Obtains keys for dictionary. While all notes are the same, this is used to account for any spelling mistakes
            #or changes made by user
            dict_keys_raw = holding_list[set_index - 1].rstrip()
            dict_keys_split = dict_keys_raw.split("\t")
            dict_keys_split.pop(0)
            dict_keys_split.pop(3)


            #creates list of dictionaries
            for all_items in holding_list[set_index:set_stop - 2]:
                #resets dictionary
                dict_template = {}

                #strips current thing
                values = all_items.strip()
                split_values = values.split("\t")
                split_values.pop(3)

                #Creates keys each time
                for keys in dict_keys_split:
                    dict_template[keys] = ""

                # assigns values to dictionary
                for things in range(0,4):
                    dict_template[dict_keys_split[things]] = split_values[things]

                # appends dictionary into list
                final_list.append(dict_template)
            return final_list
        except:
            return None



def retrieve_categories(total_data: List[Dict[str,str]], total_bnk: List[Dict[str,str]]):
    """
    Recieves all data from the text file and determines the kinds of categories that the audio has.
    :param total_data: List of dictionaries containing all data.
    :return: lists?
    """
    #Creates empty dictionaries for the bnk and wem file names
    bnk_dictionary = {}
    wem_dictionary = {}


    #if there is no data, exit the program
    if (total_data == None and total_bnk == None):
        failure = tk.Tk()
        def fail_func():
            failure.destroy()
        fail_desc = tk.Label(failure, text="There's no wem or bnk data in here! Please pick a different notes file.")
        continue_button = tk.Button(failure, text="Close", command=fail_func)
        fail_desc.pack()
        continue_button.pack()
        wem_dictionary = None
        bnk_dictionary = None

    elif(total_data != None and total_bnk == None):
        wem_dictionary = wem_notes(total_data)
        bnk_dictionary = None
    elif (total_data == None and total_bnk != None):
        wem_dictionary = None
        bnk_dictionary = bnk_notes(total_bnk)
    else:
        wem_dictionary = wem_notes(total_data)
        bnk_dictionary = bnk_notes(total_bnk)

    return wem_dictionary, bnk_dictionary


def doc_louis_notes(total_data: List[Dict[str,str]]) -> Dict[str, List[Dict[str,str]]]:
    """
    If the doc louis notes file is open, separate into per character advice, win, loss, and other.
    :param total_data:
    :return:
    """

    wem_dictionary = {}
    # creates list of all opponents
    category_list = ["Glass Joe", "Von Kaiser", "Disco Kid", "King Hippo", "Piston Hondo", "Bear Hugger", "Great Tiger",
                    "Don Flamenco", "Aran Ryan", "Soda Popinski", "Bald Bull", "Super Macho Man", "Sandman", "Donkey Kong", "Win", "Loss", "Cornerman", "Other"]
    checker_list = []
    # Creates their dictionary keys
    for fighters in category_list:
        wem_dictionary[fighters] = []

    # for each file in the notes, match each file to their respective character and place in dictionary
    for elements in total_data:
        list_of_keys = list(elements.keys())
        file_name = elements[list_of_keys[1]].lower()


        for fighters in category_list:
            name = fighters.replace(" ", "")

            if (name.lower() in file_name):
                wem_dictionary[fighters].append(elements)
                checker_list.append(elements)
                break
            else:
                pass

        if elements not in checker_list:
            wem_dictionary["Other"].append(elements)

    return wem_dictionary

def wem_notes(total_data: List[Dict[str,str]]) -> Dict[str, List[Dict[str,str]]]:
    """
    If there are wem file notes, take total wem data and determine if it is from Doc Louis. If not, categorize into four categories.
    :param total_data: All wem file data in list of dictionaries
    :return: Dictionary per category containing list of more dictionaries with further information.
    """


    #creates dictionary template
    wem_dictionary = {}

    category_list = ["Crowd", "SFX", "Cornerman", "Other"]
    check_list = []

    #create template of all category names
    for categories in category_list:
        wem_dictionary[categories] = []

    #for loop to go through total data
    for elements in total_data:
        list_of_keys = list(elements.keys())
        file_name = elements[list_of_keys[1]].lower()

        if ("doclouis" in file_name):
            wem_dictionary = doc_louis_notes(total_data)
            return wem_dictionary
        else:
            pass

        #categorizes each file name into respective list
        for categories in category_list:
            #removes any spaces in categories
            name = categories.replace(" ", "")

            if (name.lower() in file_name):
                # if the category name is in the file name, put in dictionary with category
                wem_dictionary[categories].append(elements)
                check_list.append(elements)
                break

            else:
                pass

        if elements not in check_list:
            wem_dictionary["Other"].append(elements)

    return wem_dictionary


def bnk_notes(total_bnk):
    """
    If there are bnk file notes, take total bnk data and determine if it is from Doc Louis. If not, categorize into five categories.
    :param total_bnk: All bnk file notes in one large list.
    :return: Dictionary of categories containing lists of dictionaries with further information
    """

    bnk_dictionary = {}

    category_list = ["SFX", "Reactions", "Punches", "Knockdown", "Other"]
    check_list = []

    for categories in category_list:
        bnk_dictionary[categories] = []

    #for loop to go through total data
    for elements in total_bnk:
        list_of_keys = list(elements.keys())
        file_name = elements[list_of_keys[1]].lower()

        if ("doclouis" in file_name):
            bnk_dictionary = doc_louis_notes(total_bnk)
            return bnk_dictionary
        else:
            pass

         #categorizes each file name into respective list
            for categories in category_list:

                #removes any spaces in categories
                name = categories.replace(" ", "")

                if (name.lower() in file_name):
                    # if the category name is in the file name, put in dictionary with category
                    bnk_dictionary[categories].append(elements)
                    check_list.append(elements)
                    break

                elif ("react" in file_name):
                    bnk_dictionary["Reactions"].append(elements)
                    check_list.append(elements)
                    break

                elif ("right" in file_name):
                    bnk_dictionary["Punches"].append(elements)
                    check_list.append(elements)
                    break

                elif ("left" in file_name):
                    bnk_dictionary["Punches"].append(elements)
                    check_list.append(elements)
                    break

                else:
                    pass

            if elements not in check_list:
                bnk_dictionary["Other"].append(elements)

    return bnk_dictionary

def program_directories(path: str, program_int: int):
    with open("program_directories_settings.txt", "r") as settings_file:
        settings_info = settings_file.readlines()
    with open("program_directories_settings.txt", "w") as settings_file_w:
        if (program_int == 0):
            settings_info[0] = "Foobar2000 Directory = " + path + "\n"
        elif (program_int == 1):
            settings_info[1] = "Hex Editor Directory = " + path + "\n"
        elif (program_int == 2):
            settings_info[2] = "Items Directory = " + path + "\n"

        settings_file_w.writelines(settings_info)

