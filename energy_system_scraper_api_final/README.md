
# Energy System Scraper API

## **Overview**

The **Energy System Scraper API** is a web scraper designed to collect and process real-time energy system data. This API uses a combination of web scraping, data processing pipelines, and caching mechanisms to provide valuable insights into forecasted and actual energy demand. The solution supports various endpoints for data extraction, transformation, and aggregation, offering a simple and efficient way to access energy-related data for analysis, forecasting, and reporting.

The core functionality of the system includes:

- **Data Scraping**: Fetches real-time energy data.
- **Data Processing**: Transforms raw data into meaningful insights.
- **Data Aggregation**: Provides aggregated views of data based on specified criteria.
- **Caching**: Uses Redis for caching frequently accessed data, improving system performance.

## **Tech Stack**

The **Energy System Scraper API** is built using the following technologies:

- **FastAPI**: For building and serving the API.
- **BeautifulSoup** and **Selenium**: For web scraping.
- **pandas**: For data manipulation and aggregation.
- **SQLite**: For storing processed data.
- **Redis**: For caching data and improving performance.
- **Uvicorn**: ASGI server for serving the FastAPI app.

## **Getting Started**

### **1. Clone the Repository**

```bash
git clone <>
```

### **2. Create a Virtual Environment**

To create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
.env\Scriptsctivate
```

### **3. Install Dependencies**

Use the `requirements.txt` file to install all the required libraries:

```bash
pip install -r requirements.txt
```

### **4. Run the Application Locally**

To run the application locally:

```bash
python main.py
```

The application will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## **API Endpoints**

### **1. /scrape-data**

This endpoint fetches raw data from the source, processes it, and stores it in the database. If the data is already cached, it will return cached data.

- Method: **GET**
- Response: JSON indicating success or error.

### **2. /fetch-processed-data**

This endpoint retrieves processed data without saving it to the database.

- Method: **GET**
- Response: JSON with processed data.

### **3. /aggregated-data**

This endpoint aggregates the data based on a specified time period (e.g., monthly) and metric (e.g., sum, average).

- Method: **GET**
- Query Parameters:
    - **aggregation_type**: The type of aggregation (e.g., monthly, yearly).
    - **metric**: The metric to calculate (e.g., sum, average, min, max).
    - **date_range**: Date range for aggregation (optional).
- Response: JSON with aggregated data.

### **4. /fetch-raw-data**

This endpoint fetches raw data directly from the source without any transformation.

- Method: **GET**
- Response: JSON with raw data.

### **5. /fetch-all-data**

This endpoint retrieves all data stored in the database.

- Method: **GET**
- Response: JSON with all data from the database.

## **Database Configuration**

The application uses SQLite to store the processed energy data. Ensure the database file path is correctly set in the `config.py` file:

```python
"DATABASE_URL": f"sqlite:///{os.path.join(BASE_DIR, '..', 'db_storage', 'actual_forecast_report.db')}",
```

## **Caching**

To improve performance and avoid repeated processing, Redis is used for caching. The configuration can be found in the `config.py` file:

```python
"REDIS_HOST": "localhost",
"REDIS_PORT": 6379,
"REDIS_DB": 0,
```

## **Testing**

The project includes unit tests for various components of the application. To run the tests:

```bash
pytest
```

## **Deployment**

### **Railway Deployment**

To deploy the application on Railway:

1. Push the project to GitHub.
2. Create a new project on Railway and link your GitHub repository.
3. Railway will automatically detect the app and build it.
4. The application will be deployed, and the URL will be available in the Railway dashboard.

The deployment should be accessible at:

```bash
https://<your-railway-app-name>.up.railway.app
```

## **Environment Variables**

Ensure the following environment variables are configured in your deployment platform:

- **DATABASE_URL**: The connection URL for your SQLite database.
- **REDIS_HOST**, **REDIS_PORT**, **REDIS_DB**: Redis connection details.