```markdown
# 🚗 Tripalytics - Your Trip Analyst! 📊

Hey there! Welcome aboard Tripalytics! Here, we've crafted a nifty Flask API that swallows CSV data and serves up some fun analytics. Why? Well, because we can! 🥳

**Psst**... wanna join in on the fun? **Jobsity is hiring!** Jump right in!

## 📜 Table of Contents
- [What's Inside?](#whats-inside)
- [Documentation](#documentation)
- [Setting Things Up](#setting-things-up)
  - [Requirements](#requirements)
  - [Installation & Setup](#installation--setup)
- [APIs: What Can You Do?](#apis-what-can-you-do)
- [Test Drive! 🚀](#test-drive)
- [Chip In!](#chip-in)
- [License & Stuff](#license--stuff)

## 🧐 What's Inside?

Dive deep into the world of data with our Flask API. It munches on CSV files, stores data in PostgreSQL, and even plays with them to give you cool insights.

![Jobsity Magic](https://example.com/jobsity_logo.png)

## 📖 Documentation

We've documented everything! Dive into our:

- **[ER Model](./project_documentation/ER_model/)**
- **[Data Catalog](./project_documentation/data_catalog/)**
- **[AWS Architecture Sample](./project_documentation/aws_architecture/)**

## 🛠 Setting Things Up

Let's get this party started! 🎉

### Requirements

- A love for Python (3.6+ should do)
- PostgreSQL - 'cause where else would we keep our secrets?
- `pip` - Python's little helper

### Installation & Setup

1. Steal...err, I mean clone our code:
   ```bash
   git clone https://github.com/LeandroMartins0/Tripalytics.git
   ```

2. Dive into the project:
   ```bash
   cd Tripalytics
   ```

3. Let's create some isolated magic (optional but cool):
   ```bash
   python -m venv venv
   ```

4. Power up the magic:
   - For our Windows buddies:
     ```bash
     venv\Scripts\activate
     ```
   - For the macOS and Linux rockstars:
     ```bash
     source venv/bin/activate
     ```

5. Time for some more magic (dependencies, duh!):
   ```bash
   pip install -r requirements.txt
   ```

6. Whisper to PostgreSQL - tell it your secrets in `app/database/session.py`.

7. Fire up the engines!
   ```bash
   python main.py
   ```

8. And voilà! Catch the action at `http://localhost:5000`. 💥

## 🎯 APIs: What Can You Do?

We got tools! Here's a quick list:
- `/ingestion_status`: Last data munching status.
- `/weekly_average/<float:x1>/<float:y1>/<float:x2>/<float:y2>`: Weekly trip avg within a box.
- `/weekly_average/<string:region>`: Weekly trip avg by region.
- `/datasource_regions/<string:datasource>`: Regions per data source.
- `/grouped_trips`: Trips grouped by origin, destination, and time.
- `/latest_region/<string:datasource>`: Latest region for a given datasource.
...and a few more. Explore!

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

## 🤝 Chip In!

Found a bug or got a brilliant idea? Jump in! Open an issue, create a pull request, or just cheer us on!

## 📄 License & Stuff

We're all friends here! This project is under the [MIT License](LICENSE). Use, modify, share - just give a nod our way!

Join the fun! 🎉 Be a part of Jobsity!

![Cool Jobsity Team](https://example.com/jobsity_team_photo.jpg)
```