# LookAround

LookAround is a Location Bingo Game application.

![Image](https://github.com/ptaxx/LookAround/blob/main/assets/ScreenshotHome.png)

LookAround is our SDA Python course final project. 

This project was made for people who like to travel, and for business owners, who woulf like to promote their respective business. The player can play the game, by completing the tasks on a bingo board. The application uses OpenWeatherAPI.

## Technology

This project is based on:

Python 3.12.3

Django5.1.3

MYSQL

## Installation

1. Clone the repository:

   git clone [https://github.com/ptaxx/LookAround.git]
   
2. Create a virtual environment:

   python -m venv venv

   On Linux/Mac source venv/bin/activate   
   
   On Windows: venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Copy the example environment file:

   cp .env.example .env

5. Database Setup

   Ensure MySQL is installed and running.

   Create a MySQL database named lookaround.

   Update the database configuration in .env with your MySQL credentials

6. Migrate the models:

   python manage.py migrate

7. Start the development server

   python manage.py runserver

## API reference

This app uses OpenWeatherAPI to fetch data.

You should get your own API key at https://openweathermap.org/ and update API_KEY in the .env file

## Views

In this project we use ClassBased views.

## Credits

This project was made as a collaboration by

Kati Kraavi

Kristjan Peek

Daniil Popov

Tanel Tarkvee

Monika Vihmand
