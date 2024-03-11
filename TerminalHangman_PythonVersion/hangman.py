import random

class colors:
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
class Hangman:
    def __init__(self, lines, a, b):
        self.rand_num = lines[random.randint(a, b)]
        self.ls_word_hint = self.rand_num.split(",")
        self.word = self.ls_word_hint[0].lower()
        self.hint = self.ls_word_hint[1]
        self.guesses = []
        self.wrongmoves = 0
        self.hang_man = [
            """
              ___
              |   |
                  |
                  |
                  |
                  |
            __|
            """,
            """
              ___
              |   |
              O   |
                  |
                  |
                  |
            __|
            """,
            """
              ___
              |   |
              O   |
              |   |
                  |
                  |
            __|
            """,
            """
              ___
              |   |
              O   |
             /|   |
                  |
                  |
            __|
            """,
            """
              ___
              |   |
              O   |
             /|\\  |
                  |
                  |
            __|
            """,
            """
              ___
              |   |
              O   |
             /|\\  |
             /    |
                  |
            __|
            """,
            """
              ___
              |   |
              O   |
             /|\\  |
             / \\  |
                  |
            __|
            OHH NOO!! YOU DIED
            """
        ]

    def guess(self, guess_char):
        if guess_char in self.guesses:
            print(colors.fg.orange,"Character already guessed!!")
        else:
            self.guesses.append(guess_char)
        if guess_char not in self.word:
            self.wrongmoves += 1

    def display_word(self):
        display = ''
        for letter in self.word:
            if letter in self.guesses:
                display += letter
            else:
                display += '_'
        print(display)

    def word_guessed(self):
        return set(self.word) <= set(self.guesses)

    def display_game(self):
        if self.wrongmoves > 0:
            if self.wrongmoves == 7 and not self.word_guessed():
                print(self.hang_man[6])  # Print the last hangman illustration if the player loses
            else:
                print( colors.fg.red,self.hang_man[self.wrongmoves-1])


class EasyHangman(Hangman):
    def __init__(self, lines):
        super().__init__(lines, 0, 19)

    def guess(self, guess_char):
        super().guess(guess_char)

    def display_word(self):
        super().display_word()

    def display_game(self):
        super().display_game()


class MediumHangman(Hangman):
    def __init__(self, lines):
        super().__init__(lines, 20, 39)

    def guess(self, guess_char):
        super().guess(guess_char)

    def display_word(self):
        super().display_word()

    def display_game(self):
        super().display_game()


class HardHangman(Hangman):
    def __init__(self, lines):
        super().__init__(lines, 40, 59)

    def guess(self, guess_char):
        super().guess(guess_char)

    def display_word(self):
        super().display_word()

    def display_game(self):
        super().display_game()


def score(name, wrongmoves):
    default_score = 60
    final_score = default_score - (wrongmoves * 10)
    score_file_path = "highscore.txt"
    print(colors.fg.pink,"Your Score:",final_score)
    with open(score_file_path, "r+") as score_file:
        content = score_file.readlines()
        contentsplit = [i.split(",") for i in content]
        found = False

        for i in range(len(contentsplit)):
            if contentsplit[i][0] == name:
                found = True
                if int(contentsplit[i][1]) < final_score:
                    contentsplit[i][1] = str(final_score)
                    print(colors.fg.green,"Your Highest score:", final_score)
                else:
                    print(colors.fg.green,"Your Highest score:", contentsplit[i][1])

        if not found:
            contentsplit.append([name, str(final_score)])
            print("Your Highest score:", final_score)

        # Rewind the file pointer to the beginning
        score_file.seek(0)

        # Clear the file content
        score_file.truncate()

        # Write the updated scores back to the file
        for entry in contentsplit:
            # Check if entry has expected number of elements
            if len(entry) == 2:
                score_file.write(f"{entry[0]},{entry[1]}\n")


# Main
f = open("wordhint.txt", "r")
lines = f.readlines()
f.close()

print(colors.fg.purple,"Welcome to hangman!!")
print(colors.fg.orange,"Enter player name:")
name = input()
print(colors.fg.blue,"Choose the difficulty level:")
print(colors.fg.cyan,"For Easy, enter 1")
print(colors.fg.cyan,"For Medium, enter 2")
print(colors.fg.cyan,"For Hard, enter 3")
level = int(input("Enter your choice: "))

if level == 1:
    game = EasyHangman(lines)
elif level == 2:
    game = MediumHangman(lines)
elif level == 3:
    game = HardHangman(lines)

while game.wrongmoves <= 7:
    print(colors.fg.yellow,"Hint:", game.hint)
    game.display_word()
    print(colors.fg.red,"Wrong Moves:", game.wrongmoves)
    game.display_game()

    if game.wrongmoves == 7 and not game.word_guessed():
        print(colors.fg.red,"You Lost!!")
        print(colors.fg.green,"Word:", game.word)
        score(name, game.wrongmoves)
        break

    print(colors.fg.purple,"Enter your guess:")
    guess_char = input().lower()

    while len(guess_char) != 1:
        print(colors.fg.red,"Please enter a valid character!")
        guess_char = input().lower()

    game.guess(guess_char)

    if game.word_guessed():
        print(colors.fg.green,"Congratulations! You guessed the word:", game.word)
        score(name, game.wrongmoves)
        break
