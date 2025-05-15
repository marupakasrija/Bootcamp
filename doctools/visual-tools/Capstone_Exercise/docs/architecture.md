# ChoiceMate Architecture Overview

This document describes the high-level architecture and key components of the ChoiceMate AI Shopping Assistant.

## System Overview

ChoiceMate is designed as a multi-tiered web application that facilitates personalized product discovery through a conversational interface. It integrates a frontend user interface, a backend application server, a database, external AI services, and a data processing layer that includes web scraping and machine learning.

## Architecture Diagram

(See the Block Diagram immersive for a visual representation of the architecture)

## Key Components

1.  **Frontend (React.js):**
    * Provides the user interface, including the login/signup pages, the chat interface, and the product recommendations display.
    * Handles user input and interactions.
    * Communicates with the Backend via RESTful APIs.
    * Manages UI state and responsiveness.

2.  **Backend (Node.js/Express.js):**
    * Serves as the application server and API layer.
    * Handles user authentication and session management.
    * Routes user requests from the Frontend to appropriate services.
    * Orchestrates interactions between the Database, Gemini API, Web Scraping Module, and ML Model.
    * Implements business logic for processing user preferences and filtering data.

3.  **MongoDB Database:**
    * NoSQL database used for storing application data.
    * Stores user information (credentials - securely hashed, profiles).
    * Stores chat history for context and personalization.
    * Could potentially store cached product data (though real-time scraping is primary).

4.  **Gemini API:**
    * External AI service for Natural Language Processing (NLP).
    * Receives user queries from the Backend.
    * Analyzes chat messages to understand user intent and extract structured product preferences (e.g., category, budget, features).
    * Returns the extracted preferences to the Backend.

5.  **Web Scraping Module (Python/BeautifulSoup):**
    * Separate module (likely invoked by the Backend) responsible for extracting real-time product data from e-commerce websites (Amazon, Flipkart).
    * Uses libraries like BeautifulSoup and Requests to parse HTML content.
    * Collects key product attributes (title, price, rating, link, etc.).
    * Includes logic for handling potential scraping blocks or HTML structure changes (requires maintenance).

6.  **ML Model (Pickle file):**
    * A pre-trained machine learning model (likely trained using Python libraries like Pandas and scikit-learn, and saved as a `.pkl` file).
    * Loaded by the Backend.
    * Takes structured product data (from scraping) and user preferences (from Gemini API) as input.
    * Applies recommendation logic to rank and select the most relevant products.

## Data Flow

1.  User interacts with the Frontend chat.
2.  Frontend sends the chat message to the Backend API.
3.  Backend sends the message to the Gemini API for NLP.
4.  Gemini API returns structured preferences to the Backend.
5.  Backend initiates the Web Scraping Module to gather data from relevant E-commerce Websites based on preferences.
6.  Web Scraping Module returns raw data to the Backend.
7.  Backend processes and structures the scraped data.
8.  Backend feeds the structured data and user preferences to the loaded ML Model.
9.  ML Model returns recommended product details to the Backend.
10. Backend sends the recommendations to the Frontend.
11. Frontend displays the recommended products to the User.
12. User clicks a link, and the Frontend redirects them to the E-commerce Website.
13. User interactions and chat history are logged in the MongoDB Database via the Backend.

## Key Constraints

* **Real-time Data Dependency:** System performance and recommendation accuracy are tied to the success and speed of the web scraping process.
* **External API Dependency:** Functionality relies on the availability and performance of the Gemini API.
* **Data Volume:** Handling and processing large volumes of scraped data efficiently is critical.
* **E-commerce Website Changes:** Changes in the target websites' structure require updates to the scraping module.
* **ML Model Maintenance:** The recommendation model may need periodic retraining to maintain accuracy and adapt to new trends.

This architecture provides a foundation for a flexible and intelligent shopping assistant, allowing for future enhancements such as supporting more platforms, integrating advanced AI features, and improving recommendation algorithms.
