import stix2 as stix


class CrudProvider:
    def __init__(self):
        self.__objects = []

    def list(self) -> list:
        return self.__objects

    def add(self, stix_dictionary: dict) -> None:
        self.__objects.append(stix_dictionary)

    def update(self, index, stix_dictionary: dict) -> bool:
        try:
            self.__objects[index] = stix_dictionary
            return True
        except IndexError:
            return False

    def delete(self, stix_dictionary: dict) -> bool:
        try:
            self.__objects.remove(stix_dictionary)
            return True
        except ValueError:
            return False
