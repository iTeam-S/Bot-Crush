import os, time, pickle
import hashlib


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
		Browser.find_element_by_tag_name('body').screenshot("conn.png")
		if 'login' in Browser.current_url:
			print('Je me login encore')
			try:
				os.remove('cookies.pkl')
			except FileNotFoundError:
				pass
			finally:
				connexion(Browser)
		return
	Browser.get('https://mbasic.facebook.com/')
	# Login to the fb account
	# print(Browser.page_source)
	# print(Browser.current_url)
	if '/cookie/' in Browser.current_url:
		print('ato va')
		Browser.find_element_by_xpath('//button[@type="submit"]').click()
	Browser.find_element_by_tag_name('body').screenshot("conn1.png")
	username_ipt = Browser.find_element_by_id("m_login_email")
	username_ipt.send_keys(os.environ.get("ITEAMS_LOGIN"))
	print("Variable env => ",os.environ.get("ITEAMS_LOGIN"))

	password_ipt = Browser.find_element_by_name("pass")
	password_ipt.send_keys(os.environ.get("ITEAMS_PASS"))

	Browser.find_element_by_name("login").click()
	while not pageLoaded(Browser): time.sleep(0.5)
	Browser.find_element_by_tag_name('body').screenshot("conn1.png")
	print("connexion success")
	with open("cookies.pkl","wb") as fcookies:
		pickle.dump(Browser.get_cookies() , fcookies)

		
def encrypt(string):
	hash = hashlib.sha224()

	string_crypt = hash.update(string.encode('utf8'))
	return hash.hexdigest()


def decode(txt_encode):
	txt = ''
	for u in txt_encode.split('-'):
		txt = txt + chr(int(u))
	return txt


def encode(txt):
	txt_encode = ''
	for u in txt:
		txt_encode = txt_encode + str(ord(u)) + '-'
	return txt_encode[:-1]