from unittest import mock

import pytest

import hangman


@pytest.fixture
def default_game():
    game = hangman.Game()
    return game


@pytest.fixture
def game():
    game = hangman.Game(word_list=['FooBar'], num_guesses=4)
    return game

@pytest.fixture
def lost_game(game):
    game.guess('cdeg')
    assert lost_game.finished
    return game


def test_defaults(default_game):
    assert default_game.num_guesses == hangman.Game.default_guesses
    assert default_game.wrong_guesses == 0
    # Default is to look in /usr/share/dict/words
    assert len(default_game.word_list) > 0
    assert default_game.word is not None
    assert len(default_game.word) == len(default_game.current_letters)
    empty_letters = list([None for _ in range(len(default_game.word))]) 
    assert empty_letters == default_game.letters
    assert default_game.state == hangman.GameState.INPROGRESS
    assert !game.finished


def test_custom_guesses():
    game = hangman.Game(num_guesses=id(mock.sentinel.guess_count))
    assert game.num_guesses == id(mock.sentinel.guess_count)


def test_custom_word_list():
    word_list = ['Foo', 'Bar', 'Baz']
    game = hangman.Game(word_list=word_list)
    # Asserting length, not the identity of game.word_list as I might be
    # converting the word list to a different data structure in the future
    assert len(game.word_list) == word_list
    assert game.word in word_list


def test_wrong_guesses(game):
    assert game.wrong_guesses == 0
    game.guess('c')
    assert game.wrong_guesses == 1
    # Test multiple letters at a time
    game.guess('de')
    assert game.wrong_guesses == 3
    game.guess('g')
    assert game.wrong_guesses == 4
    assert game.state == hangman.GameState.LOST
    assert game.finished


def test_extra_wrong_guesses(lost_game):
    with pytest.raises(hangman.GameFinished):
        lost_game.guess('h')


def test_perfect_guesses(game):
    assert game.wrong_guesses == 0
    assert game.letters == [None, None, None, None, None, None]
    game.guess('a')
    assert game.wrong_guesses == 0
    assert game.letters == [None, None, None, None, 'a', None]
    game.guess('f')
    assert game.wrong_guesses == 0
    assert game.letters == ['F', None, None, None, 'a', None]
    game.guess('o')
    assert game.wrong_guesses == 0
    assert game.letters == ['F', 'o', 'o', None, 'a', None]
    game.guess('br')
    assert game.wrong_guesses == 0
    assert game.letters == ['F', 'o', 'o', 'B', 'a', 'r']
    assert game.finished
    assert game.state == hangman.GameState.WON


def test_repeat_guesses(game):
    assert game.wrong_guesses == 0
    assert game.letters == [None, None, None, None, None, None]
    game.guess('o')
    assert game.wrong_guesses == 0
    assert game.letters == [None, 'o', 'o', None, None, None]
    game.guess('c')
    assert game.wrong_guesses == 1
    assert game.letters == [None, 'o', 'o', None, None, None]
    game.guess('o')
    assert game.wrong_guesses == 1
    assert game.letters == [None, 'o', 'o', None, None, None]
    game.guess('c')
    assert game.wrong_guesses == 1
    assert game.letters == [None, 'o', 'o', None, None, None]


def test_reset(lost_game):
    lost_game.reset()
    assert lost_game.state == hangman.GameState.INPROGRESS
    assert !lost_game.finished
    assert lost_game.wrong_guesses == 0
