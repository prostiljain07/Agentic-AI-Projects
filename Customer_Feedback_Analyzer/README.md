# Customer Feedback Analyzer

A small Python app for analyzing customer reviews with AI. The project combines a Streamlit frontend, a FastAPI backend, and a SQLite database to classify reviews, assign a sentiment score, identify the main topic, and save results for later review.

## Features

- Paste one or more customer reviews at a time
- Analyze each review for:
  - sentiment label: positive, negative, or neutral
  - score from 1 to 5
  - main theme such as delivery, price, service, or quality
- View a simple summary of the analyzed batch
- Save results to a local SQLite database
- Review previously saved results from the app history

## Tech Stack

- Python 3.10+
- Streamlit for the web UI
- FastAPI for the analysis API
- Google GenAI for review analysis
- SQLite for local data storage

## Project Structure

- [app.py](app.py) - Streamlit frontend and results display
- [api.py](api.py) - FastAPI backend that calls the AI model
- [database.py](database.py) - SQLite helpers for saving and loading history
- [main.py](main.py) - basic entry point
- [pyproject.toml](pyproject.toml) - project dependencies

## Getting Started

1. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies
   ```bash
   pip install -e .
   ```

3. Set up your environment variable for the AI service
   Create a file named `.env` in the project root and add:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

4. Start the backend server
   ```bash
   uvicorn api:app --reload
   ```

5. In a second terminal, start the Streamlit app
   ```bash
   streamlit run app.py
   ```

6. Open the local Streamlit URL shown in the terminal and begin analyzing reviews.

## Usage

- Paste customer reviews into the text area, one review per line.
- Click Analyze to get sentiment results for each review.
- Use Save to database to store the results locally.
- Open the Saved history section to view prior entries.

## Notes

- The app expects a valid Google API key to generate analysis results.
- Saved records are stored in a local file named `feedback.db` in the project directory.
