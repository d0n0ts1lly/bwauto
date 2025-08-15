from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv
import mysql.connector
import random

def dwn():
    time.sleep(5)
    # Ждём кнопку Download/Export
    down_but = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cprt-btn-white.export-csv-button"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", down_but)
    driver.execute_script("arguments[0].click();", down_but)
    time.sleep(5)

    # Пробуем найти OK, но без ошибки если нет
    ok_buttons = driver.find_elements(By.CSS_SELECTOR, ".cprt-btn-yellow")
    if ok_buttons:
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(ok_buttons[0]))
            ok_buttons[0].click()
            print("✅ Кнопка OK нажата")
            time.sleep(10)
        except:
            print("⚠ Кнопка OK нашлась, но не кликнулась")
    else:
        print("ℹ Кнопка OK не появилась — продолжаем")
    


download_dir = os.path.abspath("/Users/d0n0ts1lly/Desktop/bwauto/to_BD/copart_download")

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir, 
    "download.prompt_for_download": False,       
    "download.directory_upgrade": True,          
    "safebrowsing.enabled": True               
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22BMW%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755087829153")

    wait = WebDriverWait(driver, 30)


    export_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.export-csv-button"))
    )
    export_button.click()

    try:
        # Ждем кнопку согласия с куками
        cookie_accept = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_accept.click()
        print("✅ Cookie баннер закрыт")
    except:
        print("ℹ Cookie баннер не найден, идем дальше")

    time.sleep(5)

    export_button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.export-csv-button"))
    )
    export_button.click()

    time.sleep(5)

    email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    email_input.clear()
    email_input.send_keys("worldauto@ukr.net")
    time.sleep(5)

    password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_input.clear()
    password_input.send_keys("autocola1")
    time.sleep(5)

    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cprt-btn-yellow")))
    login_button.click()
    time.sleep(5)



    down_but = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cprt-btn-white.export-csv-button")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", down_but)
    driver.execute_script("arguments[0].click();", down_but)

    time.sleep(5)


    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23MakeCode:AUDI%20OR%20%23MakeDesc:Audi%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755087161008")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22CHEVROLET%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755087856342")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22DODGE%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755087889113")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22FORD%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755087931691")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22HONDA%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755087971944")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22HYUNDAI%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088054340")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22INFINITI%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088090041")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22JEEP%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088110603")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22KIA%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088140164")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22LAND%20ROVER%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088170217")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22LEXUS%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088181066")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22MAZDA%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088206898")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22MERCEDES-BENZ%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088223365")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22MITSUBISHI%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088264648")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22NISSAN%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088378890")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22PORSCHE%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088413462")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22RAM%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088427207")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22SUBARU%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088457590")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22TESLA%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088471371")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22TOYOTA%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088558906")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22VOLKSWAGEN%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088505967")
    dwn()

    driver.get("https://www.copart.com/ru/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22MAKE%22:%5B%22lot_make_desc:%5C%22VOLVO%5C%22%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23EXUPLTS:auction_date_utc:*%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2015%20TO%202026%5D%22%5D%7D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=AUTOMOBILE,%5B0%20TO%209999999%5D,%5B2015%20TO%202026%5D,Audi&from=%2FvehicleFinder&fromSource=widget&qId=655dade8-be5d-47c3-9e34-130c4cb31ff7-1755088600335")
    dwn()


finally:
    driver.quit()

time.sleep(10)


conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='23032023',  
    database='copart_db'   
)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS cars (
    lot_url VARCHAR(255),
    lot_number VARCHAR(50),
    retail_value VARCHAR(50),
    sale_date VARCHAR(100),
    year INT,
    make VARCHAR(50),
    model VARCHAR(100),
    engine VARCHAR(100),
    cylinders VARCHAR(10),
    vin VARCHAR(50),
    title VARCHAR(100),
    odometer VARCHAR(50),
    odometer_desc VARCHAR(50),
    damage VARCHAR(100),
    current_bid VARCHAR(50),
    my_bid VARCHAR(50),
    item_number VARCHAR(50),
    sale_name VARCHAR(100),
    auto_grade VARCHAR(50),
    sale_light VARCHAR(50),
    announcements VARCHAR(255),
    sort_order INT
)
""")

cursor.execute("DELETE FROM cars")
conn.commit() 

csv_folder_path = '/Users/d0n0ts1lly/Desktop/bwauto/to_BD/copart_download'

for file_name in os.listdir(csv_folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_folder_path, file_name)
        
        print(f"Обробка файлу: {file_name}") 

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)  

            for row in reader:
                if not row or len(row) != 21:
                    continue  

                sort_order_value = random.randint(1, 1_000_000)  # Случайное число

                cursor.execute("""
                    INSERT INTO cars (  
                        lot_url, lot_number, retail_value, sale_date, year, make, model,
                        engine, cylinders, vin, title, odometer, odometer_desc,
                        damage, current_bid, my_bid, item_number, sale_name,
                        auto_grade, sale_light, announcements, sort_order
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, row + [sort_order_value])

        conn.commit()
        print(f"Файл {file_name} оброблено і дані збережено в базі.")

        os.remove(file_path)
        print(f"Файл {file_name} видалено.")

cursor.close()
conn.close()

print("✅ Дані успішно збережені в базу MySQL.")
