# Drink-mixer
Raspberry Pi Drink mixer - This is a project i did for my last project in my raspberry pi automation course.
This program is designed to run on a raspberry pi and to work with a MySQL server with 3 tables included in the SQL.txt.

This operates by connecting the raspberry pi to a 8 channel sain-smart relay board to power up to 8 12v perstallic pumps, though it can be modified to control more.

After using the CLI (command line interface) to assign drinks types to pumps, the program will filter the drink mix database based on what drinks are available.
  Example: Rum is assigned to pump 1 and CocaCola is assigned pump 2. The two available drinks will be straight rum, and Rum      and Coke.

The user is not required to know any of the drink mixes ahead of time, as all drink mixes will be stored in a database. If a drink is assigned to a pump, it will figure out what drinks it can make, and which pumps to turn on, using threaded processes for each pump.

Things I would like to add:
  Improved user interface, GUI over commandline
  Web server integration for the drink mix database
  continuing development of the drink mix database
