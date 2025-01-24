from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from unidecode import unidecode


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
    country = unidecode(country) # to deal with diacritics or special characters
    country = country.lower()
    country = country.replace(" ", "-")

    return country


def transform_league_to_text(league):
    league = re.sub(r"\([0-9]+\)", "", league).strip()

    return league

def transform_league_to_url(league):
    league = unidecode(league) # to deal with diacritics or special characters
    league = league.lower()
    league = league.replace(" ", "-")

    return league

def get_football_data():

    call_get_football_countries = get_football_countries()

    country_leagues = {}
    

    driver = call_get_football_countries[0]
    get_countries = call_get_football_countries[1] #i need to use he ".text"

    country_to_url = []

    for country in get_countries: #modify country string so i can add it to the xpath string
        country_to_url.append(transform_country_to_url(country.text))

    for i in range (1, 5): #for it to can be clicked it needs to be "visible" - so my solution was to zoom out the page          #4,5 - for test on a few leagues
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

                print()
                print()


                time.sleep(5)

                get_matches = get_matches_info(driver,country_url,league_url)

                print()
                print()
                print()
                print()
                for match in get_matches:
                    print(f"MATCH = {match.text}")
                print()
                print()
                print()
                print()

                league_results = get_matches[0]
                league_standings = get_matches[1]
                #get_matches[2] is the time when match starts
                #so the matches start from get_matches[3]
                for i in range (3, len(get_matches)):
                    match.click()
                    get_match_info(driver, match)
                    driver.back()

                

                
                time.sleep(1000)
                driver.back()
                leagues.append(league.text)

            country_leagues[country_text] = leagues

            
            # print(f"country_leagues = {country_leagues}")

            ################################################
                #so, if i press on the match, i do not see the standings, so i need to press the standing before entering the match
            ################################################




            time.sleep(500)
            
            driver.back()
        except Exception as e:
            print(f"get_football_data ERROR = {e}")

    # print(country_leagues)

    # driver.quit()

    return driver, country_leagues


def get_matches_info(driver, country, league): #what matches are, results, standings

    ##########

    #so, to move to a match, we need to press on a href that looks something like: football/country/league/home_team_formatted-away_team_formatted-somecode/

    ##########
    


    try:
       
        xpath = '//a[contains(@href, "football/' + country + '/' + league +'/")]'

        # print(f"xpath = {xpath}")

        get_matches = driver.find_elements(By.XPATH, xpath)

        time.sleep(5)
        
        print("GOING TO CLICK ON MATCH")
        time.sleep(5)
        

        print()
        print()
        print(f"END METHOD - get_all_matches")
        
        return get_matches
    

    except Exception as e:
        print(f"move_to_match error = {e}")  
    


def get_standings_info(driver, standings): #TO DO
    pass #TO DO

def get_results_info(driver, results):#TO DO
    pass #TO DO

def get_match_info(driver, match):

    driver.execute_script("document.body.style.zoom='30%'")

    types_of_bets = [] #here i ll store all types of bets... those will be names of the dictionaries

    one_x_two = {}
    over_under = {}
    asian_handicap = {}
    both_teams_to_score = {}
    double_chance = {}
    draw_no_bet = {}
    halftime_fulltime = {}
    odd_or_even = {}

    

    general_xpath = '//ul/li/span'
    # print(f"general xpath = {general_xpath}")

    all_types_of_bets = []

    find_types = driver.find_elements(By.XPATH, general_xpath)

    i = 0


    while find_types[i].text != '': #get type of bets but without whats on "more" button
        type = find_types[i]
        all_types_of_bets.append(type)
        i = i + 1

    ###
        #so we get the "visible" elements here
    ###
    """
    BET TYPE = 1X2
    BET TYPE = Over/Under
    BET TYPE = Asian Handicap
    BET TYPE = Both Teams to Score
    BET TYPE = Double Chance
    BET TYPE = European Handicap
    BET TYPE = Draw No Bet
    """
    # now we go through each type and try to retreive the odds:

    for i in range (len(all_types_of_bets)):
        bet_type = all_types_of_bets[i]
        print(f"bet type = {bet_type.text}")
        bet_type.click()
        if i == 0:
            print("1X2")
            # get_1x2_odds(driver)
        if i == 1:
            print("over/under")
            # print(get_over_under_odds(driver))
        if i == 2:
            print("asian handicap")
            get_asian_handicap_odds(driver)
            time.sleep(15)
        if i == 3:
            print("btts")
        if i == 4:
            print("double chance")
        if i == 5:
            print("european handicap")
        if i == 6:
            print("draw no bet")

        time.sleep(3)
        
        

    
    time.sleep(100)
    ##################
        #the list from "more" is hidden so i need to remove the attribute that hides it... that's what im doing here
    ##################
    ul_element = driver.find_element(By.XPATH, "//ul[contains(@class, 'hidden-links')]")
    driver.execute_script("arguments[0].classList.remove('links-invisible');", ul_element) #remove what hides the list

    # time.sleep(2)

    # hidden_xpath = ul_element.find_elements(By.XPATH, "./li/span")
    # for type in hidden_xpath:
    #     type.click()
    #     time.sleep(12)
    #     print(f"element = {type.text}")
    #     all_types_of_bets.append(type)



