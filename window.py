import tkinter.messagebox

import requests
from bs4 import BeautifulSoup as BS
from tkinter import ttk
from tkinter import *


def get_html(url):

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"
        }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.text
    return None


def get_date_url():
    req = get_html('https://www.transfermarkt.world/ticker/index/live')
    soup = BS(req, 'html.parser')
    dates = soup.find('div', class_='kalender-wrapper').find_all('a', href=True)
    dates = [a['href'] for a in dates]
    for i in range(len(dates)):
        dates[i] = dates[i].replace('/live/index?datum=', '')
    return dates


def sets(date):
    rowss1 = list()
    resp = requests.get("http://ovz1.j18020789.m1yvm.vps.myjino.ru/datas")
    file = resp.json()
    print(file)
    for row in file:
        if row[-1] == date:
            rowss1.append(row[:-1])
    return rowss1


def get_text_date(dates):
    list_text = list()
    for i in range(len(dates)):
        short_list = list()
        text_date = dates[i].split('-')
        short_list.append(text_date[2])
        if text_date[1] == '01':
            short_list.append('января')
        elif text_date[1] == '02':
            short_list.append('февраля')
        elif text_date[1] == '03':
            short_list.append('марта')
        elif text_date[1] == '04':
            short_list.append('апреля')
        elif text_date[1] == '05':
            short_list.append('мая')
        elif text_date[1] == '06':
            short_list.append('июня')
        elif text_date[1] == '07':
            short_list.append('июля')
        elif text_date[1] == '08':
            short_list.append('августа')
        elif text_date[1] == '09':
            short_list.append('сентября')
        elif text_date[1] == '10':
            short_list.append('октября')
        elif text_date[1] == '11':
            short_list.append('ноября')
        else:
            short_list.append('декабря')

        short_list.append(text_date[0])
        list_text.append(str(f"{short_list[0]} {short_list[1]} {short_list[2]}"))
    print(list_text)
    return list_text


def get_prep():

    def sort(col, reverse):
        l = [(float(tree.set(k, col)), k) for k in tree.get_children("")]
        l.sort(reverse=reverse)
        for index, (_, k) in enumerate(l):
            tree.move(k, "", index)
        tree.heading(col, command=lambda: sort(col, not reverse))
        return None


    try:
        window = Tk()
        window.title(f"Прогнозы на {lang.get()}")
        row_table = sets(lang.get())
        columns = (row_table[0], row_table[1], row_table[2], row_table[3],
                   row_table[4], row_table[5], row_table[6])
        tree = ttk.Treeview(window, columns=columns, show="headings")
        tree.grid(row=0, column=0, sticky='news')

        tree.heading(row_table[0], text="Стадия турнира")
        tree.heading(row_table[1], text="Команда 1")
        tree.heading(row_table[2], text="Счет/время")
        tree.heading(row_table[3], text="Команда 2")
        tree.heading(row_table[4], text="П1", command=lambda: sort(4, False))
        tree.heading(row_table[5], text="Н", command=lambda: sort(5, False))
        tree.heading(row_table[6], text="П2", command=lambda: sort(6, False))

        tree.column('#1', anchor='n', width=200)
        tree.column('#2', anchor='n', width=150)
        tree.column('#3', anchor='n', width=80)
        tree.column('#4', anchor='n', width=150)
        tree.column('#5', anchor='n', width=40)
        tree.column('#6', anchor='n', width=40)
        tree.column('#7', anchor='n', width=40)

        for ones in row_table:
            tree.insert("", 'end', values=ones)

        scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='news')
    except:
        window.destroy()
        tkinter.messagebox.showinfo(title='Ошибка', message='Отсутствуют данные для прогнозов на выбранный день')


if __name__ == '__main__':
    dates = get_date_url()
    dates_text = get_text_date(dates)
    root = Tk()
    root.title("Прогнозы на матчи")

    position = {'padx':3, 'pady':3, 'anchor':NW}

    lang = StringVar()

    frame_info = Frame(width=1)
    frame_info.grid(row=0, column=0)
    frame_info2 = Frame(width=1)
    frame_info2.grid(row=2, column=0)
    frame_dates = Frame(width=1)
    frame_dates.grid(row=1, column=0, pady=14)
    header = ttk.Label(frame_info, text="Выберите дату матчей", font='Arial 14')
    header.grid(row=0, column=0)

    buttn = Button(frame_info2, text='Получить прогноз', command=get_prep)
    buttn.grid(row=0, column=0, sticky='e')

    for i in range(len(dates)):
        lang_btn = ttk.Radiobutton(frame_dates, text=dates_text[i], value=dates[i], variable=lang)
        if i < 5:
            lang_btn.grid(row=0, column=i, padx=7, pady=4)
        elif i < 10:
            lang_btn.grid(row=1, column=i-5, padx=4, pady=4)
        elif i < 15:
            lang_btn.grid(row=2, column=i-10, padx=4, pady=4)
        else:
            lang_btn.grid(row=3, column=i-15, padx=4, pady=4)

    root.mainloop()
