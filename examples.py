from greysqale.database import GSQLDatabase
from greysqale.constraints import DefaultValue, NotNull
from greysqale.fields import IntegerField, IDField, VarcharField
from greysqale.query import CreateTable
from greysqale.table import ModelTable

class Employee(ModelTable):
    name = VarcharField(name = 'name', constraints = [NotNull()])
    age = IntegerField(name = 'age', constraints = [NotNull()])
    salary = IntegerField(name = 'salary', constraints = [NotNull()])

db = GSQLDatabase('postgres', 'postgres', 'testdb')
db.add(Employee)