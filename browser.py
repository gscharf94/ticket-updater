from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time


def loginWorkstraight():
	### login to Workstraight
	
	driver = webdriver.Chrome()
	username = "scharfgustavo@gmail.com"
	password = "Program25056!"

	URL = "https://www.workstraight.com/login/"

	driver.get(URL)

	usernameBar = driver.find_element_by_name("username")
	passwordBar = driver.find_element_by_name("password")

	usernameBar.send_keys(username)
	passwordBar.send_keys(password)

	loginButton = driver.find_element_by_name("LoginButton")
	loginButton.click()

	return driver

def getOpenOrders(driver):
	### gets HTML table of open work orders
	### runs them through processOpenOrderList() and 
	### returns a list of responses
	URL = "https://www.workstraight.com/universe/spacetime/Core.work?go=list&id=open"
	driver.get(URL)

	time.sleep(3)

	dropdown = Select(driver.find_element_by_name("wo_list_length"))

	dropdown.select_by_value('100')

	time.sleep(5)

	table = driver.find_element_by_id("wo_list")
	html = table.get_attribute("innerHTML")

	openWorkOrders = processOpenOrderList(html)

	return openWorkOrders

def processOpenOrderList(text):
	### takes in HTML of open orders
	### returns list of responses
	listy = []
	temp = text

	while True:
		index = temp.find("https://www.workstraight.com/universe/spacetime/Core.work?go=view&amp;id=")
		if index == -1:
			break
		else:
			workOrder = temp[index+73:index+76]
			temp = temp[index+77:len(temp)]
			listy.append(workOrder)

	finalListy = []

	for elem in listy:
		if elem in finalListy:
			pass
		else:
			finalListy.append(elem)


	return finalListy

def getTicketNumsFromWorkOrder(workOrder,driver):
	### goes to the individual work order page
	### and gets the ticket nums associated with jobs
	URL = "https://www.workstraight.com/universe/spacetime/Core.work?go=view&id="+workOrder
	driver.get(URL)

	pageHTML = driver.page_source


	index = pageHTML.find("Ticket num:")
	pageHTML = pageHTML[index:len(pageHTML)]
	endIndex = pageHTML.find("</span>")

	ticketNums = pageHTML[0:endIndex]

	return ticketNums

def processTicketNums(ticketNums):
	### goes from "Ticket num: 123456 + 123456"
	### into ['123456','123456']

	for elem in ticketNums:
		ticketNums[elem][0] = ticketNums[elem][0][11:len(ticketNums[elem][0])]
	for elem in ticketNums:
		if "\n" in ticketNums[elem][0]:
			ticketNums[elem][0] = ticketNums[elem][0].replace("\n","")
	for elem in ticketNums:
		if " " in ticketNums[elem][0]:
			ticketNums[elem][0] = ticketNums[elem][0].replace(" ","")
	for elem in ticketNums:
		ticketNums[elem] = ticketNums[elem][0].split("+")

	return ticketNums


def getDict():
	### basically main function on this page for workstraight
	### calls login()
	### gets python list of open orders [ getListOfOpen()]

	driver = loginWorkstraight()

	openWorkOrders = getOpenOrders(driver)

	workOrderDict = {}

	for elem in openWorkOrders:
		workOrderDict[elem] = []

	for workOrder in openWorkOrders:
		nums = getTicketNumsFromWorkOrder(workOrder,driver)
		workOrderDict[workOrder].append(nums)

	time.sleep(3)
	driver.close()

	workOrderDict = processTicketNums(workOrderDict)

	return workOrderDict

def loginSunshine():

	driver = webdriver.Chrome()

	username = "fiber1communications@gmail.com"
	password = "Fiber1470"

	URL = "https://sso.4iqidentity.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dhttpsexactix.sunshine811.com%26redirect_uri%3Dhttps%253A%252F%252Fexactix.sunshine811.com%252Fauth-callback%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520TixApi%2520email%26state%3Dad54df6cf8624217acb214cd288b1db8%26nonce%3Ddefaf02bae4d48f890d393c1e27c2373"
	driver.get(URL)

	usernameBar = driver.find_element_by_id("Username")
	passwordBar = driver.find_element_by_id("Password")

	submitButton = driver.find_element_by_class_name("mdl-button")

	usernameBar.send_keys(username)
	passwordBar.send_keys(password)

	submitButton.click()

	return driver

def getToSearch(driver):
	driver.get("https://exactix.sunshine811.com/tickets/dashboard")

