import xml.etree.ElementTree as elementsTree
import json


class Converter:
    def __init__(self):
        self.person_dicts_list = []
        self.json_string = {"persons": []}

    def set_person_dicts_list_from_xml(self, path_to_source_xml):
        tree = elementsTree.parse(path_to_source_xml)
        root = tree.getroot()
        persons = root.findall('PERSON')
        for i in range(len(persons)):
            self.person_dicts_list.append(
                {
                    "first_name": persons[i].find('FIRST_NAME'),
                    "last_name": persons[i].find('LAST_NAME'),
                    "year_of_birth": persons[i].find('YEAR_OF_BIRTH'),
                    "month_of_birth": persons[i].find('MONTH_OF_BIRTH'),
                    "day_of_birth": persons[i].find('DAY_OF_BIRTH'),
                    "company": persons[i].find('COMPANY'),
                    "project": persons[i].find('PROJECT'),
                    "role": persons[i].find('ROLE'),
                    "room": persons[i].find('ROOM'),
                    "hobby": persons[i].find('HOBBY')
                }
            )

    def update_person_dicts_list(self, new_values_list):
        dists_list_length = len(self.person_dicts_list)
        new_values_list_length = len(new_values_list)
        if new_values_list_length == dists_list_length:
            for i in range(new_values_list_length):
                self.person_dicts_list[i]["first_name"] = new_values_list[i][0]
                self.person_dicts_list[i]["last_name"] = new_values_list[i][1]
                self.person_dicts_list[i]["year_of_birth"] = new_values_list[i][2]
                self.person_dicts_list[i]["month_of_birth"] = new_values_list[i][3]
                self.person_dicts_list[i]["day_of_birth"] = new_values_list[i][4]
                self.person_dicts_list[i]["company"] = new_values_list[i][5]
                self.person_dicts_list[i]["project"] = new_values_list[i][6]
                self.person_dicts_list[i]["role"] = new_values_list[i][7]
                self.person_dicts_list[i]["room"] = new_values_list[i][8]
                self.person_dicts_list[i]["hobby"] = new_values_list[i][9]
        else:
            print("Length of the got new values list is incorrect")

    def set_json_string(self):
        self.json_string["persons"] = self.person_dicts_list

    def create_json_file(self, file_path):
        with open(file_path, "w") as updated_data_file:
            json.dump(self.json_string, updated_data_file, indent=4)

    def data_file_processing(self, path_to_source_file, path_to_destination_file, update_data_list):
        self.set_person_dicts_list_from_xml(path_to_source_file)
        self.update_person_dicts_list(update_data_list)
        self.set_json_string()
        self.create_json_file(path_to_destination_file)


if __name__ == '__main__':
    new_values = (
        ('Andrew', 'Pospelko', 1990, 'Feb', 29, 'Lohika Odessa', 'Training Project', 'Coach', '111', 'Teaching'),
        ('Dmitry', 'Naumov', 1973, 'Oct', 9, 'Lohika Kyiv', 'Training Project', 'Trainee', '222',
         'couch potato time spending'),
        ('Roger', 'Waters', 1943, 'Sep', 6, 'PE', 'Pink Floyd', 'Rhythm guitar player', 'A1', 'singing'),
    )
    new_json = Converter()
    new_json.data_file_processing("samples/xml/test_data.xml", "samples/json/updated_test_data.json", new_values)
