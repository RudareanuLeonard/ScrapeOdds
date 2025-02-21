from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from unidecode import unidecode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import json


#I COULD USE A CLASS TO STORE country-leagues-matches-typeofbets BETTER... TO DO for later



SITE = "https://www.oddsportal.com/"
SITE_FOOTBALL = "https://www.oddsportal.com/football/"


def get_football_countries():
    driver = webdriver.Chrome() #chrome webdriver
    driver.get(SITE_FOOTBALL)
    driver.execute_script("document.body.style.zoom='1%'")

    time.sleep(5)
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
    driver.execute_script("document.body.style.zoom='10%'")
    country_to_url = []

    for country in get_countries: #modify country string so i can add it to the xpath string
        country_to_url.append(transform_country_to_url(country.text))

    for i in range (3,8): #for it to can be clicked it needs to be "visible" - so my solution was to zoom out the page          #4,5 - for test on a few leagues
        country = get_countries[i] #webelement
        country_url = country_to_url[i]


        #for each country we have one or more leagues
        leagues = []
        country_text = country.text



        try:
            country.click()
            driver.execute_script("document.body.style.zoom='25%'")
            time.sleep(3)

            xpath = '//li/a[contains(@href, "football/' + country_url + '/")]'


            find_leagues = driver.find_elements(By.XPATH, xpath)

            for el in find_leagues:
                league = el # put webelements here so i can access it in another merthod
                print(f"get football data method; league = {el.text}")

                league_text = transform_league_to_text(el.text)

                league_url = transform_league_to_url(league_text)

                time.sleep(1)
                
                league.click()

 

                time.sleep(1)

                get_matches = get_matches_info(driver,country_url,league_url)

           
                # for match in get_matches:
                #     print(f"MATCH = {match.text}")
 
                league_results = get_matches[0]
                league_standings = get_matches[1]

                # print(f"GET MATCHES = {get_matches}")

                print()
                print()
                print()
                print()
                print()
                print()
                print()

                print("GET FOOTBALL DATA - get matches")

                #get_matches[2] is the time when match starts
                #so the matches start from get_matches[4]

                for i in range (4, len(get_matches)):
                    match = get_matches[i]
                    print(f" match = {match.text}")
                    match_name = match.text
                    # match.click()
                    driver.execute_script("window.open(arguments[0].href, '_blank');", match)
                    time.sleep(5)
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(5)
                    get_match_info(driver, match_name, country_text, league_text)
                    driver.close()

                    # Switch back to the original tab
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(5)

                

                
                time.sleep(3)
                driver.back()
                leagues.append(league.text)

            country_leagues[country_text] = leagues

            
            
            driver.back()
        except Exception as e:
            print(f"get_football_data ERROR = {e}")


    return driver, country_leagues


def get_matches_info(driver, country, league): #what matches are, results, standings

    ##########

    #so, to move to a match, we need to press on a href that looks something like: football/country/league/home_team_formatted-away_team_formatted-somecode/

    ##########
    


    try:
       
        xpath = '//a[contains(@href, "football/' + country + '/' + league +'/")]'


        get_matches = driver.find_elements(By.XPATH, xpath)

        time.sleep(1)
        
        

        
        return get_matches
    

    except Exception as e:
        print(f"move_to_match error = {e}")  
    


def get_standings_info(driver, standings): #TO DO
    pass #TO DO

def get_results_info(driver, results):#TO DO
    pass #TO DO


cnt_drive_back = 0

def get_match_info(driver, match_name, country_text, league_text):

    global cnt_drive_back
    cnt_drive_back = 0


    driver.execute_script("document.body.style.zoom='30%'")
    time.sleep(3)

    elements_of_match_name = match_name.split("\n") #if the match is played, i also get the score here

    team_regex = re.compile(r"\b[A-Za-z]+(?:[A-Za-z0-9\- ]*[A-Za-z0-9])?\b")

