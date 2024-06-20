const axios = require("axios");
const cheerio = require("cheerio");
const fs = require("fs").promises;
const { isMainThread } = require("worker_threads");
const path = require("path");

const baseUrl =
  "https://parts.cat.com/api/product/list?sortBy=2&urlKeyword=shop-by-attachment&storeIdentifier=CATCorp&locale=en_US&storeId=21801&langId=-1";
const targetUrl = "https://parts.cat.com/en/catcorp/shop-by-attachment";

const headers = {
  Accept: "application/json, text/plain, */*",
  "Accept-Encoding": "gzip, deflate, br, zstd",
  "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,de;q=0.6",
  "Cache-Control": "no-cache",
  Pragma: "no-cache",
  Referer:
    "https://parts.cat.com/en/catcorp/shop-by-attachment?beginIndex=32&pageSize=16&productBeginIndex=32",
  "Sec-Ch-Ua":
    '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  "Sec-Ch-Ua-Mobile": "?0",
  "Sec-Ch-Ua-Platform": '"Windows"',
  "Sec-Fetch-Dest": "empty",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Site": "same-origin",
  "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
};

/**
 * Ensures that the directory for a given file path exists.
 *
 * @param {string} filePath The file path for which the directory should be created.
 * @returns {Promise<void>} A promise that resolves when the directory is created.
 * @throws {Error} If an error occurs while creating the directory.
 */
async function ensureDirectoryExistence(filePath) {
  const dirname = path.dirname(filePath);
  try {
    // Create directory if it doesn't exist
    await fs.mkdir(dirname, { recursive: true });
  } catch (error) {
    if (error.code !== "EEXIST") {
      // Ignore error if directory already exists
      throw error;
    }
  }
}

/**
 * Returns the current timestamp in the format "DD-MM-YYYY-HH-MM-SS".
 * @returns {string} The current timestamp.
 */
const getCurrentTimestamp = () => {
  const now = new Date();

  const padZero = (number) => number.toString().padStart(2, "0");

  const day = padZero(now.getDate());
  const month = padZero(now.getMonth() + 1); // Months are zero-based
  const year = now.getFullYear();
  const hours = padZero(now.getHours());
  const minutes = padZero(now.getMinutes());
  const seconds = padZero(now.getSeconds());

  return `${day}-${month}-${year}-${hours}-${minutes}-${seconds}`;
};

/**
 * Fetches initial details such as cookies and session IDs needed for further requests.
 *
 * @returns {Promise<{cookies: string[], trackingId: string, pccSessionId: string}>} A promise that resolves with an object containing cookies, tracking ID, and session ID.
 * @throws {Error} If an error occurs while fetching initial details.
 */
async function fetchInitialDetails() {
  try {
    const response = await axios.get(targetUrl, { headers });
    const cookies = response.headers["set-cookie"];
    const $ = cheerio.load(response.data);

    const trackingId = $('meta[name="X-Cat-Api-Tracking-Id"]').attr("content");
    const pccSessionId = $('meta[name="X-Cat-Pcc-Session-Id"]').attr("content");

    return { cookies, trackingId, pccSessionId };
  } catch (error) {
    console.error("Error fetching initial details:", error.message);
    throw error;
  }
}

/**
 * Fetches products from the API using the offset for pagination.
 *
 * @param {number} offset The offset for pagination.
 * @param {string[]} cookies Cookies for the session.
 * @param {string} trackingId Tracking ID for the API.
 * @param {string} pccSessionId Session ID for the API.
 * @returns {Promise<object[]>} A promise that resolves with a list of products.
 * @throws {Error} If an error occurs while fetching data from the API.
 */
