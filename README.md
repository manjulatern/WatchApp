### Dependencies: 
* Python 3.7
* ChromeDriver for your chrome

1. Install VirtualEnv Wrapper
	* For Windows:
		`pip install virtualenvwrapper-win`
	* For Unix:
		`pip install virtualenvwrapper`

2. Virtual environment
	
	> This creates a new virtual environment and automatically activates it
	`mkvirtualenv watchscrapyenv`

	> To deactivate
	`deactivate watchscrapyenv`

	> To again enter the environment
	`workon watchscrapyenv`

3. Download the application provided and install all the requirements

	> Activate virtual enviroment
	`workon watchscrapyenv`

	> Install all the required libraries
	`pip install -r requirements.txt`

4. Now navigate to WatchExtraction/WatchInfo folder

	`cd WatchExtraction/WatchInfo`

5. Prepare application database

	> Setup database
	`python manage.py migrate`

	> Note: This will import all the history database for gold as well

6. Setup Cron Job
	
	* Cron Job settings

	> You can change the cron job setting in the django settings WatchExtraction/WatchInfo/settings.py.Default: Runs at 5 PM everyday

	`CRONJOBS = [
    		('0 17 * * *', 'goldapp.cron.gold_data_cron','>> ~/cron.log')
			]`
	
	* To schedule crontab job

	`python manage.py crontab add`

	* To see status of crontab job

	`python manage.py crontab show`

	* To stop all crontab job

	`python manage.py crontab remove`

7. Create a superuser
	
	`python manage.py createsuperuser`

8. Run Application

	`python manage.py runserver`

9. Admin Panel
	
	`http://127.0.0.1:8000/admin`

	> Create other users

10. Setup the application 
	* Navigate to the setup page.
	* Insert the location of your chromedriver.
	* You can download chromedriver from `https://chromedriver.chromium.org/downloads` based on your Chrome version
