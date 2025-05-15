# CHOICEMATE - Your AI Shopping Assistant

## Project Overview

CHOICEMATE is an AI-powered personalized product recommendation system designed to enhance the online shopping experience. It helps users find the most relevant products across major e-commerce platforms like Amazon and Flipkart by understanding their needs through natural language chat interactions. The system leverages real-time web scraping, machine learning, and conversational AI to provide tailored suggestions with direct purchase links.

## Features

* **Personalized Recommendations:** Get product suggestions based on your specific preferences provided via chat.

* **AI Chat Assistant:** Interact with an intelligent assistant (powered by Gemini API) to describe your desired product, budget, and features.

* **Real-time Data:** Product information is scraped in real-time from Amazon and Flipkart to ensure up-to-date recommendations.

* **Cross-Platform Search:** Discover and compare products available on different e-commerce sites.

* **Direct Purchase Links:** Easily access recommended products on their original platform.

* **Secure Authentication:** Sign up and log in securely, including Google OAuth options.

## Technologies Used

* **Frontend:** React.js, Tailwind CSS/Bootstrap

* **Backend:** Node.js, Express.js

* **Database:** MongoDB

* **AI/ML:** Google Gemini API, Python (BeautifulSoup, Pandas, Pickle)

## Installation

To set up and run ChoiceMate locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd choicemate

   ```

2. **Set up the Backend:**

   * Navigate to the backend directory: `cd backend`

   * Install dependencies: `npm install`

   * Set up environment variables (e.g., MongoDB connection string, Gemini API key, Google OAuth credentials). Create a `.env` file if necessary based on project guidelines.

   * Install Python dependencies for scraping and ML: `pip install beautifulsoup4 requests pandas` (Ensure Python 3.x is installed)

   * Place your trained ML model (`.pkl` file) in the appropriate backend directory.

   * Start the backend server: `npm start`

3. **Set up the Frontend:**

   * Navigate to the frontend directory: `cd ../frontend`

   * Install dependencies: `npm install`

   * Configure API endpoints if necessary (usually in an environment file).

   * Start the frontend development server: `npm start`

The application should now be running on your local machine (typically backend on port 5000 and frontend on port 3000).

## Usage

1. Open your web browser and go to the frontend URL (e.g., `http://localhost:3000`).

2. Sign up for a new account or log in using your credentials or Google OAuth.

3. Once logged in, use the chat interface to describe the product you are looking for. Provide details like product type, budget, brand preferences, and desired features.

4. The AI assistant will process your request, scrape relevant data, and provide a list of recommended products.

5. Click on the "View Product" links to be redirected to the product page on Amazon or Flipkart.

## Troubleshooting

* **Backend not starting:** Check console logs for port conflicts or missing environment variables. Ensure MongoDB is running.

* **Frontend not connecting:** Verify the backend server is running and check the API endpoint configuration in the frontend.

* **Scraping issues:** E-commerce website structures change frequently. The scraping logic may need updates. Check Python script logs for errors. Ensure you are not being blocked by the website (consider adding delays or rotating headers).

* **No recommendations:** Ensure the Gemini API key is valid and the API is reachable. Verify the ML model file (`.pkl`) is correctly placed and loaded. Check if the scraping process successfully fetched data.

* **Incorrect recommendations:** The AI model may need retraining with more diverse data. Refine your chat queries to be more specific.

## Contributing

Contributed by Me and my friends

## License

MIT Licensed
