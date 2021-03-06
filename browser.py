from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup


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

	# openWorkOrders = processOpenOrderList(html)
	openWorkOrders = parse_table_html(html)

	return openWorkOrders

def parse_table_html(text):
	sp = BeautifulSoup(text, 'html.parser')
	ret = {}
	for row in sp.find_all('tr'):
		link = row.find('a')
		if link == None:
			continue
		link = link.getText()
		title = row.find('span').getText()
		ret[link] = title
	return ret




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

	work_order_ids_titles = getOpenOrders(driver)

	openWorkOrders = []
	for item in work_order_ids_titles:
    		openWorkOrders.append(item)


	

	workOrderDict = {}

	for elem in openWorkOrders:
		workOrderDict[elem] = []

	for workOrder in openWorkOrders:
		nums = getTicketNumsFromWorkOrder(workOrder,driver)
		workOrderDict[workOrder].append(nums)

	time.sleep(3)
	driver.close()

	workOrderDict = processTicketNums(workOrderDict)
	# driver.close()

	return workOrderDict, work_order_ids_titles

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

def get_ticket_expiration(driver):
	sections = driver.find_elements_by_class_name("iq-ticket-entry-section")

	for section in sections:
		html = section.get_attribute("innerHTML")
		ind = html.find("Expires:</label>")
		if ind == -1:
			continue
		return html[ind+17:ind+27]

def get_ticket_text(driver):
	currentURL = driver.current_url
	driver.get(currentURL+"#tab2")

	time.sleep(1)

	sections = driver.find_elements_by_class_name("mat-tab-body-content")

	for section in sections:
		html = section.get_attribute("innerHTML")
		ind = html.find("Ticket : ")
		if ind == -1:
			continue
		html = html[ind:]
		ind = html.find("</pre>")
		return html[:ind]

	

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
		time.sleep(1)
		print('looking for element...')
		c = 0
		while c < 100:
			try:
				test = driver.find_element_by_class_name("iq-list-item")
				test.click()
				break
			except:
				c += 1

		print('clicked element')
		time.sleep(3)
		print('getting exp date')
		exp_date = get_ticket_expiration(driver)
		print('getting ticket text')
		ticket_text = get_ticket_text(driver)
		print('getting html')
		html = saveResponsesHTML(driver)

	print('we leave here')
	return html, exp_date, ticket_text

def saveResponsesHTML(driver):
	currentURL = driver.current_url
	driver.get(currentURL[:-5]+"#tab4")

	time.sleep(1)

	while True:
		try:
			currentOnlyCheck = driver.find_element_by_id("mat-radio-7")
			# currentOnlyCheck.send_keys(Keys.SPACE)
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

def create_ticket_metadata_dict(work_order_responses):
	ret = {}
	for item in work_order_responses:
		ret[item] = work_order_responses[item].copy()

	for work_order_id in ret:
		for ticket_num in ret[work_order_id]:
			ret[work_order_id][ticket_num] = {'expiration':None,'text':None}
	return ret


def handler(dicty):
	print(f'before starting: {dicty}')
	driver = loginSunshine()
	metadata = create_ticket_metadata_dict(dicty)

	contactDict = {}
	for orderID in dicty:
		contactDict[orderID] = {}

	for workOrder in dicty:
		for ticket in dicty[workOrder]:
			getToSearch(driver)
			html, exp_date, ticket_text = searchTicket(ticket,driver)
			responseList = finalList(html)
			print(f'before breaking: {dicty}')
			for response in responseList:
				dicty[workOrder][ticket].append(response)

			metadata[workOrder][ticket]['expiration'] = exp_date
			metadata[workOrder][ticket]['text'] = ticket_text

			# saveContactHTML(driver)

	driver.close()
	return dicty, metadata

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

