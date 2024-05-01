# Commands to use the database-

## To create image  and run the container:
- `sudo ./build.bat`  after giving executable permissions to build.bat



## To connect to Database Container through Terminal:

- sudo docker exec -it dbcont bash
- psql "dbname=ppe_detection  user=admin password=admin1234 port=5432 "

## To connect to Database Container through PGadmin:
- enter the following credentials
- username = admin
- password =  admin1234
- database = ppe_detection
- host = localhost
