import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz


def getWOS_data(author_name: str, root: str, field_names: list, pubs: list):
    result = []
    page = requests.get(root + "/authors/publication?auteur=" + author_name)
    soup = BeautifulSoup(page.content, "lxml")

    links = soup.select("p.text-primary a:first-child")

    scores = [link.parent.parent.select_one(
        "p:last-of-type small a") for link in links]

    titles = [link.string.strip() for link in links]
    urls = [link.get("href") for link in links]

    for score_index in range(len(scores)):
        score = extract_article(scores[score_index], root)
        for pub in pubs:
            if fuzz.ratio(pub["title"].upper(), titles[score_index].upper()) >= 95:
                if score is not None:
                    score["url"] = urls[score_index]
                    result.append({
                        "scholar_info": pub,
                        "WOS_info": clean_data(score, field_names)
                    })
                else:
                    score = {"url": urls[score_index]}
                    result.append({
                        "scholar_info": pub,
                        "WOS_info": clean_data(score, field_names)
                    })

                break
    return result


def clean_data(wos_obj, field_names):
    pub = {}

    for field_name in field_names:
        try:
            pub[field_name.split(':')[1]] = wos_obj[field_name]
        except IndexError:
            pub[field_name] = wos_obj[field_name]
        except KeyError:
            pass
    return pub


def extract_article(link, root: str):
    if link is not None:
        page = requests.get(root + link.get("href"))
        soup = BeautifulSoup(page.content, "lxml")
        sections = soup.select(".col-md-8 .card-body")

        link = flatten([["".join([string.strip() for string in info.get_text().split("\n")]) for info in section.select("h6")]
                        for section in sections])

    return link


def flatten(info_list: list):
    info_list = [item for sublist in info_list for item in sublist]
    info = {}

    for info_obj in info_list:
        (key, value) = info_obj.split(" :")
        info[key] = value

    return info
