from typing import Tuple, List, Dict
import tkinter as tk

def window_opener(total_data_tuple: Tuple[Dict[str,List[Dict[str,str]]]]):
    """
    makes window of alllll data
    :param total_data_tuple:
    :return: window
    """
    main_window = tk.Tk()

    main_window.mainloop()