# Extract only team names using regex
    teams = [el for el in elements_of_match_name if team_regex.fullmatch(el)]

    match_time = elements_of_match_name[0]
    match_home_team = teams[0]
    match_away_team = teams[1]

    date_xpath = '//*[@id="react-event-header"]/div/div/div/div/p'
    date_find_elements = driver.find_elements(By.XPATH, date_xpath)
    date_position = 1
    date = date_find_elements[date_position].text.strip(",")
    # print(f"match time = {match_time}")
    # print(f"match home team = {match_home_team}")
    # print(f"match away team = {match_away_team}")

    match_dict = {}
    
    match_dict["date"] = date
    match_dict["country"] = country_text
    match_dict["league"] = league_text
    match_dict["time"] = match_time
    match_dict["home_team"] = match_home_team
    match_dict["away_team"] = match_away_team


    
    #hover on "More"



    # print(f"date = {date}")


    # time.sleep(1000)



    general_xpath = '//ul/li/span'

    all_types_of_bets = []

    find_types = driver.find_elements(By.XPATH, general_xpath)



    i = 0

    time_start = time.time()
    try:
        for i in range(len(find_types) - 2):
            
            cnt_drive_back = cnt_drive_back + 1



            more_xpath = '//*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[2]/div[2]/div/div/div/button/div'
            more = driver.find_element(By.XPATH, more_xpath)
            hover_more = ActionChains(driver).move_to_element(more)
            hover_more.perform()
            bet_type = find_types[i]

            print(f"BET TYPE = {bet_type.text}")
            bet_type.click()

            # print(f"i = {i}")
            
            # Wait until the element is present again after the click (to avoid stale element reference)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, general_xpath)))
            
            # print(f"EL BEFORE update = {el.text}")

          
            find_types = driver.find_elements(By.XPATH, general_xpath)
            
            bet_type = find_types[i]  #the updated element reference
            bet_type_text = bet_type.get_attribute("textContent").strip()
            # print(f"EL AFTER update = {bet_type_text}")
            time.sleep(3)
            if bet_type_text == '1X2':
                home_draw_away = get_1x2_odds(bet_type)
                match_dict[bet_type_text] = home_draw_away
                # print(f"home_draw_away = {home_draw_away}")
                # print()
                # time.sleep(5)
            if bet_type_text == "Over/Under":
                # print("HEEREREREREREREREREREEREREREREREREREREREREERERERERERERERERERERERERE")
                over_under = get_over_under_odds(driver)
                match_dict[bet_type_text] = over_under
                # print(f"over_under = {over_under}")
                # print()

            if bet_type_text == "Asian Handicap":
                asian_handicap = get_asian_handicap_odds(driver)
                match_dict[bet_type_text] = asian_handicap
                # print(f"ah = {asian_handicap}")
                # print()
        
            if bet_type_text == "Both Teams to Score":
                btts = get_both_teams_to_score_odds(driver)
                match_dict[bet_type_text] = btts
                # print()

            if bet_type_text == "Double Chance":
                double_chance = get_double_chance_odds(driver)
                match_dict[bet_type_text] = double_chance
                # print(f"double chance = {double_chance}")
                # print()
                # time.sleep(5)

            if bet_type_text == "European Handicap":
                european_handicap = get_european_handicap_odds(driver)
                match_dict[bet_type_text] = european_handicap
                # print(f"european handicap = {european_handicap}")
                # print()

            if bet_type_text == "Draw No Bet":
                draw_no_bet = get_draw_no_bet_odds(driver)
                match_dict[bet_type_text] = draw_no_bet
                # print(f"draw no bet = {draw_no_bet}")
                # print()

            if bet_type_text == "Correct Score":
                correct_score = get_correct_score_odds(driver)
                match_dict[bet_type_text] = correct_score
                # print(f"correct score = {correct_score}")
                # print()

            if bet_type_text == "Half Time / Full Time" or bet_type.text == "Half Time/Full Time":
                half_time_full_time = get_half_time_full_time_odds(driver)
                match_dict[bet_type_text] = half_time_full_time
                # print(f"ht/ft = {half_time_full_time}")
                # print()

            if bet_type_text == "Odd or Even":
                odd_or_even = get_odd_even_odds(driver)
                match_dict[bet_type_text] = odd_or_even
                # print(f"odd or even = {odd_or_even}")
                # print()
            
            time.sleep(3)  # Add sleep if necessary

    except Exception as e:
        print(f"for error = {e}")
        
   


    # print(f"cnt = {cnt_drive_back}")

    # time.sleep(1000)
    time_end = time.time()

    print(f"It took {time_end - time_start} to get all of this data")
    print()
    print()
    # print()
    # print(f"match dict =")
    # print(match_dict)
    write_in_json(match_dict, country_text, league_text, date, match_time, match_home_team, match_away_team) #also can get them from dict in function 

    print("wrote in json, now getting ready to quit")

    # driver back x times
    # try:
    #     for i in range(cnt_drive_back):
    #         more_xpath = '//*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[2]/div[2]/div/div/div/button/div'
    #         more = driver.find_element(By.XPATH, more_xpath)
    #         hover_more = ActionChains(driver).move_to_element(more)
    #         hover_more.perform()
    #         driver.back()
    # except Exception as e:
    #     print(f"DRIVER BACK ERROR = {e}")


