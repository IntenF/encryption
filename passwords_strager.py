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
    '''ログをリセットします。完全に消去するため注意が必要です'''
    with open(log_file, 'wb') as f:
        encryption = pandas.DataFrame(columns=['password', 'solt', 'iv'])
        pickle.dump(encryption, f)
    with open(log_file, 'rb') as f:
        encryption = pickle.load(f)

def write_pass(name, password, solt, iv):
    '''ログにパスワードを記録します
        name 項目名(隠しません)
        password　パスワード（暗号化して記録します）
        solt ソルト（パスワードへの辞書攻撃を防ぎます）
        iv CBCモードの暗号化に必要な初期化ベクトル
    '''
    global encryption, pass_words
    secret_key = hashlib.sha256(solt + pass_words.encode('utf-8')).digest()  # ハッシュ化された
    aes = AES.new(secret_key, AES.MODE_CBC, iv)
    encryption_data = aes.encrypt(pad(password))
    newone = pandas.DataFrame([[encryption_data, solt, iv]], index=[name], columns=['password', 'solt', 'iv'])
    encryption = encryption.append(newone)
    with open(log_file, 'wb') as f:
        pickle.dump(encryption, f)

def set_pass():
    '''パスワードを入力をもとにセットします
    :return:　なし
    '''
    name = input('項目名を入力してください')
    password = input("項目に対するパスワードを入力してください")
    solt = secrets.token_bytes(32)
    iv = os.urandom(16)
    write_pass(name, password, solt, iv)

def del_pass(name):
    global encryption
    if name not in encryption.index:
        print('{}という項目名はありません'.format(name))
        return
    encryption = encryption.drop(name)
    return

def read_pass(name):
    '''
    ログからパスワードを読み込みます
    :param name:項目名
    :return: パスワード（UTF8）
    '''
    global encryption, pass_words
    encryption_data, solt, iv = encryption.ix[name]
    secret_key = hashlib.sha256(solt + pass_words.encode('utf-8')).digest()
    aes = AES.new(secret_key, AES.MODE_CBC, iv)
    return depad(aes.decrypt(encryption_data).decode('utf-8'))

def view_pass():
    '''
    パスワードを対話的なIFで表示します
    :return: なし
    '''
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
            print(name+'\n',read_pass(name))

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

    cmdstring = 'パスワード閲覧ですか？入力ですか？削除ですか？(view(v)/set(s)/delete(d))\n終了するときは"exit,リセットは"reset",マスタパスワードを入れなおす"repass"\n:'
    cmd = input(cmdstring)
    while cmd != 'exit':
        if cmd == 'set' or cmd == 's':
            set_pass()
        elif cmd == 'view' or cmd == 'v':
            view_pass()
        elif cmd == 'delete' or cmd == 'd':
            name = input('項目名をいれてください\n:')
            del_pass(name)
        elif cmd == 'reset':
            if input('記録していたすべての情報が消えます。\n本当によろしいですか？(y/n):') == 'y':
                reset_log()
        elif cmd == 'repass':
            pass_words = input("パスワードを入力してください")
        cmd = input(cmdstring)
