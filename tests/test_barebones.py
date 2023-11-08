import pytest

from lib.barebones import Literal, Concat, Repetition, match  # Replace with actual import

# Test literals
def test_literal_matches():
    literal_a = Literal('a')
    assert literal_a.matches('a')
    assert not literal_a.matches('b')
    assert not literal_a.matches('')

# Test concatenation
def test_concatenation_matches():
    concat_ab = Concat(Literal('a'), Literal('b'))
    assert concat_ab.matches('ab')
    assert not concat_ab.matches('ba')
    assert not concat_ab.matches('a')
    assert not concat_ab.matches('b')
    assert not concat_ab.matches('')

# Test the matcher function
def test_matcher():
    # Single literal
    ast = Literal('a')
    assert match(ast, 'a')
    assert not match(ast, 'b')
    
    # Concatenation
    ast = Concat(Literal('a'), Literal('b'))
    assert match(ast, 'ab')
    assert not match(ast, 'ba')
    assert not match(ast, 'a')
    assert not match(ast, 'b')
    assert not match(ast, 'abc')

    # TODO add more tests for other types of nodes

def test_repetition_zero_occurrences():
    repeated_a = Repetition(Literal('a'))
    assert match(repeated_a, '')  # Zero occurrences of 'a'
    assert match(repeated_a, 'a')  # One occurrence of 'a'
    assert match(repeated_a, 'aa')  # Multiple occurrences of 'a'
    assert not match(repeated_a, 'b')  # Does not match other characters

# Test Repetition node with one or more occurrences
def test_repetition_one_or_more_occurrences():
    repeated_a = Repetition(Literal('a'))
    assert match(repeated_a, 'a')  # Should match a single 'a'
    assert match(repeated_a, 'aaaa')  # Should match multiple 'a's in a row

# Test Repetition node within concatenation
def test_repetition_within_concatenation():
    repeated_a_concat_b = Concat(Repetition(Literal('a')), Literal('b'))
    assert match(repeated_a_concat_b, 'b')  # Matches 'b' with zero 'a's
    assert match(repeated_a_concat_b, 'ab')  # Matches 'ab'
    assert match(repeated_a_concat_b, 'aaab')  # Matches 'aaab' with multiple 'a's
    assert not match(repeated_a_concat_b, 'aabbc')  # Does not match due to extra 'c'

# Test Repetition node followed by another Repetition node
def test_consecutive_repetitions():
    repeated_a_followed_by_repeated_b = Concat(Repetition(Literal('a')), Repetition(Literal('b')))
    assert match(repeated_a_followed_by_repeated_b, '')  # Matches empty string
    assert match(repeated_a_followed_by_repeated_b, 'a')  # Matches 'a'
    assert match(repeated_a_followed_by_repeated_b, 'b')  # Matches 'b'
    assert match(repeated_a_followed_by_repeated_b, 'aaabbb')  # Matches 'aaabbb'
    assert not match(repeated_a_followed_by_repeated_b, 'aaabbbc')  # Does not match due to 'c'