def write_in_json(match_dict, country_text, league_text, date, match_time, match_home_team, match_away_team):
    json_object = json.dumps(match_dict, indent = 4)
    match_time = match_time.replace(":", "")
    json_file_name = date + "_" + country_text +"_" + league_text + "_" + match_time + "_" + match_home_team + "_" + match_away_team + ".json"

    json.dumps(match_dict)  # This is where the error occurs

    # time.sleep(10)



    with open(json_file_name, "w") as f:
        f.write(json_object)



def is_decimal_odd(text):
    decimal_pattern = r"^\d+\.\d{1,2}$"  # Matches decimal odds (e.g., 1.50, 2.00, 10.75)
    return bool(re.match(decimal_pattern, text))


def get_1x2_odds(driver):
    print()
    print()
    print()


    global cnt_drive_back


    xpath_all_odds = '//div/div/div/div/div/div/div/p'



    all_elements = driver.find_elements(By.XPATH, xpath_all_odds)

    pos_average_word = -1

    for i in range(0, len(all_elements)):
        if all_elements[i].text == "Average": #because i get more things than what i need
            pos_average_word = i


    if pos_average_word >= 0:
        all_elements = all_elements[:pos_average_word]


    pos_first_decimal_odd = 5 #hardcoded but tried something and did not work...
    all_elements = all_elements[pos_first_decimal_odd:]


    pattern = r'\b[1-9]\.[0-9][0-9]\b'

    cnt = 0
    home_odds = []
    draw_odds = []
    away_odds = []
    
    global cnt_drive_back

    for i in range(len(all_elements)): #because 0 1 2 3 are used for some stuff about the match... and could not remove them
        odd = all_elements[i].get_attribute("textContent").strip()
        # print(f"odd = {odd}")
        if odd != '-' and is_decimal_odd(odd):
            if i % 3 == 0:
                home_odds.append(float(odd))
            if i % 3 == 1:
                draw_odds.append(float(odd))
            if i % 3 == 2:
                away_odds.append(float(odd))

    # print(f"all home odds = {home_odds} and its len = {len(home_odds)}")
    # print(f"all draw odds = {draw_odds} and its len = {len(draw_odds)}")
    # print(f"all away odds = {away_odds} and its len = {len(away_odds)}")

    print()
    print()

    average_home_odd = 0
    average_draw_odd = 0
    average_away_odd = 0
    
    if len(home_odds) > 0:
        average_home_odd = round(sum(home_odds) / len(home_odds), 2)
    
    if len(draw_odds) > 0:
        average_draw_odd = round(sum(draw_odds) / len(draw_odds), 2)
    
    if len(away_odds) > 0:
        average_away_odd = round(sum(away_odds) / len(away_odds), 2)

    # print(f"average home odd = {average_home_odd}")
    # print(f"average draw odd = {average_draw_odd}")
    # # print(f"average away  odd = {average_away_odd}")

    # driver.back()
    # driver.forward()

    return [average_home_odd, average_draw_odd, average_away_odd]



