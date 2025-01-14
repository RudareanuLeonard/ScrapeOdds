from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

SITE = "https://www.oddsportal.com/"
SITE_FOOTBALL = "https://www.oddsportal.com/football/"


def get_football_countries():
    driver = webdriver.Chrome() #chrome webdriver
    driver.get(SITE_FOOTBALL)
    # print(f"DRIVER = {type(driver)}")
    # DRIVER = <class 'selenium.webdriver.chrome.webdriver.WebDriver'>
    # driver.fullscreen_window()
    driver.execute_script("document.body.style.zoom='10%'")

    time.sleep(10)
    try:
        #if i remove /div/div -> i also get the leagues, but also more stuff that i do not need;
        #if it looks like //div/div/a[...] i get only the countries
        get_countries = driver.find_elements(By.XPATH,'//div/div/a[contains(@href,"football/")]')
    except Exception as e:
        print(f"Exception while finding")

    return driver,get_countries


def transform_country_to_url(country):
    country = country.lower()
    country = country.replace(" ", "-")

    return country


def transform_league_to_text(league):
    league = re.sub(r"\([0-9]+\)", "", league).strip()

    return league


def get_football_data():

    call_get_football_countries = get_football_countries()

    country_leagues = {}
    

    driver = call_get_football_countries[0]
    get_countries = call_get_football_countries[1] #i need to use he ".text"


    country_to_url = []

    for country in get_countries: #modify country string so i can add it to the xpath string
        country_to_url.append(transform_country_to_url(country.text))

    for i in range (0, len(get_countries)): #for it to can be clicked it needs to be "visible" - so my solution was to zoom out the page
        country = get_countries[i] #webelement
        country_url = country_to_url[i]

        # print(f"country = {len(country.text)}")
        #for each country we have one or more leagues
        leagues = []
        country_text = country.text

        try:
            country.click()
            time.sleep(5)

            xpath = '//li/a[contains(@href, "football/' + country_url + '/")]'


            find_leagues = driver.find_elements(By.XPATH, xpath)

            for el in find_leagues:
                # print(f"country = {country_text}")
                league = transform_league_to_text(el.text)
                leagues.append(league)
                # print(f"league = {league}")


            # print(f"country = {country.text} and leagues = {leagues}")

            country_leagues[country_text] = leagues

            
            time.sleep(5)

            print(f"current dictionary:")
            print(country_leagues)
            driver.back()
        except Exception as e:
            print(f"error = {e}")




    driver.quit()

if __name__ == "__main__":
    get_football_data()
    # print(transform_league_to_text("League 1 (12)"))