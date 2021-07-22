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
- Selecting rows
```python
print(Employee.select('*')) # Will select all columns
```
Output:
```python
Employee({'id': 17, 'age': 24, 'department': 'Accounting', 'name': 'ABC', 'salary': 30000})
Employee({'id': 18, 'age': 29, 'department': 'IT', 'name': 'DEF', 'salary': 40000})
Employee({'id': 19, 'age': 19, 'department': 'HR', 'name': 'GHI', 'salary': 0})
```
```python
print(Employee.select('id', 'name')) # Will select only id and name
```
Output:
```python
Employee({'id': 17, 'name': 'ABC'})
Employee({'id': 18, 'name': 'DEF'})
Employee({'id': 19, 'name': 'GHI'})
```


Caveats and Todos:
- Implement select rows with filters
- Implement update rows
- Implement Aggregate functions
- Add more fields and constraints, implement ForeignKey properly
