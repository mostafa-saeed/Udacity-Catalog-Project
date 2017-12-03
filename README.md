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
### Update all currently installed packages.
* `sudo apt update`
* `sudo apt upgrade`

### Change the SSH port from 22 to 2200.
* Use `sudo vim /etc/ssh/sshd_config` and then change Port 22 to Port 2200 , save & quit.
* Reload SSH using `sudo service ssh restart`.

### Configure the Uncomplicated Firewall (UFW).
* Use `sudo ufw default deny incoming` to deny all incoming connections by default.
* Use `sudo ufw default allow outgoing` to allow all outgoing connections by default.
* Use `sudo ufw allow 2200` to allow the new SSH port.
* Use `sudo ufw allow www` to allow HTTP requests.
* Use `sudo ufw allow ntp` to allow the NTP port.
* Now let's active our firewall using `sudo ufw enable`.

### Install and configure Apache.
* Use `sudo apt install apache2` to install apache server.
* Use `sudo vim /etc/apache2/sites-enabled/000-default.conf` to configure Apache.
* Inside the `<VirtualHost *:80>` Add `WSGIScriptAlias / /path/to/Udacity-Catalog-Project/application.wsgi` to make apache serve the application.
* Serve static files (optional): Add the following code (Also inside the `<VirtualHost *:80>`):
```
Alias /assets/ /home/ubuntu/Udacity-Catalog-Project/assets/

<Directory /home/ubuntu/Udacity-Catalog-Project/assets>
    Options Indexes FollowSymLinks MultiViews
    AllowOverride None
    Require all granted
    allow from all
</Directory>
```
* Now let's restart apache using `sudo service apache2 restart`.

### Install and configure PostgreSQL.
* Use `sudo apt install postgresql postgresql-contrib` to install PostgreSQL.
* Use `sudo -u postgres psql` to access database server as root user.
* Create new database using `CREATE DATABASE catalog`.
* Create new user using `CREATE USER catalog WITH ENCRYPTED PASSWORD '123';`.
* Grant the new user access to the database using `GRANT ALL PRIVILEGES ON DATABASE "catalog" TO catalog;`.
