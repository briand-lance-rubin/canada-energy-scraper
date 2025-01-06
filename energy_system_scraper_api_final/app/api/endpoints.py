from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.scraper.fetcher import Fetcher
from app.scraper.parser import Parser
from app.scraper.transformer import Transformer
from app.database.operations import DatabaseOperations
from config import logger, CONFIG  # Import CONFIG here
from app.api.models import AggregatedDataRequest  # Import AggregatedDataRequest
import pandas as pd  # Import pandas as pd
from app.cache.cache import Cache  # Import Cache for caching functionality

router = APIRouter()

@router.get("/")
async def root():
    """
    Root endpoint to confirm the API is running.
    """
    logger.info("Root endpoint accessed.")
    return {
        "message": "Welcome to the Energy System Scraper API!",
        "description": (
            "This API provides endpoints for scraping, processing, and analyzing "
            "energy market data. Use the available endpoints to fetch raw, processed, "
            "and aggregated data, or to store data into the database for further analysis."
        ),
        "usage": {
            "scrape_data": "/scrape-data",
            "fetch_processed_data": "/fetch-processed-data",
            "fetch_raw_data": "/fetch-raw-data",
            "fetch_all_data": "/fetch-all-data",
            "aggregated_data": "/aggregated-data?aggregation_type=monthly&metric=average",
        },
        "note": "Replace 'monthly' and 'average' in the aggregated_data example with your desired values."
    }

@router.get("/scrape-data")
async def scrape_data():
    """
    Endpoint to scrape data, transform it in batches, and save it to the database.
    """
    logger.info("Received request to scrape data.")
    try:
        cache = Cache()  # Initialize cache

        # Check if the data is already in the cache
        cache_key = "scraped_data"
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info("Data retrieved from cache.")
            return {"status": "success", "data": cached_data}

        # If data is not in cache, fetch and process it
        logger.info("Fetching new data.")
        fetcher = Fetcher(CONFIG["SCRAPER_URL"])  # Correct instantiation
        html_content = await fetcher.fetch()  # Ensure 'await' is added here for async function

        # Step 2: Parse the HTML content
        parser = Parser()
        headers, rows = parser.parse_table(html_content)

        # Combine headers and rows into raw_data
        raw_data = []
        for row in rows:
            row_data = dict(zip(headers, row))  # Combine header and row to form a dictionary
            raw_data.append(row_data)

        # Log raw_data for verification
        logger.info(f"Prepared raw_data: {raw_data[:5]}...")  # Log a sample of the raw data

        # Step 3: Transform the data in batches
        transformer = Transformer()

        # Log the value of batch_size before passing it
        batch_size = 500
        logger.info(f"Passing batch_size={batch_size} to transform_data")
        transformed_data_generator = transformer.transform_data(raw_data, batch_size=batch_size)

        # Step 4: Check the type of the returned data
        processed_data = []
        if isinstance(transformed_data_generator, list):  # If it's a list of DataFrames (batches)
            for batch_df in transformed_data_generator:
                if isinstance(batch_df, pd.DataFrame):
                    processed_data.extend(batch_df.to_dict(orient="records"))
                else:
                    logger.error(f"Expected a DataFrame, but got {type(batch_df)}")
        elif isinstance(transformed_data_generator, pd.DataFrame):  # If it's a single DataFrame
            processed_data.extend(transformed_data_generator.to_dict(orient="records"))
        else:
            logger.error(f"Unexpected return type: {type(transformed_data_generator)}")

        # Log processed data for verification
        logger.info(f"Processed data: {processed_data[:5]}...")  # Log a sample of the processed data

        # Step 5: Save processed data to the database
        db_ops = DatabaseOperations()

        # Ensure processed_data is in the right format (list of dicts or DataFrame)
        if isinstance(processed_data, pd.DataFrame):
            # If it's already a DataFrame, we can save it directly
            db_ops.save_data(processed_data.to_dict(orient="records"))
        elif isinstance(processed_data, list):
            # If it's a list, we can save it directly as a list of dicts
            db_ops.save_data(processed_data)
        else:
            logger.error(f"Unexpected data format: {type(processed_data)}")

        # Cache the processed data
        cache.set(cache_key, processed_data)

        logger.info("Data scraped, transformed, and saved successfully.")
        return {"status": "success", "message": "Data scraped, transformed, and saved successfully."}
    except Exception as e:
        logger.error(f"Error during scrape process: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/fetch-processed-data")
