#
# Basic properties based tests using Hypothesis
# 

from hypothesis import given, assume, event, settings, Phase
import hypothesis.strategies as st

# strategy for generating random lists of integers
intlist = st.lists(st.integers())


# some properties about list reverse 
@given(intlist)
def test_reverse_twice(x):
    assert list(reversed(list(reversed(x)))) == x

@given(intlist, intlist)
def test_reverse_append(x, y):
    assert list(reversed(x + y)) == list(reversed(y)) + list(reversed(x))

    
