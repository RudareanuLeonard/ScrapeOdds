from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
    driver.execute_script("document.body.style.zoom='10%'")
    country_to_url = []

    for country in get_countries: #modify country string so i can add it to the xpath string
        country_to_url.append(transform_country_to_url(country.text))

    for i in range (1, 5): #for it to can be clicked it needs to be "visible" - so my solution was to zoom out the page          #4,5 - for test on a few leagues
        country = get_countries[i] #webelement
        country_url = country_to_url[i]


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

                league_url = transform_league_to_url(league_text)

                time.sleep(8)
                
                league.click()

 

                time.sleep(5)

                get_matches = get_matches_info(driver,country_url,league_url)

           
                for match in get_matches:
                    print(f"MATCH = {match.text}")
 
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

                print("GET FOOTBALL DATA A")

                #get_matches[2] is the time when match starts
                #so the matches start from get_matches[3]
                for i in range (3, len(get_matches)):
                    match = get_matches[i]
                    print(f" match = {match.text}")
                    match.click()
                    get_match_info(driver, match)
                    driver.back()

                

                
                time.sleep(1000)
                driver.back()
                leagues.append(league.text)

            country_leagues[country_text] = leagues

            


            time.sleep(500)
            
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

        time.sleep(5)
        
        

        
        return get_matches
    

    except Exception as e:
        print(f"move_to_match error = {e}")  
    


def get_standings_info(driver, standings): #TO DO
    pass #TO DO

def get_results_info(driver, results):#TO DO
    pass #TO DO

