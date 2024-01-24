import requests
import base64
from time import sleep
import tqdm

def crypt(if_de=True):
    normal_key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' + '0123456789' + '=.+-_/'
    cipher_key = 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm' + '0123456789' + '=.+-_/'
    if if_de:
        return {k: v for k, v in zip(cipher_key, normal_key)}
    return {v: k for k, v in zip(cipher_key, normal_key)}

def encrypt(plain_text):
    encrypt_dictionary = crypt(if_de=False)
    _cipher_text = base64.b64encode(plain_text.encode()).decode()
    return ''.join(list(map(lambda k: encrypt_dictionary[k], _cipher_text)))

def decrypt(cipher_text):
    _ciphertext = ''.join(list(map(lambda k: crypt()[k], cipher_text)))
    return base64.b64decode(_ciphertext).decode()


    

def cytranslate(content): 
    
        headers = {
            'authority': 'api.interpreter.caiyunai.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'app-name': 'xy',
            'cache-control': 'no-cache',
            'content-type': 'application/json;charset=UTF-8',
            'device-id': '',
            'origin': 'https://fanyi.caiyunapp.com',
            'os-type': 'web',
            'os-version': '',
            'pragma': 'no-cache',
            'referer': 'https://fanyi.caiyunapp.com/',
            'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
            'x-authorization': 'token:qgemv4jr1y38jyq6vhvi',
        }

        json_data = {
            'browser_id': 'beba19f9d7f10c74c98334c9e8afcd34',
        }
        requests.options('https://api.interpreter.caiyunai.com/v1/user/jwt/generate', headers=headers, json=json_data)
        jwt=requests.post('https://api.interpreter.caiyunai.com/v1/user/jwt/generate', headers=headers, json=json_data).json()['jwt']

        headers = {
            'authority': 'api.interpreter.caiyunai.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'app-name': 'xy',
            'cache-control': 'no-cache',
            'content-type': 'application/json;charset=UTF-8',
            'device-id': '',
            'origin': 'https://fanyi.caiyunapp.com',
            'os-type': 'web',
            'os-version': '',
            'pragma': 'no-cache',
            'referer': 'https://fanyi.caiyunapp.com/',
            'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            't-authorization': jwt,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
            'x-authorization': 'token:qgemv4jr1y38jyq6vhvi',
        }

        json_data = {
            'source': content,
            'trans_type': 'ja2zh',
            'request_id': 'web_fanyi',
            'media': 'text',
            'os_type': 'web',
            'dict': True,
            'cached': True,
            'replaced': True,
            'detect': True,
            'browser_id': 'beba19f9d7f10c74c98334c9e8afcd34',
        }
        requests.options('https://api.interpreter.caiyunai.com/v1/translator', headers=headers, json=json_data)
        response = requests.post('https://api.interpreter.caiyunai.com/v1/translator', headers=headers, json=json_data)
        
        result=response.json()['target']
        if type(result)==str:
            return decrypt(result)
        elif type(result)==list:
            return list(map(lambda x:decrypt(x),result))


def batch_translate(content_list,num_per_batch=100):
    result=[]
    for i in (tqdm.tqdm(range(0,len(content_list),num_per_batch))):
        result+=cytranslate(content_list[i:i+num_per_batch])
        sleep(1)
    return result
