#!/usr/bin/env python3
import enum
import random


class GameState(enum.Enum):

    INPROGRESS = 0

    LOST = 1

    WON = 2


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
        self.wrong_guesses = 0
        self.letters = list([None for _ in range(len(self.word))])
        self.state = GameState.INPROGRESS

    @property
    def finished(self):
        return self.state != GameState.INPROGRESS

    def guess(self, guesses):
        if not self.finished:
            raise 
        # Use lowercase for normalization
        lower_word = self.word.lower()
        for guess in guesses:
            if guess.lower() in lower_word:
                pass
            else:
                self.wrong_guesses += 1
                if self.wrong_guesses >= self.num_guesses:
                    self.state = GameState.LOST