def searchTicket(ticketnum,driver):
	x = False
	while x == False:
		try:
			ticketSearch = driver.find_element_by_id("mat-input-0")
			break
		except:
			pass
	ticketSearch.send_keys(ticketnum)
	time.sleep(3)

	daList = driver.find_element_by_class_name("iq-list-items")

	html = daList.get_attribute("innerHTML")

	if len(html) == 2602:
		print("COULD NOT FIND TICKET")
	else:
		print("FOUND TICKET")
		time.sleep(1.5)
		test = driver.find_element_by_class_name("iq-list-item")
		test.click()
		time.sleep(3)
		html = saveResponsesHTML(driver)

	return html

def saveResponsesHTML(driver):
	currentURL = driver.current_url
	driver.get(currentURL+"#tab4")

	# time.sleep(5)

	while True:
		try:
			currentOnlyCheck = driver.find_element_by_id("mat-radio-7")
			currentOnlyCheck.click()
			showEventsCheck = driver.find_element_by_class_name("mat-checkbox-label")
			showEventsCheck.click()
			break
		except:
			pass


	time.sleep(.5)


	daList = driver.find_element_by_class_name("iq-list-items")
	html = daList.get_attribute('innerHTML')

	return html

def saveContactHTML(driver):
	currentURL = driver.current_url
	driver.get(currentURL[0:-1]+'3')

	time.sleep(3)

	pageHTML = driver.page_source

	f = open('deleteThis.txt','w')
	f.write(pageHTML)
	f.close()

def handler(dicty):
	driver = loginSunshine()

	contactDict = {}
	for orderID in dicty:
		contactDict[orderID] = {}

	for workOrder in dicty:
		for ticket in dicty[workOrder]:
			getToSearch(driver)
			html = searchTicket(ticket,driver)
			responseList = finalList(html)
			for response in responseList:
				dicty[workOrder][ticket].append(response)

			# saveContactHTML(driver)

	driver.close()
	return dicty

def getResponses(text):
	responses = []
	temp = text
	index = 0
	while index != -1:
		index = temp.find("status-column")
		temp = temp[index:len(temp)]
		# print(temp)
		endIndex = temp.find("</div>")
		response = temp[15:endIndex]
		temp = temp[endIndex+5:len(temp)]
		responses.append(response)
	return responses

def getServiceArea(text):
	responses = []
	temp = text
	index = 0
	while index != -1:
		index = temp.find("service-area-column")
		temp = temp[index:len(temp)]
		endIndex = temp.find("</div>")
		response = temp[89:endIndex]
		temp = temp[endIndex+5:len(temp)]
		responses.append(response)
	return responses

def getResponses2(text):
	responses = []
	temp = text
	index = 0
	while index != -1:
		index = temp.find("response-column")
		temp = temp[index:len(temp)]
		# print(temp)
		endIndex = temp.find("</div>")
		response = temp[94:endIndex]
		temp = temp[endIndex+5:len(temp)]
		responses.append(response)
	return responses

def getComments(text):
	responses = []
	temp = text
	index = 0
	while index != -1:
		index = temp.find("comments-column")
		temp = temp[index:len(temp)]
		# print(temp)
		endIndex = temp.find("</div>")
		response = temp[100:endIndex]
		temp = temp[endIndex+5:len(temp)]
		responses.append(response)
	return responses


def finalList(text):
	daList = []
	responses = getResponses(text)
	serviceArea = getServiceArea(text)
	responses2 = getResponses2(text)
	comments = getComments(text)

	for x,elem in enumerate(responses):
		row = []
		row.append(responses[x])
		row.append(serviceArea[x])
		row.append(responses2[x])
		row.append(comments[x])
		daList.append(row)

	for elem in daList[1:-1]:
		print(elem)

	return daList[1:-1]

def getWorkOrderTitles(workOrders):
	idList = []

	driver = loginWorkstraight()

	for workOrder in workOrders:
		idList.append(workOrder)

	URL = "https://www.workstraight.com/universe/spacetime/Core.work?go=list&id=open"
	driver.get(URL)

	time.sleep(5)

	dropdown = Select(driver.find_element_by_name("wo_list_length"))

	dropdown.select_by_value('100')

	time.sleep(.5)

	table = driver.find_element_by_id("wo_list")
	html = table.get_attribute('innerHTML')

	titleList = []

	dicty = {}

	temp = html

	while True:
		index = temp.find('<span class="text-success-title">')
		if index == -1:
			break
		else:
			temp = temp[index+33:len(temp)]
			endIndex = temp.find("</span>")
			name = temp[0:endIndex]
			titleList.append(name)
			temp = temp[endIndex:len(temp)]

	for x,name in enumerate(titleList):
		dicty[idList[x]] = name

	driver.close()

	return dicty

