import time
import logging
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


driver_path = "../chromedriver.exe"
# s = Service(driver_path)
# driver = webdriver.Chrome(service=s)



# funcion abstraida
def launch_chromedriver(url, **kwargs):
    '''
    GOAL:
    Launch the webdriver with different conditions depending on
    arguments passed.
    ARGUMENTS:
    a) -c <chromedriver-path>: Optional argument. Indicates unusual
    path where the '.exe' can be found. Omit this argument if
    chromedriver is in path.
    b) -p <proxy-address>: Optional argument. Indicates the address
    of the proxy server to connect to. Omit this argument if no
    proxies will be used.
    '''

    logging.info('Received a call to "launch_chromedriver".')

    chrome_options = webdriver.Options()
    chrome_options.add_argument('--headless') # para ejecutar sin interfaz
    chrome_options.add_argument('--disable-gpu') # Windows need.
    chrome_options.add_argument('--no-sandbox') # Bypass OS security
    chrome_options.add_argument('--ignore-ssl-errors=yes') # Bypass non-secure errors
    chrome_options.add_argument('--ignore-certificate-errors') # Bypass non-secure errors
    chrome_options.add_argument('start-maximized') # abrirlo lo mas grande posible

    # Loading proxies.
    if 'proxy' in kwargs:
        logging.info('Launching chromedriver with proxies.')
        proxy_server = '--proxy-server=' + kwargs['proxy']
        chrome_options.add_argument(proxy_server)

    # Loading Chromedriver path.
    if 'path' in kwargs:
        chromedriver_path = kwargs['path']
        logging.info('Chromedriver located in unusual path.')
        logging.debug('New path: %s.', chromedriver_path)
        driver = webdriver.Chrome(
            executable_path=chromedriver_path,
            chrome_options=chrome_options
        )
    else:
        driver = webdriver.Chrome(chrome_options=chrome_options)
        logging.info('Chromedriver located in path.')

    # Launching
    try:
        driver.get(url)
        time.sleep(2)
        logging.info('Driver up & running.')
        return(driver)

    except Exception as e:
        logging.error(e, exc_info=True)
        sys.exit()


def main():
    print("Hello")
    url = "https://comillas.edu"

    # url = "https://es.wikipedia.org/wiki/Aaron_Swartz#JSTOR"
    launch_chromedriver(url=url, path = driver_path)


if __name__ == "__main__":
    main()