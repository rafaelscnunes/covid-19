"""
:Project:    automation
:Version:    2019.12
:Owner:      Rafael Nunes
:Author:     Rafael Nunes - rafaelscnunes@gmail.com
:Date:       2020.04.18
:Created on: PyCharm
--------------------------------------------------------------------------------

    ***  Description using reStructuredText syntax  ***

--------------------------------------------------------------------------------
"""
import os
import re
import time
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = '../chromedriver'
COVID_URL = 'https://covid.saude.gov.br'
OUTPUT_FOLDER = '/Users/rafaelscnunes/Downloads'
WAIT_TIME = 5


def click_ArquivoCSV():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

    driver.get(COVID_URL)
    driver.implicitly_wait(WAIT_TIME)

    buttons = {
        'download': '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/div[1]/div[2]/ion-button',
        'COVID': '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-header/ion-toolbar/div/div[2]/ion-button[1]',
        'SRAG': '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-header/ion-toolbar/div/div[2]/ion-button[2]',
        'Sobre': '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-header/ion-toolbar/div/div[2]/ion-button[3]'
    }

    actions = ActionChains(driver)
    actions.pause(5)
    actions.click(driver.find_element_by_xpath(buttons['download']))
    actions.pause(2)
    actions.click(driver.find_element_by_xpath(buttons['SRAG']))
    actions.pause(3)
    actions.click(driver.find_element_by_xpath(buttons['download']))
    actions.pause(2)
    actions.perform()

    html = driver.page_source
    driver.quit()

    parts = urlparse(COVID_URL, allow_fragments=True)
    filename = f'{parts.netloc}.html'
    with open(os.path.join(OUTPUT_FOLDER, filename), 'w') as f_out:
        f_out.write(html)

    date_time = re.search('(\d{2}):(\d{2}) (\d{2})\/(\d{2})\/(\d{4})', html)
    file_pattern = r'download="(.*?[\.csv|\.xlsx])"'

    try:
        download_filenames = re.search(file_pattern, html).groups()
        for download_filename in download_filenames:
            download_file = os.path.join(OUTPUT_FOLDER, download_filename)

            timestamp = f'{date_time.group(5)}{date_time.group(4)}{date_time.group(3)}{date_time.group(1)}{date_time.group(2)}'
            output_filename = f'{timestamp}_{download_filename}.csv'
            output_file = os.path.join(OUTPUT_FOLDER, output_filename)

            with open(output_file, 'wb') as f_out:
                with open(download_file, 'rb') as f_in:
                    f_out.write(f_in.read())
            os.remove(download_file)

            print(f'File {output_file} is available')
            print(f'Downloaded {download_filename} from {COVID_URL} with timestamp: {date_time.group(0)}')

    except AttributeError:
        exit(f'Error downloading CSV file from {COVID_URL}')


if __name__ == '__main__':
    click_ArquivoCSV()