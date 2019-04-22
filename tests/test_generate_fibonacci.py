from src import generate_fibonacci


def test_sequence():
    expected_seq = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    actual_seq = generate_fibonacci.generate_fibonacci(len(expected_seq))
    for i in range(len(actual_seq)):
        assert expected_seq[i] == actual_seq[i]


def test_no_argument_gets_value_as_list():
    actual_seq = generate_fibonacci.generate_fibonacci()
    assert isinstance(actual_seq, list)


def test_no_argument_gets_list_length_0():
    actual_seq = generate_fibonacci.generate_fibonacci()
    assert len(actual_seq) == 0


def test_none_argument_gets_value_as_list():
    actual_seq = generate_fibonacci.generate_fibonacci(None)
    assert isinstance(actual_seq, list)


def test_none_argument_gets_list_length_0():
    actual_seq = generate_fibonacci.generate_fibonacci(None)
    assert len(actual_seq) == 0


def test_0_argument_gets_value_as_list():
    actual_seq = generate_fibonacci.generate_fibonacci(0)
    assert isinstance(actual_seq, list)


def test_0_argument_gets_list_length_0():
    actual_seq = generate_fibonacci.generate_fibonacci(0)
    assert len(actual_seq) == 0


def test_1_argument_gets_value_as_list():
    actual_seq = generate_fibonacci.generate_fibonacci(1)
    assert actual_seq[0] == 1


def test_1_argument_gets_list_length_1():
    actual_seq = generate_fibonacci.generate_fibonacci(1)
    assert len(actual_seq) == 1
