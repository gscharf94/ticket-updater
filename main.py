from browser import getDict, handler, getWorkOrderTitles 
from spreadsheet import createSpreadsheet, addTitles
from sendMail import sendMail
import time, datetime
import pickle


dateToday = datetime.date.today()

sysPATH = "C:\\Users\\Gustavo\\Documents\\Programming Stuff\\check if ready\\bin\\new\\huh\\"
picklePath1 = sysPATH+"pickleDumps\\workOrderTickets "+str(dateToday)+".p"
picklePath2 = sysPATH+"pickleDumps\\workOrderResponses "+str(dateToday)+".p"
picklePath3 = sysPATH+"pickleDumps\\workOrderTitles "+str(dateToday)+".p"
excelPath = sysPATH+"excelDumps\\"+str(dateToday)+" "+time.strftime("%a %I%p.xlsx")

# vv this is for testing

# workOrderTickets = pickle.load(open(picklePath1,'rb'))


# VV this is what usually should be turned on

workOrderTickets = getDict()
pickle.dump(workOrderTickets,open(picklePath1,'wb'))

# print(workOrderTickets)

workOrderResponses = {}
for workOrder in workOrderTickets:
	workOrderResponses[workOrder] = {}
	for ticket in workOrderTickets[workOrder]:
		workOrderResponses[workOrder][ticket] = []



# vv this is for testing
# workOrderResponses = pickle.load(open(picklePath2,'rb'))

# VV this is what usually should be turned on

workOrderResponses = handler(workOrderResponses)
pickle.dump(workOrderResponses,open(picklePath2,'wb'))


titleDict = getWorkOrderTitles(workOrderResponses)
pickle.dump(titleDict, open(picklePath3, 'wb'))
print(titleDict)

# vv this is for testing
# titleDict = pickle.load(open(picklePath3, 'rb'))






fileNames = createSpreadsheet(workOrderResponses,excelPath,titleDict)
for file in fileNames:
	# excelPath = sysPATH+"excelDumps\\"+file
	addTitles(titleDict,file)

sendMail(fileNames)

print('Email sent out succesfully...')


