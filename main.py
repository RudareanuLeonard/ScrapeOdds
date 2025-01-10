from selenium import webdriver
from selenium.webdriver.common.by import By
import time

SITE = "https://www.oddsportal.com/"
SITE_FOOTBALL = "https://www.oddsportal.com/football/"


def get_football_data():
    driver = webdriver.Chrome() #chrome webdriver
    driver.get(SITE_FOOTBALL)
    # driver.fullscreen_window()
    driver.execute_script("document.body.style.zoom='10%'")

    time.sleep(10)
    try:
        #if i remove /div/div -> i also get the leagues, but also more stuff that i do not need;
        #if it looks like //div/div/a[...] i get only the countries
        get_countries = driver.find_elements(By.XPATH,'//div/div/a[contains(@href,"football/")]')
    except Exception as e:
        print(f"Exception while finding")
    
    #now i need to format the list with countries to make it look appropiate for accessing as website
    # countries_formatted = []

    # for el in get_countries:
    #     country = el.text.lower()
    #     country = country.replace(' ','-')
    #     print(f"country = {country}")

    
    for country in get_countries: #for it to can be clicked it needs to be "visible" - so my solution was to zoom out the page
        
        # print(f"country = {country.text}")

        try:
            
            country.click()
            time.sleep(10)
            driver.back()
        except Exception as e:
            print(f"exception occured")
            time.sleep(10)
            print()
    driver.quit()

if __name__ == "__main__":
    get_football_data()