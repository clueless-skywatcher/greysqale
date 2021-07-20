from .constraints import *

class Field:
    def __init__(self, name = None, **kwargs):
        self.field_name = name
        self.field = None
        self.constraints = []
        self.kwargs = kwargs
    
    def _build_str(self):
        s = f"{self.field_name} {self.field}"
        for constraint in self.constraints:
            s += f" {constraint._construct()}"
        return s

class SerialField(Field):
    def __init__(self, name = 'srl', constraints = []):
        super().__init__(name = name, constraints = constraints)
        self.field = 'SERIAL'
        self.constraints = constraints


class IDField(SerialField):
    def __init__(self, name = 'id'):
        super(IDField, self).__init__(name = name)
        self.constraints = [PrimaryKey(), NotNull()]

class NumericField(Field):
    def __init__(self, name = 'None', constraints = []):
        super(NumericField, self).__init__(name = name, constraints = constraints)
        self.field = 'NUMERIC'
        self.constraints = constraints

class IntegerField(Field):
    def __init__(self, name = 'None', constraints = []):
        super(IntegerField, self).__init__(name = name, constraints = constraints)
        self.field = 'INTEGER'
        self.constraints = constraints

class VarcharField(Field):
    def __init__(self, name = 'None', constraints = [], max_length = 255):
        super(VarcharField, self).__init__(name = name, constraints = constraints)
        self.max_length = max_length
        self.field = f'VARCHAR({self.max_length})'
        self.constraints = constraints
        

