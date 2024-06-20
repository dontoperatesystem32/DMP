const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

const baseUrl = 'https://parts.cat.com/api/product/list?sortBy=2&urlKeyword=shop-by-attachment&storeIdentifier=CATCorp&locale=en_US&storeId=21801&langId=-1';
const targetUrl = 'https://parts.cat.com/en/catcorp/shop-by-attachment';

const headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,de;q=0.6',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Referer': 'https://parts.cat.com/en/catcorp/shop-by-attachment?beginIndex=32&pageSize=16&productBeginIndex=32',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
};

const fetchInitialDetails = async () => {
    try {
        const response = await axios.get(targetUrl, { headers });
        const cookies = response.headers['set-cookie'];
        const $ = cheerio.load(response.data);

        const trackingId = $('meta[name="X-Cat-Api-Tracking-Id"]').attr('content');
        const pccSessionId = $('meta[name="X-Cat-Pcc-Session-Id"]').attr('content');

        return { cookies, trackingId, pccSessionId };
    } catch (error) {
        console.error('Error fetching initial details:', error.message);
        throw error;
    }
};

const fetchProducts = async (offset, cookie, trackingId, pccSessionId) => {
    const url = `${baseUrl}&offset=${offset}`;
    try {
        const response = await axios.get(url, {
            headers: {
                ...headers,
                'Cookie': cookie,
                'X-Cat-Api-Tracking-Id': trackingId,
                'X-Cat-Pcc-Session-Id': pccSessionId
            }
        });
        return response.data.products;
    } catch (error) {
        console.error(`Error fetching data from offset ${offset}:`, error.message);
        throw error;
    }
};

const delay = (s) => new Promise((resolve) => setTimeout(resolve, 1000*s));

const main = async () => {
    let allProducts = [];
    const { cookies, trackingId, pccSessionId } = await fetchInitialDetails();

    // Convert cookies array to a single string
    const cookieString = cookies.map(cookie => cookie.split(';')[0]).join('; ');

    for (let offset = 0; offset <= 78; offset++) {
        let success = false;
        let attempts = 0;
        while (!success && attempts < 5) {
            try {
                console.log(`Fetching data for offset ${offset}, attempt ${attempts + 1}`);
                const products = await fetchProducts(offset, cookieString, trackingId, pccSessionId);
                allProducts = allProducts.concat(products);
                success = true;
            } catch (error) {
                attempts++;
                if (attempts < 5) {
                    console.log(`Retrying after error...`);
                    await delay(2); // Wait 2 seconds before retrying
                } else {
                    console.error(`Failed to fetch data for offset ${offset} after ${attempts} attempts`);
                }
            }
        }
        await delay(0.5); // Wait 1 second between requests to avoid overwhelming the server
    }

    // Save the collected data to a JSON file
    fs.writeFileSync('products.json', JSON.stringify(allProducts, null, 2));
    console.log('Data saved to products.json');
};

main();