def get_1x2_odds(driver):
    xpath_all_odds = '//div/div/div/p'

    all_elements = driver.find_elements(By.XPATH, xpath_all_odds)
    # get_home_odds = driver.find_elements(By.CSS_SELECTOR, "[data-v-10e18331]") ------ IT RETURNS BETTER RESULTS, BUT WHAT IF THE CHANGES the data-v... ? so i ll use the previous one

    pos_average_word = -1

    for i in range(0, len(all_elements)):
        if all_elements[i].text == "Average": #because i get more things than what i need
            pos_average_word = i

    if pos_average_word >= 0:
        all_elements = all_elements[:pos_average_word]

    pattern = r'\b[1-9]\.[0-9][0-9]\b'

    cnt = 0
    home_odds = []
    draw_odds = []
    away_odds = []

    for odd in all_elements:
        odd_match = re.match(pattern, odd.text)
        odd_match = odd_match.group() if odd_match else None
        if odd_match != None:
            if cnt % 3 == 0:
                home_odds.append(float(odd_match))
            if cnt % 3 == 1:
                draw_odds.append(float(odd_match))
            if cnt % 3 == 2:
                away_odds.append(float(odd_match))
            cnt += 1

    average_home_odd = round(sum(home_odds) / len(home_odds), 2)
    average_draw_odd = round(sum(draw_odds) / len(draw_odds), 2)
    average_away_odd = round(sum(away_odds) / len(away_odds), 2)
    # print()
    # print()
    # print()
    # print(f"home odds = {average_home_odd}")
    # print(f"draw odds = {average_draw_odd}")
    # print(f"away odds = {average_away_odd}")
    # print(f"LEN OF GET HOME ODDS = {len(get_home_odds)}")

    return [home_odds, draw_odds, away_odds]



def get_over_under_odds(driver):
    driver.execute_script("document.body.style.zoom='10%'")

    time.sleep(5) #time to load the page

    xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'

    try:
        all_elements = driver.find_elements(By.XPATH, xpath)

        time.sleep(10)

        #i need to create a dictionary where i put type_of_bet and it odds:
        over_under_dict = {}
        for el in all_elements:
            if el.text is not None:
                el.click()
                xpath_odds = '//div/div/div/p[contains(@class, "height-content line-through")]'
                find_all_odds_web_elements = driver.find_elements(By.XPATH, xpath_odds)

                i = 0
                over_odd = 0
                under_odd = 0
                cnt = len(find_all_odds_web_elements) // 2

                for i in range(len(find_all_odds_web_elements)):
                    odd = float(find_all_odds_web_elements[i].text)
                    if i % 2 == 0:
                        over_odd += odd
                    else:
                        under_odd += odd

                over_odd = over_odd / cnt
                over_odd = round(over_odd, 2)
                under_odd = under_odd // cnt
                under_odd = round(under_odd, 2)
                
                if el.text not in over_under_dict:
                    over_under_dict[el.text] = [over_odd, under_odd]
                    
                    
                # el.click() #now i click on every category to display odds for it, but i do not get the odds with this, i need to do some extra work
                el.click()
                time.sleep(2)
        over_under_dict = {key.split('\n')[0]: value for key, value in over_under_dict.items()}
        return over_under_dict
        
    except Exception as e:
        print(f"over under method err = {e}")


def get_asian_handicap_odds(driver):
    driver.execute_script("document.body.style.zoom='50%'")
    # driver.execute_script("document.body.style.zoom='10%'")
    # driver.execute_script("document.body.style.zoom='10%'")

    time.sleep(5) #time to load the page

    xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'
    
    try:
        all_elements = driver.find_elements(By.XPATH, xpath)
        time.sleep(10)

        a_h_dict = {}

        for el in all_elements:
            if el.text is not None:
                el.click()
                xpath_odds = '//div/div/div/p[contains(@class, "height-content line-through")]'
                find_all_odds_web_elements = driver.find_elements(By.XPATH, xpath_odds)

                i = 0
                home_odd = 0 #over become home
                home_odds_list = []
                away_odd = 0 #under become away
                away_odds_list = []

                for i in range(len(find_all_odds_web_elements)):
                    odd = float(find_all_odds_web_elements[i].text)
                    if i % 2 == 0:
                        home_odd += odd
                        home_odds_list.append(odd)
                    else:
                        away_odd += odd
                        away_odds_list.append(odd)

                home_odd = round(sum(home_odds_list) / len(home_odds_list), 2)
                away_odd = round(sum(away_odds_list) / len(away_odds_list), 2)  
                
                if el.text not in a_h_dict:
                    a_h_dict[el.text] = [home_odd, away_odd]
                
                    
                # el.click() #now i click on every category to display odds for it, but i do not get the odds with this, i need to do some extra work
                el.click()
                time.sleep(2)
        a_h_dict = {key.split('\n')[0]: value for key, value in a_h_dict.items()}

        print(f"a_h_dict = {a_h_dict}")
        return a_h_dict

    except Exception as e:
        print(f"asian handicap error = {e}")




if __name__ == "__main__":
    get_football_data()