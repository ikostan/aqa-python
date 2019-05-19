from src import generate_fibonacci
import allure


@allure.title("Fibonacci. Generated sequence is correct")
def test_sequence():
    expected_seq = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    actual_seq = generate_fibonacci.generate_fibonacci(len(expected_seq))
    for i in range(len(actual_seq)):
        assert expected_seq[i] == actual_seq[i]


@allure.title("Fibonacci. Empty list returns if no argument is got")
def test_no_argument_gets_value_as_list():
    actual_seq = generate_fibonacci.generate_fibonacci()
    assert isinstance(actual_seq, list)


@allure.title("Fibonacci. Returned list length==0 if no argument is got")
def test_no_argument_gets_list_length_0():
    actual_seq = generate_fibonacci.generate_fibonacci()
    assert len(actual_seq) == 0


@allure.title("Fibonacci. Empty list returns if argument is None")
def test_none_argument_gets_value_as_list():
    actual_seq = generate_fibonacci.generate_fibonacci(None)
    assert isinstance(actual_seq, list)


@allure.title("Fibonacci. Returned list length==0 if argument is None")
def test_none_argument_gets_list_length_0():
    actual_seq = generate_fibonacci.generate_fibonacci(None)
    assert len(actual_seq) == 0


@allure.title("Fibonacci. Empty list returns if argument==0")
def test_0_argument_gets_value_as_list():
    actual_seq = generate_fibonacci.generate_fibonacci(0)
    assert isinstance(actual_seq, list)


@allure.title("Fibonacci. Returned list length==0 if argument==0")
def test_0_argument_gets_list_length_0():
    actual_seq = generate_fibonacci.generate_fibonacci(0)
    assert len(actual_seq) == 0


@allure.title("Fibonacci. Returned list item=1 if argument==1")
def test_1_argument_gets_value_as_list():
    actual_seq = generate_fibonacci.generate_fibonacci(1)
    assert actual_seq[0] == 1


@allure.title("Fibonacci. Returned list length==1 if argument==1")
def test_1_argument_gets_list_length_1():
    actual_seq = generate_fibonacci.generate_fibonacci(1)
    assert len(actual_seq) == 1
