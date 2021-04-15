import time
from smsactivateru import Sms, SmsTypes, SmsService, GetBalance, GetFreeSlots, GetNumber, SetStatus, GetStatus
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time
"""
create wrapper with secret api-keysearch here: http://sms-activate.ru/index.php?act=profile)
"""
wrapper = Sms('59f99Af3754fd7c9b5dA932840473d0A')

# getting balance
balance = GetBalance().request(wrapper)
# show balance
print('На счету {} руб.'.format(balance))

# getting free slots (count available phone numbers for each services)
available_phones = GetFreeSlots(
        country=SmsTypes.Country.UA
).request(wrapper)
# show for vk.com, whatsapp and youla.io)
print('Telegram: {} номеров'.format(available_phones.Telegram.count))

# try get phone for youla.io
activation = GetNumber(
        service=SmsService().Telegram,
        country=SmsTypes.Country.UA,
        #operator=SmsTypes.Operator.Beeline
).request(wrapper)



print('id: {} phone: {}'.format(str(activation.id), str(activation.phone_number)))

# getting and show current activation status
response = GetStatus(id=activation.id).request(wrapper)
print(response)
tel2 = open("tel2.txt","w")
tel2.write(activation.phone_number)
tel2.close()


cpass = configparser.RawConfigParser()

api = open("API.txt","r")
api_id = api.read()
api.close()
hash = open("hash.txt","r")
api_hash = hash.read()
hash.close()
tel2 = open("tel2.txt","r")
phone = tel2.read()
tel2.close()
rar = open("tel2.txt", "r")
dad = rar.read()
rar.close()
tg = open('Aka-TG-Soft/' + dad + '.json', 'w', encoding='UTF-8')
tg.write('{"session_file": "'+ dad + '", "phone": "' + dad + '", "register_time": 1593619313, "app_id": 21724, "app_hash": "3e0cb5efcd52300aec5994fdfc5bdc16", "sdk": "4.3 Jelly Bean MR2 (18)", "app_version": "0.20.4.786-armeabi-v7a", "device": "Realme 2", "lang_pack": "en", "success_registred": true, "proxy": [2, "127.0.0.1", 9158, true, null, null], "first_name": "Anonimus", "last_name": "", "last_check_time": 0, "deleted": false, "ipv6": false, "username": "Anonimus", "avatar": ""}')
tg.close()
tg.close()
client = TelegramClient(phone, api_id, api_hash)

client.connect()

client.is_user_authorized()
client.send_code_request(phone)

user_action = input('Press enter if you sms was sent or type "cancel": ')
if user_action == 'cancel':
        set_as_cancel = SetStatus(                id=activation.id,
                status=SmsTypes.Status.Cancel
        ).request(wrapper)
        print(set_as_cancel)
        exit(1)

# set current activation status as SmsSent (code was sent to phone)
set_as_sent = SetStatus(
        id=activation.id,
        status=SmsTypes.Status.SmsSent
).request(wrapper)
print(set_as_sent)

# .. wait code
while True:
        time.sleep(1)
        response = GetStatus(id=activation.id).request(wrapper)
        if response['code']:
                print('Your code:{}'.format(response['code']))
                break

# set current activation status as End (you got code and it was right)
set_as_end = SetStatus(
        id=activation.id,
        status=SmsTypes.Status.End).request(wrapper)
print(set_as_end)


client.sign_in(phone, input('[+] введите код из смс: '))
client.disconnect()
rar = open("tel2.txt", "r")
dad = rar.read()
rar.close()
os.replace(dad + '.session', 'Aka-TG-Soft/' + dad + '.session')

restart_program()