def get_match_info(driver, match):

    driver.execute_script("document.body.style.zoom='30%'")

    match_dict = {}

    one_x_two = {}
    over_under = {}
    asian_handicap = {}
    both_teams_to_score = {}
    double_chance = {}
    draw_no_bet = {}
    halftime_fulltime = {}
    odd_or_even = {}



    
    #hover on "More"

    more_xpath = '//*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[2]/div[2]/div/div/div/button/div'
    more = driver.find_element(By.XPATH, more_xpath)
    hover_more = ActionChains(driver).move_to_element(more)
    hover_more.perform()


    general_xpath = '//ul/li/span'

    all_types_of_bets = []

    find_types = driver.find_elements(By.XPATH, general_xpath)

    print("ALL TYPES find_types")
    match_dict = {}

    for i in range(0, len(find_types)):
        type = find_types[i].text
        if i != 1:
            if type == "1X2":
                print("1X2")
                home_draw_away = get_1x2_odds(driver)
                print(home_draw_away)
                print()
                print()
            if type == "Over/Under":
                print("Over/Under")
                over_under = get_over_under_odds(driver)
                print(over_under)
                print()
                print()

    print("NOW TIME SLEEP 100 seconds")
    time.sleep(100)



    i = 0

    # for el in find_types:
    #     print(f"find types el = {el.text}")

    # time.sleep(10)

    while find_types[i].text != '': #get type of bets but without whats on "more" button
        type = find_types[i]
        all_types_of_bets.append(type)
        i = i + 1


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
    

    # for i in range(len(all_types_of_bets)):
    #     bet_type = all_types_of_bets[i].text
    

    # time.sleep(10)


    # ### get all elements because i do the hover on more
    # for i in range (len(all_types_of_bets) - 1): #because the last one is set privacy
    #     bet_type = all_types_of_bets[i]
    #     print(f"bet type = {bet_type.text}")
    #     more_xpath = '//*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[2]/div[2]/div/div/div/button/div'
    #     # more = driver.find_element(By.XPATH, more_xpath)
    #     # hover_more = ActionChains(driver).move_to_element(more)
    #     # hover_more.perform()
    #     start = time.time()
    #     time.sleep(5)
    #     if bet_type.text != "Home/Away":
            
    #         if bet_type.text == "1X2":
    #             # home_draw_away = get_1x2_odds(driver)
    #             # match_dict["1x2"] = home_draw_away
    #             # print(f"1x2 = {home_draw_away}")
    #             print("1x2")
    #         if bet_type.text == "Over/Under":
    #             # over_under = get_over_under_odds(driver)
    #             # match_dict["over_under"] = over_under
    #             # print(f"over under = {over_under}")
    #             print("over/under")
    #             time.sleep(100)
    #         # if bet_type.text == "Asian Handicap":
    #         #     # asian_handicap = get_asian_handicap_odds(driver)
    #         #     # match_dict["asian_handicap"] = asian_handicap
    #         #     # print(f"asian handicap = {asian_handicap}")
    #         #     print("asian handicap")
    #         # if bet_type.text == "Both Teams to Score":
    #         #     # both_teams_to_score = get_both_teams_to_score_odds(driver)
    #         #     # match_dict["btts"] = both_teams_to_score
    #         #     # print(f"btts = {both_teams_to_score}")
    #         #     print("btts")
    #         # if bet_type.text == "Double Chance":
    #         #     # double_chance = get_double_chance_odds(driver)
    #         #     # match_dict["double_chance"] = double_chance
    #         #     # print(f"double chance = {double_chance}")
    #         #     print("double chance")
    #         # if bet_type.text == "European Handicap":
    #         #     # european_handicap = get_european_handicap_odds(driver)
    #         #     # match_dict["european_handicap"] = european_handicap
    #         #     # print(f"european handicap = {european_handicap}")
    #         #     print("european handicap")
    #         # if bet_type.text == "Draw No Bet":
    #         #     # draw_no_bet = get_draw_no_bet_odds(driver)
    #         #     # match_dict["draw_no_bet"] = draw_no_bet
    #         #     # print(f"draw no bet = {draw_no_bet}")
    #         #     print("draw no bet")
    #         # if bet_type.text == "Correct Score":
    #         #     # correct_score = get_correct_score_odds(driver)
    #         #     # match_dict["correct_score"] = correct_score
    #         #     # print(f"correct score = {correct_score}")
    #         #     print("correct score")
    #         # if bet_type.text == "Half Time / Full Time ":
    #         #     # half_time_full_time = get_half_time_full_time_odds(driver)
    #         #     # match_dict["ht_ft"] = half_time_full_time
    #         #     # print(f"half time / full time = {half_time_full_time}")
    #         #     print("ht / ft")
    #         # if bet_type.text == "Odd or Even":
    #         #     # odd_even = get_odd_even_odds(driver)
    #         #     # match_dict["odd_even"] = odd_even
    #         #     # print(f"odd or even = {odd_even}")
    #         #     print("odd or even")

    #         bet_type.click()

    #         end = time.time()
    #         print()
    #         print()
    #         print()
    #         print("Match dict:")
    #         print(match_dict)

    #         print(f"TIME TAKEN FOR A MATCH = {end - start} seconds")
    #     else:
    #         print("THAT IS HOME/AWAY")

    
    


    time.sleep(1000)





def get_1x2_odds(driver):
    print()
    print()
    print()
    print("HELLO WE ARE INSIDE THE 1X2 METHOD")
    # //*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[3]/div/div/div/div/div/div/div/a
    xpath_all_odds = '//div/div/div/div/div/div/div/a'

    """
    
    xpath 1 = //*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[3]/div/div/div[1]/div/div/div/div/p

    xpath 2 = //*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[3]/div/div/div[1]/div/div/div/div/p
    
    xpath 3 = //*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[3]/div/div/div[1]/div/div/div/div/p

    xpath 4 = //*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[3]/div/div/div[1]/div/div/div/div/p

    """

    all_elements = driver.find_elements(By.XPATH, xpath_all_odds)
    # all_elements = driver.find_elements(By.CSS_SELECTOR, "[data-v-10e18331]")
    # get_home_odds = driver.find_elements(By.CSS_SELECTOR, "[data-v-10e18331]") ------ IT RETURNS BETTER RESULTS, BUT WHAT IF THE CHANGES the data-v... ? so i ll use the previous one

    print("NOW I AM GONNA PRINT ALL ELEMENTS")
    print()
    for el in all_elements:
        print(f"element = {el.text}")
        time.sleep(2)

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
        print(f"odd = {odd.text}  (it is the odd before regex)")
        odd_match = re.match(pattern, odd.text)
        odd_match = odd_match.group() if odd_match else None
        print(f"odd_match = {odd_match}   (it is the odd after regex)")
        if odd_match != None:
            if cnt % 3 == 0:
                home_odds.append(float(odd_match))
            if cnt % 3 == 1:
                draw_odds.append(float(odd_match))
            if cnt % 3 == 2:
                away_odds.append(float(odd_match))
            cnt += 1

        # print(f"all home odds = {home_odds}")
        # print(f"all draw odds = {draw_odds}")
        # print(f"all away odds = {away_odds}")

    average_home_odd = round(sum(home_odds) / len(home_odds), 2)
    average_draw_odd = round(sum(draw_odds) / len(draw_odds), 2)
    average_away_odd = round(sum(away_odds) / len(away_odds), 2)

    # print(f"average home odd = {average_home_odd}")
    # print(f"average draw odd = {average_draw_odd}")
    # print(f"average away  odd = {average_away_odd}")

    time.sleep(100)

    return [average_home_odd, average_draw_odd, average_away_odd]