def get_over_under_odds(driver):
    driver.execute_script("document.body.style.zoom='30%'")

    global cnt_drive_back


    
    xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'

    try:
        all_elements = driver.find_elements(By.XPATH, xpath)

        #i need to create a dictionary where i put type_of_bet and it odds:
        over_under_dict = {}
        for o_u_type in all_elements:
            
            # print(f"element = {o_u_type.text}")
            o_u_type.click() #clicked on o_u_type
            cnt_drive_back += 1  # add when click to open the category odds
            xpath_odds = '//div/div/div/p[@data-v-10e18331]'
            # time.sleep(1)
            find_all_odds = driver.find_elements(By.XPATH, xpath_odds)

            over_odd = 0
            over_odds_list = []

            under_odd = 0
            under_odds_list = []

            for i in range(len(find_all_odds)):
                odd = find_all_odds[i]
                odd = odd.get_attribute("textContent").strip()
                # print(f"ODD = {odd}")
                # time.sleep(5)
                if odd != '-':
                    # print(f"ODD = {odd}")
                    if i % 2 == 0:
                        over_odds_list.append(float(odd))
                    else:
                        under_odds_list.append(float(odd))

            over_odd = 0
            under_odd = 0
            if len(over_odds_list) > 0 and len(under_odds_list) > 0:
                over_odd = round(sum(over_odds_list) / len(over_odds_list), 2)
                under_odd = round(sum(under_odds_list) / len(under_odds_list), 2)

            if o_u_type.text not in over_under_dict:
                over_under_dict[o_u_type.text] = [over_odd, under_odd]

            # time.sleep(2)
            cnt_drive_back += 1  # add when click to close the category odds
            o_u_type.click()
        
        over_under_dict = {key.split('\n')[0]: value for key, value in over_under_dict.items()}
        return over_under_dict
        
    except Exception as e:
        print(f"over under method err = {e}")

def get_asian_handicap_odds(driver):
    # time.sleep(5)
    driver.execute_script("document.body.style.zoom='50%'")
    # driver.execute_script("document.body.style.zoom='10%'")
    # driver.execute_script("document.body.style.zoom='10%'")

    global cnt_drive_back

    xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'

    try:
        all_elements = driver.find_elements(By.XPATH, xpath)
        # time.sleep(5)

        a_h_dict = {}

        for el in all_elements:
            if el.text is not None:
                el.click()
                cnt_drive_back += 1  # add when click to open the category odds

                # xpath_odds = '//div/div/div/p[contains(@class, "height-content line-through")]'
                xpath_odds = '//div/div/div/p[@data-v-10e18331]'
                # time.sleep(5)
                find_all_odds_web_elements = driver.find_elements(By.XPATH, xpath_odds)
                # time.sleep(3)

                home_odd = 0 #over become home
                home_odds_list = []
                away_odd = 0 #under become away
                away_odds_list = []

                for i in range(len(find_all_odds_web_elements)):
                    # odd = float(find_all_odds_web_elements[i].text)
                    odd = find_all_odds_web_elements[i].get_attribute("textContent").strip()
                    if odd != '-':
                        if i % 2 == 0:
                            home_odds_list.append(float(odd))
                        else:
                            away_odds_list.append(float(odd))

                home_odd = 0
                away_odd = 0
                if len(home_odds_list) > 0 and len(away_odds_list) > 0:
                    home_odd = round(sum(home_odds_list) / len(home_odds_list), 2)
                    away_odd = round(sum(away_odds_list) / len(away_odds_list), 2)

                if el.text not in a_h_dict:
                    a_h_dict[el.text] = [home_odd, away_odd]

                # time.sleep(2)
                # el.click() #now i click on every category to display odds for it, but i do not get the odds with this, i need to do some extra work
                cnt_drive_back += 1  # add when click to close the category odds
                el.click()
                
        a_h_dict = {key.split('\n')[0]: value for key, value in a_h_dict.items()}

        # print(f"a_h_dict = {a_h_dict}")
        return a_h_dict
    except Exception as e:
        print(f"asian handicap error = {e}")





