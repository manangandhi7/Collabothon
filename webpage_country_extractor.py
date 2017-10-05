import html
import collections
from bs4 import BeautifulSoup
import json
import regex as re


def get_country_dict(countries):
    country_dict = {}

    for country in countries:
        country_names = []
        country_names.append(country['translations']['deu']['common'])
        country_names.append(country['name']['common'])
        country_names.extend(country['altSpellings'])
        country_names = {country_name for country_name in country_names if len(country_name) > 2}
        country_dict[country['cca3']] = country_names
    return country_dict

def write_output_file(target_file_name):
    with open('countries.json', encoding='utf8') as f:
        countries = json.load(f)

    country_dict = get_country_dict(countries)
    # german_country_names = [country['translations']['deu']['common'] for country in countries]
    english_country_names = {country['cca3']: country['name']['common'] for country in countries}

    with open(target_file_name, encoding='utf8') as f:
        file_html = f.read()

    text = file_html

    # Inject custom script
    text = text.replace('</head>', '<script src="viewer.js"></script>'
                                                  '<link rel="stylesheet" type="text/css" href="viewer.css"></link>'
                                                  '</head>', 1)

    # soup = BeautifulSoup(html, 'html.parser')
    # text = soup.getText()

    found_isos = set()

    matches = []

    country_counter = collections.defaultdict(int)
    foreign_counter = collections.defaultdict(int)

    for country_iso, country_names in country_dict.items():
        for country_name in country_names:
            country_matches = list(re.finditer(r'\b{}\b'.format(re.escape(country_name)), text))
            if not country_matches:
                continue
            for match in country_matches:
                matches.append({
                    'country_iso': country_iso,
                    'match': match
                })
                print('Found "{}" ({})'.format(country_name, country_iso))
                found_isos.add(country_iso)
                country_counter[country_iso] += 1

    matches.sort(key=lambda match: match['match'].start(), reverse=True)

    for match in matches:
        print(match['match'].start(), match['match'].group())

    for match in matches:
        found_text = match['match'].group()
        name = english_country_names[match['country_iso']]
        text = ''.join([
            text[:match['match'].start()],
            '<span class="country-match" data-match="{}" data-country-name="{}" data-country-iso="{}" data-found-text="{}">{}</span>'.format(name, name, match['country_iso'], found_text, found_text),
            text[match['match'].end():]
        ])

    print('Found countries: {}'.format(found_isos))
    print(len(found_isos))

    print(country_counter)

    country_matches = matches
    matches = []
    foreign_expressions = {'Foreign', 'Ausland', 'Niederlassung', r'außerhalb\s+Deutschlands',
                           'USD', 'US-Dollar', ' Dollar', 'Wechselkurs', 'Wechselkursrisiken'}

    for foreign_expression in foreign_expressions:
        foreign_matches = list(re.finditer(r'\b{}\b'.format(foreign_expression), text))
        if not foreign_matches:
            continue
        for match in foreign_matches:
            matches.append(match)
            foreign_counter[match.group()] += 1
            print('Found "{}"'.format(foreign_expression))

    matches.sort(key=lambda match: match.start(), reverse=True)


    for match in matches:
        found_text = match.group()
        text = ''.join([
            text[:match.start()],
            '<span class="foreign-match" data-match="{}">{}</span>'.format(match.group(), match.group()),
            text[match.end():]
        ])
    foreign_matches = matches

    text = text.replace('<body', '<body data-matches="{}"'.format(html.escape(json.dumps({
        'foreign': {match.group(): foreign_counter[match.group()] for match in foreign_matches},
        'country': {english_country_names[match['country_iso']]: country_counter[match['country_iso']] for match in country_matches}
    })).replace('"', '\\"')))

    out_file_name = 'out_{}'.format(target_file_name)

    print('Writing to "{}"'.format(out_file_name))

    with open(out_file_name, 'w', encoding='utf8') as f:
        f.write(text)


if __name__ == '__main__':
    for target_file_name in ['3bscientific-web_page.html', 'superstars.html']:
        write_output_file(target_file_name)
