#-*- encoding: utf-8 -*-
# @author 852802020@qq.com

import os, sys
import smtplib
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

class MailService(object):
	__mailInfo = {
		'from': '852802020@qq.com',
		'hostname': 'smtp.qq.com',
		'username': '852802020@qq.com',
		'password': '*********',#qq 授权码，使用前开启stmp等协议
		'mailsubject': 'Score Notification',
		'mailencoding': 'utf-8'
	}
	
	def __init__(self, email_Number, email_context):
		self.email_number = email_Number
		self.email_context = email_context
	
	def sendMail(self):
		flag = True
		try:
			smtp = SMTP_SSL(MailService.__mailInfo['hostname'])
			#smtp.ehlo(mailInfo['hostname'])
			smtp.login(MailService.__mailInfo['username'], MailService.__mailInfo['password'])	 
			msg = MIMEText(self.email_context, 'plain', MailService.__mailInfo['mailencoding'])
			msg['Subject'] = Header(MailService.__mailInfo['mailsubject'], MailService.__mailInfo['mailencoding'])
			msg['from'] = MailService.__mailInfo['from']
			msg['to'] = ';'.join(self.email_number)
			smtp.sendmail(MailService.__mailInfo['from'], self.email_number, msg.as_string())
			smtp.quit()
		except Exception:
			flag =False
		return flag

if __name__ == '__main__':
	mailCustomer = MailService(['3489325642@qq.com'], 'bingo...')
	if mailCustomer.sendMail():
		pass