from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time


def soup_to_counties(soup: BeautifulSoup) -> list[BeautifulSoup]:
    return soup.find_all("div",
                        attrs={"data-testid": "county-row"})


def general_to_info(general: BeautifulSoup) -> (str, int):
    name, *other, total_vote_count, percentage = general.find_all("span")
    name = name.find("span").text
    total_vote_count = total_vote_count.text
    total_vote_count = total_vote_count.replace(" votes", "").replace(",", "")
    total_vote_count = total_vote_count.replace(u'\xa0', u'')
    return name, int(total_vote_count)


def county_to_data(county: BeautifulSoup) -> (str, list[int]):
    general, votes, *other = county.find_all("div")
    name, total = general_to_info(general)
    dem = 0
    rep = 0
    table = votes.find("div").find("table")
    candidates = table.find("tbody")
    for candidate in candidates.find_all("tr"):
        candidate_name, party, votes, *other = candidate.find_all("td")
        party = party.find("div").text
        votes = votes.find("div").find("span").text
        votes = int(votes.replace(" ", "").replace(u'\xa0', u''))
        if party == "D":
            dem += votes
        elif party == "R":
            rep += votes
    return name, dem, rep, total
            


def main():
    url = "https://www.nbcnews.com/politics/2024-elections/" \
    "arizona-us-house-district-2-results"
    driver = webdriver.Chrome()
    driver.get(url)
    driver.execute_script('document.title')
    time.sleep(3)
    element = driver.find_element("id",
                        "house-2-results-table-toggle")
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html)
    counties = soup_to_counties(soup)
    for i in counties:
        print(county_to_data(i))
    driver.close()



if __name__ == "__main__":
    main()
