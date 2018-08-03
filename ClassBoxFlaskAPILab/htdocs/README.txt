1. vagrant ssh
2. use the /sproc files to set up your amazeriffic database tables and schema
3. Create your dbconfig.txt file
4. In order to use the authentication, you will need to add the following to the 
	config file /etc/apache2/sites-available/amazeriffic.conf:
        WSGIPassAuthorization On    within the <directory > tags.
        
    The resulting conf should look like this:
    	
		<virtualhost *:80>
			ServerName amazeriffic
			DocumentRoot "/var/www/html/htdocs"
 
			WSGIDaemonProcess amazeriffic user=www-data group=www-data threads=5 home=/var/www/html/htdocs/
			WSGIScriptAlias / /var/www/html/htdocs/amazeriffic.wsgi
 
			<directory /var/www/html/htdocs>
				WSGIProcessGroup amazeriffic
				WSGIApplicationGroup %{GLOBAL}
				WSGIScriptReloading On
				WSGIPassAuthorization On		
				AllowOverride All
				Require all granted
			</directory>
		</virtualhost>      
		
5. restart apache after updated config
6. Now, you should be ready to work on your RESTful API to create a task, and to modify 
your API to get a task, as instructed in amazeriffic.py (search for 'for lab' in the .py file and read the requirements.)
