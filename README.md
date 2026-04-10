# AI-Integrated Library Management System — Data Analysis & Prediction

An end-to-end analytical solution designed to modernize traditional library operations through data science and predictive modeling. This project focuses on transaction analysis, student behavior mapping, and automated fine calculation.

-----

## 📋 Table of Contents

1.  [Project Overview](https://www.google.com/search?q=%23project-overview)
2.  [Problem Statement](https://www.google.com/search?q=%23problem-statement)
3.  [Objectives](https://www.google.com/search?q=%23objectives)
4.  [Key Features](https://www.google.com/search?q=%23key-features)
5.  [System Architecture](https://www.google.com/search?q=%23system-architecture)
6.  [Tech Stack](https://www.google.com/search?q=%23tech-stack)
7.  [Project Structure](https://www.google.com/search?q=%23project-structure)
8.  [Dataset Description](https://www.google.com/search?q=%23dataset-description)
9.  [Data Preprocessing](https://www.google.com/search?q=%23data-preprocessing)
10. [Exploratory Data Analysis](https://www.google.com/search?q=%23exploratory-data-analysis)
11. [Machine Learning Model](https://www.google.com/search?q=%23machine-learning-model)
12. [Results & Insights](https://www.google.com/search?q=%23results--insights)
13. [Screenshots](https://www.google.com/search?q=%23screenshots)
14. [Installation & Setup](https://www.google.com/search?q=%23installation--setup)
15. [Usage](https://www.google.com/search?q=%23usage)
16. [Deployment](https://www.google.com/search?q=%23deployment)
17. [Future Improvements](https://www.google.com/search?q=%23future-improvements)
18. [Limitations](https://www.google.com/search?q=%23limitations)
19. [Contribution Guidelines](https://www.google.com/search?q=%23contribution-guidelines)
20. [License](https://www.google.com/search?q=%23license)
21. [Acknowledgements](https://www.google.com/search?q=%23acknowledgements)
22. [Project Team](https://www.google.com/search?q=%23project-team)

-----

## 📖 Project Overview

The **AI-Integrated Library Management System** is a data-driven project that moves beyond basic record-keeping. By utilizing a synthetic dataset of 1,000+ transactions involving 200 students and 30 titles, this project applies Python-based analytical tools to uncover hidden patterns in book circulation and applies Machine Learning to predict financial liabilities (fines) based on overdue duration.

## ⚠️ Problem Statement

Traditional library systems act as passive databases. They record "who" took "what" but fail to answer "why" trends occur or "when" a resource will become unavailable. Manual fine calculation is prone to error, and library staff often lack visual evidence to optimize book procurement based on department-specific demand.

## 🎯 Objectives

  * **Automate Data Auditing:** Clean and format messy transaction logs into structured data.
  * **Behavioral Analysis:** Identify peak borrowing periods and most active student departments.
  * **Predictive Modeling:** Implement a Linear Regression model to forecast fine amounts.
  * **Visual Intelligence:** Provide stakeholders with high-impact charts for resource allocation.

## 🚀 Key Features

  * **Automated Cleaning Pipeline:** Handles null values and standardizes ISO dates.
  * **Dynamic Visualizations:** 8 distinct chart types covering trends, genres, and ML results.
  * **Fine Prediction Engine:** A Scikit-learn powered model for financial forecasting.
  * **Feature Engineering:** Derived columns such as "Days Overdue" and "Return Status" from raw timestamps.

## 🏗 System Architecture

The project follows a modular Data Science lifecycle:

1.  **Data Acquisition:** Loading CSV/XLSX transaction records.
2.  **Preprocessing:** Type casting, handling missing entries, and feature scaling.
3.  **EDA (Exploratory Data Analysis):** Statistical profiling and correlation analysis.
4.  **Modeling:** Splitting data into Training/Testing sets and applying Linear Regression.
5.  **Output:** Generating Matplotlib/Seaborn plots and model evaluation metrics (MSE, R2 Score).

## 🛠 Tech Stack

| Category | Tools/Libraries |
| :--- | :--- |
| **Language** | Python 3.x |
| **Data Manipulation** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Machine Learning** | Scikit-learn |
| **Environment** | Jupyter Notebook, VS Code |
| **Version Control** | Git, GitHub |

## 📂 Project Structure

```text
├── charts/                 # Generated visualization images
├── data/                   # Library transaction datasets (CSV/XLSX)
├── notebooks/              # Jupyter Notebooks for analysis & cleaning
├── report/                 # Formal academic project report (PDF)
├── research paper/         # IEEE format research documentation
├── presentation/           # PPTX for faculty demonstration
├── index.html              # Web view for GitHub Pages
└── README.md               # Project documentation
```

## 📊 Dataset Description

  * **Size:** 1000+ Transaction records.
  * **Entities:** 200 Students, 30 Unique Book Titles.
  * **Core Columns:** `TransactionID`, `StudentID`, `BookID`, `Genre`, `IssueDate`, `ReturnDate`, `ExpectedReturnDate`, `Department`.

## 🧹 Data Preprocessing Steps

1.  **Date Conversion:** Converted object-type date strings into `datetime64` for arithmetic operations.
2.  **Null Management:** Filled missing `ReturnDate` entries for active borrowings using the current date context.
3.  **Feature Engineering:** \* Calculated `Days_Overdue` = `Actual_Return_Date` - `Expected_Return_Date`.
      * Generated `Fine_Amount` based on a logic of ₹5/day for overdue items.

## 📈 Exploratory Data Analysis

We conducted deep dives into the following:

  * **Borrowing Trends:** Identification of "High-Traffic" months (e.g., Exam months).
  * **Genre Popularity:** Determining which academic genres (e.g., AI, DBMS) require more stock.
  * **Overdue Patterns:** Correlation between student departments and late returns.
  * **Demand vs Availability:** Ratio of total books to unique borrowers.

## 🤖 Machine Learning Model

**Algorithm:** Linear Regression
**Purpose:** To establish a mathematical relationship between the number of days a book is overdue and the final fine amount.

  * **Input (Feature):** `Days_Overdue`
  * **Output (Target):** `Fine_Amount`
  * **Evaluation:** The model achieved a high R² score, confirming that fine growth is linear and predictable, which can be integrated into a front-end UI for real-time calculation.

## 💡 Results & Insights

  * **Top Genre:** Computer Science books account for 45% of total transactions.
  * **Peak Period:** Borrowing spikes significantly in the 3rd and 7th months of the academic year.
  * **Financial Impact:** 15% of students consistently incur fines, suggesting a need for a notification system.

## 🖼 Screenshots

| Analysis | Visual Placeholder |
| :--- | :--- |
| **Genre Distribution** |  |
| **Monthly Trends** |  |
| **ML Regression Plot** |  |

## ⚙️ Installation & Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/farhan0386/sem-2-minor_project.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd sem-2-minor_project
    ```
3.  Install dependencies:
    ```bash
    pip install pandas numpy matplotlib seaborn scikit-learn notebook
    ```

## 🖥 Usage

1.  Open Jupyter Notebook:
    ```bash
    jupyter notebook
    ```
2.  Run `notebooks/final_analysis.ipynb` to see the complete data pipeline and visualizations.

## 🌐 Deployment

The documentation and static results are hosted via **GitHub Pages**.
[View Live Project Site](https://www.google.com/search?q=https://farhan0386.github.io/sem-2-minor_project/)

## 🔮 Future Improvements

  * **Advanced ML:** Implementing Random Forest to predict *which* student is likely to be overdue.
  * **Chatbot Integration:** Using NLP to handle book queries.
  * **Real-time Dashboard:** Connecting the backend to a Streamlit or Flask web app.

## ⚠️ Limitations

  * **Synthetic Data:** The dataset is generated; real-world human behavior may vary.
  * **Linearity:** The current fine model only considers time, not "Book Rarity" or "Student History."

## 🤝 Contribution Guidelines

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/NewAnalysis`).
3.  Commit your Changes (`git commit -m 'Add some NewAnalysis'`).
4.  Push to the Branch (`git push origin feature/NewAnalysis`).
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🎓 Acknowledgements

  * **Faculty Mentors** at K.R. Mangalam University for their guidance in AI/ML.
  * **Open Source Community** for Pandas and Scikit-learn documentation.

## 👥 Project Team

  * **Farhan** (Team Leader & Lead Developer)
  * **Avijit** (Developer)
  * **Kartik** (Technical Documentation)
  * **Tanishka** (Documentation Support)
  * **Aman** (Data Collection)
  * **Trigya** (Data Collection)

-----

**Institution:** K.R. Mangalam University, Gurugram  
**Department:** CSE (AI & ML)
