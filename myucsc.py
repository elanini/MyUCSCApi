#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

login_url='https://my.ucsc.edu/psp/ep9prd/?cmd=login&languageCd=ENG&'
frame_url='https://ais-cs.ucsc.edu/psc/csprd/EMPLOYEE/PSFT_CSPRD/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y&TargetFrameName=None'
shopping_cart_url='https://ais-cs.ucsc.edu/psc/csprd/EMPLOYEE/PSFT_CSPRD/c/SA_LEARNER_SERVICES_2.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A'
search_url='http://pisa.ucsc.edu/class_search'

driver = webdriver.PhantomJS()
driver.implicitly_wait(10)

def login(username, password):
	driver.get(login_url)
	form = driver.find_element_by_id('login')
	form.find_element_by_id('userid').send_keys(username)
	form.find_element_by_id('pwd').send_keys(password)
	form.submit()
	try: assert driver.get_cookie('PS_TOKENEXPIRE') is not None
	except: raise RuntimeError('login failed') 

#load shopping cart, enter main_id, select sect_id, add
def add_to_shopping_cart(main_id, disc_id, lab_id, waitlist):
	try: assert driver.get_cookie('PS_TOKENEXPIRE') is not None
	except: raise RuntimeError('must log in prior to adding to shopping cart')

	driver.get(frame_url)
	driver.find_element_by_id('DERIVED_REGFRM1_CLASS_NBR').send_keys(main_id)
	driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$9$').click()
	for viewall in driver.find_elements_by_xpath('//a[text()="View All Sections"]'):
		viewall.click()
	for button in driver.find_elements_by_xpath('//td[div/span[text()="{}" or text()="{}"]]/preceding-sibling::td/div/input'.format(disc_id, lab_id)):
		button.click()
	driver.find_element_by_id('DERIVED_CLS_DTL_NEXT_PB').click()

	if waitlist:
		driver.find_element_by_id('DERIVED_CLS_DTL_WAIT_LIST_OKAY$125$').click()

	driver.find_element_by_id('DERIVED_CLS_DTL_NEXT_PB$280$').click()


#enroll in classes, they must all be in the shopping cart
#todo: print better results
def enroll(*id_list):
	try: assert driver.get_cookie('PS_TOKENEXPIRE') is not None
	except: raise RuntimeError('must log in prior to adding to enrolling')

	driver.get(shopping_cart_url)
	for main_id in id_list:
		try:
			entry = driver.find_element_by_xpath('//td[div/span/a[contains(., "{}")]]/preceding-sibling::td/div/input[not(@type="hidden")]'.format(main_id))
			entry.click()
		except Exception:
			raise RuntimeError('class is not in shopping cart')

	driver.find_element_by_id('DERIVED_REGFRM1_LINK_ADD_ENRL$291$').click()
	driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_SUBMIT').click()

	WebDriverWait(driver, 100).until(EC.text_to_be_present_in_element((By.ID, 'DERIVED_REGFRM1_TITLE1'), '3.  View results'))

	for row in driver.find_elements_by_xpath('//table[@class="PSLEVEL1GRIDWBO"]/tbody/tr'):
		print row.text



#search for class in the latest available quarter using pisa.ucsc.edu
def name2id(subject, class_num):
	driver.get(search_url)
	Select(driver.find_element_by_id('reg_status')).select_by_value('all') #all classes, not just closed
	Select(driver.find_element_by_id('subject')).select_by_value(subject) 
	driver.find_element_by_id('catalog_nbr').send_keys(class_num)
	driver.find_element_by_id('search_anchor').click()
	
	#first td element of second entry of table of search results
	#todo: change to xpath
	main_id = driver.find_element_by_id('results_table') \
				.find_elements_by_tag_name('tr')[1] \
				.find_elements_by_tag_name('td')[0].text
	return main_id

#load shopping cart, add class number, obtain class name from that
#must log in prior
#todo: find better method for obtaining name using id
def id2name(main_id):
	try: assert driver.get_cookie('PS_TOKENEXPIRE') is not None
	except: raise RuntimeError('must log in prior to finding name')

	driver.get(frame_url)
	driver.find_element_by_id('DERIVED_REGFRM1_CLASS_NBR').send_keys(main_id)
	driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$9$').click()
	return driver.find_element_by_id('DERIVED_CLS_DTL_DESCR50').text

if __name__ == "__main__":
	login('username', 'password')
	#add_to_shopping_cart(42530, 0, 0, False)
	enroll('42530')
	#add_to_shopping_cart(40933, 0, 40934, False)
	#print name2id('CMPS', '101')
	#print id2name('42744')








