from src.data_file_processor import DataFileProcessor
import pytest
import os
import json
import allure

processor = DataFileProcessor()
xml_path = os.path.dirname(os.path.realpath(__file__)) + "/samples/xml/test_data.xml"
json_path = os.path.dirname(os.path.realpath(__file__))+ "/samples/json/updated_test_data.json"
key_names = ('first_name', 'last_name', 'year_of_birth', 'month_of_birth', 'day_of_birth', 'company', 'project', 'role',
             'room', 'hobby')
original_content = {
    'persons': [
        {
            'first_name': 'Lector',
            'last_name': 'Pythonov',
            'year_of_birth': '1991',
            'month_of_birth': 'Jan',
            'day_of_birth': '31',
            'company': 'Huhhle',
            'project': 'Cleaning department',
            'role': 'Looker at window',
            'room': '123',
            'hobby': 'Adulation'
        },
        {
            'first_name': 'YOUR_FIRST_NAME',
            'last_name': 'YOUR_LAST_NAME',
            'year_of_birth': 'YOUR_YYYY',
            'month_of_birth': 'YOUR_Month',
            'day_of_birth': 'YOUR_DD',
            'company': 'YOUR_COMPANY',
            'project': 'YOUR_PROJECT',
            'role': 'YOUR_ROLE',
            'room': 'YOUR_ROOM',
            'hobby': 'YOUR_HOBBY'
        },
        {
            'first_name': 'TEST_FIRST_NAME',
            'last_name': 'TEST_LAST_NAME',
            'year_of_birth': '2000',
            'month_of_birth': 'May',
            'day_of_birth': '11',
            'company': 'TEST_COMPANY',
            'project': 'TEST_PROJECT',
            'role': 'TEST_ROLE',
            'room': 'TEST_ROOM',
            'hobby': 'TEST_HOBBY'
        }
    ]
}
new_content = {
    "persons": [
        {
            "first_name": original_content["persons"][0]["first_name"],
            "last_name": original_content["persons"][0]["last_name"],
            "year_of_birth": original_content["persons"][0]["year_of_birth"],
            "month_of_birth": original_content["persons"][0]["month_of_birth"],
            "day_of_birth": original_content["persons"][0]["day_of_birth"],
            "company": original_content["persons"][0]["company"],
            "project": original_content["persons"][0]["project"],
            "role": original_content["persons"][0]["role"],
            "room": original_content["persons"][0]["room"],
            "hobby": original_content["persons"][0]["hobby"]
        },
        {
            "first_name": "Dmitry",
            "last_name": "Naumov",
            "year_of_birth": "1973",
            "month_of_birth": "Oct",
            "day_of_birth": "9",
            "company": "Lohika Kyiv",
            "project": "Training Project",
            "role": "Trainee",
            "room": "5",
            "hobby": "couch potato time spending"
        },
        {
            "first_name": original_content["persons"][2]["first_name"],
            "last_name": original_content["persons"][2]["last_name"],
            "year_of_birth": original_content["persons"][2]["year_of_birth"],
            "month_of_birth": original_content["persons"][2]["month_of_birth"],
            "day_of_birth": original_content["persons"][2]["day_of_birth"],
            "company": original_content["persons"][2]["company"],
            "project": original_content["persons"][2]["project"],
            "role": original_content["persons"][2]["role"],
            "room": original_content["persons"][2]["room"],
            "hobby": original_content["persons"][2]["hobby"]
        }
    ]
}
old_to_new_values = (
    {'key_name': 'first_name', 'original_value_substring': 'YOUR',
     'new_value': new_content["persons"][1]["first_name"]},
    {'key_name': 'last_name', 'original_value_substring': 'YOUR',
     'new_value': new_content["persons"][1]["last_name"]},
    {'key_name': 'year_of_birth', 'original_value_substring': 'YOUR',
     'new_value': new_content["persons"][1]["year_of_birth"]},
    {'key_name': 'month_of_birth', 'original_value_substring': 'YOUR',
     'new_value': new_content["persons"][1]["month_of_birth"]},
    {'key_name': 'day_of_birth', 'original_value_substring': 'YOUR',
     'new_value': new_content["persons"][1]["day_of_birth"]},
    {'key_name': 'company', 'original_value_substring': 'YOUR',
     'new_value': new_content["persons"][1]["company"]},
    {'key_name': 'project', 'original_value_substring': 'YOUR',
     'new_value': new_content["persons"][1]["project"]},
    {'key_name': 'role', 'original_value_substring': 'YOUR',
     'new_value': new_content["persons"][1]["role"]},
    {'key_name': 'room', 'original_value_substring': 'YOUR',
     'new_value': new_content["persons"][1]["room"]},
    {'key_name': 'hobby', 'original_value_substring': 'YOUR',
     'new_value': new_content["persons"][1]["hobby"]}
)


