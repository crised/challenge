"""
Unit tests.
Functions are test in isolation, not in integration.
"""

from challenge import Person, write_csv_file, post_to_http_bin, build_persons_tuple, get_top_10
from unittest import TestCase, main, SkipTest
import os


class ValidateTestCases(TestCase):
    def test_write_csv_file(self):
        file_name = 'answer.csv'
        if os.path.exists(file_name):
            os.remove(file_name)
        write_csv_file([Person(name='Chewbacca', species='Wookiee', height='228', appearances=5),
                        Person(name='Darth Vader', species='Human', height='202', appearances=4),
                        Person(name='Obi-Wan Kenobi', species='Human', height='182', appearances=6),
                        Person(name='Han Solo', species='Human', height='180', appearances=4),
                        Person(name='Luke Skywalker', species='Human', height='172', appearances=5),
                        Person(name='Palpatine', species='Human', height='170', appearances=5),
                        Person(name='C-3PO', species='Droid', height='167', appearances=6),
                        Person(name='Leia Organa', species='Human', height='150', appearances=5),
                        Person(name='R2-D2', species='Droid', height='96', appearances=7),
                        Person(name='Yoda', species="Yoda's species", height='66', appearances=5)])
        with open('answer.csv') as f:
            line = f.readline().strip().split(',')
            self.assertEqual('name', line[0])
            self.assertEqual('species', line[1])
            self.assertEqual('height', line[2])
            self.assertEqual('appearances', line[3])
            line = f.readline().strip().split(',')
            self.assertEqual('Chewbacca', line[0])
            count = 9
            for _ in f.readlines():
                count -= 1
            self.assertEqual(0, count)

    def test_write_csv_file_bad_input(self):
        with self.assertRaises(ValueError):
            write_csv_file(['bad'])

    def test_build_persons_tuple(self):
        result = build_persons_tuple([('https://swapi.co/api/people/3/', 7),
                                      ('https://swapi.co/api/people/2/', 6),
                                      ('https://swapi.co/api/people/10/', 6),
                                      ('https://swapi.co/api/people/20/', 5),
                                      ('https://swapi.co/api/people/5/', 5),
                                      ('https://swapi.co/api/people/13/', 5),
                                      ('https://swapi.co/api/people/21/', 5),
                                      ('https://swapi.co/api/people/1/', 5),
                                      ('https://swapi.co/api/people/4/', 4),
                                      ('https://swapi.co/api/people/14/', 4)])
        self.assertEqual(result[0].name, 'Chewbacca')
        self.assertEqual(result[-1].name, 'Yoda')

    def test_get_top_10(self):
        result = get_top_10()
        print(result)
        self.assertIn('3', result[0][0])
        self.assertEqual(7, result[0][1])
        self.assertIn('14', result[-1][0])

    def test_post_to_http_bin(self):
        status_code, response = post_to_http_bin()
        self.assertEqual(200, status_code)
        self.assertIn('name', response)
        self.assertIn('Chewbacca', response)
        self.assertIn('Yoda', response)


if __name__ == '__main__':
    main()
