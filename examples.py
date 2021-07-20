from greysqale.database import GSQLDatabase
from greysqale.constraints import DefaultValue, NotNull
from greysqale.fields import IntegerField, IDField, VarcharField
from greysqale.query import CreateTable
from greysqale.table import ModelTable

from decouple import config

class Employee(ModelTable):
    name = VarcharField(name = 'name', constraints = [NotNull()])
    age = IntegerField(name = 'age', constraints = [NotNull()])
    salary = IntegerField(name = 'salary', constraints = [NotNull()])

db = GSQLDatabase(config('POSTGRES_USERNAME'), config('POSTGRES_PASSWORD'), config('POSTGRES_DBNAME'))
db.add(Employee)

# print(Employee._insert_table_query(age = 25, name = 'Raju', salary = 30000))
Employee.insert(age = 24, name = 'Somi', salary = 30000)