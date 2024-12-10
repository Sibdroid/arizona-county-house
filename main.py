from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import requests
import time
import json


def soup_to_counties(soup: BeautifulSoup) -> list[BeautifulSoup]:
    """Accesses counties from a BeautifulSoup representing a result page.

    Args:
        soup (BeautifulSoup): represents an entire page.

    Returns:
        A list of smaller BeautifulSoups representing
        counties. Each contains information on the following:
        (! represent fields of data used later)
            * !the county's name! ('general');
            * !the amount of votes cast! ('general');
            * the percentage of votes calculate ('general')
            * each candidate's name ('votes');
            * !each candidate's party! ('votes');
            * !the amount of votes each candidate got! ('votes');
            * the percentage of votes each candidate got ('votes');
    """
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


def district_results_to_data(state: str, district: int):
    url = "https://www.nbcnews.com/politics/2024-elections/" \
    f"{state}-us-house-district-{district}-results"
    driver = webdriver.Chrome()
    driver.get(url)
    driver.execute_script('document.title')
    time.sleep(3)
    try:
        element = driver.find_element("id",
                            f"house-{district}-results-table-toggle")
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
        time.sleep(3)
    except NoSuchElementException:
        pass
    html = driver.page_source
    soup = BeautifulSoup(html)
    counties = soup_to_counties(soup)
    for i in counties:
        yield county_to_data(i)
    driver.close()
    
    

def main():
    COUNTY_DICT = {}
    for district in range(1, 10):
        for result in district_results_to_data("arizona", district):
            name, *votes = result
            for key, vote in zip([f"{name} D", f"{name} R", f"{name} Total"],
                                 votes):
                try:
                    COUNTY_DICT[key] += vote
                except KeyError:
                    COUNTY_DICT[key] = vote
        time.sleep(6)
        print(f"{district} done")
        print(COUNTY_DICT)
        print(" ")
    with open("results.json", "w") as file:
        json.dump(COUNTY_DICT, file)


if __name__ == "__main__":
    main()
