from browser import getDict, handler, getWorkOrderTitles 
from spreadsheet import createSpreadsheet, addTitles
from sendMail import sendMail
from logger import append_to_file, success_file


import time, datetime
import pickle
import os

dateToday = datetime.date.today()

start_time = time.time()

sysPATH = "C:\\Users\\Gustavo\\Documents\\Programming Stuff\\ticketupdater\\"
picklePath1 = sysPATH+"pickleDumps\\workOrderTickets\\w"+str(dateToday)+".p"
picklePath2 = sysPATH+"pickleDumps\\workOrderResponses\\r"+str(dateToday)+".p"
picklePath3 = sysPATH+"pickleDumps\\workOrderTitles\\t"+str(dateToday)+".p"
picklePath4 = sysPATH+"pickleDumps\\workOrderMetadata\\m"+str(dateToday)+".p"
excelPath = sysPATH+"excelDumps\\"+str(dateToday)+" "+time.strftime("%a %I%p.xlsx")

copyInto = "C:\\Users\\Gustavo\\Documents\\Programming Stuff\\tickethelper\\pickle_dump\\"
homeCopyInto = "C:\\Users\\Gustavo\\Documents\\Programming Stuff\\tickethelper\\"

# vv this is for testing

# workOrderTickets = pickle.load(open(picklePath1,'rb'))
# titleDict = pickle.load(open(picklePath3, 'rb'))


# VV this is what usually should be turned on

append_to_file(f'Starting program date: {dateToday}',"SRT")
append_to_file('Resetting success file','SRT')
success_file(False)

append_to_file('Getting work order information','SRT')

workOrderTickets, titleDict = getDict()
pickle.dump(workOrderTickets,open(picklePath1,'wb'))
pickle.dump(titleDict, open(picklePath3, 'wb'))

pickle.dump(workOrderTickets,open(copyInto + f'w{str(dateToday)}.p','wb'))
pickle.dump(titleDict, open(copyInto + f't{str(dateToday)}.p', 'wb'))

append_to_file('Saved work order information','GUD')

workOrderResponses = {}

for workOrder in workOrderTickets:
	workOrderResponses[workOrder] = {}
	for ticket in workOrderTickets[workOrder]:
		workOrderResponses[workOrder][ticket] = []

# vv this is for testing
# workOrderResponses = pickle.load(open(picklePath2,'rb'))
# metadata = pickle.load(open(picklePath3, 'rb'))

# VV this is what usually should be turned on

append_to_file('Getting response information','SRT')


def trim_dict(dicty, n):
	# allows you to test with lower num of tickets
	new_dict = {}
	for x, key in enumerate(dicty):
		if x > n:
			break
		new_dict[key] = dicty[key]
	return new_dict



ticket_data = handler(workOrderResponses)
workOrderResponses = ticket_data[0]
metadata = ticket_data[1]

pickle.dump(workOrderResponses,open(picklePath2,'wb'))
pickle.dump(workOrderResponses,open(copyInto + f'r{str(dateToday)}.p', 'wb'))

pickle.dump(metadata,open(picklePath4,'wb'))
pickle.dump(metadata,open(copyInto+f'm{str(dateToday)}.p','wb'))

append_to_file('Saved response information','GUD')


append_to_file('Creating spreadsheets','SRT')
# these need to be merged
fileNames = createSpreadsheet(workOrderResponses,excelPath,titleDict)
for file in fileNames:
    	# excelPath = sysPATH+"excelDumps\\"+file
	addTitles(titleDict,file)
append_to_file('Spreadsheets created','GUD')


append_to_file('Starting email sending','SRT')
sendMail(fileNames)

append_to_file('Emails sent out','GUD')

end_time = time.time()

time_elapsed = end_time - start_time
append_to_file('FINISHED SUCCESFULLY','GUD')
append_to_file(f'Time elapsed: {round(time_elapsed/60,2)}m: {round(time_elapsed%60,2)}s','---')

time_update_path = homeCopyInto + 'last_update.txt'

with open(time_update_path,'w+') as f:
	new_date = datetime.datetime.today()
	day = str(new_date.day).zfill(2)
	mon = str(new_date.month).zfill(2)
	hour = str(new_date.hour).zfill(2)
	min = str(new_date.minute).zfill(2)

	message = f"{mon}-{day} {hour}:{min}"
	f.write(message)

# here we run the script that updates website
append_to_file('Pushing to heroku','PSH')
os.chdir("C:\\Users\\Gustavo\\Documents\\Programming Stuff\\tickethelper\\")
os.system('update.bat')
append_to_file('Finished. Hopefully it compiles','PSH')
success_file(True)