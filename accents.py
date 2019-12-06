
# -*- coding: utf-8 -*-

import unicodedata

""" Normalise (normalize) unicode data in Python to remove umlauts, accents etc. """

fr = open('16-17.txt', 'r')
l = fr.readline()
print(l)
l = unicodedata.normalize('NFKD', l)
print(l)
print(str(l))
exit(0)
data = 'naïve café\naaaa'
normal = unicodedata.normalize('NFKD', data)
normal = str(normal)
normal = normal.replace('\n', '')
print(normal)

# prints "naive cafe"