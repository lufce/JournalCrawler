import requests as webs
import time

def translation_english_list(en_list):
    url = 'https://script.google.com/macros/s/AKfycbx9rvUejjOOe-v1Q-55Ex5ORIsTWKPCIztn33ykbXcZ3U2Rng/exec'
    
    ja_list = []

    for en in en_list:
        time.sleep(1)
        res = webs.post(url, data={'value':en})

        if res.status_code == 200:
            ja_list.append(res.text)
        else:
            ja_list.append('translation failed. status_code:{}'.format(res.status_code))
    
    return ja_list
        