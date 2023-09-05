import requests
from bs4 import BeautifulSoup as BS
import keras


def get_html(url):

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"
        }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.text
    return None


def get_search_datas(file, file_copy, home, away):
    datas = list()
    for row in file:
        parce = row.strip('[]').replace(' ', '').replace(']\n', '').split(',')
        if int(parce[0]) == home:
            for i in range(8):
                datas.append(parce[i])
    for row_new in file_copy:
        parce_copy = row_new.strip('[]').replace(' ', '').replace(']\n', '').split(',')
        if int(parce_copy[0]) == away:
            for i in range(7):
                datas.append(parce_copy[i])
        # for row_new in file_copy:
        #     parce_copy = row_new.strip('[]').replace(' ', '').replace(']\n', '').split(',')
        #     if parce[8] == parce_copy[0]:
        #         for i in range(6):
        #             parce.append(parce_copy[i + 1])
        # file_copy.seek(0)
        # datas.append(parce)
    return datas


def get_date_url():
    req = get_html('https://www.transfermarkt.world/ticker/index/live')
    soup = BS(req, 'html.parser')
    datas = soup.find('div', class_='kalender-wrapper').find_all('a', href=True)
    datas = [a['href'] for a in datas]
    return datas


def reconstuctor(parce):
    for p in parce:
        p.pop(0)
        p.pop(7)
        p.pop(2)
        p.pop(8)
        p[2] = float(p[4]) / float(p[2])
        p[8] = float(p[10]) / float(p[8])
        p.pop(3)
        p.pop(8)
        p.pop(3)
        p.pop(7)
        p[0] = float(p[0]) / 1050
        p[1] = float(p[1]) / 15
        p[2] = float(p[2]) / 3
        p[3] = float(p[3]) / 3
        p[4] = float(p[4]) / 1050
        p[5] = float(p[5]) / 15
        p[6] = float(p[6]) / 3
    return parce


def set(date):
    url = f"https://www.transfermarkt.world/live/index?datum={date}"
    r = get_html(url)
    soup = BS(r, "html.parser")
    team_home = list()
    team_away = list()
    url_team = list()
    score = list()
    match_info = list()
    text_date = list()

    matches_all_h = soup.find_all("td", class_='club verein-heim')
    all_score = soup.find_all("td", class_='ergebnis')
    matches_all_a = soup.find_all("td", class_='club away verein-gast')
    all_info = soup.find_all("td", class_="zeit hide-for-small")
    input = list()

    model_loaded = keras.models.load_model('model')
    # datas = get_search_datas(open('000_input.txt'), open('000_input.txt'))
    for i in range(len(all_score)):
        flag = 0
        url_team = (matches_all_h[i].find('a', href=True)["href"]).split('/')
        url_team1 = int(url_team[4])
        url_away = (matches_all_a[i].find('a', href=True)["href"]).split('/')
        url_away1 = int(url_away[4])
        datas = get_search_datas(open('000_input.txt'), open('000_input.txt'), url_team1, url_away1)

        if len(datas) > 10:
            match_info.append(all_info[i].text.strip())
            team_home.append(matches_all_h[i].text.strip())
            score.append(all_score[i].text.strip())
            team_away.append(matches_all_a[i].text.strip())
            text_date.append(date)
            input.append(datas)


    prep = reconstuctor(input)
    print(prep)
    pred = model_loaded.predict(prep[:len(prep)])
    print(pred)

    print(input)
    print(team_home)
    print(team_away)
    print(score)
    print(match_info)
    print(url_team)
    row = list()
    templ1 = list()
    templ2 = list()
    templ3 = list()
    row.append(match_info)
    row.append(team_home)
    row.append(score)
    row.append(team_away)

    for i in range(len(pred)):
        templ1.append("%.2f" % (pred[i][0] * 100))
        templ2.append("%.2f" % (pred[i][1] * 100))
        templ3.append("%.2f" % (pred[i][2] * 100))

    row.append(templ1)
    row.append(templ2)
    row.append(templ3)
    row.append(text_date)
    row_table = list()
    for i in range(len(team_home)):
        fff = list()
        for j in range(8):
            fff.append(row[j][i])
        with open('text_datas.txt', 'a', encoding='utf-8') as file:
            file.write(str(fff) + '\n')
        row_table.append(fff)

    return None


if __name__ == '__main__':

    with open('text_datas.txt', 'r+') as file:
        file.truncate()
    row_table = list()
    dates = get_date_url()
    for c in range(len(dates)):
        dates[c] = dates[c].replace('/live/index?datum=', '')
    set(dates[9])
    for xxxx in range(20):
        try:
            set(dates[xxxx])
        except Exception:
            continue