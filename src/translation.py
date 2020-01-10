import requests as webs
import time

def translation_en_into_ja(en_str):
    __url = 'https://script.google.com/macros/s/AKfycbx9rvUejjOOe-v1Q-55Ex5ORIsTWKPCIztn33ykbXcZ3U2Rng/exec'

    time.sleep(1)
    res = webs.post(__url, data={'value':en_str})

    if res.status_code == 200:
        return res.text
    else:
        return 'translation failed. status_code:{}'.format(res.status_code)

def translation_english_list(en_list, is_new_list):
    ja_list = []

    if isinstance(en_list, list) == False:
        buf = en_list
        
        en_list = []
        en_list.append(buf)

    for i in range(len(en_list)):
        if is_new_list[i]:
            ja_list.append( translation_en_into_ja(en_list[i]) )
        else:
            ja_list.append('')
    
    return ja_list
        