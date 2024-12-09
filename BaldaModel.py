import random


class BaldaModel:
    def __init__(self, size=5, dictionary=None):
        if size < 5:
            raise ValueError("Размер игрового поля должен быть не менее 5.")
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.current_player = 1
        self.pass_count = 0
        self.dictionary = set()
        self.words_used = set()
        self.game_over = False
        self.initial_word = "БАЛДА"
        self.place_initial_word()

    def place_initial_word(self):
        center_row = self.size // 2
        start_col = (self.size - len(self.initial_word)) // 2
        for idx, letter in enumerate(self.initial_word):
            self.grid[center_row][start_col + idx] = letter
        self.words_used.add(self.initial_word)
        self.pass_count = 0
        self.current_player = 1

    def add_letter(self, row, col, letter):
        letter = letter.upper()
        if not letter.isalpha() or len(letter) != 1:
            print(f"Неверный ввод: '{letter}'. Нужна одна буква.")
            return False

        if not (0 <= row < self.size and 0 <= col < self.size):
            print(f"Позиция ({row}, {col}) вне границ поля.")
            return False

        if self.grid[row][col]:
            print(f"Позиция ({row}, {col}) уже занята буквой '{self.grid[row][col]}'.")
            return False

        self.grid[row][col] = letter
        self.pass_count = 0
        self.check_game_over()
        self.switch_player()
        return True

    def add_word(self, word, positions):
        word = word.upper()
        if not self.is_valid_word(word):
            print(f"Слово '{word}' невалидно или уже использовано.")
            return False

        for (letter, (row, col)) in zip(word, positions):
            if not (0 <= row < self.size and 0 <= col < self.size):
                print(f"Позиция ({row}, {col}) вне границ поля.")
                return False
            if self.grid[row][col] and self.grid[row][col] != letter:
                print(f"Позиция ({row}, {col}) уже занята буквой '{self.grid[row][col]}'.")
                return False
            self.grid[row][col] = letter

        self.words_used.add(word)
        self.pass_count = 0
        self.check_game_over()
        self.switch_player()
        return True

    def is_valid_word(self, word):
        word = word.upper()
        return word in self.dictionary and word not in self.words_used

    def pass_turn(self):
        self.pass_count += 1
        if self.pass_count >= 2:
            self.game_over = True
        else:
            self.switch_player()

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def get_current_player(self):
        return self.current_player

    def is_game_over(self):
        return self.game_over or self.is_grid_full()

    def is_grid_full(self):
        return all(self.grid[row][col] != '' for row in range(self.size) for col in range(self.size))

    def check_game_over(self):

        if self.is_grid_full() or self.pass_count >= 2:
            self.game_over = True

    def get_grid(self):
        return self.grid

    def reset_game(self):
        self.grid = [['' for _ in range(self.size)] for _ in range(self.size)]
        self.words_used.clear()
        self.game_over = False
        self.place_initial_word()
