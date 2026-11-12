# 🇹🇿 Tanzania Local Market Commodity Tracker

> A lightweight, pure-Python data analysis tool designed to track and analyze commodity prices (Maize, Rice, and Fuel) across key Tanzanian commercial hubs (Dar es Salaam, Mwanza, and Arusha).

## 🚀 About the Project
Market price volatility affects households, farmers, and businesses across East Africa. This project was built to practice foundational data engineering and software development skills—specifically data parsing, structural cleaning, and algorithmic aggregation without relying on heavy external frameworks. 

It serves as a clean, local-first utility to monitor regional pricing trends in Tanzanian Shillings (TZS).

## 📊 Features
* **Structured Data Ingestion:** Safely reads and parses raw market data from local CSV files using Python's built-in `csv` module.
* **Automated Data Cleaning:** Sanitizes text entries (trimming whitespace) and converts string metrics into numerical data types for accurate computation.
* **Regional Price Analysis:** Dynamically calculates cross-regional averages to highlight price differences between major cities like Dar es Salaam, Mwanza, and Arusha.
* **Lightweight & Dependency-Free:** Built entirely with native Python, ensuring it can run smoothly on low-bandwidth or resource-constrained machines.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Modules:** `csv` (Data parsing)
* **Version Control:** Git & GitHub

## 📂 Project Structure
```text
commodity-tracker/
│
├── commodities.csv       # Raw dataset containing regional prices and dates
├─ tracker.py            # Main script for data loading, cleaning, and analysis
├── .gitignore            # Files and folders to exclude from version control
└── README.md             # Project documentation