# greysqale
A Basic ORM for PostgreSQL written in Python using psycopg2.

Features:
- Connecting to a database
```python
from greysqale.database import GSQLDatabase

# Just declare and it will automatically connect!
db = GSQLDatabase('db_username', 'db_password', 'db_name')

```
- Adding a new table
```python
from greysqale.database import GSQLDatabase
from greysqale.table import ModelTable
from greysqale.fields import IntegerField, VarcharField
from greysqale.constraints import DefaultValue, NotNull

db = GSQLDatabase('db_username', 'db_password', 'db_name')

# This, like Django's ORM (and other ORMs), will create the ID column by itself, so no need to specify explicitly!
class Employee(ModelTable):
    name = VarcharField(name = 'name', constraints = [NotNull()])
    age = IntegerField(name = 'age', constraints = [NotNull()])
    salary = IntegerField(name = 'salary', constraints = [NotNull()])
    department = VarcharField(name = 'department', constraints = [NotNull(), DefaultValue('IT')])
    
# Add the newly created model to the table
db.add(Employee)
```
- Inserting a row to the table
```python
Employee.insert(name = 'Mark', age = 45, salary = 60000) # Creates an employee with default department IT
Employee.insert(name = 'Sam', age = 39, salary = 40000, department = 'HR')
```
