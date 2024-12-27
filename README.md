# Recruitment Pipeline Projection Tool

The **Recruitment Pipeline Projection Tool** is an interactive Streamlit application that allows users to analyze historical recruitment data, calculate conversion rates, and project pipeline volumes for various recruitment stages. The tool provides customizable stages, data visualizations, and the ability to download projections as CSV files.

---

## Features

- **Customizable Recruitment Stages**:
  - Configure recruitment stages (e.g., Applications, Phone Screen, Offers, etc.) via an intuitive sidebar.

- **Historical Data Upload**:
  - Upload historical recruitment data in CSV format to analyze trends and conversion rates.

- **Conversion Rate Analysis**:
  - Automatically calculate conversion rates between recruitment stages based on historical data.

- **Pipeline Projection**:
  - Predict the number of candidates required at each stage to meet hiring targets.

- **Interactive Visualizations**:
  - View recruitment trends over time using line charts.
  - Display projected pipeline volumes with bar charts.

- **CSV Download**:
  - Export projected pipeline data and conversion rates as a downloadable CSV file.

---

## How It Works

1. **Set Recruitment Stages**:
   - Use the sidebar to customize the number and names of recruitment stages.

2. **Upload Historical Data**:
   - Upload a CSV file containing recruitment data with the following columns:
     - `Year` (required)
     - Columns for each recruitment stage (e.g., `Applications`, `Hires`, etc.).

3. **Analyze Conversion Rates**:
   - The app calculates the average conversion rates between consecutive recruitment stages.

4. **Project Pipeline**:
   - Input a target number of hires to estimate required volumes at earlier stages.

5. **Visualize and Export**:
   - View historical and projected pipeline data through interactive charts.
   - Download projection results as a CSV file.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/recruitment-pipeline-tool.git
   cd recruitment-pipeline-tool

2. Install dependencies:

    ```bash
    pip install -r requirements.txt

3. Run the app:

    ```bash
    streamlit run app.py
