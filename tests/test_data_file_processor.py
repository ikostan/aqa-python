from src.data_file_processor import Data_File_Processor
import os

processor = Data_File_Processor()
xml_path = "samples/xml/test_data.xml"
json_path = "samples/json/updated_test_data.json"
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


def test_xml_is_existing():
    is_existing = os.path.isfile(xml_path)
    assert is_existing


def test_converted_xml():
    test_result = False
    error_message = ""
    got_xml_content = processor.get_python_structure_from_xml(xml_path)
    actual_persons = got_xml_content["persons"]
    expected_persons = original_content["persons"]
    if len(actual_persons) == len(expected_persons):
        for i in range(len(actual_persons)):
            actual_person = actual_persons[i]
            expected_person = expected_persons[i]
            actual_person_len = len(actual_person)
            expected_person_len = len(expected_person)
            if actual_person_len == expected_person_len and error_message == "":
                for key_name in key_names:
                    if actual_person[key_name] == expected_person[key_name]:
                        test_result = True
                    else:
                        test_result = False
                        error_message = "person: " + str(i) + " has incorrect attribute value with key: " + key_name + \
                                        " => actual value: " + actual_person[key_name] + "; expected value: " + \
                                        expected_person[key_name]
                        break
            else:
                test_result = False
                if error_message == "":
                    error_message = "person: " + str(i) + " has incorrect number of attributes => actual: " + \
                                    str(actual_person_len) + "; expected: " + str(expected_person_len)
                break
    else:
        test_result = False
        error_message = "incorrect number of persons => actual: " + str(len(actual_persons)) + "; expected: " + \
                        str(len(expected_persons))
    assert test_result, error_message


def test_json_is_existing():
    is_existing = os.path.isfile(json_path)
    assert is_existing


def test_teardown():
    os.remove(json_path)