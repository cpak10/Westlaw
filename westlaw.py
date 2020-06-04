from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.action_chains import ActionChains

#this_Will_piss_offBelgia
chrome_options = Options()
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": 'C:\\Users\\Admin\\Desktop\\Westlaw\\downloads',
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    }
)
driver = webdriver.Chrome(options = chrome_options)

# prelim info
username = input('Enter in your username: ')
password = input('Enter your password: ')
matter = input('Enter matter number: ')
date = input('Enter date in mm/dd/yyyy: ')

# sign-in page
driver.get('https://signon.thomsonreuters.com/?productid=CBT&lr=0&culture=en-US&returnto=https%3a%2f%2f1.next.westlaw.com%2fCosi%2fSignOn&tracetoken=0603201020140x9W77SNOewqmJnjF4FizWZuA6XtWKq-JrDNH0iqe-1S9QLjLIYUlhnStmHpRo_eeuXfatj2ceRb5_zXKs_gporImRryKNf56tbJfJFMQHuZJj4AKDWiHHEL8Gva0g5GP1d8ZqGbJzobKyhgSoGdPkY0FbC6JlNH_MKCgGRoSOqf12BVbjA_7J7coVfwxYNcc8sGKzjlpK_syfw2TlVIjS9QLWlSgjXY4BIO_OgijT8iFav6bSe59i9Om5PjbFtXBVB3U_gDmueG0SefUGtaPZOcRozcbR4LRrlyqtA3OwtjwkEuyCDBW6cS08cPwy0HOsbFu35qOZ77nQACjYANqOT_dw0jc_piaA_cbIcM-THc&bhcp=1')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Username')))
username_textbox = driver.find_element_by_id('Username')
password_textbox = driver.find_element_by_id('Password')
username_textbox.send_keys(username)
password_textbox.send_keys(password)
sign_in = driver.find_element_by_name('SignIn')
sign_in.click()

# matter selection
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'co_clientIDTextbox')))
matter_textbox = driver.find_element_by_id('co_clientIDTextbox')
matter_textbox.send_keys(matter)
contin = driver.find_element_by_id('co_clientIDContinueButton')
contin.click()

# folder selection
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'co_dropdownBoxanchorLabel')))
folder = driver.find_element_by_class_name('co_dropdownBoxanchorLabel')
folder.click()

# specific folder
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div[3]/div/div[3]/div/div[1]/div/div[1]/div/div[2]/div[1]/fieldset/ul/li/div/div/a/span')))
specific = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div[3]/div/div[3]/div/div[1]/div/div[1]/div/div[2]/div[1]/fieldset/ul/li/div/div/a/span')

for i in range(1, 100):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/div[2]/div/div[1]/div/table/tbody/tr[{}]/td[2]/div/a'.format(i))))
    all_cases = driver.current_url
    case = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/div[2]/div/div[1]/div/table/tbody/tr[{}]/td[2]/div/a'.format(i))
    case.click()
    for j in range(2, 100):
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div[5]/div/div[3]/div/table[6]/tbody/tr[{}]/td[2]'.format(j))))
        current_case = driver.current_url
        filing_date = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[5]/div/div[3]/div/table[6]/tbody/tr[{}]/td[2]'.format(j))
        if driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[5]/div/div[3]/div/table[6]/tbody/tr[{}]/td[2]'.format(j)).text == date:
            download_filing = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[5]/div/div[3]/div/table[6]/tbody/tr[{}]/td[4]/a[1]'.format(j))
            download_filing.click()
            driver.get(current_case)
        else:
            driver.get(all_cases)
            break