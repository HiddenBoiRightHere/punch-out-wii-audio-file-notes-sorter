from typing import List, Tuple, Dict

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
            print("This file is missing the information required. Not all information is perfect in the notes, so try another one!")
            return None


def bnk_opener(path: str) -> List[Dict[str,str]]:
    """
    Retrieves all bnk file information if available, and places it in a list of dictionaries.
    :param path:
    :return: List of dictionaries containing ID, Name, Audio Source File, Wwise object path, and notes
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
            print("There is no BNK file information here. That's okay! It's not required.")
            return None



def retrieve_categories(total_data: List[Dict[str,str]], total_bnk: List[Dict[str,str]]):
    """
    Recieves all data from the text file and determines the kinds of categories that the audio has.
    :param total_data: List of dictionaries containing all data.
    :return: lists?
    """
    fighter_list = ["GlassJoe", "DiscoKid", "VonKaiser"]

    crowd_list = []
    sfx_list = []
    opponent_list = []
    other_list = []


    for elements in total_data:
        list_of_keys = list(elements.keys())

        file_name = elements[list_of_keys[1]]
        internal_matches = ["CROWD", "Crowd"]

        if any(x in file_name for x in internal_matches):
            crowd_list.append(elements)
        else:
            pass

    print(total_bnk)






