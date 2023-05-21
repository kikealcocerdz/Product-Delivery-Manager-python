from abc import abstractmethod

class InputFile:

    def __init__(self, input_file):
        pass

    @abstractmethod
    def get_data_from_input_file(self, input_file):
        pass

    @abstractmethod
    def validate_input_file_labels(self, data):
        pass