To create and initialize the db file:
```
python manage.py makemigrations
python manage.py migrate
```

To run the server and start listening to a port and serving requests:
```
python manage.py makemigrations
```

To load professors data from excel file:
it will store them inside the db file, do not run this command on further runs.
```
python manage.py import_professors path/to/your/excel/file.xlsx
```


