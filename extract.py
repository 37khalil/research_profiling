import os
import json
import time
from scholarly import scholarly, ProxyGenerator
from apiLayer import get_scopus_data
from WOS import getWOS_data

if not os.path.exists("output/"):
    os.makedirs("output/")

config = json.load(open('app-config.json', ))


def clean_author(author_obj, field_names, bib_names, scholar_pub_names):
    author = {}
    scrap_scholar_pubs(author_obj, bib_names, scholar_pub_names)

    for field in field_names:
        author[field] = author_obj[field]

    return author


def scrap_scholar_pubs(author_obj, bib_names, scholar_pub_names):
    for pub_index in range(len(author_obj["publications"])):
        scholar_info = scholarly.fill(author_obj["publications"][pub_index])
        info = {}

        for bib_name in bib_names:
            try:
                info[bib_name] = scholar_info["bib"][bib_name]
            except KeyError:
                pass

        for name in scholar_pub_names:
            try:
                info[name] = scholar_info[name]
            except KeyError:
                pass

        info["author"] = info["author"].split("and")
        author_obj["publications"][pub_index] = info


def scholar_scrap(author_name, field_names, bib_names, scholar_pub_names):
    author = clean_author(scholarly.fill(next(
        scholarly.search_author(author_name)
    )
    ), field_names, bib_names, scholar_pub_names)

    return author


# Scholar
author = scholar_scrap(
    "imad hafidi",
    config["scholar"]["scholar_profil_fields"],
    config["scholar"]["scholar_bib_fields"],
    config["scholar"]["scholar_pub_fields"]
)

# WOS
author["publications"] = getWOS_data(
    author["name"],
    config["WOS"]["root"],
    config["WOS"]["fields"],
    author["publications"]
)

# Scopus
author["publications"] = get_scopus_data(
    config["scopus"]["api_endpoint"],
    config["scopus"]["headers"],
    config["scopus"]["fields"],
    author["publications"]
)

with open("output/" + author["scholar_id"] + ".json", "w", encoding="UTF-8") as file:
    json.dump(author, file, ensure_ascii=False)
