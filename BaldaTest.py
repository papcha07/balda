import unittest

from BaldaModel import BaldaModel


class TestBaldaGameModel(unittest.TestCase):
    def setUp(self):

        self.dictionary = {
            'КОТ', 'СОК', 'ТОК', 'КОНОК', 'КОРОВА', 'БАЛДА',
            'МАМА', 'ПАПА', 'ДОМ', 'НОМА', 'ТЕСТ', 'СТОЛ',
            'ЛЕС', 'ГОРОД', 'РЕКА', 'МОСТ', 'ЗОНА', 'МАШИНА'
        }
        self.model = BaldaModel(dictionary=self.dictionary)


    def test_add_letter_invalid_position(self):
        result = self.model.add_letter(-1, 0, 'К')
        self.assertFalse(result)
        result = self.model.add_letter(0, 10, 'К')
        self.assertFalse(result)

    def test_add_letter_already_occupied(self):
        center_row = self.model.size // 2
        start_col = (self.model.size - len("БАЛДА")) // 2
        result = self.model.add_letter(center_row, start_col, 'К')  # Перезапись первой буквы "Б"
        self.assertFalse(result)

        test_char0 = self.model.add_letter(0,0,'А')
        test_char1 = self.model.add_letter(0,0,'Б')
        self.assertFalse(test_char1)

    def test_add_letter_invalid_input(self):
        result = self.model.add_letter(0, 0, 'AB')
        self.assertFalse(result)
        result = self.model.add_letter(0, 0, '1')
        self.assertFalse(result)
        result = self.model.add_letter(0, 0, '@')
        self.assertFalse(result)
        result = self.model.add_letter(0,0,'А')
        self.assertTrue(result)

    def test_pass_turn(self):
        self.model.pass_turn()
        self.assertEqual(self.model.pass_count, 1)
        self.assertEqual(self.model.current_player, 2)
        self.assertFalse(self.model.is_game_over())
        self.model.pass_turn()
        self.assertEqual(self.model.pass_count, 2)
        self.assertTrue(self.model.is_game_over())

    def test_is_game_over_when_grid_is_full(self):
        for row in range(self.model.size):
            for col in range(self.model.size):
                self.model.add_letter(row, col, 'А')
        self.assertTrue(self.model.is_game_over())

    def test_add_word_valid(self):
        result = self.model.add_word('КОТ', [(2, 2), (2, 3), (2, 4)])
        self.assertTrue(result)

    def test_add_word_invalid(self):
        result = self.model.add_word('НЕИЗВЕСТНОЕ', [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])
        self.assertFalse(result)

        self.model.add_word('КОТ', [(2, 2), (2, 3), (2, 4)])
        result = self.model.add_word('КОТ', [(1, 1), (1, 2), (1, 3)])
        self.assertFalse(result)






