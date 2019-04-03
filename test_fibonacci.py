import fibonacci


def test_sequence():
    expected_seq = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    actual_seq = fibonacci.generateFibonacci(len(expected_seq))
    for i in range(len(actual_seq)):
        assert expected_seq[i] == actual_seq[i]


def test_no_argument_gets_value_as_list():
    actual_seq = fibonacci.generateFibonacci()
    assert isinstance(actual_seq, list)


def test_no_argument_gets_list_length_0():
    actual_seq = fibonacci.generateFibonacci()
    assert len(actual_seq) == 0


def test_none_argument_gets_value_as_list():
    actual_seq = fibonacci.generateFibonacci(None)
    assert isinstance(actual_seq, list)


def test_none_argument_gets_list_length_0():
    actual_seq = fibonacci.generateFibonacci(None)
    assert len(actual_seq) == 0