def get_home_away_odds(driver):
    print("HOME AWAY ODDS METHOD")




def get_over_under_odds(driver):
    driver.execute_script("document.body.style.zoom='10%'")

    time.sleep(5) #time to load the page

    # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    # return"TEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEST"

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
                    if find_all_odds_web_elements[i].text != '-':
                        odd = float(find_all_odds_web_elements[i].text)
                        if i % 2 == 0:
                            over_odd += odd
                        else:
                            under_odd += odd

                over_odd = over_odd / cnt
                over_odd = round(over_odd, 2)
                under_odd = under_odd / cnt
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
    driver.execute_script("document.body.style.zoom='200%'")
    # driver.execute_script("document.body.style.zoom='10%'")
    # driver.execute_script("document.body.style.zoom='10%'")

    time.sleep(5) #time to load the page

    # xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'
    
    try:
    #     all_elements = driver.find_elements(By.XPATH, xpath)
    #     time.sleep(10)
    #     pattern = r'\b[1-9]\.[0-9][0-9]\b'

    #     a_h_dict = {}

    #     for el in all_elements:
    #         if el.text is not None:
    #             el.click()
    #             xpath_odds = '//div/div/div/p[contains(@class, "height-content line-through")]'
    #             find_all_odds_web_elements = driver.find_elements(By.XPATH, xpath_odds)

    #             i = 0
    #             home_odd = 0 #over become home
    #             home_odds_list = []
    #             away_odd = 0 #under become away
    #             away_odds_list = []

    #             for i in range(len(find_all_odds_web_elements)):
    #                 if find_all_odds_web_elements[i].text == '-':
    #                     print(f"WE got - = {find_all_odds_web_elements[i].text} ")
    #                 odd_el = find_all_odds_web_elements[i]
    #                 odd = odd_el.text

    #                 if odd != '-':
    #                     if i % 2 == 0:
    #                         home_odd += odd
    #                         home_odds_list.append(float(odd))
    #                     else:
    #                         away_odd += odd
    #                         away_odds_list.append(float(odd))

    #             if len(home_odds_list) > 0:
    #                 home_odd = round(sum(home_odds_list) / len(home_odds_list), 2)
                
    #             if len(away_odds_list) > 0:
    #                 away_odd = round(sum(away_odds_list) / len(away_odds_list), 2)  
                
    #             if el.text not in a_h_dict:
    #                 a_h_dict[el.text] = [home_odd, away_odd]
                
                    
    #             # el.click() #now i click on every category to display odds for it, but i do not get the odds with this, i need to do some extra work
    #             el.click()
    #             time.sleep(2)
    #     a_h_dict = {key.split('\n')[0]: value for key, value in a_h_dict.items()}

    #     return a_h_dict


        print("TEST ME GETTING AH ODDS  NOT WORKING ANYMORE FFS")

    except Exception as e:
        print(f"asian handicap error = {e}")


