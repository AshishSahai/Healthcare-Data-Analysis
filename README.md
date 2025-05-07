# 🏥 Healthcare Data Analysis with SQL Integration

This project performs exploratory data analysis (EDA) on a healthcare dataset. It cleans, analyzes, and visualizes healthcare data with integration of SQL for querying and analysis.

## 📁 Dataset

Place your `healthcare_dataset.csv` file in the project directory. Optionally, a SQLite database file (`healthcare.db`) can be used for structured queries.

### Expected CSV Fields
- Name, Gender, Age, Blood Type
- Medical Condition, Admission Date, Discharge Date
- Hospital, Doctor, Insurance Provider
- Billing Amount, Admission Type, Medication

## 💡 Key Features

- Data Cleaning & Preprocessing
- SQL-based Analysis with Pandas & SQLite
- Missing & Duplicate Data Detection
- Visualization of:
  - Insurance Providers by Medical Condition
  - Billing by Age Group
  - Stay Duration vs Billing Amount
- Summary Insights

## 🗃 SQL Integration

You can load the dataset into a SQLite database using the following:

```python
import sqlite3
import pandas as pd

df = pd.read_csv("healthcare_dataset.csv")
conn = sqlite3.connect("healthcare.db")
df.to_sql("patients", conn, if_exists="replace", index=False)

# Example SQL query
query = "SELECT Medical_Condition, COUNT(*) FROM patients GROUP BY Medical_Condition"
pd.read_sql_query(query, conn)
```

📊 Visualizations

    📈 Bar chart: Total billing by age group

    📉 Line chart: Average billing by age group

    🟡 Scatter plot: Stay duration vs. billing amount

    🏥 Grouped bar chart: Insurance providers by medical condition

🛠 Requirements

    Python 3.7+

    pandas

    matplotlib

    seaborn

    numpy

    sqlite3 (included with Python)

Install dependencies

pip install pandas matplotlib seaborn numpy

🚀 Usage

Run the script:

python your_script_name.py

Make sure:

    healthcare_dataset.csv is in the same directory

    healthcare.db will be created if using SQL integration

📁 Outputs

    duplicate_rows.csv: Saved duplicate records

    healthcare.db: SQLite database (optional)

🔒 Data Privacy

⚠️ If using real-world healthcare data, ensure compliance with HIPAA, GDPR, or other relevant data protection laws.
📃 License

This project is licensed under the MIT License.

MIT License

Copyright (c) 2025 Ashish Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