def get_both_teams_to_score_odds(driver):
    # time.sleep(5) #time to load the page
    # print("IN BTTS METHOD")

    xpath_all_odds = '//div/p[@data-v-10e18331]'
    # xpath_all_odds = '//*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div/div/p'
    yes_list = []
    yes_avg_odd = 0

    no_list = []
    no_avg_odd = 0

    try:
        all_elements = driver.find_elements(By.XPATH, xpath_all_odds)

        for i in range(len(all_elements)):
            # print(f"all elements[i] = {all_elements[i].text}")
            odd = all_elements[i].get_attribute("textContent").strip()
            if odd != '-':
                if i % 2 == 0:
                    yes_list.append(float(odd))
                else:
                    no_list.append(float(odd))


        yes_avg_odd = 0
        no_avg_odd = 0

        if len(yes_list) > 0:
            yes_avg_odd = round(sum(yes_list) / len(yes_list), 2)

        if len(no_list) > 0:
            no_avg_odd = round(sum(no_list) / len(no_list), 2)
        


        return [yes_avg_odd, no_avg_odd]
    except Exception as e:
        print(f"BTTS ERROR = {e}")


def get_double_chance_odds(driver):
    # time.sleep(5)
    xpath_all_odds = '//div/div/div/p[@data-v-10e18331]'

    try:
        all_elements = driver.find_elements(By.XPATH, xpath_all_odds)
        
        pos_average_word = -1

        for i in range(0, len(all_elements)):
            if all_elements[i].text == "Average": #because i get more things than what i need
                pos_average_word = i

        if pos_average_word >= 0:
            all_elements = all_elements[:pos_average_word]

        print()
        print()
        print()
    
        pattern = r'\b[1-9]\.[0-9][0-9]\b'

        cnt = 0
        home_draw_odds = []
        home_away_odds = []
        draw_away_odds = []

        for odd in all_elements:
            odd = odd.get_attribute("textContent").strip()
            # print(f"odd = {odd}")
            if odd != '-':
                if cnt % 3 == 0:
                    home_draw_odds.append(float(odd))
                if cnt % 3 == 1:
                    home_away_odds.append(float(odd))
                if cnt % 3 == 2:
                    draw_away_odds.append(float(odd))
            cnt += 1

        # time.sleep(5)

        average_home_draw_odd = 0
        average_home_away_odd = 0
        average_draw_away_odd = 0

        if len(home_draw_odds) > 0:
            average_home_draw_odd = round( sum(home_draw_odds)/len(home_draw_odds), 2)
        
        if len(home_away_odds) > 0:
            average_home_away_odd = round( sum(home_away_odds)/len(home_away_odds), 2)

        if len(draw_away_odds) > 0:
            average_draw_away_odd = round( sum(draw_away_odds)/len(draw_away_odds), 2)


        return[average_home_draw_odd, average_home_away_odd, average_draw_away_odd]

    except Exception as e:
        print(f"double chance error = {e}")

