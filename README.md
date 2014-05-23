Checks for site title, sends email when it does not exist.

There are easier ways to do this, but wanted to use a real browser.

Prereqs:  
Java - needed to run the selenium standalone server  
Firefox - browser being used  
python - needed to run python script  
  
  
  
1. Go to http://docs.seleniumhq.org/download/.  Go to the section "Selenium Server (formerly the Selenium RC Server)" and download the latest version of selenium server.  The file should look something like "selenium-server-standalone-x.xx.x.jar", where x is the version number.  
  
2.  Open a terminal and run the selenium server jar file.  For example, run the following:  
java -jar selenium-server-standalone-x.xx.x.jar

3.  Open another terminal and run the sitechecker.  

"""Takes command line arguments and processes them

    -u		--url			<string>	'http://area515.org'
    -t		--title			<string>	'Des Moines Makerspace'
    -f		--fromemail		<string>	'somebot@gmail.com'
    -p		--password		<string>	'somebotspassword'
    -to		--toemail		<string>	'persontoalert@gmail.com'
    -lo		--log			<string>	'sitechecker-area515.log'
    
"""

Example scenario.  We want to check the site http://area515.org for the title "Des Moines Makerspace".  If the site is unavailable, we want to send an email to "persontoalert@gmail.com".  We will send this email from a gmail account like, "somebot@gmail.com".  We also want a log of the everything going on.  Our log will be named, "sitechecker-area515.log".

Our example command looks like this:  
python sitechecker.py -u 'http://area515.org' -t 'Des Moines Makerspace' -f 'somebot' -p 'sombotspassword' -to 'persontoalert@gmail.com' -lo 'sitechecker-area515.log'

(Optional)  
1.  Make sitechecker.py executable.  In a terminal, go to the directory that contains "sitechecker.py" and enter the following:  
chmod +x ./sitechecker.py

After this you will be able to run the command as follows:  
./sitechecker.py -u 'http://area515.org' -t 'Des Moines Makerspace' -f 'somebot' -p 'sombotspassword' -to 'persontoalert@gmail.com' -lo 'sitechecker-area515.log'

2.  Schedule the sitechecker to run every hour (crontab).  Run the following:  
crontab -e -u youruser  
  
"youruser" is the username you want the command to run as.  
  
At the end of this file, enter:  

0 * * * * /home/youruser/sitechecker/sitechecker.py -u 'http://area515.org' -t 'Des Moines Makerspace' -f 'somebot' -p 'sombotspassword' -to 'persontoalert@gmail.com' -lo 'sitechecker-area515.log'  

Exit and save the file.

