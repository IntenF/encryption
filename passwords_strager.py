# encoding utf-8

import os
import hashlib
import pandas
import secrets
from Crypto.Cipher import AES

import pickle

pass_words = ""#input("パスワードを入力してください")
log_file = 'pass.log'

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
depad = lambda s: s[:-ord(s[-1])]

def reset_log():
    with open(log_file, 'wb') as f:
        encryption = pandas.DataFrame(columns=['password', 'solt', 'iv'])
        pickle.dump(encryption, f)
    with open(log_file, 'rb') as f:
        encryption = pickle.load(f)

def set_pass():
    global encryption, pass_words
    name = input('項目名を入力してください')
    password = input("項目に対するパスワードを入力してください")
    solt = secrets.token_bytes(32)
    iv = os.urandom(16)
    secret_key = hashlib.sha256(solt + pass_words.encode('utf-8')).digest() #ハッシュ化された
    aes = AES.new(secret_key, AES.MODE_CBC, iv)
    encryption_data = aes.encrypt(pad(password))
    newone = pandas.DataFrame([[encryption_data, solt, iv]], index=[name], columns=['password', 'solt', 'iv'])
    encryption= encryption.append(newone)
    with open(log_file, 'wb') as f:
        pickle.dump(encryption, f)

def view_pass():
    global encryption, pass_words
    print('パスワード閲覧モード：\n\t項目名を指定してパスワードが見れます\n\tやめるには"exit"\t項目名表示:"view"')
    while True:
        name = input('\t:')
        if name == 'exit':
            break
        elif name == 'view':
            ind = [x for x in encryption.index]
            print('\t',ind)
        elif name not in encryption.index:
            print('\t{}という項目はありません'.format(name))
        else:
            encryption_data, solt, iv = encryption.ix[name]
            secret_key = hashlib.sha256(solt + pass_words.encode('utf-8')).digest()
            aes = AES.new(secret_key, AES.MODE_CBC, iv)
            print(name+'\n',depad(aes.decrypt(encryption_data).decode('utf-8')))


    #項目名のリストを出力


if __name__ == '__main__':
    pass_words = input("マスタパスワードを入力してください")
    import os.path
    if os.path.isfile(log_file) == False:
        with open(log_file, 'wb') as f:
            encryption = pandas.DataFrame(columns=['password', 'solt', 'iv'])
            pickle.dump(encryption, f)
        print('はじめての使用ですね。新しくログファイルを生成しました。')
    with open(log_file, 'rb') as f:
        encryption = pickle.load(f)

    cmdstring = 'パスワード閲覧ですか？入力ですか？(view(v)/set(s))\n終了するときは"exit,リセットは"reset",マスタパスワードを入れなおす"repass"\n:'
    cmd = input(cmdstring)
    while cmd != 'exit':
        if cmd == 'set' or cmd == 's':
            set_pass()
        elif cmd == 'view' or cmd == 'v':
            view_pass()
        elif cmd == 'reset':
            if input('記録していたすべての情報が消えます。\n本当によろしいですか？(y/n):') == 'y':
                reset_log()
        elif cmd == 'repass':
            pass_words = input("パスワードを入力してください")
        cmd = input(cmdstring)
