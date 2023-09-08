
```markdown
# 🚗 Tripalytics: Analyzing Your Journeys 📊

Welcome to Tripalytics, a dynamic Flask API that seamlessly ingests CSV data to provide insightful travel analytics.

## 📜 Table of Contents
- [Overview](#overview)
- [Documentation](#documentation)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Configuration](#installation--configuration)
- [API Features](#api-features)
- [API Examples](#api-examples)
- [Contributing](#contributing)
- [Licensing](#licensing)

## 🌐 Overview

Unlock the potential of data with this Flask API. It digests CSV files, archives data in PostgreSQL, and crafts valuable insights for you.

## 📖 Documentation

For a comprehensive understanding of the project, please explore:

- **[ER Model](./project_documentation/ER_model/)**
- **[Data Catalog](./project_documentation/data_catalog/)**
- **[AWS Architecture Sample](./project_documentation/aws_architecture/)**

## 🛠 Getting Started

Let's set the stage!

### Prerequisites

- Python (version 3.6 or higher)
- Pip (version 23.2.0 or later)
- PostgreSQL (Ensure a database named "triptalytics" with the password "1234" is created)

### Installation & Configuration

1. Clone the repository:
   ```bash
   git clone https://github.com/LeandroMartins0/Tripalytics.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Tripalytics
   ```

3. Install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL: Modify the connection settings in `app/database/session.py` if different from the default.

5. Launch the application:
   ```bash
   python main.py
   ```

6. Access the API on: `http://localhost:5000`.

## 🎯 API Features

Here's a snapshot of what the API offers:
- `/ingestion_status`: Get the most recent data ingestion status.
- `/weekly_average/<float:x1>/<float:y1>/<float:x2>/<float:y2>`: Retrieve weekly trip averages within specified coordinates.
- `/weekly_average/<string:region>`: Fetch weekly trip averages by region.
- `/datasource_regions/<string:datasource>`: Display regions for each data source.
... Dive in for more!

## 🚀 Test Drive!

You wanna play? Check out these examples using the API endpoints:

### `/ingestion_status`

- **Method:** GET
- **Description:** Provides information about the last data ingestion status.

Example usage:
```bash
curl http://127.0.0.1:5000/ingestion_status
```

### `/weekly_average/14.4/49.9/14.6/50.1`

- **Method:** GET
- **Description:** Calculates the weekly average of trips within a bounding box.

Example usage:
```bash
curl http://127.0.0.1:5000/weekly_average/14.4/49.9/14.6/50.1
```

### `/datasource_regions/funny_car`

- **Method:** GET
- **Description:** Retrieves the regions associated with a specific data source.

Example usage:
```bash
curl http://127.0.0.1:5000/datasource_regions/funny_car
```

### `/weekly_average/Prague`

- **Method:** GET
- **Description:** Calculates the weekly average of trips for a specific region.

Example usage:
```bash
curl http://127.0.0.1:5000/weekly_average/Prague
```

### `/most_recent_datasource_for_top_regions`

- **Method:** GET
- **Description:** Identifies the most recent data source for the top regions with the highest trip counts.

Example usage:
```bash
curl http://127.0.0.1:5000/most_recent_datasource_for_top_regions
```

### `/total_records`

- **Method:** GET
- **Description:** Retrieves the total number of records in the database.

Example usage:
```bash
curl http://127.0.0.1:5000/total_records
```

### `/select_all_records`

- **Method:** GET
- **Description:** Retrieves all records from the database.

Example usage:
```bash
curl http://127.0.0.1:5000/select_all_records
```

## 🤝 Contributing

Stumbled upon an improvement or detected a bug? We welcome collaboration! Open an issue, suggest a pull request, or share your insights.

## 📄 Licensing

Respect for intellectual property! This project operates under the [MIT License](LICENSE). Feel free to use, alter, and share—just credit the source.

Thank you for considering Tripalytics. Feedback and contributions are always appreciated!

```