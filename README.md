>> Dependencies: 
- Python 3.7
- ChromeDriver for your chrome

1. Install VirtualEnv Wrapper
- For Windows:
	> pip install virtualenvwrapper-win
- For Unix:
	> pip install virtualenvwrapper

2. Virtual environment
- mkvirtualenv watchscrapyenv
> This creates a new virtual environment and automatically activates it

	To deactivate:
	- deactivate watchscrapyenv

	To again enter the environment
	- workon watchscrapyenv

3. Download the application provided and install all the requirements

- Activate virtual enviroment
	> workon watchscrapyenv

- pip install -r requirements.txt

4. Now navigate to WatchExtraction/WatchInfo folder
	> cd WatchExtraction/WatchInfo

5. Prepare application database
	> python manage.py migrate

6. Run Application
	> python manage.py runserver

7. Setup the application 
	> Navigate to the setup page.
	> Insert the location of your chromedriver.
	> You can download chromedriver from https://chromedriver.chromium.org/downloads based on your Chrome version






