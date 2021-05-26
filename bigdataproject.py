import boto3
import json
import requests
import time
from requests.auth import HTTPBasicAuth

translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

base_url = 'https://search-kuzunundiyari-b2x7id4t5ldcdm44oeewbkmesm.us-east-1.es.amazonaws.com/video/_doc/'

dir_name = "output/"
file_name = "output.json"

supported_languages = ["af", "sq", "am", "ar", "hy", "az", "bn", "bs", "bg", "ca", "zh", "zh-TW", "hr", "cs", "da", "fa-AF", "nl", "en", "et", "fa", "tl", "fi", "fr", "fr-CA", "ka", "de", "el", "gu", "ht", "ha", "he", "hi", "hu", "is", "id", "it", "ja", "kn", "kk", "ko", "lv", "lt", "mk", "ms", "ml", "mt", "mn", "no", "fa", "ps", "pl", "pt", "ro", "ru", "sr", "si", "sk", "sl", "so", "es", "es-MX", "sw", "sv", "tl", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi", "cy"]
t_data = {"af": "", "sq": "", "am": "", "ar": "", "hy": "", "az": "", "bn": "", "bs": "", "bg": "", "ca": "", "zh": "", "zh-TW": "", "hr": "", "cs": "", "da": "", "fa-AF": "", "nl": "", "en": "", "et": "", "fa": "", "tl": "", "fi": "", "fr": "", "fr-CA": "", "ka": "", "de": "", "el": "", "gu": "", "ht": "", "ha": "", "he": "", "hi": "", "hu": "", "is": "", "id": "", "it": "", "ja": "", "kn": "", "kk": "", "ko": "", "lv": "", "lt": "", "mk": "", "ms": "", "ml": "", "mt": "", "mn": "", "no": "", "fa": "", "ps": "", "pl": "", "pt": "", "ro": "", "ru": "", "sr": "", "si": "", "sk": "", "sl": "", "so": "", "es": "", "es-MX": "", "sw": "", "sv": "", "tl": "", "ta": "", "te": "", "th": "", "tr": "", "uk": "", "ur": "", "uz": "", "vi": "", "cy": ""}

translated_data = {}
source_lan = 'en'

username = "username"
password = "password"

def downloadFile ():
    s3 = boto3.client('s3')
    s3.download_file('bigdataprojectbucket', dir_name+file_name, 'downloaded.json')
    print(file_name, "File Downloaded from AWS S3")

def jsonToText ():
    file = open("downloaded.json", "r", encoding="utf-8-sig")
    dictionary = json.loads(file.read())
    print("The text of the video is: (", source_lan , ")" , str(dictionary['results']['transcripts'][0]['transcript']))
    return str(dictionary['results']['transcripts'][0]['transcript'])

def translate_text (text,s_lan, t_lan) :
    return translate.translate_text(Text=text, SourceLanguageCode=s_lan, TargetLanguageCode=t_lan)

def find_next_available():
    for n in range(100):
        url = base_url + str(n+1)
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        if not response.json()['found']:
            return url

def update_translated(obj):
    translated_data.update(obj)

def translate_all_lan(source_text):
    translated_data.update({str(source_lan): str(source_text)})
    for lan in supported_languages:
        if source_lan != lan:
            text = translate_text(source_text,source_lan,lan).get('TranslatedText')
            print("Translated lang :'", lan, "' Text is :", text)
            translated_data.update({str(lan) : str(text)})

def post_translated (url, obj):
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, headers=headers, data=json.dumps(obj), auth=HTTPBasicAuth(username, password))
    print(url)
    print(r)
    print(r.text)

def delete_given_url (url):
    r = requests.delete(url, auth=HTTPBasicAuth(username, password))
    print(r)
    print(r.text)




downloadFile()
supported_languages.remove(source_lan)

translate_all_lan(jsonToText())
post_translated(find_next_available(), translated_data)