def get_both_teams_to_score_odds(driver):
    time.sleep(5) #time to load the page

    xpath_all_odds = '//div/div/div/p[contains(@class, "height-content line-through")]'
    # xpath_all_odds = '//*[@id="app"]/div[1]/div[1]/div/main/div[3]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div/div/p'
    yes_list = []
    yes_average = 0

    no_list = []
    no_average = 0

    try:
        all_elements = driver.find_elements(By.XPATH, xpath_all_odds)

        for i in range(len(all_elements)):
            if all_elements[i].text != '-':
                odd = float(all_elements[i].text)
                if i % 2 == 0:
                    yes_list.append(odd)
                else:
                    no_list.append(odd)


        cnt = len(all_elements) // 2

        yes_avg_odd = round(sum(yes_list) / cnt, 2)
        no_avg_odd = round(sum(no_list) / cnt, 2)


        return [yes_avg_odd, no_avg_odd]
    except Exception as e:
        print(f"BTTS ERROR = {e}")


def get_double_chance_odds(driver):
    time.sleep(5)
    xpath_all_odds = '//div/div/div/p'

    try:
        all_elements = driver.find_elements(By.XPATH, xpath_all_odds)
        
        pos_average_word = -1

        for i in range(0, len(all_elements)):
            if all_elements[i].text == "Average": #because i get more things than what i need
                pos_average_word = i

        if pos_average_word >= 0:
            all_elements = all_elements[:pos_average_word]

    
        pattern = r'\b[1-9]\.[0-9][0-9]\b'

        cnt = 0
        home_draw_odds = []
        home_away_odds = []
        draw_away_odds = []

        for odd in all_elements:
            odd_match = re.match(pattern, odd.text)
            odd_match = odd_match.group() if odd_match else None
            if odd_match != None:
                if cnt % 3 == 0:
                    home_draw_odds.append(float(odd_match))
                if cnt % 3 == 1:
                    home_away_odds.append(float(odd_match))
                if cnt % 3 == 2:
                    draw_away_odds.append(float(odd_match))
            cnt += 1

        time.sleep(5)
        average_home_draw_odd = round( sum(home_draw_odds)/len(home_draw_odds) ,2)
        average_home_away_odd = round( sum(home_away_odds)/len(home_away_odds) ,2)
        average_draw_away_odd = round( sum(draw_away_odds)/len(draw_away_odds) ,2)


        return[average_home_draw_odd, average_home_away_odd, average_draw_away_odd]

    except Exception as e:
        print(f"double chance error = {e}")

def get_european_handicap_odds(driver):
    driver.execute_script("document.body.style.zoom='50%'")
    
    time.sleep(5) #time to load the page

    xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'

    try:
        all_elements = driver.find_elements(By.XPATH, xpath)
        e_h_dict = {}

        for element in all_elements:
            if element.text is not None:
                element.click()
                xpath_odds = '//div/div/div/p[contains(@class, "height-content line-through")]'
                find_all_odds_web_elements = driver.find_elements(By.XPATH, xpath_odds)

                home_odds = []
                draw_odds = []
                away_odds = []

                for i in range(len(find_all_odds_web_elements)):
                    if find_all_odds_web_elements[i].text != '-':
                        odd = find_all_odds_web_elements[i].text

                        if i % 3 == 0:
                            home_odds.append(float(odd))
                        if i % 3 == 1:
                            draw_odds.append(float(odd))
                        if i % 3 == 2:
                            away_odds.append(float(odd))


                avg_home_odd = round(sum(home_odds)/len(home_odds), 2)
                avg_draw_odd = round(sum(draw_odds)/len(draw_odds), 2)
                avg_away_odd = round(sum(away_odds)/len(away_odds), 2)
                

        time.sleep(5)
        element.click()
        return [avg_home_odd, avg_draw_odd, avg_away_odd]
    except Exception as e:
        print(f"get european handicap odds = {e}")

