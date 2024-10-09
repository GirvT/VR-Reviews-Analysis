'''
| Object      | Div Class     | Content Type | Content Class    |
|-------------|---------------|--------------|------------------|
| Review Page | c9QyIf        |              |                  |
| Review Entry| jxjCjc        |              |                  |
| Name        | TSUbDb        | a            |                  |
| Num Reviews | FGlxyd        | a            | Msppse           |
| Stars       | PuaHbe        | span         | lTi8oc z3HNkc    |
| Date        | PuaHbe        | span         | dehysf lTi8oc    |
| Review      | Jtu6Td        | span         | review-full-text |
| Likes       | GmO6pf        | span         | QWOdjf           |
| Responce    | v6zSSb lororc | span         | d6SCIc           |
'''
from bs4 import BeautifulSoup
import re
import pandas as pd

open_link = "page_source_sandbox.html"
write_link = "sandbox_reviews.csv"

with open(open_link, encoding="utf8") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

review_soup = soup.find("div", {"class": "c9QyIf"})
review_entries = review_soup.find_all("div", {"class": "WMbnJf vY6njf gws-localreviews__google-review"})

reviews_list = list()
for entry in review_entries:
    name = entry.find("div", {"class": "TSUbDb"}).find("a").contents[0]
    print(name)
    try:
        num_reviews = re.findall("(?<=>)([0-9]+)(?= review)",
                                str(entry.find("a", {"class": "Msppse"}).contents[0]))[0]
    except:
        num_reviews = None
    print(num_reviews)
    stars = entry.find("span", {"class": "lTi8oc z3HNkc"})["aria-label"]
    print(stars)
    date = entry.find("span", {"class": "dehysf lTi8oc"}).contents[0]
    print(date)       
    try:
        review_body = re.findall("(?<=>)([A-Za-z0-9 _.,!?%&@*\"'\/$()+â€¦™-]+)(?=<\/span>)",
                                 str(entry.find("div", {"class": "Jtu6Td"}).find_all("span")[0]))[0]
    except:
        review_body = None
    print(review_body)
    try:
        likes = entry.find("span", {"class": "QWOdjf"}).contents[0]
    except:
        likes = None
    print(likes)
    try:
        responce = str(entry.find("span", {"class": "d6SCIc"}).contents).replace("<br/>", "").replace(" , ", "").replace(",,","")[2:-2]
    except:
        responce = None
    print(responce)
    new_row = {'Name':name,
               'Number of Reviews':num_reviews,
               'Stars Given':stars,
               'Relative Date':date,
               'Review':review_body,
               'Likes':likes,
               'Responce':responce}
    reviews_list.append(new_row)

reviews_df = pd.DataFrame.from_dict(reviews_list)
reviews_df.to_csv(write_link, index=False)

