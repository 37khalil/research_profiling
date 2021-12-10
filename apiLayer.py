import requests


def get_scopus_data(api_endpoint, headers, field_names, pubs):
    publications = []
    for pub in pubs:
        response = requests.get(
            api_endpoint + '?query=TITLE("' + pub["scholar_info"]["title"] + '")&count=1', headers=headers)

        if "dc:title" in response.json()["search-results"]["entry"][0] and response.json()["search-results"]["entry"][0]["dc:title"].upper() == pub["scholar_info"]["title"].upper():
            pub["scopus_info"] = clean_data(
                response.json()["search-results"]["entry"][0], field_names)
            publications.append(pub)

    return publications


def clean_data(scopus_obj, field_names):
    pub = {}

    for field_name in field_names:
        try:
            pub[field_name.split(':')[1]] = scopus_obj[field_name]
        except IndexError:
            pub[field_name] = scopus_obj[field_name]
        except KeyError:
            pass
    return pub
