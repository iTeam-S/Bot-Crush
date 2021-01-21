import os, time, pickle


def pageLoaded(Browser):
	'''
	    Pour verifier qu'un driver a fini de charger la page...
	        True dans ce cas , sinon False
	'''
	status = Browser.execute_script('return document.readyState;')
	return status == 'complete'


def connexion(Browser):
	'''
		fonction de connexion pour le driver donnee en parametre
		avec verification de presence de cookie.
	'''
	Browser.get('https://mbasic.facebook.com/')
	if os.path.isfile('cookies.pkl'):
		with open("cookies.pkl", "rb") as fcookies:
			cookies = pickle.load(fcookies)
			for cookie in cookies:
				try:
					Browser.add_cookie(cookie)
				except:
					os.remove('cookies.pkl')
					connexion(Browser)
		Browser.get('https://mbasic.facebook.com/')
		while not pageLoaded(Browser): time.sleep(0.5)
		if 'login.php' in Browser.current_url:
			try:
				os.remove('cookies.pkl')
			except FileNotFoundError:
				pass
			finally:
				connexion(Browser)
		return
	Browser.get('https://mbasic.facebook.com/')
	#Login to the fb account
	username_ipt = Browser.find_element_by_id("m_login_email")
	username_ipt.send_keys( (os.environ.get("ITEAMS_LOGIN"))
	print("Variable env => ",os.environ.get("ITEAMS_LOGIN"))

	password_ipt = Browser.find_element_by_name("pass")
	password_ipt.send_keys(os.environ.get("ITEAMS_PASS"))

	Browser.find_element_by_name("login").click()
	while not pageLoaded(Browser): time.sleep(0.5)

	with open("cookies.pkl","wb") as fcookies:
		pickle.dump(Browser.get_cookies() , fcookies)


