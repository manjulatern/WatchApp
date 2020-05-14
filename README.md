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

- pip install -r requirements.txt [File is attached in the application]

4. Now navigate to WatchExtraction/WatchInfo folder
	> cd WatchExtraction/WatchInfo

5. Prepare application database
	> python manage.py migrate

6. Run Application
	> python manage.py runserver

7. Setup the application [Only for Christies and Sothebys]
	> Navigate to the setup page.
	> Insert the location of your chromedriver.
	> You can download chromedriver from https://chromedriver.chromium.org/downloads based on your Chrome version
	> This is required for Christies/Sothebys
	[Info] The latest version of chromedriver has some issues and hence shows some unstability signs. I am still workong to fix this.

>> Known issues

1. Christies spider is a little bit unstable due to chromedriver unstability. I have contacted google developers about this issue. You can test this in your system and let me know the results.
2. Sotheybys is the most secure one as already mentioned, this requires some additional work to finish.
3. Heritage doesn't provide information on prices unless logged in. If you can provide me a valid username/password for this, i can pull those informations as well.






