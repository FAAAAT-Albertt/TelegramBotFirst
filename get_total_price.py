import requests
import json

def get_response(path_photo, url="https://proverkacheka.com/api/v1/check/get"):

    data={'token':'23750.yyZn5yRLlXQwzZRet'}
    files = {'qrfile': open(f'{path_photo}','rb')}
    res = requests.post(url, data=data, files=files).json()

    return res
