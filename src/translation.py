import requests as webs
import time

def translation_english_list(en_list, is_new_list):
    url = 'https://script.google.com/macros/s/AKfycbx9rvUejjOOe-v1Q-55Ex5ORIsTWKPCIztn33ykbXcZ3U2Rng/exec'
    
    ja_list = []

    for i in range(len(en_list)):
        if is_new_list[i]:
                
            time.sleep(1)
            res = webs.post(url, data={'value':en_list[i]})

            if res.status_code == 200:
                ja_list.append(res.text)
            else:
                ja_list.append('translation failed. status_code:{}'.format(res.status_code))
        
        else:
            ja_list.append('')
    
    return ja_list
        