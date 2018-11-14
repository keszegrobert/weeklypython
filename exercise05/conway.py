import unittest


class GameOfLife():
    def evolve(self, cells):
        next_generation = set()
        for cell in cells:
            if self.__should_survive(cell, cells):
                next_generation.add(cell)
            for neighbour in self.__get_neighbours(cell):
                if self.__should_become_alive(neighbour, cells):
                    next_generation.add(neighbour)
        return list(next_generation)

    def __should_become_alive(self, cell, cells):
        return cell not in cells and\
            self.__count_living_neighbours(cell, cells) == 3

    def __should_survive(self, cell, cells):
        number_of_neighbours = self.__count_living_neighbours(cell, cells)
        return number_of_neighbours == 2 or number_of_neighbours == 3

    def __count_living_neighbours(self, cell, cells):
        (x, y) = cell
        number_of_neighbours = 0
        for (dx, dy) in self.__get_neighbour_offsets():
            neighbour = (x + dx, y + dy)
            if neighbour in cells:
                number_of_neighbours += 1
        return number_of_neighbours

    def __get_neighbour_offsets(self):
        return [
            (-1,  1), (0,  1), (1,  1),
            (-1,  0),          (1,  0),
            (-1, -1), (0, -1), (1, -1),
        ]

    def __get_neighbours(self, cell):
        neighbours = []
        (x, y) = cell
        for (dx, dy) in self.__get_neighbour_offsets():
            neighbours.append((x + dx, y + dy))
        return neighbours


class GameOfLifeTest(unittest.TestCase):
    def setUp(self):
        self.game = GameOfLife()

    def test_a_sejt_elpusztul_ha_kevesebb_mint_ket_szomszedja_van(self):
        self.evolve([(0, 0)])
        self.assert_dead((0, 0))
        self.evolve([(0, 0), (1, 0)])
        self.assert_dead((0, 0))
        self.assert_dead((1, 0))

    def test_a_sejt_elve_marad_ha_2v3_szomszedja_van(self):
        self.evolve([
                    (1, 1), (2, 1),
            (0, 2), (1, 2)
        ])
        self.assert_alive((0, 2))
        self.assert_alive((1, 2))

    def test_a_sejt_meghal_ha_3nal_tobb_szomszedja_van(self):
        self.evolve([
            (0, 0), (1, 1), (2, 1),
            (0, 2), (1, 2), (2, 2)
        ])
        self.assert_dead((1, 1))
        self.assert_dead((1, 2))


    def test_harman_egyutt_szulnek_ujat(self):
        self.evolve([
                    (1, 1), (2, 1),
            (0, 2),
        ])
        self.assert_alive((1, 2))

    def evolve(self, cells):
        self.next_generation = self.game.evolve(cells)

    def assert_dead(self, cell):
        self.assertFalse(cell in self.next_generation)

    def assert_alive(self, cell):
        self.assertTrue(cell in self.next_generation)


if __name__ == '__main__':
    unittest.main()