async def fetch_processed_data():
    """
    Endpoint to fetch processed data without saving it to the database.
    """
    logger.info("Received request to fetch processed data.")
    try:
        # Initialize cache
        cache = Cache()
        cache_key = "processed_data"

        # Check if the data is already in the cache
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info("Data retrieved from cache.")
            return {"status": "success", "data": cached_data}

        # If not in cache, fetch raw data
        fetcher = Fetcher(CONFIG["SCRAPER_URL"])
        html_content = await fetcher.fetch()  # Ensure 'await' is added here for async function

        # Parse the HTML content
        parser = Parser()
        headers, rows = parser.parse_table(html_content)

        # Combine headers and rows into raw_data
        raw_data = []
        for row in rows:
            row_data = dict(zip(headers, row))  # Combine header and row to form a dictionary
            raw_data.append(row_data)

        # Transform the data
        transformer = Transformer()
        batch_size = 500
        transformed_data_generator = transformer.transform_data(raw_data, batch_size=batch_size)

        # Collect processed data batches for the response
        processed_data = []
        if isinstance(transformed_data_generator, list):  # If it's a list of DataFrames (batches)
            for batch_df in transformed_data_generator:
                if isinstance(batch_df, pd.DataFrame):
                    processed_data.extend(batch_df.to_dict(orient="records"))
                else:
                    logger.error(f"Expected a DataFrame, but got {type(batch_df)}")
        elif isinstance(transformed_data_generator, pd.DataFrame):  # If it's a single DataFrame
            processed_data.extend(transformed_data_generator.to_dict(orient="records"))
        else:
            logger.error(f"Unexpected return type: {type(transformed_data_generator)}")

        # Cache the processed data
        cache.set(cache_key, processed_data)

        logger.info("Processed data fetched successfully.")
        return {"status": "success", "data": processed_data}
    except Exception as e:
        logger.error(f"Error fetching processed data: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/fetch-all-data")
async def fetch_all_data():
    """
    Endpoint to fetch all data from the database.
    """
    logger.info("Received request to fetch all data from the database.")
    try:
        # Fetch all data from the database
        db_ops = DatabaseOperations()
        data = db_ops.fetch_all_data()

        logger.info("All data fetched successfully.")
        return {"status": "success", "data": data.to_dict(orient="records")}
    except Exception as e:
        logger.error(f"Error fetching all data: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/aggregated-data")
async def aggregated_data(
    aggregation_type: str = Query(..., description="Type of aggregation (monthly, yearly, etc.)"),
    metric: str = Query(..., description="Metric to calculate (average, sum, min, max, etc.)"),
    date_range: Optional[str] = Query(None, description="Date range for aggregation, e.g., '2023-01-01_to_2023-12-31'"),
    category: Optional[str] = Query(None, description="Optional category for grouping the data, e.g., region, product")
):
    """
    Endpoint to fetch aggregated data based on the aggregation type and metric.
    """
    logger.info(f"Received request for {aggregation_type} aggregation with metric {metric}.")

    # Parse date range if provided
    if date_range:
        start_date, end_date = date_range.split("_to_")
    else:
        start_date, end_date = None, None

    try:
        # Fetch data from the database
        db_ops = DatabaseOperations()
        data = db_ops.fetch_all_data()

        # Perform aggregation based on the requested type
        if aggregation_type == "monthly":
            data["Month"] = data["Date"].dt.to_period("M")
            if metric == "average":
                aggregated_data = data.groupby("Month").mean().reset_index()
            elif metric == "sum":
                aggregated_data = data.groupby("Month").sum().reset_index()
            elif metric == "min":
                aggregated_data = data.groupby("Month").min().reset_index()
            elif metric == "max":
                aggregated_data = data.groupby("Month").max().reset_index()
            else:
                raise HTTPException(status_code=400, detail="Unsupported metric")

        elif aggregation_type == "yearly":
            data["Year"] = data["Date"].dt.year
            if metric == "average":
                aggregated_data = data.groupby("Year").mean().reset_index()
            elif metric == "sum":
                aggregated_data = data.groupby("Year").sum().reset_index()
            elif metric == "min":
                aggregated_data = data.groupby("Year").min().reset_index()
            elif metric == "max":
                aggregated_data = data.groupby("Year").max().reset_index()

        # If a category is specified, apply the grouping by category
        if category:
            aggregated_data = aggregated_data.groupby(category).agg({metric: "sum"})

        # Ensure `Month` is converted to string in the output
        if "Month" in aggregated_data:
            aggregated_data["Month"] = aggregated_data["Month"].astype(str)

        # Return the aggregated data
        logger.info(f"Aggregation completed for {aggregation_type} with metric {metric}.")
        return {"status": "success", "aggregated_data": aggregated_data.to_dict(orient="records")}

    except Exception as e:
        logger.error(f"Error during aggregation: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/fetch-raw-data")
async def fetch_raw_data():
    """
    Endpoint to fetch raw data (without transformation or saving).
    """
    logger.info("Received request to fetch raw data.")
    try:
        # Step 1: Fetch raw HTML content
        fetcher = Fetcher(CONFIG["SCRAPER_URL"])
        html_content = fetcher.fetch()

        # Step 2: Parse the HTML content
        parser = Parser()
        headers, rows = parser.parse_table(html_content)

        # Combine headers and rows into raw_data
        raw_data = {"headers": headers, "rows": rows}
        logger.info("Raw data fetched successfully.")
        return {"status": "success", "data": raw_data}
    except Exception as e:
        logger.error(f"Error fetching raw data: {e}")
        return {"status": "error", "message": str(e)}
