from greysqale.database import GSQLDatabase
from greysqale.constraints import DefaultValue, NotNull
from greysqale.fields import IntegerField, IDField, VarcharField
from greysqale.table import ModelTable

from decouple import config

class Employee(ModelTable):
    name = VarcharField(name = 'name', constraints = [NotNull()])
    age = IntegerField(name = 'age', constraints = [NotNull()])
    salary = IntegerField(name = 'salary', constraints = [NotNull()])
    department = VarcharField(name = 'department', constraints = [NotNull(), DefaultValue('IT')])
    

db = GSQLDatabase(config('POSTGRES_USERNAME'), config('POSTGRES_PASSWORD'), config('POSTGRES_DBNAME'), pool = 'simple')
db.add(Employee)

# Employee.insert(age = 24, name = 'ABC', salary = 30000, department = 'Accounting')
# Employee.insert(age = 29, name = 'DEF', salary = 40000, department = 'IT')
# Employee.insert(age = 19, name = 'GHI', salary = 0, department = 'HR')

s = Employee.select('*')
for row in s:
    print(row)