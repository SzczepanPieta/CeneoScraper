from requests import get, codes
from bs4 import BeautifulSoup
import json

def get_element(ancestor, selector=None, attribute = None, return_list = False):
    try:
        if return_list:
            return [tag.text.strip() for tag in opinion.select(selector)]  
        if not selector and attribute:
            return ancestor[attribute]
        if attribute:
             return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except (AttributeError, TypeError):
        return None

selectors = {
    "id": [None, "data-entry-id"],
    "author":["span.user-post__author-name"],
    "recomendation":["span.user-post__author-recomendation > em"],
    "stars":["span.user-post__score-count"],
    "content":[ "div.user-post__text"],
    "pros":["div.review-feature__title--positives ~ div.review-feature__item"],
    "cons":["div.review-feature__title--negatives ~ div.review-feature__item"],
    "upvote":["button.vote-yes","data-total-vote"],
    "downvote":["button.vote-no","data-total-vote"],
    "posted":["span.user-post__published > time:nth-child(1)","datetime"],
    "purchased":["span.user-post__published > time:nth-child(2)","datetime"],
}

product_code="36991221"
url=f"https://www.ceneo.pl/{product_code}#tab=reviews"
all_opinions = []
while url:
    print(url)
    response = get(url)
    if response.status_code == codes['ok']:
        page_dom=BeautifulSoup(response.text, "html.parser")
        opinions = page_dom.select("div.js_product-review")
        for opinion in opinions:
            single_opinion = {}
            for key, value in selectors.items():
                single_opinion[key] = get_element(opinion, *value)
            all_opinions.append(single_opinion)
    try:
        url = "https://www.ceneo.pl" + get_element(page_dom, "a.pagination__next", "href")
    except TypeError:
        url = None
with open(f"./opinions/{product_code}.json","w", encoding="UTF-8") as jf:    
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
           
