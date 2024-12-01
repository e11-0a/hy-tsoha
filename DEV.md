Generate styles from Tailwind file:
```
./tailwindcss-linux-x64 -i styles.css -o static/styles.css --watch
```
 
Wipe and recreate db:
```
psql -U <your postgres user> -d <your database> -a -f sql/wipe-db.sql
psql -U <your postgres user> -d <your database> -a -f sql/create-db.sql
psql -U <your postgres user> -d <your database> -a -f sql/create-test.sql
```

Run dev instace:
```
flask --app app.py run --debug
```

Run devtool:
```
./devtool.py -c ./config.ini
./devtool.py -c ./config.ini -o newuser -i
./devtool.py -c ./config.ini -o newcourse -i
./devtool.py -c ./config.ini -o newmaterial -i
./devtool.py -c ./config.ini -o modify -i
```
