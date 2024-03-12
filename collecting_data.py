'''
This script is used to scraping Game (Card) data from appstore and google play aiming for finding useful marketing data to help a company make decisions on their product strategies.

Langauge: Python
Packages used: requests, BeautifulSoup, pandas
'''

import requests
from bs4 import BeautifulSoup   #parse HTML Code 
import pandas as pd


def get_title(game_soup):
    '''
        This function takes in a BeautifulSoup object and returns the title of the product
    '''
    
    title_element = game_soup.find("h1", class_ = "product-header__title app-header__title").text.strip()
    return title_element

def get_provider(game_soup):
    '''
        This function takes in a BeautifulSoup object and returns the provider of the product
    '''
    company_element = game_soup.find("h2", class_ = "product-header__identity app-header__identity").text.strip()
    return company_element

def get_ranking(game_soup):
    '''
        This function takes in a BeautifulSoup object and returns the title of the product
    '''
    rank_element = game_soup.find("a", class_ = "inline-list__item").text.strip()
    return rank_element

def get_review_score(game_soup):
    '''
        This function takes in a BeautifulSoup object and returns the review score of the product
    '''
    review_score_element = game_soup.find("figcaption", class_ = "we-rating-count star-rating__count").text.split(' • ')[0]
    return review_score_element

def get_review_count(game_soup):
    '''
        This function takes in a BeautifulSoup object and returns the review count of the product
    '''
    review_count_element = game_soup.find("figcaption", class_ = "we-rating-count star-rating__count").text.split(' • ')[1]
    return review_count_element

def get_price(game_soup):
    '''
        This function takes in a BeautifulSoup object and returns the price of the product
    '''
    price_element = game_soup.find('li', class_ = "inline-list__item inline-list__item--bulleted app-header__list__item--price").text.strip()
    return price_element

def get_iphone_compatability(game_soup):
    '''
        This function takes in a BeautifulSoup object and returns the compatability of the product on iPhone
    '''
    element = game_soup.find("dt", string=lambda text: "iphone" in text.lower())
    compatability_element = element.parent.find("dd").text.strip()
    return compatability_element

def get_size(game_soup):
    '''
        This function takes in a BeautifulSoup object and returns the size of the product 
    '''
    element = game_soup.find("dt", string=lambda text: "size" in text.lower())
    size_element = element.parent.find("dd").text.strip()
    return size_element

def get_description(game_soup):
    '''
        This function takes in the BeautifulSoup object and returns the description of the game
    '''
    short_description = ""
    description_element_wrap = game_soup.find('div', class_ = "section__description")
    for short_description_p in description_element_wrap.find_all('p'):
        short_description += short_description_p.text.strip()
        short_description += "\n"
    return short_description


def get_screenshots(link):
    game_page = requests.get(link)
    game_soup = BeautifulSoup(game_page.content, "html.parser")
    title = get_title(game_soup)
    provider = get_provider(game_soup)
    ranking = get_ranking(game_soup)
    review_score = get_review_score(game_soup)
    review_count = get_review_count(game_soup)
    price = get_price(game_soup)
    description = get_description(game_soup)
    compatability = get_iphone_compatability(game_soup)
    size = get_size(game_soup)
    return title, provider, ranking, review_score, review_count, price, description, compatability, size
    

if __name__ == "__main__":
    #link for appstore card games page
    URL = "https://apps.apple.com/sg/charts/iphone/card-games/7005"
    page = requests.get(URL) 
    soup = BeautifulSoup(page.content, "html.parser")

    #find the game list sections 
    game_section = soup.find_all("div", class_="l-row chart")
    #get the lists for free and paid games and fetch their links
    free_games = game_section[0].find_all("li", class_ = "l-column small-2 medium-3 large-2 we-lockup--shelf-align-top we-lockup--in-app-shelf")
    paid_games = game_section[1].find_all("li", class_ = "l-column small-2 medium-3 large-2 we-lockup--shelf-align-top we-lockup--in-app-shelf")

    free_game_links = []
    for free_game in free_games:
        game_link = free_game.find("a")['href'] + "?platform=iphone"
        free_game_links.append(game_link)

    paid_game_links = []
    for paid_game in paid_games:
        game_link = paid_game.find("a")["href"] + "?platform=iphone"
        paid_game_links.append(game_link)

    #dictionary container used to store the game details
    results_dict = {
        "title": [],
        "provider": [],
        "ranking": [],
        "review_score": [],
        "review_count": [],
        "price": [],
        "description": [],
        "compatability": [],
        "size": []
    }

    #iterate through each game and get their details
    for game_links in [free_game_links, paid_game_links]:
        for game_link in game_links:
            title, provider, ranking, review_score, review_count, price, description, compatability, size = get_screenshots(game_link)
            results_dict["title"].append(title)
            results_dict["provider"].append(provider)
            results_dict["ranking"].append(ranking)
            results_dict["review_score"].append(review_score)
            results_dict["review_count"].append(review_count)
            results_dict["price"].append(price)
            results_dict["description"].append(description)
            results_dict["compatability"].append(compatability)
            results_dict["size"].append(size)

    #convert the dictionary to a pandas dataframe
    games_df = pd.DataFrame.from_dict(results_dict)
    #save the result
    games_df.to_csv("dataset_top_card_games.csv", index = False, encoding='utf_8_sig')
