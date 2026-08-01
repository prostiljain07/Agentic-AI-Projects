# AI Shopping Assistant

This project is a simple AI-powered shopping assistant built with Python, Streamlit, LangChain, and a local SQLite database. It lets users search for products, view ratings, and place orders through a chat-style interface.

## What the app does

The assistant can:
- Search products by keyword, price, and organic status
- Retrieve average customer ratings for products
- Help users place an order after they confirm a product
- Analyze an uploaded product image to find similar products

## Project structure

- app.py - Streamlit web app UI
- shopping_agent.py - LangChain agent and shopping tools
- reviews_api.py - Helper functions for reading product review data
- store.db - SQLite database containing products, reviews, and orders
- images/ - Sample images used in the project

## Requirements

Make sure you have Python 3.10+ installed.

Install the required packages:

```bash
pip install streamlit python-dotenv langchain langchain-groq
```

## Environment setup

Create a .env file in this folder and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

## Run the app

From this folder, run:

```bash
streamlit run app.py
```

The app will open in your browser.

## Example prompts

Try prompts like:
- I want organic honey under $15
- Show me products with 4.5+ rating and under $20
- Find me a good olive oil
- I uploaded a product image and want similar items

## Notes

- Product search results come from the local SQLite database.
- Ratings are read from the reviews table.
- Checkout writes orders into the database when the user confirms a purchase.
