rsa.py
	RSA鍵暗号をテストするためのコード
	http://qiita.com/QUANON/items/e7b181dd08f2f0b4fdbe
	をもとに作成

passwords_strager.py
	パスワードを保存するためのロガー
	マスタパスワードでいろいろな秘密ごとを保存できます。マスタパスワードがばれない限りは今のところ誰にも解けない。
	使用暗号　AES

	必要なライブラリ
		os, pandas, pickle, hashlib, secrests, Crypto
		だいたいAnacondaに入ってます。Cryptoは"pip install pycrypto"で入れる
		
