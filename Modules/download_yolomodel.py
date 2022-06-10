import os
import pathlib
import logging

def attempt_download_weigth(local_weights_path):

    weigth_name = os.path.basename(local_weights_path)
    
    if not (os.path.exists(local_weights_path) and os.path.getsize(local_weights_path) > 1E6):  # weights exist and > 1MB
        logging.debug('Yolo weigth %s dont found. Downloading...',weigth_name)
        url = 'https://pjreddie.com/media/files/' + weigth_name
        logging.debug('Downloading ' + url)
        logging.debug('curl -f ' + url + ' -o ' + local_weights_path)
        r = os.system('curl -f ' + url + ' -o ' + local_weights_path)
        # Error check
        if not (r == 0 and os.path.exists(local_weights_path) and os.path.getsize(local_weights_path) > 1E6):  # weights exist and > 1MB
            os.system('rm ' + local_weights_path)

def attempt_download_cfg(local_cfg_path):

    cfg_name = os.path.basename(local_cfg_path)
    
    if not (os.path.exists(local_cfg_path)):  # cfg exist and > 1MB
        logging.debug('Yolo cfg %s dont found. Downloading...',cfg_name)
        url = 'https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/' + cfg_name
        logging.debug('Downloading ' + url)
        logging.debug('curl -LJO -f ' + url + ' -o ' + local_cfg_path)
        r = os.system('curl -f ' + url + ' -o ' + local_cfg_path)
        # Error check
        if not (r == 0 and os.path.exists(local_cfg_path)):  # cfg exist and > 1MB
            os.system('rm ' + local_cfg_path)