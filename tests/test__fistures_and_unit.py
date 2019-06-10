import pytest


@pytest.fixture(scope="class", autouse=True)
def setup_class(conf_fixture):
    print("\nTest_1:")
    pytest.variable_of_setup_class_1 = conf_fixture + "_1"
    pytest.variable_of_setup_class_2 = conf_fixture + "_2"
    pytest.variable_of_setup_class_3 = conf_fixture + "_3"


class TestClass:

    def test_1(self, setup_class):
        print("---test_1:", pytest.variable_of_setup_class_1,
              " and", pytest.variable_of_setup_class_2,
              " and", pytest.variable_of_setup_class_3)
        assert True

    def test_2(self, setup_class):
        print("---test_2:", pytest.variable_of_setup_class_1,
              " and", pytest.variable_of_setup_class_2,
              " and", pytest.variable_of_setup_class_3)
        assert True