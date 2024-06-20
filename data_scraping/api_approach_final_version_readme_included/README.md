# Product Scraper

This project is a web scraper that fetches product information from a [specified URL](https://parts.cat.com/en/catcorp/shop-by-attachment), processes the data, and saves it into a CSV file. The script is written in Node.js using `axios` for HTTP requests, `cheerio` for parsing HTML, and `fs.promises` for file operations.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Node.js and npm.
- Alternatively, you can run with Docker, for this Docker and Docker Compose should be installed.
- You have an internet connection.

## Installation

To install the dependencies, run the following command:

```sh
npm install
```

## Usage

To run the scraper, use the following command:

```sh
npm run start
```

or

```sh
node index.js
```

This will start the scraper, fetch the product data, and save it to a `products-<timestamp>.csv` file in the `csv` folder in the project directory. The timestamp will reflect the time of scraping.

## Docker Usage

You can also run the scraper using Docker and Docker Compose. This method ensures that all dependencies are containerized and the environment is consistent.

### Build and Run with Docker Compose

1. Build and start the container:

    ```sh
    docker-compose up --build
    ```

    This command will build the Docker image and start the container, mounting the `csv` folder from your host system into the container. The output CSV files will be written to the `csv` directory with timestamps.

### Docker Compose Configuration

The `docker-compose.yml` file is configured to build the image from the Dockerfile in the current directory, set the appropriate time zone to `Asia/Baku`, and mount a volume for the output CSV files:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - TZ=Asia/Baku
    volumes:
      - ./csv:/usr/src/app/csv
```

## Script Details

### fetchInitialDetails

Fetches initial details such as cookies and session IDs needed for further requests.

**Returns**: A promise that resolves with an object containing cookies, tracking ID, and session ID.

### fetchProducts

Fetches products from the API using the offset for pagination.

**Parameters**:
- `offset` (number): The offset for pagination.
- `cookies` (string[]): Cookies for the session.
- `trackingId` (string): Tracking ID for the API.
- `pccSessionId` (string): Session ID for the API.

**Returns**: A promise that resolves with a list of products.

### delay

Delays execution for a given number of seconds.

**Parameters**:
- `s` (number): The number of seconds to delay.

### worker

Worker function for fetching products in a range of offsets.

**Parameters**:
- `offsetRange` (number[]): The range of offsets to fetch products for.
- `cookies` (string[]): Cookies for the session.
- `trackingId` (string): Tracking ID for the API.
- `pccSessionId` (string): Session ID for the API.

**Returns**: A promise that resolves with a list of product information dictionaries.

### main

Main function to coordinate the fetching and saving of product data.

**Usage**: This function is executed when the script is run. It handles the initial setup, divides the work among multiple workers, and saves the final product data to a CSV file with a timestamp in the `csv` folder.

## Additional Notes

- **Setting Offsets**: The script divides the work among multiple workers based on the specified number of offsets. It is important to set an appropriate number of offsets to ensure efficient pagination and data fetching.
- **Optimal Number of Threads**: The script uses multiple threads to fetch product data concurrently. Choose the optimal number of threads based on the expected product count and available system resources. This helps in maximizing efficiency and reducing the overall execution time.
- **Product Count Check**: Although the number of products is unlikely to change frequently, it is recommended to check the total product count before scraping. This ensures that the offsets and threads are appropriately configured to handle any changes in the product count.

By considering these additional factors, you can ensure that the scraper runs efficiently and handles any variations in the product count.