from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator:
    def __init__(self, file_size, message=None):
        self.file_size = file_size
        self.message = message
        
    @property
    def message(self):
        return self.__message
    
    @message.setter
    def message(self, value):
        if not value:
            self.__message = f"file size must be less than {self.file_size}MB!"
        else:
            self.__message = value

    def __call__(self, value):
        if value > self.file_size * 1024 * 1024:
            raise ValidationError(self.message)
