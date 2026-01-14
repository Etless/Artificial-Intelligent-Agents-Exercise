import a_star_algorithm as a_star

WIDTH = 6
MAP = [1, 1, 2, 2, 1, 1,
       1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 1, 1,
       1, 1,10,10, 2, 1,
       1, 1, 1, 2, 2, 1,
       1, 1, 1, 1, 1, 1,
       1, 2,10,10, 1, 1,
       1, 1, 1, 1, 1, 1,
       1,10, 1, 1, 1, 1,]

path = a_star.a_star_search(MAP, WIDTH, (1,0), (4,7))
print(path)