def get_european_handicap_odds(driver):
    driver.execute_script("document.body.style.zoom='50%'")
    
    # time.sleep(5) #time to load the page

    xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'
    avg_home_odd = 0
    avg_draw_odd = 0
    avg_away_odd = 0

    global cnt_drive_back

    try:
        all_elements = driver.find_elements(By.XPATH, xpath)
        e_h_dict = {}

        for element in all_elements:
            if element.text is not None:
                element.click()
                cnt_drive_back += 1  # add when click to open the category odds
                xpath_odds = '//div/div/div/div/div/div/p[@data-v-10e18331]'
                find_all_odds_web_elements = driver.find_elements(By.XPATH, xpath_odds)

                home_odds = []
                draw_odds = []
                away_odds = []

                for i in range(len(find_all_odds_web_elements)):
                    odd = find_all_odds_web_elements[i].get_attribute("textContent").strip()
                    # print(f"ODD = {odd}")
                    if find_all_odds_web_elements[i].text != '-':
                        if i % 3 == 0:
                            home_odds.append(float(odd))
                        if i % 3 == 1:
                            draw_odds.append(float(odd))
                        if i % 3 == 2:
                            away_odds.append(float(odd))


                avg_home_odd = 0
                avg_draw_odd = 0
                avg_away_odd = 0
                if len(home_odds) > 0:
                    avg_home_odd = round(sum(home_odds)/len(home_odds), 2)
                
                if len(draw_odds) > 0:
                    avg_draw_odd = round(sum(draw_odds)/len(draw_odds), 2)
                
                if len(away_odds) > 0:
                    avg_away_odd = round(sum(away_odds)/len(away_odds), 2)

                if element.text not in e_h_dict:
                    e_h_dict[element.text] = [avg_home_odd, avg_draw_odd, avg_away_odd]
                
                cnt_drive_back += 1  # add when click to close the category odds
                element.click()
        e_h_dict = {key.split('\n')[0]: value for key, value in e_h_dict.items()}
        return e_h_dict
    except Exception as e:
        print(f"get european handicap odds = {e}")

def get_draw_no_bet_odds(driver):
    # time.sleep(3)
    xpath_all_odds = '//div/p[@data-v-10e18331]'
    all_elements = driver.find_elements(By.XPATH, xpath_all_odds)

    pos_average_word = -1

    for i in range(0, len(all_elements)):
        if all_elements[i].text == "Average": #because i get more things than what i need
            pos_average_word = i

    if pos_average_word >= 0:
        all_elements = all_elements[:pos_average_word]


    # start_decimal_odds = 10
    # all_elements = all_elements[start_decimal_odds:]

    # for el in all_elements:
    #     el = el.get_attribute("textContent").strip()
    #     print(f"el = {el}")

    # time.sleep(10)

    pattern = r'\b[1-9]\.[0-9][0-9]\b'

    home_list = []
    away_list = []
    cnt = 0
    home_odd = 0
    away_odd = 0

    for odd in all_elements:
        odd = odd.get_attribute("textContent").strip()
        # print(f'odd element = {odd}')
        # print(f"cnt = {cnt}")
        # print()
        if odd != '-':
            odd = float(odd)
            if cnt % 2 == 0:
                home_list.append(float(odd))
            else:
                away_list.append(float(odd))
        cnt += 1
    # time.sleep(100)

    home_odd = 0
    away_odd = 0

    if len(home_list) > 0:
        home_odd = round(sum(home_list) / len(home_list) , 2)

    if len(away_list) > 0:
        away_odd = round(sum(away_list) / len(away_list) , 2)

    return [home_odd, away_odd]

