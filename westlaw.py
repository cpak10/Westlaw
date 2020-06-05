from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import getpass
import time
import os

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
password = getpass.getpass('Enter your password: ')
matter = input('Enter matter number: ')
date = input('Enter today\'s date in mm/dd/yyyy: ')

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

# specific folder (Not required for personal research folder)

errored_cases = []

# navigating through cases
for i in range(1, 100):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/div[2]/div/div[1]/div/table/tbody/tr[{}]/td[2]/div/a'.format(i))))
    except TimeoutException:
        break
    try: 
        all_cases = driver.current_url
        case = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/div[2]/div/div[1]/div/table/tbody/tr[{}]/td[2]/div/a'.format(i))
        case.click()

        # update case
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'title')))
        try:
            update_button = driver.find_element_by_id('co_docketsUpdate')
            update_button.click()
            try:
                WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.ID, 'co_docketsUpdate')))
                time.sleep(5)
            except TimeoutException:
                errored_cases.append(driver.find_element_by_id('title').text)
                do_not_wait_button = driver.find_element_by_id('coid_docketsWaitMessage_continueButton')
                do_not_wait_button.click()
                time.sleep(5)
        except NoSuchElementException:
            pass
        
        # pull filings
        docket = driver.find_element_by_class_name('co_docketsTable')
        for j in range(2, 100):
            if docket.find_element_by_xpath('.//tr[{}]/td[2]'.format(j)).text == date:
                try:
                    larger_str = docket.find_element_by_xpath('.//tr[{}]/td[4]/a[1]'.format(j)).text
                    smaller_str = 'View'
                    pdf = larger_str.find(smaller_str)
                    if pdf >= 0:
                        download_filing = docket.find_element_by_xpath('.//tr[{}]/td[4]/a[1]'.format(j))
                        download_filing.click()
                        try:
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'co_multipartPdfDialogCloseButton')))
                            multiple_pdf = driver.find_element_by_id('tbl_pdfParts')
                            get_multi_pdf = multiple_pdf.find_element_by_xpath('.//tbody/tr[2]/td[2]/a')
                            get_multi_pdf.click()
                            time.sleep(5)
                            close_button = driver.find_element_by_id('co_multipartPdfDialogCloseButton')
                            close_button.click()
                            time.sleep(5)
                        except TimeoutException:
                            pass

                        # renaming downloads
                        docket_number = driver.find_element_by_id('codeSetName').text
                        file_docket_number = docket_number.replace(':', '-')
                        file_date = date.replace('/', '-')
                        file_number = docket.find_element_by_xpath('.//tr[{}]/td[1]'.format(j)).text
                        orig_file_name = file_docket_number + '_DocketEntry_' + file_date + '_' + file_number
                        print(orig_file_name)
                        new_date = date[6:] + ' ' + date[0:2] + ' ' + date[3:5]
                        raw_desc = docket.find_element_by_xpath('.//tr[{}]/td[3]'.format(j)).text
                        try:
                            new_desc = raw_desc[:60]
                        except IndexError:
                            new_desc = raw_desc
                        raw_filing = docket.find_element_by_xpath('.//tr[{}]/td[1]'.format(j)).text
                        new_filing = '[' + raw_filing + ']'
                        new_file_name = new_date + ' ' + new_filing + ' ' + new_desc
                        new_file_name = new_file_name.replace('\\', '')
                        new_file_name = new_file_name.replace('/', '')
                        new_file_name = new_file_name.replace(':', '')
                        new_file_name = new_file_name.replace('*', '')
                        new_file_name = new_file_name.replace('?', '')
                        new_file_name = new_file_name.replace('\"', '')
                        new_file_name = new_file_name.replace('<', '')
                        new_file_name = new_file_name.replace('>', '')
                        new_file_name = new_file_name.replace('|', '')
                        print(new_file_name)
                        time.sleep(5)
                        os.rename(r'C:\\Users\\Admin\\Desktop\\Westlaw\\downloads\\' + orig_file_name + '.pdf', r'C:\\Users\\Admin\\Desktop\\Westlaw\\downloads\\' + new_file_name + '.pdf')
                    else:
                        pass
                except NoSuchElementException:
                    pass
            else:
                driver.get(all_cases)
                break
    except NoSuchElementException:
        break
print(errored_cases)