from dataloader import *

#flip = input("Please put a number 0-1 for different files. 0 is Glass Joe, 1 is Doc Louis: ")
#flip = int(flip)

flip = 0

if flip == 0:
    total_data = wem_opener("example_data/SuperMachoMan.txt")
    total_bnk = bnk_opener("example_data/SuperMachoMan.txt")
else:
    total_data = wem_opener("example_data/DocLewis.txt")
    total_bnk = bnk_opener("example_data/DocLewis.txt")

retrieve_categories(total_data, total_bnk)
