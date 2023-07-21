# Flask OLX Scraper

This project is a web application based on the Flask framework, which allows users to view random ads from the OLX website. Users can register and log in to the system to get updated lists of ads.

## Installation
1. Clone the project repository:
```shell
git clone 
cd flask_olx
```
2. Create and activate a virtual environment:
```shell
python3 -m venv venv
source venv/bin/activate
venv\Scripts\activate (for Windows)
```
3. Create a .env file based on the .env.sample template and fill it with the necessary values
4. Install the dependencies:
```shell
pip install -r requirements.txt
```
5. Run database migration:
```shell
flask db init
flask db migrate
flask db upgrade
```
6. Start the server:
```shell
flask run
```
Now you can visit the app at http://127.0.0.1:5000/

## Endpoints:
http://127.0.0.1:5000/register - for user registration
http://127.0.0.1:5000/login - for user login
http://127.0.0.1:5000/update_ads - to get OLX ads

## Usage Instructions
- The _**/update_ads**_ page will display 100 random classified ads from the OLX website.
- To update the list of ads, click the "Update" button. This endpoint is accessible only to authenticated users.
- To get a new set of 100 random ads, simply press the "Update" button again.
