# for setting up flask with wsgi for python:
# Reference 1: http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/ 
#  Reference 2: http://terokarvinen.com/2016/deploy-flask-python3-on-apache2-ubuntu

1. Ubuntu loaded with flask and wsgi
2. create .wsgi file for the app, can put it in the top level of where the app's py code is. e.g. amazeriffic.wsgi  in the same folder of amazeriffic.py  and is in /var/www/html/htdocs.  This path is used in the amazeriffic.conf file. 

Content of file amazeriffic.wsgi:

	import sys
 
	sys.path.append('/var/www/html/htdocs/')
 
	from amazeriffic import app as application

3. Use your favorite text editor in Ubuntu (e.g. vi) create app's .conf file in /etc/apache2/sites-available
	For the amazeriffic project, the file will be  /etc/apache2/sites-available/amazeriffic.conf. 
	
	Content of file:
	
	<virtualhost *:80>
		ServerName amazeriffic
 
		WSGIDaemonProcess amazeriffic user=www-data group=www-data threads=5 home=/var/www/html/htdocs/
		WSGIScriptAlias / /var/www/html/htdocs/amazeriffic.wsgi
 
		<directory /var/www/html/htdocs>
			WSGIProcessGroup amazeriffic
			WSGIApplicationGroup %{GLOBAL}
			WSGIScriptReloading On
			AllowOverride All
			Require all granted
		</directory>
	</virtualhost>

4. add 127.0.0.1 amazeriffic to /etc/hosts   # no need when no registered domain name. You don't have a registered domain name for this class.
5. sudo a2dissite 000-default.conf
6. sudo a2ensite amazeriffic.conf
7. sudo a2enmod wsgi						# important
8. sudo systemctl restart apache2			# restart apache server
	In Ubuntu 16.04, there is no output from restart if no error.  
9. sudo systemctl status apache2			# You may use to check apache status. use q to return to prompt at the end of the status display.
	
10. Test on Ubuntu VM with :   curl localhost:80
11. Test with browser on host machine: http://localhost:8080
12. In theory, with reload set to on in the .conf file, when py code is changed, don't need to restart apache.  Use the touch command to make the changes effective, see example:
touch /var/www/html/htdocs/amazeriffic.wsgi. 

# But, I found that need to update the amazerific.wigi file (e.g. put a space at the end of one of the comment, then save, before issuing the touch command.

13. Now, follow the instructions in file "setUpAppDatabases.txt" to set up the amazeriffic database schema (tables and procedures).