def get_correct_score_odds(driver):
    driver.execute_script("document.body.style.zoom='10%'")


    global cnt_drive_back



    # time.sleep(5) #time to load the page

    xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'

    try:
        all_elements = driver.find_elements(By.XPATH, xpath)

        cs_dict = {}


        for el in all_elements:
            el.click()# opens the score
            cnt_drive_back += 1  # add when click to open the category odds
            xpath_odds = '//div/div/div/div/div/div/p[@data-v-10e18331]'

            find_all_odds_web_elements = driver.find_elements(By.XPATH, xpath_odds)

            odds_list = []

            for odd in find_all_odds_web_elements:
                odd = odd.get_attribute("textContent").strip()
                print(f"odd = {odd}")
                if odd != '-':
                    odds_list.append(float(odd))

            print(f"odds list = {odds_list}")
            time.sleep(2)

            avg_odd = 0
            if len(odds_list) > 0:
                avg_odd = round(sum(odds_list) / len(odds_list), 2)

            print(f"odd for {el.text} is {avg_odd}")

            if el.text is not None:
                if el.text not in cs_dict:
                    cs_dict[el.text] = avg_odd
                
            cnt_drive_back += 1  # add when click to close the category odds
            el.click()# close the score

        cs_dict = {key.split('\n')[0]: value for key, value in cs_dict.items()}

        
        return cs_dict

    except Exception as e:
        print(f"get_correct_score_odds = {e}")

def get_half_time_full_time_odds(driver):
    driver.execute_script("document.body.style.zoom='30%'")

    global cnt_drive_back
    # time.sleep(5)

    ht_ft_dict = {}

    xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'
    try:
        all_elements = driver.find_elements(By.XPATH, xpath)
        for el in all_elements:
            el.click() #click on element to open
            cnt_drive_back += 1  # add when click to open the category odds
            xpath_odds = '//div/p[@data-v-10e18331]'
            time.sleep(1)
            find_all_odds_web_elements = driver.find_elements(By.XPATH, xpath_odds)

            odds = []

            for odd in find_all_odds_web_elements:
                odd = odd.get_attribute("textContent").strip()
                if odd != '-':
                    odds.append(float(odd))

            avg_odd = 0

            if len(odds) > 0:
                avg_odd = round(sum(odds) / len(odds) , 2)

            if el.text not in ht_ft_dict:
                ht_ft_dict[el.text] = avg_odd

            cnt_drive_back += 1  # add when click to close the category odds
            el.click()
            
        ht_ft_dict = {key.split('\n')[0]: value for key, value in ht_ft_dict.items()}

        return ht_ft_dict

    except Exception as e:
        print(f"get_ht_ft_method err = {e}")

def get_odd_even_odds(driver):
    # time.sleep(5)
    xpath_all_odds = '//div/div/div/p'

    try:

        all_elements = driver.find_elements(By.XPATH, xpath_all_odds)

        pos_average_word = -1

        for i in range(0, len(all_elements)):
            if all_elements[i].text == "Average": #because i get more things than what i need
                pos_average_word = i

        if pos_average_word >= 0:
            all_elements = all_elements[:pos_average_word]

        start_decimal_odds = 10
        all_elements = all_elements[start_decimal_odds:]

        # for el in all_elements:
        #     el = el.get_attribute("textContent").strip()
        #     print(f"el = {el}")
        
        # time.sleep(4)

        pattern = r'\b[1-9]\.[0-9][0-9]\b'

        cnt = 0

        odd_b = []
        even = []

        avg_odd_odd = 0
        avg_even_odd = 0



        for odd in all_elements:
            # print(f"odd = {odd.text}")
            # print()
            odd = odd.get_attribute("textContent").strip()
            if odd != '-' and is_decimal_odd(odd) == True:
                # print(f"odd = {odd}")
                if cnt % 2 == 0:
                    odd_b.append(float(odd))
                else:
                    even.append(float(odd))
            cnt += 1

        avg_odd_odd = 0
        avg_even_odd = 0
        # time.sleep(100)
        if len(odd_b) > 0:
            avg_odd_odd = round(sum(odd_b) / len(odd_b), 2)
        
        if len(even) > 0:
            avg_even_odd = round(sum(even) / len(even), 2)

        odd_even_dict = {
            "odd": avg_odd_odd,
            "even": avg_even_odd
        }


        return odd_even_dict
    except Exception as e:
        print(f"get_odd_even odds error = {e}")




if __name__ == "__main__":
    get_football_data()