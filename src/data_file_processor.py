import xml.etree.ElementTree as elementsTree
import json


class DataFileProcessor:
    def __init__(self):
        self.python_structure_upper_level = {"persons": None}

    def get_dict_upper_level_key(self):
        key_name = None
        keys = self.python_structure_upper_level.keys()
        if len(keys) == 1:
            for key in keys:
                key_name = key
        else:
            print('ERROR: number of upper level keys is greater than 1')
        return key_name

    def get_python_structure_from_xml(self, xml_file_path):
        person_dicts_list = []
        tree = elementsTree.parse(xml_file_path)
        root = tree.getroot()
        persons = root.findall('PERSON')
        key_pairs = [
            {"python_key": "first_name", 'xml_key': 'FIRST_NAME'},
            {"python_key": "last_name", 'xml_key': 'LAST_NAME'},
            {"python_key": "year_of_birth", 'xml_key': 'YEAR_OF_BIRTH'},
            {"python_key": "month_of_birth", 'xml_key': 'MONTH_OF_BIRTH'},
            {"python_key": "day_of_birth", 'xml_key': 'DAY_OF_BIRTH'},
            {"python_key": "company", 'xml_key': 'COMPANY'},
            {"python_key": "project", 'xml_key': 'PROJECT'},
            {"python_key": "role", 'xml_key': 'ROLE'},
            {"python_key": "room", 'xml_key': 'ROOM'},
            {"python_key": "hobby", 'xml_key': 'HOBBY'}
        ]
        for person in persons:
            person_dict = {}
            for key in key_pairs:
                person_attribute = person.find(key['xml_key'])
                if person_attribute is not None:
                    person_dict[key['python_key']] = person_attribute.text
            person_dicts_list.append(person_dict)
        python_structure = self.python_structure_upper_level
        upper_level_key_name = self.get_dict_upper_level_key()
        python_structure[upper_level_key_name] = person_dicts_list
        return python_structure

    def update_python_structure(self, python_structure, update_data_list):
        upper_level_key_name = self.get_dict_upper_level_key()
        persons_list = python_structure[upper_level_key_name]
        for update_object in update_data_list:
            key_name = update_object["key_name"]
            original_value_substring = update_object["original_value_substring"]
            new_value = update_object["new_value"]
            for person in persons_list:
                if key_name in person:
                    if original_value_substring in person[key_name]:
                        person[key_name] = new_value
        python_structure[upper_level_key_name] = persons_list
        return python_structure

    def create_json_file(self, python_structured_data, json_file_path):
        with open(json_file_path, "w") as updated_data_file:
            json.dump(python_structured_data, updated_data_file, indent=4)

    def data_file_processing(self, path_to_source_file, path_to_destination_file, update_data_list):
        source_python_structure = self.get_python_structure_from_xml(path_to_source_file)
        updated_python_structure = self.update_python_structure(source_python_structure, update_data_list)
        self.create_json_file(updated_python_structure, path_to_destination_file)


if __name__ == '__main__':
    old_to_new_values = (
        {'key_name': 'first_name', 'original_value_substring': 'YOUR', 'new_value': 'Dmitry'},
        {'key_name': 'last_name', 'original_value_substring': 'YOUR', 'new_value': 'Naumov'},
        {'key_name': 'year_of_birth', 'original_value_substring': 'YOUR', 'new_value': '1973'},
        {'key_name': 'month_of_birth', 'original_value_substring': 'YOUR', 'new_value': 'Oct'},
        {'key_name': 'day_of_birth', 'original_value_substring': 'YOUR', 'new_value': '9'},
        {'key_name': 'company', 'original_value_substring': 'YOUR', 'new_value': 'Lohika Kyiv'},
        {'key_name': 'project', 'original_value_substring': 'YOUR', 'new_value': 'Training Project'},
        {'key_name': 'role', 'original_value_substring': 'YOUR', 'new_value': 'Trainee'},
        {'key_name': 'room', 'original_value_substring': 'YOUR', 'new_value': '222'},
        {'key_name': 'hobby', 'original_value_substring': 'YOUR', 'new_value': 'couch potato time spending'}
    )
    converter = DataFileProcessor()
    print(converter.get_python_structure_from_xml("../tests/samples/xml/test_data.xml"))
    converter.data_file_processing("../tests/samples/xml/test_data.xml", "../tests/samples/json/updated_test_data.json",
                                   old_to_new_values)
