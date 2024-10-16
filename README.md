# Alerta EDM

Alerta EDM, is a simple web application to inform incoming programmed power outages for the mozambican people in differents states/areas.

## Features 
- Scrape scheduled power outages from EDM website using personalized commands or a GET request.
- Expose these power outages through a web page or REST API.
- Filter by date and province
- Ability to view previous power outages

## Table of Contents

- [Installation](#installation-and-setup-configuration)
- [Usage](#usage)
- [Running the Scraper](#running-the-scraper)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [License](#license)

---

## Installation and Setup Configuration

### Pre-requisites
Ensure you have Python 3xx in your machine.


1. **Clone the repository:**

    ```bash
    git clone https://github.com/AghastyGD/alerta-edm
    ```

2. **Navigate to the project directory:**

    ```bash
    cd alerta-edm
    ```
3. **Create and activate a virtual environment:**
    ```bash
    # Create virtual environment
    python -m venv venv
    
    # Activate virtual environment
    # On Windows
    venv\Scripts\activate
    
    # On MacOS/Linux
    source venv/bin/activate
    ```

4. **Install the requirements:**

    ```bash
    pip install -r requirements.txt
    ```
    
5. **Setup environment variables:**

    Create a .env file in the root directory to configure env variables. You can do something like this:
    ```bash
    cp .env.sample .env
    ```
    and then fill theses variables with your values:
    ```bash
   # .env
    DJANGO_ENVIRONMENT= # choose between 'dev' or 'prod'
    DATABASE_URL= your_db_url # only applicable if you are in prod environment
    SECRET_KEY= your_secret_key
    BROWSER=your_browser # Currently we support only 'chrome' and 'firefox'
    ```
6. **Run migrations:**
    ```bash
    # make migrations
    python manage.py makemigrations
    
    # migrate
    python manage.py migrate
    ```
    

## Usage

### Run the server
```bash
python manage.py runserver 
```
**Only for Windows users**:

_If you face any error about `pkg_resources` module not found when executing the project, please install or upgrade setuptools:_
```bash
pip install setuptools
```
Once the server is running, you can access the application at `http://localhost:8000/` in your web browser.

## Running the Scraper

### Scraper Logic

- **`core/scraper.py`**: This script is responsible for all the logic of pulling information from the programmed power outage table on the EDM website. It scrapes the data, rearranges it, and sends it to our database.

#### Custom Command: `scrap`

- **`core/management/commands/scrap.py`**: This file defines a custom Django management command `scrap`, which inherits the logic from `scraper.py`. By running this command, you can execute the scraper directly from the terminal without needing to interact with the code manually.

    To run the scraper using the custom management command, execute the following:

    ```bash
    python manage.py scrap
    ```

    This command will:
    1. Scrape the scheduled power outage data from the EDM website.
    2. Format and clean the data as needed.
    3. Insert the data into project's database.

---

#### Scraping via URL

In addition to running the scraper manually using the `scrap` management command, you can also trigger the scraping via a simple HTTP GET request to a specific endpoint.

- **Endpoint**: `/run-scraper/`
- **Method**: `GET`
- **Description**: : This endpoint triggers the same scraping process that the scrap management command does, but in a web-friendly way. It collects data from the EDM website and inserts it into the database. This is useful for automating or remotely triggering the scraper.

    **Example Request**:
    
    ```bash
    curl -X GET http://localhost:8000/run-scraper/
    ```

    Upon hitting this endpoint, the backend will:
    1. Scrape the power outage data from the EDM website.
    2. Insert the data into the database.
    3. Return a success response if the operation was successful or an error message if something went wrong.

---
## API Endpoints
### 1. Power Outages List API: 
- **Endpoint:** /api/power-outages/
- **Method:** GET
- **Description:** List all power outages.
- **Query Parameters:**
    - start_date: The start date to filter outages (optional, format: YYYY-MM-DD).
    - end_date: The end date to filter outages (optional, format: YYYY-MM-DD).

### 2. Power Outage Detail API:
- **Endpoint:** /api/power-outage/{id}/
- **Method:** GET
- **Description:** Retrieve details of a specific power outage.

### 3. Power Outages by State:
- **Endpoint:** /api/power-outages/{slug}/
- **Method:** GET
- **Description:** Get scheduled outages for a specific state.
- **Query Parameters:**
    - start_date: The start date to filter outages (optional).
    - end_date: The end date to filter outages (optional).


      **Example Request:**
        ```bash
        curl -X GET http://localhost:8000/api/power-outages/provincia-de-sofala/?start_date=2024-07-15&end_date=2024-10-16"
        ```
    
      **Example Response:**
        ```json
        {
          "province": "Provincia de Sofala",
          "total_outages": 2,
          "outages": [
            {
              "date": "2024-08-20",
              "locations": [
                {
                  "area": "DRC",
                  "affected_zone": "Matacuane, Macurungo",
                  "start_time": "06:00",
                  "end_time": "16:00"
                }
              ]
            },
            {
              "date": "2024-09-22",
              "locations": [
                {
                  "area": "Beira",
                  "affected_zone": "Ponta Gêa, Maquinino",
                  "start_time": "08:00",
                  "end_time": "15:00"
                }
              ]
            }
          ]
        }
        ```

### 4. Swagger API Documentation:
- **Endpoint:** /api/swagger/
- **Method:** GET
- **Description**: Although Django Rest Framework already provides a basic interface for testing API endpoints (the default browsing page), Swagger has been added as a richer and more interactive alternative for exploring and testing the API.

## Testing
To run the tests, navigate to the root directory of the project and in your terminal do:
```bash
python manage.py test
```
Running specific test:
```bash
python manage.py test core.tests.test_models
```

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details

## Aditional details
- This API is still in development, however some features are still being studied.
- Contributions are welcome! Feel free to fork the repository and submit a pull request with any improvements or bug fixes.

If you have any questions or encounter issues, don't hesitate to reach out: [https://augusto-domingos.vercel.app/](https://augusto-domingos.vercel.app/)
