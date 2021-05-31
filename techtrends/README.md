# TechTreds Web Application

This is a Flask application that lists the latest articles within the cloud-native ecosystem.

## Run 

To run this application there are 3 steps required:

1. Install all the dependencies inside `requirements.txt` file by running: `pip install -r requirements.txt`
2. Initialize the database by using the `python init_db.py` command. This will create or overwrite the `database.db` file that is used by the web application.
3.  Run the TechTrends application by using the `python app.py` command. The application is running on port `3111` and you can access it by querying the `http://127.0.0.1:3111/` endpoint if running locally or `http://<VRTUAL_MACHINE_PUBLIC_IP>:3111/` if running on a Virtual Machine.
