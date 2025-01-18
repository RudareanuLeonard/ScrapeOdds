from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re


#I COULD USE A CLASS TO STORE country-leagues-matches-typeofbets BETTER... TO DO for later



SITE = "https://www.oddsportal.com/"
SITE_FOOTBALL = "https://www.oddsportal.com/football/"


def get_football_countries():
    driver = webdriver.Chrome() #chrome webdriver
    driver.get(SITE_FOOTBALL)
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

def transform_league_to_url(league):
    league = league.lower()
    league = league.replace(" ", "-")

    return league

def get_football_data():

    call_get_football_countries = get_football_countries()

    country_leagues = {}
    
    cnt = 0

    driver = call_get_football_countries[0]
    get_countries = call_get_football_countries[1] #i need to use he ".text"

    country_to_url = []

    for country in get_countries: #modify country string so i can add it to the xpath string
        country_to_url.append(transform_country_to_url(country.text))

    for i in range (2, 5): #for it to can be clicked it needs to be "visible" - so my solution was to zoom out the page          #4,5 - for test on a few leagues
        country = get_countries[i] #webelement
        country_url = country_to_url[i]

        # print(f"country to url = {country_to_url}")

        #for each country we have one or more leagues
        leagues = []
        country_text = country.text



        try:
            country.click()
            time.sleep(5)

            xpath = '//li/a[contains(@href, "football/' + country_url + '/")]'


            find_leagues = driver.find_elements(By.XPATH, xpath)

            for el in find_leagues:
                league = el # put webelements here so i can access it in another merthod

               
                print(f"league = {el.text}")
                league_text = transform_league_to_text(el.text)
                print()
                # print()
                # print(f"league text = {league_text} and tpye league text = {type(league_text)}")
                print()
                print()
                league_url = transform_league_to_url(league_text)

                time.sleep(8)
                
                league.click()


                # print(f"counrty to url val = {country_url} type = {type(country_url)}")
                # print()
                # print()
                # print(f"league url type = {type(league_url)}")
                print()
                print()


                time.sleep(5)

                move_to_match(driver,country_url,league_url)


                time.sleep(1000)
                driver.back()
                leagues.append(league.text)

            country_leagues[country_text] = leagues

            
            # print(f"country_leagues = {country_leagues}")

            time.sleep(5)
            
            driver.back()
        except Exception as e:
            print(f"get_football_data ERROR = {e}")

    print(country_leagues)

    # driver.quit()

    return driver, country_leagues


def move_to_match(driver, country, league):

    ##########

    #so, to move to a match, we need to press on a href that looks something like: football/country/league/home_team_formatted-away_team_formatted-somecode/

    ##########
    


    try:
        text_after = ".+"
        # xpath = '//a[contains(@href, "football/' + country + '/' + league + '/' + text_after +'/")]' - close one
        xpath = '//a[contains(@href, "football/' + country + '/' + league +'/")]'
        # xpath = f'//div/a[contains(@href, "football/{country}/{league}/")]' - ???
        # xpath = 'a[contains(@href, "football/algeria/ligue-1/oran-cr-belouizdad-lK3qJL2A/")]' #i suppose we get algeria...
        
        print(f"xpath = {xpath}")

        get_matches = driver.find_elements(By.XPATH, xpath)

        time.sleep(5)
        print()
        print()
        
        for i in range(4, len(get_matches) - 2):
            match = get_matches[i]
            text = match.text
            print(f"text = {text}")
            # if i != 2 and i != 3:
            #     try:
            #         match.click()
            #         time.sleep(5)
            #         driver.back()
            #     except:
            #         print("Click not worked")
            # # else:
            #     print(" I = 2")



        # for match in get_matches:
        #     print(f"get_matches =  {match.text}")
        print()
        print()
        print(f"END METHOD")
    except Exception as e:
        print(f"move_to_match error = {e}")  
    
        

if __name__ == "__main__":
    get_football_data()