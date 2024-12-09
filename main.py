from bs4 import BeautifulSoup
import pandas as pd
import requests


def url_to_soup(url: str) -> BeautifulSoup:
    text = requests.get(url).text
    return BeautifulSoup(text, features="lxml")


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
    df = pd.DataFrame(table)
    return df


def main():
    url = "https://www.nbcnews.com/politics/2024-elections/" \
    "arizona-us-house-district-2-results"
    soup = url_to_soup(url)
    counties = soup_to_counties(soup)
    print(county_to_data(counties[0]))


if __name__ == "__main__":
    main()