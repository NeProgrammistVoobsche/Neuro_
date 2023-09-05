import requests
from bs4 import BeautifulSoup as BS
from multiprocessing import Pool

def get_html(url):

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"
        }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.text
    return None


def save_data(xxxx):
    print(xxxx)
    file_output = open(f"{xxxx[0]}_output.txt", "a")
    file_input = open(f"{xxxx[0]}_input.txt", "a")
    for maincounter in range(xxxx[0], xxxx[1]):
        try:
            url = f"https://www.transfermarkt.world/liverpool-fc-montevideo/spielplandatum/verein/{maincounter + 1}"
            
            r = get_html(url)

            soup = BS(r, "lxml")
            
            budget_str = soup.find("div", class_="data-header__box--small").text
            if budget_str.split()[1] == 'тыс':
                budget_num = float(budget_str.split()[0].replace(',', '.')) / 1000
            elif budget_str.split()[1] == 'млн':
                budget_num = float(budget_str.split()[0].replace(',', '.'))
            else:
                budget_num = float(budget_str.split()[0].replace(',', '.')) * 1000

            table = soup.find("div", class_="responsive-table")

            last_matches = table.find_all("a", class_="ergebnis-link")

            if last_matches[0].find("span", class_="greentext"):
                previous_matches = [1, 0, 0]
            elif last_matches[0].find("span", class_="redtext"):
                previous_matches = [0, 0, 1]
            else:
                previous_matches = [0, 1, 0]

            points_last = 0
            ctrl = 0
            for match in last_matches[1:6]:
                if match.find("span", class_="greentext"):
                    points_last += 3
                elif match.find("span", class_="redtext"):
                    pass
                else:
                    points_last += 1

            table_str = soup.find('tr', class_='table-highlight').find_all('td', class_='zentriert')

            place = int(table_str[0].text)
            matches = int(table_str[2].text)
            rangeballs = int(table_str[3].text)
            points = int(table_str[4].text)

            place_of_match = table.find("td", class_="zentriert hauptlink").text

            if place_of_match == 'Д':
                place_of_match_id = 1
            elif place_of_match == 'Г':
                place_of_match_id = 2
            else:
                place_of_match_id = 3

            versus_id = int(table.find("td", class_="no-border-links hauptlink").find("a").get("href").split('/')[-3])

            match_info = [maincounter + 1, budget_num, points_last,
                    place, matches, rangeballs,
                    points, place_of_match_id, versus_id]

            print(f"input: {match_info}\toutput: {previous_matches}")

            file_input.write(str(match_info) + "\n")

            if len(match_info) > 8:
                file_output.write(str(previous_matches) + "\n")

        except Exception as error:
            print(error)
            continue


if __name__ == '__main__':
    ids = [[i, i + 10000] for i in range(0, 100000, 10000)]
    with Pool(10) as pool:
        pool.map(save_data, ids)