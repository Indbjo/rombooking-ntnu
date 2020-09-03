from selenium import webdriver
import time
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta

DRIVER = None


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
    radio_picker = DRIVER.find_element_by_xpath(f'//div[@id="place-{seat_priority_list_by_number[0]}-overlay"]/input[1]')
    DRIVER.execute_script("arguments[0].click()", radio_picker)

    description_input = DRIVER.find_element_by_id('name')
    description_input.send_keys('Lesing')

    confirm_button = DRIVER.find_element_by_name('confirm')
    #driver.execute_script("arguments[0].click()", confirm_button)

    time.sleep(10)


def select_room(priority_list_by_id):
    radio_picker = DRIVER.find_element_by_xpath(f'//tr[@id="{priority_list_by_id[0]}"]/td[@title="Velg"]/input[1]')
    DRIVER.execute_script("arguments[0].click()", radio_picker)
    order_button = DRIVER.find_element_by_id('rb-bestill')
    DRIVER.execute_script("arguments[0].click()", order_button)
    WebDriverWait(DRIVER, 3).until(
        EC.presence_of_element_located((By.ID, 'name'))
    )


def select_times():
    area = 'Gløshaugen'
    building = 'Realfagbygget'
    roomtype = 'Lesesal'
    start_picker = DRIVER.find_element_by_id('start')
    duration_picker = DRIVER.find_element_by_id('duration')
    area_picker = DRIVER.find_element_by_id('area')
    building_picker = DRIVER.find_element_by_id('building')
    roomtype_picker = DRIVER.find_element_by_id('roomtype')
    single_seat_picker = DRIVER.find_element_by_id('single_place')

    start, duration, selected_date = set_time_period_for_booking()

    select_option(start, start_picker)
    select_option_by_id(f'duration_{duration}', duration_picker)

    date_picker = DRIVER.find_element_by_id('preset_date')
    date_picker.send_keys(selected_date)

    select_option(area, area_picker)
    select_option(building, building_picker)
    select_option(roomtype, roomtype_picker)

    DRIVER.execute_script("arguments[0].setAttribute('checked', 'checked')", single_seat_picker)

    print("options set")

    submit_button = DRIVER.find_element_by_id('preformsubmit')
    DRIVER.execute_script('arguments[0].click()', submit_button)

    print("submitted")
    WebDriverWait(DRIVER, 3).until(
        EC.presence_of_element_located((By.ID, '360E3-107'))
    )


def login():
    DRIVER.get('https://tp.uio.no/ntnu/rombestilling/')
    url = DRIVER.current_url
    url = url.replace("selectorg", "login")
    url += "&org=ntnu.no"
    DRIVER.get(url)
    WebDriverWait(DRIVER, 3).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username = DRIVER.find_element_by_id('username')
    password = DRIVER.find_element_by_id('password')

    username.send_keys(config.ntnu_username)
    time.sleep(1)
    password.send_keys(config.ntnu_password)
    time.sleep(1)

    button = DRIVER.find_element_by_xpath("//form[@name='f']/button[1]")
    DRIVER.execute_script('arguments[0].click()', button)
    WebDriverWait(DRIVER, 5).until(
        EC.presence_of_element_located((By.ID, 'start'))
    )


@DeprecationWarning
def select_org():
        DRIVER.get('https://tp.uio.no/ntnu/rombestilling/')
        form = DRIVER.find_elements_by_name('f')[0]
        label = DRIVER.find_element_by_xpath("//form[@name='f']/label[1]")
        with open('html.html', 'r') as file:
            print("reading html")
            html_string = file.read()
            print("html read")
        print("removing label")
        DRIVER.execute_script("arguments[0].parentNode.removeChild(arguments[0])", label)
        print("label removed")
        print("adding new child")
        DRIVER.execute_script(f"form = arguments[0]; temp = document.createElement('template'); temp.innerHTML = `{html_string}`; form.appendChild(temp.content.firstChild);", form)
        print("child added")
        print("clicking button")
        submit = DRIVER.find_element_by_id('selectorg_button')
        submit.click()
        print("button clicked")

        print("logging in")
        login()


def book_room():
    global DRIVER
    DRIVER = webdriver.Safari()
    try:
        login()
        select_times()
        select_room(['360E3-107'])
        select_seat([7])
    except Exception as e:
        print(f"Something went wrong: {e}")
    finally:
        DRIVER.close()


book_room()