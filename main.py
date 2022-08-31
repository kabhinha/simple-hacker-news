from bs4 import BeautifulSoup
from pathlib import Path
from pprint import pprint as Print
from datetime import datetime
import requests

def req_data():
    res = requests.get("https://news.ycombinator.com/")
    soup = BeautifulSoup(res.text, "html.parser")
    titles = soup.select(".titlelink")
    subs = soup.select(".subtext")
    return titles, subs

def filter_rec(t, s):
    new_records = []
    for ind, title in enumerate(t):
        title_link = title.get("href", None) # , default
        vote = s[ind].select(".score")
        if len(vote):
            scoring = int(vote[0].text.split()[0])
            if scoring > 100:
                new_records.append((title, title_link, s[ind], scoring))
    return new_records

def show(data, view=False):
    d = []
    for t, a, s, v in data:
        d.append((
            "title: " + t.text,
            "link: " + a,
            "Voting: " + str(v)
        ))

    d = Sort(d)
    if view:
        Print(d)
    else:
        d_save = []
        for i in d:
            rec = "\n"
            for j in i:
                rec += j+"\n"
            rec += ""
            d_save.append(rec)
        return d_save

def Save(data):
    with open(bdir / "news.txt", 'w') as f:
        d = show(data)
        today = str(datetime.now().strftime("%a -> %d/%m/%y -> %H:%M"))
        f.write(f"News for {today}\n")
        f.writelines(d)

def Sort(data):
    if type(data)!=str:
        return sorted(data, key=lambda k:k[2], reverse=True)


if __name__ == "__main__":
    bdir = Path(__file__).parent
    cho = input("Wanna see or save?(se/sa) ")
    title, subtexts = req_data()
    new_data = filter_rec(title, subtexts)
    if cho.lower()=="se":
        show(new_data, True)
    else:
        Save(new_data)
        print("done")

