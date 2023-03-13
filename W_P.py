import requests
from bs4 import BeautifulSoup
from collections import defaultdict

# from time import *

url_list = []
inf_list = defaultdict(set)

for count in range(2):

    page = count * 50  # 50 title in page
    # sleep(3) it's helped to server

    url = f'''https://myanimelist.net/topanime.php?limit={page}'''  # url for title

    response = requests.get(url)

    body = BeautifulSoup(response.text, "lxml")

    name_box = body.find_all("tr", class_="ranking-list")  # class
    rank = body.find_all("td", class_="rank ac")  # rank in the top of top
    score_box = body.find_all("td", class_="score ac fs14")  # score

    # print(len(name_box), len(rank), len(score_box))

    for i, j, k in zip(name_box, rank, score_box):
        name = i.find("h3", class_="hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3").text.replace("\n", "")

        info_box = i.find("div", class_="information di-ib mt4").text.replace("\n", "").split()

        eps = info_box[1][1:] + ' eps'
        a_type = info_box[0]
        members = info_box[-2] + ' members'
        first_data = ' '.join(info_box[3:5])
        last_data = ' '.join(info_box[6:8])
        data_ = first_data + ' - ' + last_data

        score = k.find("div", class_="js-top-ranking-score-col di-ib al").text
        rank_ = j.text.replace("\n", "")
        card = i.find("a").get("href")
        url_list.append(card)

        inf_list[name] = eps, a_type, members, data_, score, rank_
        # print(rank_, name, eps, a_type, members, data_, score, sep="\n")
        # print("-------------")

    your_score_box = body.find("td", class_="your-score ac fs14")
    # your_score = your_score_box.find("span", class_="text on score-label score-na").text


def get_url(rank, *args):
    if rank == 0:
        return get_url(int(input('Введите номер аниме в топе: ')))
    elif rank > 0:
        inf_list_keys = list(inf_list.keys())

        print(inf_list_keys[rank - 1] + ' :', url_list[rank - 1])
        print(inf_list[inf_list_keys[rank - 1]])
    if rank > 0:
        return get_url(int(input('Введите номер еще одного аниме, если хотите выйти, напишите "-1": ')))
    if rank < 0:
        print('Поиск аниме завершен')


get_url(int(input('Введите номер аниме в топе: ')))
