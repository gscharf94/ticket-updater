from browser import getDict, handler, getWorkOrderTitles 
from spreadsheet import createSpreadsheet, addTitles
from sendMail import sendMail
import time, datetime
import pickle


dateToday = datetime.date.today()

sysPATH = "C:\\Users\\Gustavo\\Documents\\Programming Stuff\\ticketupdater\\"
picklePath1 = sysPATH+"pickleDumps\\workOrderTickets\\w"+str(dateToday)+".p"
picklePath2 = sysPATH+"pickleDumps\\workOrderResponses\\r"+str(dateToday)+".p"
picklePath3 = sysPATH+"pickleDumps\\workOrderTitles\\t"+str(dateToday)+".p"
excelPath = sysPATH+"excelDumps\\"+str(dateToday)+" "+time.strftime("%a %I%p.xlsx")

copyInto = "C:\\Users\\Gustavo\\Documents\\Programming Stuff\\tickethelper\\pickle_dump\\"

# vv this is for testing

# workOrderTickets = pickle.load(open(picklePath1,'rb'))
# titleDict = pickle.load(open(picklePath3, 'rb'))


# VV this is what usually should be turned on

workOrderTickets, titleDict = getDict()
pickle.dump(workOrderTickets,open(picklePath1,'wb'))
pickle.dump(titleDict, open(picklePath3, 'wb'))

pickle.dump(workOrderTickets,open(copyInto + f'w{str(dateToday)}.p','wb'))
pickle.dump(titleDict, open(copyInto + f't{str(dateToday)}.p', 'wb'))


# workOrderResponses = {}
# for workOrder in workOrderTickets:
# 		workOrderResponses[workOrder] = {}
# 	for ticket in workOrderTickets[workOrder]:
# 			workOrderResponses[workOrder][ticket] = []

# vv this is for testing
# workOrderResponses = pickle.load(open(picklePath2,'rb'))

# VV this is what usually should be turned on

# workOrderResponses = handler(workOrderResponses)
# pickle.dump(workOrderResponses,open(picklePath2,'wb'))


# vv this is for testing
# titleDict = pickle.load(open(picklePath3, 'rb'))






# fileNames = createSpreadsheet(workOrderResponses,excelPath,titleDict)
# for file in fileNames:
# 	# excelPath = sysPATH+"excelDumps\\"+file
# 	addTitles(titleDict,file)

# sendMail(fileNames)

# print('Email sent out succesfully...')


