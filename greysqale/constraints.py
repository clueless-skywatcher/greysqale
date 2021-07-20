class Constraint:
    def __init__(self):
        self.constraint = None
        
    def _construct(self):
        return str(self.constraint)

class PrimaryKey(Constraint):
    def __init__(self):
        super(PrimaryKey, self).__init__()
        self.constraint = 'PRIMARY KEY'

class NotNull(Constraint):
    def __init__(self):
        super(NotNull, self).__init__()
        self.constraint = 'NOT NULL'

class Serial(Constraint):
    def __init__(self):
        super(Serial, self).__init__()
        self.constraint = 'SERIAL'

class DefaultValue(Constraint):
    def __init__(self, val):
        super(DefaultValue, self).__init__()
        self.constraint = f'DEFAULT {val}'

class ForeignKey(Constraint):
    def __init__(self, ref_table, on_delete = 'NONE'):
        super(ForeignKey, self).__init__()
        self.ref_table = ref_table
        self.constraint = f'REFERENCES {ref_table.name}'
        if on_delete == 'CASCADE':
            self.constraint += f'ON DELETE CASCADE'