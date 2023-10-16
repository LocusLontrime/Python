import json
import re

from contextlib import closing
from six.moves.urllib.error import HTTPError
from six.moves.urllib.request import urlopen

from six import (
    binary_type
)


class PbnNotFoundError(Exception):
    """Raised when trying to reach webpbn puzzle by non-existing id"""


def _get_utf8(string):
    if isinstance(string, binary_type):
        return string.decode('utf-8', errors='ignore')

    return string


class NonogramsOrg(object):
    """
    Grab the puzzles from http://www.nonograms.org/
    or http://www.nonograms.ru/
    """

    URLS = [
        'http://www.nonograms.ru/',
        'http://www.nonograms.org/',
    ]

    def __init__(self, _id, colored=False, url=None):
        self._id = _id
        self.colored = colored
        self.url = url or self.URLS[0]

    def _puzzle_url(self):
        if self.colored:
            path = 'nonograms2'
        else:
            path = 'nonograms'

        return '{}{}/i/{}'.format(self.url, path, self._id)

    def _puzzle_html(self, colored=None, try_other=True):
        if colored is not None:
            self.colored = colored

        url = self._puzzle_url()
        try:
            with closing(urlopen(url)) as page:
                return page.read()  # pylint: disable=no-member
        except HTTPError as ex:
            if ex.code != 404:
                raise

            if try_other:
                return self._puzzle_html(colored=not colored, try_other=False)

            raise PbnNotFoundError(self._id)

    CYPHER_RE = re.compile(r'var[\s]+d\s*=\s*(\[[0-9,\[\]\s]+\]);')

    def _puzzle_cypher(self):
        html = _get_utf8(self._puzzle_html())
        match = self.CYPHER_RE.search(html)
        if not match:
            raise PbnNotFoundError(self._id, 'Not found puzzle in the HTML')

        return json.loads(match.group(1))

    # pylint: disable=invalid-name
    @classmethod
    def decipher(cls, cyphered):
        """
        Reverse engineered version of the part of the script
        http://www.nonograms.org/js/nonogram.min.059.js
        that produces a nonogram solution for given cyphered solution
        (it can be found in puzzle HTML in the form 'var d=[...]').
        """
        x = cyphered[1]
        width = x[0] % x[3] + x[1] % x[3] - x[2] % x[3]

        x = cyphered[2]
        height = x[0] % x[3] + x[1] % x[3] - x[2] % x[3]

        x = cyphered[3]
        colours_number = x[0] % x[3] + x[1] % x[3] - x[2] % x[3]

        colours = []
        x = cyphered[4]
        for i in range(colours_number):
            colour_x = cyphered[i + 5]

            a = colour_x[0] - x[1]
            b = colour_x[1] - x[0]
            c = colour_x[2] - x[3]
            # unknown_flag = color_x[3] - a - x[2]

            rgb = hex(a + 256)[3:] + hex((b + 256 << 8) + c)[3:]
            colours.append(rgb)

        solution = [[0] * width for _ in range(height)]

        a = colours_number + 5
        x = cyphered[a]
        solution_size = x[0] % x[3] * (x[0] % x[3]) + x[1] % x[3] * 2 + x[2] % x[3]

        x = cyphered[a + 1]
        for i in range(solution_size):
            y = cyphered[a + 2 + i]
            vv = y[0] - x[0] - 1

            for j in range(y[1] - x[1]):
                v = j + vv
                solution[y[3] - x[3] - 1][v] = y[2] - x[2]

        return [colours, solution]

    def definition(self):
        """
        Return the definition of the puzzle
        in form of final solution
        """
        cypher = self._puzzle_cypher()
        return self.decipher(cypher)

    def parse(self):
        """
        Find and parse the colors and solution of
        a 'nonograms.org' puzzle by id
        """
        colours, solution = self.definition()
        print(f'colors: {colours}')
        print(f'solution: {solution}')
        colours_dict = {i: colour for i, colour in enumerate(colours, 1)}
        colours_dict[0] = f'ffffff'
        print(f'colours_dict: {colours_dict}')
        # building row and column clues:
        # 1. row clues:
        row_clues = []
        mi = len(solution[0])
        for j, row in enumerate(solution):
            clue = []
            i = 0
            while i < mi:
                temp_i = i
                while i < mi and row[i] == row[temp_i]:
                    i += 1
                if row[i - 1] > 0:
                    clue.append((i - temp_i, row[i - 1]))
            row_clues.append(tuple(clue))
        row_clues = tuple(row_clues)
        print(f'row_clues: {row_clues}')
        # 2. column_clues:
        column_clues = []
        zipped_solution = list(zip(*solution))
        mi = len(zipped_solution[0])
        for j, row in enumerate(zipped_solution):
            clue = []
            i = 0
            while i < mi:
                temp_i = i
                while i < mi and row[i] == row[temp_i]:
                    i += 1
                if row[i - 1] > 0:
                    clue.append((i - temp_i, row[i - 1]))
            column_clues.append(tuple(clue))
        column_clues = tuple(column_clues)
        print(f'column_clues: {column_clues}')

        return (column_clues, row_clues), colours_dict

    @classmethod
    def read(cls, _id, colored=False):
        """
        Search for puzzle on any of available http://www.nonograms.* sites
        """
        for index, base_url in enumerate(cls.URLS):
            try:
                return cls(_id, colored=colored, url=base_url).parse()
            except PbnNotFoundError:
                if index == len(cls.URLS) - 1:  # raise if no other choices
                    raise



