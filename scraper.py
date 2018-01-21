from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import gmtime, strftime
import datetime
import time

balance = {}
profit = 0


def wait_and_click(browser, path):
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, path))).click()


while(True):

    try:
        path_to_chromedriver = '/Users/dorukkorkmaz/Downloads/chromedriver' # change path as needed
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200,1100');
        browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options)
        url = 'https://www.tradingview.com/cryptocurrency-signals/'
        browser.get(url)

        # browser.maximize_window()
        browser.implicitly_wait(60)
        time.sleep(5)
        wait_and_click(browser, '//*[@id="js-screener-container"]/div[2]/div[7]/div[1]')
        wait_and_click(browser, '//*[@id="js-screener-container"]/div[2]/div[7]/div[2]/div/div[1]/div[2]')
        wait_and_click(browser, '//*[@id="js-screener-container"]/div[2]/div[13]')

        #select binance as exchange
        wait_and_click(browser, '/html/body/div[12]/div/div[3]/div[1]/div/div/div[4]/div[2]/div/span')
        wait_and_click(browser, '/html/body/div[12]/div/div[4]/div[3]/div[1]/div[2]')

        #close exchange list
        wait_and_click(browser, '/html/body/div[12]/div/div[3]/div[1]/div/div/div[4]/div[1]')

        #select strong buy as rating
        # browser.find_element_by_xpath('/html/body/div[12]/div/div[3]/div[1]/div/div/div[7]/div[2]/div/span').click()
        # browser.find_element_by_xpath('/html/body/div[12]/div/div[4]/div/div[1]/div[2]/label/span').click()

        #close list
        wait_and_click(browser, '/html/body/div[12]/div/div[1]/div[4]')

        #search coins with btc
        browser.find_element_by_xpath('//*[@id="js-screener-container"]/div[3]/table/thead/tr/th[1]/div/div/div[2]/input').send_keys("Btc")

        time.sleep(5)

        list = browser.find_element_by_xpath('//*[@id="js-screener-container"]/div[4]/table/tbody').text.split('\n')
        for elem in list:
            if "Strong Buy" in elem:
                parts = elem.split(' ')
                coin = parts[0]
                value = parts[2]
                if coin not in balance:
                    balance[coin] = value
                    print(datetime.datetime.now().strftime("%H:%M:%S"), "Buy", coin, value)
            elif "Sell" in elem:
                parts = elem.split(' ')
                coin = parts[0]
                value = parts[2]
                if coin in balance:
                    print(datetime.datetime.now().strftime("%H:%M:%S"), "Sell", coin, balance[coin], value)
                    profit += (float(value) - float(balance[coin]))/float(balance[coin])
                    print(profit)
                    del balance[coin]

        browser.close()

        time.sleep(3 * 60)

    except Exception as ex:
        print(ex)
        browser.close()
        pass