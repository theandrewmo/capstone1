# HoppyHour Brewery Search App

HoppyHour is a brewery search application built using Python, Flask, WTForms, Jinja, SQLAlchemy, and JavaScript. The app allows users to search for breweries and discover their information such as location, ratings, and reviews.

## Features

- **Brewery Search**: Users can search for breweries by location, name, or other criteria.
- **Brewery Details**: Users can view detailed information about a selected brewery, including its location, contact details, ratings, and reviews.
- **User Reviews**: Registered users can leave reviews and ratings for breweries.
- **User Authentication**: User registration and authentication system is implemented using Flask's user management features.

## Deployment

The HoppyHour app is deployed using [Render](https://render.com) and the database is hosted on [ElephantSQL](https://www.elephantsql.com/). The app is accessible at [HoppyHour App](https://hoppyhour.onrender.com/).

## Installation

To run the HoppyHour app locally, follow these steps:

1. Clone the repository:

   git clone (https://github.com/theandrewmo/hoppyhour)
   cd HoppyHour
   
2. Create and activate a virtual environment:

   python3 -m venv venv
   source venv/bin/activate
    
3. Install the required dependencies:
   
   pip install -r requirements.txt
   
4. Set up Environment Variables

  To set up the environment variables, follow these steps:

   1. Create a .env file in the root directory of the project.

   2. Add the following variables to the file with appropriate values:
  
      FLASK_APP=app.py
      FLASK_ENV=development
      SECRET_KEY=your_secret_key
      DATABASE_URL=your_database_url

   
 5. Run the Flask development server:

     flask run
     
     The app will be accessible at http://localhost:5000.

Database Setup
HoppyHour uses a PostgreSQL database hosted on ElephantSQL. To set up the database:

1. Create a PostgreSQL database on ElephantSQL.

2. Update the DATABASE_URL variable in the .env file with the connection URL for your database.

3. Run the database migration to create the necessary tables:

  flask db upgrade
  
  This will create the required tables in the database.
  
Contributing
Contributions to HoppyHour are welcome! If you find any bugs or have suggestions for new features, please open an issue or submit a pull request. Make sure to follow the existing code style and conventions.


License
This project is not licensed.
   
   
   
   
   
   
   
   
   
   
   
   

