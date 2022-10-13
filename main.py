from dataloader import *

flip = 0

if flip == 0:
    total_data = wem_opener("example_data/Glass_Joe.txt")
    total_bnk = bnk_opener("example_data/Glass_Joe.txt")
else:
    total_data = wem_opener("example_data/DocLewis.txt")
    total_bnk = bnk_opener("example_data/DocLewis.txt")

retrieve_categories(total_data, total_bnk)