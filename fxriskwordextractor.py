import partextractor

search_terms = {'USD', 'US-Dollar', 'Wechselkurs'}


def nodes_to_text(nodes):
    return '\n'.join(node.getText() for node in nodes)


def get_keywords_in_part(nodes):
    text = nodes_to_text(nodes)
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if any(search_term in line for search_term in search_terms):
            lines.append(line)
    return lines


parts = partextractor.get_parts('superstars.html')

for part, nodes in parts.items():
    lines = get_keywords_in_part(nodes)
    if lines:
        print('Found in {}:'.format(part.getText()))
        print('\n'.join(lines))
