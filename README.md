# Udacity-Catalog-Project

Simple catalog allow the user to login his their GMail accounts. After his login he can add, edit or delete his items in various categories.

## Online Demo:
http://udacity-catalog-project.tk/

## How to run it:
In this demo the static file 'assets' are being served using apache. So you have to configure flask to serve them or run the application on apache server. Here's an example of apache configuration:
<br>
`Alias /assets/ /path/to/Udacity-Catalog-Project/assets/`
* Clone the project using `git clone https://github.com/mostafa-saeed/Udacity-Catalog-Project`
* Change the directory using `cd Udacity-Catalog-Project`
* Update the Database configurations inside `database_setup.py` File
* Run `python application.py`

## API End Point
| Function        | Method           | URL  |
| ------------- |-------------| -----|
| List JSON Catalog   | GET | /catalog/api/ |
| Get Item   | GET | /items/:itemID/ |
| Add Item   | POST | /items/ |
| Update Item   | PUT | /items/:itemID/ |
| Delete Item   | DELETE | /items/:itemID/ |


## Server information
* IP: 18.217.66.23
* SSH Port: 2200
* Domain Name: udacity-catalog-project.tk

## Server software installed
* Python
* PostgreSQL
* UFW
* Apache server

## Server configurations
* `Key-based` SSH authentication is enforced (No password authentication).
* SSH Port is `2200`
* Apache mod_wsgi
* Allowed apache to serve `static files`
