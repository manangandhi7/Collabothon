import collections
from bs4 import BeautifulSoup


def get_parts(file_name):
    with open(file_name, encoding='utf8') as f:
        html = f.read()

    text_by_part = collections.defaultdict(list)
    soup = BeautifulSoup(html, 'html.parser')

    parts = soup.select('.b_teil')
    if not parts:
        raise Exception('Could not find any parts')
    part = parts[0]

    sibling = part.find_next_sibling()
    while True:
        sibling = sibling.find_next_sibling()
        if not sibling:
            # print('Reached end of document while looking for next part')
            break
        if sibling in parts:
            # print('found part', sibling)
            part = sibling
        text_by_part[part].append(sibling)
        classes = sibling.get('class')
        if not classes:
            classes = []
            # if 'b_teil' in classes:
            #     print(sibling.get('id'))
    # for part, texts in text_by_part.items():
    #     print(part, texts)
    return text_by_part


if __name__ == '__main__':
    print(get_parts('superstars.html'))
