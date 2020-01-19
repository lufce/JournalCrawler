import requests as webs

accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
accept_enc = 'gzip, deflate, br'
accept_lang = 'ja,en-US;q=0.9,en;q=0.8,pt;q=0.7'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
hds = {'Accept':accept,'Accept-Encoding':accept_enc,'Accept-Language':accept_lang,'User-Agent': ua}

r = webs.get('https://httpbin.org/headers', headers = hds)
print(r.text)