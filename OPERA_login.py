#! /usr/bin/env python
def id_value_find(word,ext_type):
	if word == 'x-grid3-body':
		region_limit = 60
	else:
		region_limit = 100
	dummy = -1
	count_while = 0
	while dummy == -1:
		count_while = count_while + 1
		if count_while > 10:
			print ("Not found")
			break
		html_source = driver.page_source
		word_region = html_source[(html_source.find(str(word))-region_limit):(html_source.find(str(word))+region_limit)]
		key_position = word_region.find(str(ext_type))
		if key_position == -1:
			dummy = -1
		else:
			return re.sub("\D", "", str(word_region[key_position:key_position+20]) )

####### Logging into website and accessing request data page ########
profile = webdriver.FirefoxProfile()

profile.set_preference('driver.download.folderList', 2) # custom location
profile.set_preference('driver.download.manager.showWhenStarting', False)
profile.set_preference('driver.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

driver = webdriver.Firefox(profile,executable_path=webdriver_path)
driver.get('http://wispi.meteo.fr/opensso/SSORedirect/metaAlias/idp1?SAMLRequest=nVRNj9owEL3vr4h8DyEpBWIBEg2qirQtKaGt1JvXnnQtOXbqcRbor6%2BdpYi2iAPXl%2FHM%2B1JmyBrV0mXnnvUWfnaALooOjdJI%2By9z0llNDUOJVLMGkDpOq%2BXHR5oNhrS1xhluFHlYr%2BYEs3GeTqZslI%2FTesI5ywWv8%2FRtnk1EnmajLE3z0dMEOCfRV7AojZ4Tv4ZEa8QO1hod085DwzSPh%2BM4m%2BzSKX0zpcP0O4lWnprUzPWvnp1raZLsJbZy0IADM6htYlrQiCapqs0WhLTAXeI%2FsqWSDBMp2pRE743l0Mudk5ophHC9ZIjyBc5IedL1Tmoh9Y%2FbJjy9DiH9sNuVcbmpdiRaIoINVAujsWvAVmBfJIcv28czecFbbsS%2F%2FL2kuPOP49ZYx1SPfZMYGBsrf%2FX6yeJhFtKhvW%2F2Iq%2FbTNkfVmSxKspiI44eOK61A6vBzZKLnacLLf3kt6xXpVGSH%2B9pRjC8Ye72dECkiOt%2BlDrLNErQjkRVGe5%2F7piStQQ7J1d4e7eVMvvCAnM%2BQmc7IItXMX%2FTP2s6FR1E3wMfkYODu0dbYZqWWYmhknBg3PnDvYmXiwvlfd9CfU9MN8c45WG1h0N%2F98aK0FtfehC7YGFo0CnUa3zOHl21w5uV%2FP9vWPwG&RelayState=s269178a4961f7cca9dcf915927d912421194b7ecc')

# Inputting usernames #
username = driver.find_element_by_id("IDToken1")
username.clear()
username.send_keys(opera_username)

## Input password
password = driver.find_element_by_name("IDToken2")
password.clear()
password_input = 'Zthah19961006!'
password.send_keys(str(password_input))

## Sleep required to give pages time to load ##
time.sleep(time_delay)

## Not taken to home page originally so Login button at top is clicked
driver.find_element_by_name("Login.Submit").click()

## Sleep required to give pages time to load ##
time.sleep(6)

## Not taken to home page originally so Login button at top is clicked
driver.find_element_by_xpath('//button[@type="submit"]').click()

time.sleep(time_delay)

what_key = driver.find_element_by_id(str('ext-comp-')+str(int(id_value_find('WHAT?','ext-comp'))+1))
what_text = dataset_name
what_key.send_keys(what_text)
what_key.click()
what_key.send_keys(Keys.ENTER)
