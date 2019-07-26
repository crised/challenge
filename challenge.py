"""
Star Wars API ETL
"""

import requests, csv
from collections import Counter, namedtuple

Person = namedtuple('Person', 'name species height appearances')


def get_top_10():
    """
    Find the 10 characters wh appear in most Star Wars films

    Returns:
        A list of 10 tuples indicating the api url
        for each character and the frequency of movie where each appears.
        [('https://swapi.co/api/people/3/', 7),...]

    """
    js = requests.get('https://swapi.co/api/films').json()['results']
    c = Counter()
    for movie in js:
        c.update(movie['characters'])
    return c.most_common(10)


def build_persons_tuple(commons):
    """
    Build a height descendant list of characters.

    Args:
        commons: A list of 10 tuples, returned by the 'get_top_10()' function.

    Returns:
        Returns a list consisting of 10 Person namedtuple. Each namedtuple
        consists of name, species, height and appearances in movies.
        The list is descendant sorted by the height of each character.

    """
    ans = []
    for person_str, appearances in commons:
        j = requests.get(person_str).json()
        ans.append(
            Person(name=j['name'],
                   species=requests.get(j['species'][0]).json()['name'],
                   height=int(j['height']),
                   appearances=appearances))
    return sorted(ans, key=lambda x: -x.height)


def write_csv_file(persons):
    """Write CSV file to disk.

    This functions write a CSV files
    with columns 'name, species, height, appearances'.


    Args:
        persons: items to write to file

    Raises:
        ValueError and TypeError if the persons argument
        is not in the correct format i.e. a list of 10
        namedTuple persons.
    """

    if len(persons) != 10:
        raise ValueError('Expected 10 characters in list',
                         'found: %s' % len(persons))

    if not isinstance(persons[0], Person):
        raise TypeError('Must supply Person namedtuple in list',
                        'found: %r' % persons)

    with open('answer.csv', mode='w') as ans_file:
        file_writer = csv.writer(ans_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['name', 'species', 'height', 'appearances'])
        for pe in persons:
            file_writer.writerow([pe.name, pe.species, pe.height, pe.appearances])


def post_to_http_bin():
    """
    POST CSV file to 'httpbin.org' server

    This functions reads the answer.csv file from the existing directory.
    Naturally, it will raise an exception is the file is not there.

    Returns:
        The status code of the request, and the response text from
        'httpbin.org' server.
    """
    with open('answer.csv') as file:
        r = requests.post("https://httpbin.org/post", files={'file': file})
    return r.status_code, r.text


def main():
    """
    Main Pipeline.

    First it find out the top 10 characters that appears in the movies.
    Then, it builds a height sorted list with the characters.
    Next, it writes these values to a CSV file.
    Finally it sends the CSV file to the 'httpbin.org' server.
    :return:
    """
    commons = get_top_10()
    results = build_persons_tuple(commons)
    write_csv_file(results)
    post_to_http_bin()


if __name__ == '__main__':
    main()
