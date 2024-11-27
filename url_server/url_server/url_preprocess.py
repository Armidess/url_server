import re
import joblib
import pandas as pd
from urllib.parse import urlparse
import os

def fd_length(url):
    urlpath= urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0

def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits

def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters

def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')

def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        return -1
    else:
        return 1

def shortening_service(url):
    match = re.search(r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      r'tr\.im|link\.zip\.net',
                      url)
    if match:
        return -1
    else:
        return 1
    




def pre_process(urldata):
    
    urldata['url_length'] = urldata['url'].apply(lambda i: len(str(i)))
    urldata['hostname_length'] = urldata['url'].apply(lambda i: len(urlparse(i).netloc))
    urldata['path_length'] = urldata['url'].apply(lambda i: len(urlparse(i).path))
    urldata['fd_length'] = urldata['url'].apply(lambda i: fd_length(i))
    urldata['count-'] = urldata['url'].apply(lambda i: i.count('-'))
    urldata['count@'] = urldata['url'].apply(lambda i: i.count('@'))
    urldata['count?'] = urldata['url'].apply(lambda i: i.count('?'))
    urldata['count%'] = urldata['url'].apply(lambda i: i.count('%'))
    urldata['count.'] = urldata['url'].apply(lambda i: i.count('.'))
    urldata['count='] = urldata['url'].apply(lambda i: i.count('='))
    urldata['count-http'] = urldata['url'].apply(lambda i : i.count('http'))
    urldata['count-https'] = urldata['url'].apply(lambda i : i.count('https'))
    urldata['count-www'] = urldata['url'].apply(lambda i: i.count('www'))
    urldata['count-digits']= urldata['url'].apply(lambda i: digit_count(i))
    urldata['count-letters']= urldata['url'].apply(lambda i: letter_count(i))
    urldata['count_dir'] = urldata['url'].apply(lambda i: no_of_dir(i))
    urldata['use_of_ip'] = urldata['url'].apply(lambda i: having_ip_address(i))
    urldata['short_url'] = urldata['url'].apply(lambda i: shortening_service(i))
    
    return urldata

current_directory = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_directory, 'Malicious URL Trained Model')
loaded_model = joblib.load(model_path)
# print(f"Model path: {model_path}")

def check_url(url: str) -> bool:
    # print("1")
    urldata = pd.DataFrame({'url': [url]})
    # print("2")
    urldata = pre_process(urldata)

    # print("3")
    x = urldata[['hostname_length','path_length', 'fd_length', 'count-', 'count@', 'count?','count%', 'count.',
             'count=', 'count-http','count-https', 'count-www', 'count-digits','count-letters', 'count_dir',
             'use_of_ip']]
    # print("4")
    # print(url)
    prediction = loaded_model.predict(x)
    # print("5")
    # print(prediction)
    return prediction
