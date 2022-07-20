import os 
import pandas as pd
from GRIN2B_constants import br_animal_IDs

def reformat_brainstate_file(folder_path, file_name, save_path, save_file_as):
    os.chdir(folder_path)
    br_file = pd.read_csv(file_name)
    len_br = len(br_file)*5
    start_column = list(range(0, len_br, 5))
    end_column = list(range(5, (len_br +5), 5))
    br_file['start_epoch'] = start_column
    br_file['end_epoch'] = end_column
    br_file.columns = br_file.columns.str.replace('sleep.score', 'brainstate')
    os.chdir(save_path)
    br_file.to_pickle(save_file_as + '.pkl')
    print('file saved as ' + save_file_as)

folder_path_br = '/home/melissa/preprocessing/GRIN2B/GRIN2B_raw_brainstates'
save_path_br = '/home/melissa/preprocessing/GRIN2B/GRIN2B_numpy'



for animal in br_animal_IDs:
    file_name_start = 'GRIN2B_' + animal + '_BL3-dge_ok.csv'
    save_as_br = animal + '_BL3' 
    reformat_brainstate_file(folder_path=folder_path_br, file_name = file_name_start, save_path = save_path_br, save_file_as= save_as_br)

