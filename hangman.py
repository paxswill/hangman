#!/usr/bin/env python3
import argparse
import enum
import random


class GameState(enum.Enum):

    INPROGRESS = 0

    LOST = 1

    WON = 2


class GameFinished(Exception): pass


class Game(object):

    default_guesses = 7

    def __init__(self, num_guesses=default_guesses, word_list=None):
        self.num_guesses = num_guesses
        if word_list is None:
            with open('/usr/share/dict/words', 'r') as words:
                word_list = [w if w[-1] != '\n' else w[:-1] for w in words]
        self.word_list = list(word_list)
        self.reset()

    def reset(self):
        self.word = random.choice(self.word_list)
        self._wrong_guesses = set()
        self.letters = list([None for _ in range(len(self.word))])
        # Spaces are special-cased
        if ' ' in self.word:
            self.guess(' ')
        self.state = GameState.INPROGRESS

    @property
    def finished(self):
        return self.state != GameState.INPROGRESS

    @property
    def wrong_guesses(self):
        return len(self._wrong_guesses)

    def guess(self, guesses):
        if self.finished:
            raise GameFinished()
        # Use lowercase for normalization
        lower_word = self.word.lower()
        for guess in [g.lower() for g in guesses]:
            if guess in lower_word:
                # Doing this mirroring of the words to make sure the
                # capitalization of the original word is preserved while
                # guessing.
                for index, letter in enumerate(lower_word):
                    if letter == guess:
                        self.letters[index] = self.word[index]
                if None not in self.letters:
                    self.state = GameState.WON
            elif guess not in self._wrong_guesses:
                self._wrong_guesses.add(guess)
                if self.wrong_guesses >= self.num_guesses:
                    self.state = GameState.LOST
                    break


def print_ui(game):
    letters = [l if l is not None else '_' for l in game.letters]
    print("Current letters: {}".format(" ".join(letters)))
    print("Remaining guesses: {}".format(
        game.num_guesses - game.wrong_guesses))


def play_game():
    parser = argparse.ArgumentParser(description=u'Play hangman')
    parser.add_argument('-n', '--num_guesses', default=Game.default_guesses,
                        type=int, help="The number of wrong guesses allowed.")
    args = parser.parse_args()
    game = Game(num_guesses=args.num_guesses)
    should_exit = False
    while not should_exit:
        while not game.finished:
            print_ui(game)
            guess = input("Guess: ")
            game.guess(guess)
        if game.state == GameState.WON:
            print("Congratulations, you won, the word was '{}'".format(
                      game.word))
        elif game.state == GameState.LOST:
            print("Sorry, you lost. The word was '{}'".format(game.word))
        continue_string = input("Play again? [y/N]: ")
        if len(continue_string) == 0 or continue_string[0].lower() != 'y':
            should_exit = True
        else:
            game.reset()

if __name__ == '__main__':
    play_game()
