from bs4 import BeautifulSoup
from selenium import webdriver
import requests


def soup_to_counties(soup: BeautifulSoup) -> list[BeautifulSoup]:
    return soup.find_all("div",
                        attrs={"data-testid": "county-row"})


def general_to_info(general: BeautifulSoup) -> (str, int):
    name, *other, total_vote_count, percentage = general.find_all("span")
    name = name.find("span").text
    total_vote_count = total_vote_count.text
    total_vote_count = total_vote_count.replace(" votes", "").replace(",", "")
    return name, int(total_vote_count)


def county_to_data(county: BeautifulSoup) -> (str, list[int]):
    general, votes, *other = county.find_all("div")
    table = votes.find("div").find("table")
    candidates = table.find("tbody")
    for candidate in candidates.find_all("tr"):
        name, party, votes, *other = candidate.find_all("td")
        party = party.find("div").text
        votes = votes.find("div").find("span").text
        print(party, votes)
        


def main():
    url = "https://www.nbcnews.com/politics/2024-elections/" \
    "arizona-us-house-district-2-results"
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html)
    counties = soup_to_counties(soup)
    county_to_data(counties[0])


if __name__ == "__main__":
    main()