def compare_dicts_lists(actual_dicts_list, expected_dicts_list):
    comparison_result = False
    error_message = ""
    if len(actual_dicts_list) == len(expected_dicts_list):
        for i in range(len(actual_dicts_list)):
            actual_person = actual_dicts_list[i]
            expected_person = expected_dicts_list[i]
            actual_person_len = len(actual_person)
            expected_person_len = len(expected_person)
            if actual_person_len == expected_person_len and error_message == "":
                for key_name in key_names:
                    if actual_person[key_name] == expected_person[key_name]:
                        comparison_result = True
                    else:
                        comparison_result = False
                        error_message = "dict with index: " + str(i) + " has incorrect attribute value with key: " + \
                                        key_name + " => actual value: " + actual_person[key_name] + \
                                        "; expected value: " + expected_person[key_name]
                        break
            else:
                comparison_result = False
                if error_message == "":
                    error_message = "dict with index: " + str(i) + " has incorrect number of attributes => actual: " + \
                                    str(actual_person_len) + "; expected: " + str(expected_person_len)
                break
    else:
        comparison_result = False
        error_message = "incorrect number of dicts => actual: " + str(len(actual_dicts_list)) + "; expected: " + \
                        str(len(expected_dicts_list))
    return [comparison_result, error_message]


def remove_file(file_path):
    try:
        os.remove(file_path)
    except:
        print("json is already removed")


def get_json_file_content(json_file_path):
    with open(json_file_path, "r") as json_data:
        return json.load(json_data)


# TESTS SECTION
@pytest.mark.unit
@allure.title("File processor. Test XML is existing")
def test_xml_is_existing():
    is_existing = os.path.isfile(xml_path)
    assert is_existing


@pytest.mark.unit
@allure.title("File processor. Loaded XML content is correct")
def test_loaded_xml_content():
    got_xml_content = processor.get_python_structure_from_xml(xml_path)
    test_result = compare_dicts_lists(got_xml_content["persons"], original_content["persons"])
    assert test_result[0], test_result[1]


@pytest.mark.unit
@allure.title("File processor. XML content is updated correctly")
def test_updated_content():
    got_xml_content = processor.get_python_structure_from_xml(xml_path)
    got_updated_content = processor.update_python_structure(got_xml_content, old_to_new_values)
    test_result = compare_dicts_lists(got_updated_content["persons"], new_content["persons"])
    assert test_result[0], test_result[1]


@pytest.mark.unit
@allure.title("File processor. JSON is created")
def test_json_is_existing():
    processor.data_file_processing(xml_path, json_path, old_to_new_values)
    is_existing = os.path.isfile(json_path)
    remove_file(json_path)
    assert is_existing, "file " + json_path + " was not created"


@pytest.mark.unit
@allure.title("File processor. JSON content is updated correctly")
def test_json_content():
    processor.data_file_processing(xml_path, json_path, old_to_new_values)
    got_json_content = get_json_file_content(json_path)
    test_result = compare_dicts_lists(got_json_content["persons"], new_content["persons"])
    remove_file(json_path)
    assert test_result[0], test_result[1]


# this is not test, this is teardown method
@pytest.mark.unit
def test_teardown():
    remove_file(json_path)
