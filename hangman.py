#!/usr/bin/env python3
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
            with open('/usr/share/dict/words', 'r') as words_file:
                word_list = list(words_file)
        self.word_list = list(word_list)
        self.reset()

    def reset(self):
        self.word = random.choice(self.word_list)
        self._wrong_guesses = set()
        self.letters = list([None for _ in range(len(self.word))])
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