def get_draw_no_bet_odds(driver):
    time.sleep(7)
    xpath_all_odds = '//div/div/div/p'
    all_elements = driver.find_elements(By.XPATH, xpath_all_odds)

    pos_average_word = -1

    for i in range(0, len(all_elements)):
        if all_elements[i].text == "Average": #because i get more things than what i need
            pos_average_word = i

    if pos_average_word >= 0:
        all_elements = all_elements[:pos_average_word]


    pattern = r'\b[1-9]\.[0-9][0-9]\b'

    home_list = []
    away_list = []
    cnt = 0

    for odd in all_elements:
        odd_match = re.match(pattern, odd.text)
        odd_match = odd_match.group() if odd_match else None

        if odd_match != None:
            if cnt % 2 == 0:
                home_list.append(float(odd.text))
            else:
                away_list.append(float(odd.text))

        cnt += 1

    home_odd = round(sum(home_list) / len(home_list) , 2)
    away_odd = round(sum(away_list) / len(away_list) , 2)

    return [home_odd, away_odd]

def get_correct_score_odds(driver):
    driver.execute_script("document.body.style.zoom='10%'")

    time.sleep(5) #time to load the page

    xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'

    try:
        all_elements = driver.find_elements(By.XPATH, xpath)

        cs_dict = {}

        for el in all_elements:
            el.click()# opens the score
            xpath_odds = '//div/div/div/p[contains(@class, "height-content line-through")]'
            find_all_odds_web_elements = driver.find_elements(By.XPATH, xpath_odds)

            odds_list = []

            for odd in find_all_odds_web_elements:
                if odd != '-':
                    odds_list.append(float(odd.text))

            avg_odd = round(sum(odds_list) / len(odds_list), 2)

            if el.text is not None:
                if el.text not in cs_dict:
                    cs_dict[el.text] = avg_odd
                

            el.click()# close the score

        cs_dict = {key.split('\n')[0]: value for key, value in cs_dict.items()}

        
        return cs_dict

    except Exception as e:
        print(f"get_correct_score_odds = {e}")

def get_half_time_full_time_odds(driver):
    driver.execute_script("document.body.style.zoom='30%'")
    time.sleep(5)

    ht_ft_dict = {}

    xpath = '//div/div/div[contains(@class, "flex w-full items-center justify-start pl-3 font-bold text-[#2F2F2F]")]'
    try:
        all_elements = driver.find_elements(By.XPATH, xpath)
        for el in all_elements:
            el.click() #click on element to open
            xpath_odds = '//div/div/div/p[contains(@class, "height-content line-through")]'
            time.sleep(1)
            find_all_odds_web_elements = driver.find_elements(By.XPATH, xpath_odds)

            odds = []

            for odd in find_all_odds_web_elements:
                if odd != '-':
                    odds.append(float(odd.text))

            avg_odd = round(sum(odds) / len(odds) , 2)

            if el.text not in ht_ft_dict:
                ht_ft_dict[el.text] = avg_odd

            el.click()
            
        ht_ft_dict = {key.split('\n')[0]: value for key, value in ht_ft_dict.items()}

        return ht_ft_dict

    except Exception as e:
        print(f"get_ht_ft_method err = {e}")

def get_odd_even_odds(driver):
    time.sleep(5)
    xpath_all_odds = '//div/div/div/p'

    all_elements = driver.find_elements(By.XPATH, xpath_all_odds)

    pos_average_word = -1

    for i in range(0, len(all_elements)):
        if all_elements[i].text == "Average": #because i get more things than what i need
            pos_average_word = i

    if pos_average_word >= 0:
        all_elements = all_elements[:pos_average_word]

    pattern = r'\b[1-9]\.[0-9][0-9]\b'

    cnt = 0

    odd_b = []
    even = []

    for odd in all_elements:
        odd_match = re.match(pattern, odd.text)
        odd_match = odd_match.group() if odd_match else None

        if odd_match != None:
            if cnt % 2 == 0:
                odd_b.append(float(odd_match))
            else:
                even.append(float(odd_match))
        cnt += 1

    avg_odd_odd = round(sum(odd_b) / len(odd_b), 2)
    avg_even_odd = round(sum(even) / len(even), 2)

    odd_even_dict = {
        "odd": avg_odd_odd,
        "even": avg_even_odd
    }


    return odd_even_dict

def write_in_json(text):
    pass



if __name__ == "__main__":
    get_football_data()