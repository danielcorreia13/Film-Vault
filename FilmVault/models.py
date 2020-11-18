from myLib.baseXquerys import getFilmsSortedByYear

for mov in getFilmsSortedByYear(2, 100):
    print(mov['title'])