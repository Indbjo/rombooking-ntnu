from selenium import webdriver
import time
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta

driver = webdriver.Safari()


def set_time_period_for_booking():
    start = '08:15'
    duration = '04:00'
    selected_date = (date.today() + timedelta(days=3)).strftime("%d.%m.%Y")
    return start, duration, selected_date


def select_option(option_text, element):
    for option in element.find_elements_by_tag_name('option'):
        if option.text == option_text:
            option.click()
            print(f"clicked option with text: {option.text}")
            return


def select_option_by_id(option_id, element):
    for option in element.find_elements_by_tag_name('option'):
        if option.id == option_id:
            option.click()
            print(f"clicked option with ID: {option.id}")
            return


def select_seat(seat_priority_list_by_number):
    radio_picker = driver.find_element_by_xpath(f'//div[@id="place-{seat_priority_list_by_number[0]}-overlay"]/input[1]')
    driver.execute_script("arguments[0].click()", radio_picker)

    description_input = driver.find_element_by_id('name')
    description_input.send_keys('Lesing')

    confirm_button = driver.find_element_by_name('confirm')
    driver.execute_script("arguments[0].click()", confirm_button)

    time.sleep(10)


def select_room(priority_list_by_id):
    radio_picker = driver.find_element_by_xpath(f'//tr[@id="{priority_list_by_id[0]}"]/td[@title="Velg"]/input[1]')
    driver.execute_script("arguments[0].click()", radio_picker)
    order_button = driver.find_element_by_id('rb-bestill')
    driver.execute_script("arguments[0].click()", order_button)
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, 'name'))
    )
    select_seat([7])


def select_times():
    area = 'Gløshaugen'
    building = 'Realfagbygget'
    roomtype = 'Lesesal'
    print("Locating elements", end='')
    start_picker = driver.find_element_by_id('start')
    print('.', end='')
    duration_picker = driver.find_element_by_id('duration')
    print('.', end='')
    area_picker = driver.find_element_by_id('area')
    print('.', end='')
    building_picker = driver.find_element_by_id('building')
    print('.', end='')
    roomtype_picker = driver.find_element_by_id('roomtype')
    print('.', end='')
    single_seat_picker = driver.find_element_by_id('single_place')
    print('.')

    print("Setting options")

    start, duration, selected_date = set_time_period_for_booking()

    select_option(start, start_picker)
    select_option_by_id(f'duration_{duration}', duration_picker)

    date_picker = driver.find_element_by_id('preset_date')
    date_picker.send_keys(selected_date)

    select_option(area, area_picker)
    select_option(building, building_picker)
    select_option(roomtype, roomtype_picker)

    driver.execute_script("arguments[0].setAttribute('checked', 'checked')", single_seat_picker)

    print("options set")

    submit_button = driver.find_element_by_id('preformsubmit')
    driver.execute_script('arguments[0].click()', submit_button)

    print("submitted")
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, '360E3-107'))
    )
    select_room(['360E3-107'])


def login():
    driver.get('https://tp.uio.no/ntnu/rombestilling/')
    url = driver.current_url
    url = url.replace("selectorg", "login")
    url += "&org=ntnu.no"
    driver.get(url)
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username = driver.find_element_by_id('username')
    password = driver.find_element_by_id('password')

    username.send_keys(config.ntnu_username)
    time.sleep(1)
    password.send_keys(config.ntnu_password)
    time.sleep(1)

    button = driver.find_element_by_xpath("//form[@name='f']/button[1]")
    driver.execute_script('arguments[0].click()', button)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'start'))
    )
    select_times()


@PendingDeprecationWarning
def select_org():
        driver.get('https://tp.uio.no/ntnu/rombestilling/')
        form = driver.find_elements_by_name('f')[0]
        label = driver.find_element_by_xpath("//form[@name='f']/label[1]")
        with open('html.html', 'r') as file:
            print("reading html")
            html_string = file.read()
            print("html read")
        print("removing label")
        driver.execute_script("arguments[0].parentNode.removeChild(arguments[0])", label)
        print("label removed")
        print("adding new child")
        driver.execute_script(f"form = arguments[0]; temp = document.createElement('template'); temp.innerHTML = `{html_string}`; form.appendChild(temp.content.firstChild);", form)
        print("child added")
        print("clicking button")
        submit = driver.find_element_by_id('selectorg_button')
        submit.click()
        print("button clicked")

        print("logging in")
        login()


try:
    login()
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.close()



