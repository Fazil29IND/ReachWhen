# ReachWhen - Tamil Nadu Train Journey Duration Predictor 

ReachWhen is a Machine Learning web application built with Flask that predicts the duration of train journeys based on parameters like travel distance, number of stops, and station details. It uses an XGBoost regression model trained on comprehensive railway datasets, logs prediction results into a MySQL database, and visualizes the Actual vs. Predicted durations using Matplotlib.

## Features
* **Duration Prediction:** Leverages a pre-trained XGBoost Regressor to estimate train journey times.
* **Interactive UI:** A user-friendly HTML/CSS interface served via Flask for quick data entry.
* **Data Logging:** Stores all user inputs, actual durations, and predicted durations into a MySQL database (`ReachWhen`) for tracking and analytics.
* **Visual Insights:** Generates dynamic Matplotlib bar charts comparing Actual vs. Predicted duration directly on the results page.

## Tech Stack
* **Backend:** Python, Flask
* **Machine Learning:** Scikit-Learn, XGBoost, Pandas, Numpy, Joblib, Matplotlib
* **Database:** MySQL (`mysql-connector-python`)
* **Data Visualization:** Matplotlib
* **Frontend:** HTML & CSS 

## Repository Structure
* `ReachWhen.py`: The main Flask application script handling web routing, database connections, model inference, and chart generation.
* `Machine Learning Model.pkl`: The serialized XGBoost Regressor model.
* `Machine Learning Model.ipynb`: Jupyter Notebook detailing the data exploration, preprocessing, and model training workflow.
* `Dataset1.csv`: The training dataset containing train schedules, distances, and station data.
* `Database.sql`: SQL script to instantiate the necessary MySQL database and logging tables.
* `requirements.txt`: List of Python dependencies required to run the application.

## Installation & Setup Instructions

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/ReachWhen.git](https://github.com/your-username/ReachWhen.git)
cd ReachWhen
### 2. Install dependencies
Ensure you have Python installed, then run the following command to install the required libraries:
```bash
pip install -r requirements.txt
### 3.Setup the MySQL Database
Open your MySQL client or command line.
Run the provided SQL script to create the database and table:
```bash
mysql -u root -p < Database.sql
