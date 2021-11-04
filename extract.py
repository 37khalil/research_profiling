import json
import time
from scholarly import scholarly, ProxyGenerator
from apiLayer import get_scopus_data

config = json.load(open('app-config.json', ))
pg = ProxyGenerator()
success = pg.FreeProxies()
scholarly.use_proxy(pg)


def clean_author(author_obj, field_names, bib_names, scholar_pub_names):
    author = {}
    scrap_scholar_pubs(author_obj, bib_names, scholar_pub_names)

    # # author_obj["publications"] = [pub["bib"]["title"]
    # #                               for pub in author_obj["publications"]]

    for field in field_names:
        author[field] = author_obj[field]

    return author


def scrap_scholar_pubs(author_obj, bib_names, scholar_pub_names):
    for pub in author_obj["publications"]:
        scholar_info = scholarly.fill(pub)
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

        pub = info
        pub["author"] = pub["author"].split("and")


def scholar_scrap(author_name, field_names, bib_names, scholar_pub_names):
    author = clean_author(scholarly.fill(next(
        scholarly.search_author(author_name)
    )
    ), field_names, bib_names, scholar_pub_names)

    return author


author = scholar_scrap(
    "imad hafidi",
    config["scholar"]["scholar_profil_fields"],
    config["scholar"]["scholar_bib_fields"],
    config["scholar"]["scholar_pub_fields"]
)
# author["publications"] = get_scopus_data(
#     config["scopus"]["api_endpoint"],
#     config["scopus"]["headers"],
#     config["scopus"]["fields"],
#     author["publications"]
# )

# scrap_scholar_pubs(
#     author,
#     config["scholar"]["scholar_bib_fields"],
#     config["scholar"]["scholar_pub_fields"]
# )

with open("output/" + author["scholar_id"] + ".json", "w", encoding="UTF-8") as file:
    json.dump(author, file)

# file.write(str(str(json.dumps(author)).encode('UTF-8')))
