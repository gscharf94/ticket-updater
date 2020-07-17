import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


def sendMail(files):
	fromAddr = 'scharfgustavo@gmail.com'
	toAddr = 'ggarza@fiber1communications.com, fiber1communications@gmail.com, cesar@fiber1communications.com, nrodriguez@fiber1communications.com, octavio@fiber1communications.com'

	msg = MIMEMultipart()

	date = datetime.today().strftime('%m-%d-%y')

	msg['From'] = fromAddr
	msg['To'] = toAddr
	msg['Subject'] = f'{date} Open Work Orders Report'


	body = 'All, \n\nPlease find reports attached.\n\nRegards,\n\nGustavo'

	msg.attach(MIMEText(body,'plain'))
	for file in files:
		print(f'Attaching {file}')
		filename = file
		attachment = open(filename,'rb')

		fileIndex = filename.find('2020')
		fileName = filename[fileIndex:]
		p = MIMEBase('application','octet-stream',name=fileName)
		p.set_payload((attachment).read())
		encoders.encode_base64(p)


		p.add_header('Content-Disposition','attachment; filename=%s' %fileName)
		msg.attach(p)

	s = smtplib.SMTP('smtp.gmail.com',587)
	s.starttls()
	s.login('scharfgustavo@gmail.com','hvqwfdvnknampggk')
	text = msg.as_string()
	toList = ['ggarza@fiber1communications.com','fiber1communications@gmail.com','cesar@fiber1communications.com','piticlin87.nr@gmail.com','octavio@fiber1communications.com','nrodriguez@fiber1communications.com']
	s.sendmail('scharfgustavo@gmail.com',toList,text)
	s.quit()


