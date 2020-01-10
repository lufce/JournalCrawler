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

def translation_english_list(en_list, is_new_list=None):
    ja_list = []

    #if en_list is not list but a single string, make new en_list containing the one string.
    if isinstance(en_list, str) == True:
        buf = en_list
        
        en_list = []
        en_list.append(buf)

    #if is_new_list is not given, all sentences in en_list are translated.
    if is_new_list is None:
        is_new_list = []
        for i in range(len(en_list)):    
            is_new_list.append(True)

    for i in range(len(en_list)):
        if is_new_list[i]:
            print(i)
            ja_list.append( translation_en_into_ja(en_list[i]) )
        else:
            ja_list.append('')
    
    return ja_list
        