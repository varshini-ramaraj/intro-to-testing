class ExternalClass:
    def write(self, found_mapping=False, mapping=None):
        """Ideally will write to a db somewhere"""
        pass

    def get_value_squared(self, value):
        """Ideally will read value from somewhere"""
        return value ** 2


class GenericClass:
    def __init__(self,
                 mapping: dict,
                 second_class: ExternalClass):
        self.mapping = mapping
        self.second_class = second_class

    def get_value_from_mapping(self, key):
        return self.mapping.get(key, None)

    def get_value_with_no_default(self, key):
        return self.mapping[key]

    def write_mapped_value(self, key: str):
        value = self.get_value_from_mapping(key)
        if value is None:
            self.second_class.write()
        else:
            self.second_class.write(found_mapping=True, mapping=value)
