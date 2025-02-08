# Data-visualization-project
## Overview
Data Insights Assistant is a dynamic and intuitive web application designed for **data analysis** and **visualization**. Built using Streamlit, this application enables users to upload datasets, check their quality, detect anomalies, and generate customized visualizations powered by **AI-based recommendations**.

## Features
The application consists of three primary modules, providing a seamless and powerful data exploration experience:

1. **Homepage**
   - **Introduction**: Offers an overview of the application and its capabilities.
   - **Intuitive Navigation**: A sidebar menu allows easy access to all modules.

2. **Data Quality Tests**
   - **Check Missing Values**: Identifies and displays columns with missing data and their percentages.
   - **Detect Duplicates**: Highlights duplicate rows in the dataset.
   - **Low Variance Columns**: Lists columns with a single unique value, which can be considered for removal.
   - **High Missing Value Columns**: Flags columns with more than 50% missing values.
   - **Outlier Detection**: Uses the Interquartile Range (IQR) method to find outliers in numeric columns.

3. **AI-Powered Data Analysis**
   - **Generate Recommendations**: Leverages AI to analyze data trends and provide actionable recommendations.
   - **Anomaly Detection**: Identifies unusual patterns or outliers in the dataset and provides insights on handling them.
   - **Custom Visualizations**: Allows users to describe the visualization they want, and the AI generates Python code to create it using Matplotlib, Seaborn, or Plotly.

## Project Structure
The project consists of the following files:

### 1. `app.py`
This is the main entry point of the application. It provides navigation between the different modules:
- Homepage
- Data Quality Tests
- AI-Powered Data Analysis

#### Key Features:
- **Streamlit Sidebar**: Navigation menu for switching between sections.
- **Integration with tests.py**: Redirects users to the data quality tests page.
- **Custom Visualization Generation**: Uses AI to create Python code for visualizations based on user input.

### 2. `tests.py`
This file focuses on **data quality checks**:
- **Missing Values**: Identifies columns with missing values and their percentages.
- **Duplicate Rows**: Detects and counts duplicate entries in the dataset.
- **Low Variance Columns**: Flags columns with a single unique value.
- **High Missing Values**: Highlights columns with more than 50% missing values.
- **Outliers**: Uses the IQR method to detect numeric outliers.

### 3. `LLMapp.py`
This file integrates **Anthropic's Claude API** to provide AI-powered analysis:
- **Recommendations**: Uses an AI model to analyze the dataset and generate insights and recommendations.
- **Anomaly Detection**: Identifies patterns or irregularities in the data.
- **Code Generation for Visualizations**: Based on user input, the AI generates Python code for creating advanced data visualizations.

### 4. `utils.py`
Provides utility functions for data handling and preprocessing:
- **File Reading**: Supports both CSV and Excel file uploads.
- **Data Cleaning**: Handles missing values and duplicate entries.
- **Data Overview**: Displays dataset dimensions, column names, and a preview of the data.