async function fetchProducts(offset, cookies, trackingId, pccSessionId) {
  const url = `${baseUrl}&offset=${offset}`;
  try {
    const response = await axios.get(url, {
      headers: {
        ...headers,
        Cookie: cookies.join("; "),
        "X-Cat-Api-Tracking-Id": trackingId,
        "X-Cat-Pcc-Session-Id": pccSessionId,
      },
    });
    return response.data.products || [];
  } catch (error) {
    console.error(`Error fetching data from offset ${offset}:`, error.message);
    throw error;
  }
}

/**
 * Delays execution for a given number of seconds.
 *
 * @param {number} s The number of seconds to delay.
 * @returns {Promise<void>} A promise that resolves after the specified delay.
 */
async function delay(s) {
  return new Promise((resolve) => setTimeout(resolve, s * 1000));
}

/**
 * Worker function for fetching products in a range of offsets.
 *
 * @param {number[]} offsetRange The range of offsets to fetch products for.
 * @param {string[]} cookies Cookies for the session.
 * @param {string} trackingId Tracking ID for the API.
 * @param {string} pccSessionId Session ID for the API.
 * @returns {Promise<object[]>} A promise that resolves with a list of product information dictionaries.
 */
async function worker(offsetRange, cookies, trackingId, pccSessionId) {
  const productsList = [];
  for (const offset of offsetRange) {
    let success = false;
    let attempts = 0;
    while (!success && attempts < 5) {
      try {
        console.log(
          `Fetching data for offset ${offset}, attempt ${attempts + 1}`
        );
        const fetchedProducts = await fetchProducts(
          offset,
          cookies,
          trackingId,
          pccSessionId
        );
        fetchedProducts.forEach((product) => {
          const productInfo = {
            longDescription: product.longDescription || "",
            shortDescription: product.shortDescription || "",
            parentPartNumber: product.parentPartNumber || "",
            name: product.name || "",
            partNumber: product.partNumber || "",
            manufacturer: product.manufacturer || "",
            type: product.type || "",
            thumbnail: product.thumbnail || "",
            productURL: product.productURL || "",
            imageURL: product.imageURL || "",
            buyable: product.buyable || false,
          };

          product.attributes.forEach((attribute) => {
            const attrName = `${attribute.name}_${attribute.uom}`;
            productInfo[attrName] = attribute.value || "";
          });

          productsList.push(productInfo);
        });
        success = true;
      } catch (error) {
        attempts += 1;
        if (attempts < 5) {
          console.log("Retrying after error...");
          await delay(2);
        } else {
          console.error(
            `Failed to fetch data for offset ${offset} after ${attempts} attempts`
          );
        }
      }
    }
  }
  return productsList;
}

/**
 * Main function to coordinate the fetching and saving of product data.
 */
async function main() {
  const startTime = Date.now();
  const timestamp = getCurrentTimestamp();

  const { cookies, trackingId, pccSessionId } = await fetchInitialDetails();

  const offsets = Array.from({ length: 78 }, (_, i) => i);
  const offsetChunks = Array.from({ length: 6 }, (_, i) =>
    offsets.slice(i * 13, i * 13 + 13)
  );

  const workerPromises = offsetChunks.map((chunk) =>
    worker(chunk, cookies, trackingId, pccSessionId)
  );

  const allProductsList = (await Promise.all(workerPromises)).flat();

  const csvContent = [
    Object.keys(allProductsList[0]).join(","),
    ...allProductsList.map((product) =>
      Object.values(product)
        .map((value) => `"${value}"`)
        .join(",")
    ),
  ].join("\n");

  const fileName = `./csv/products-${timestamp}.csv`;

  // Ensure directory exists
  await ensureDirectoryExistence(fileName);

  console.log(`Attempting to write file at path: ${fileName}`);
  await fs.writeFile(fileName, csvContent, "utf-8");

  const endTime = Date.now();
  const duration = (endTime - startTime) / 1000;

  console.log(
    "Data has been successfully exported in CSV format."
  );
  console.log(`Scraping completed in ${duration.toFixed(2)} seconds.`);
}

if (isMainThread) {
  main().catch((error) => console.error("Error in main:", error));
}
