# Project Overview
- This project aims to build a data pipeline that performs ETL (Extract, Transform, Load) processes, allowing users to ingest raw data in the form of Excel files, normalize the data, and store it for querying. The pipeline is designed to be extensible for future use cases, enabling complex queries on commission data across different agents and FMOs.

# Key Features
- **CLI Interface**: The project includes a CLI that allows users to upload data, input metadata, and export the normalized data.
- **Metadata-Driven Normalization**: Uses a flexible YAML configuration file to map and normalize raw input data into a consistent schema.
- **Data Storage and Queries**: Normalized data is saved to both CSV and SQLite databases, supporting structured queries to retrieve insights like top earners by commission payout.


# How It Works

## ETL Pipeline
- **Extract**: The input data, Excel files, in the future will support other formats like CSV or JSON.
- **Transform**:
  - Columns are mapped to a fixed schema based on the user's metadata.
  - Data types are aligned to the schema.
  - Business rules are applied, such as identifying Earner Type (FMO, Agent, etc.).
- **Load**: The normalized data is saved in both CSV and SQLite formats, ready for querying.

## Key Components
- **Input Data**: Any Excel file uploaded by the user
- **Metadata (YAML Config)**: Describes the structure of the input data
- **Fixed Schema**: The normalized schema designed to support future queries.
  - `Primary_Key`
  - `Earner_Name`
  - `Earner_ID`
  - `Agent_Name`
  - `Agent_ID`
  - `Commission_Amount`
  - `Commission_Period`
  - `Carrier_Name`
  - `Enrollment_Type`
  - `Plan_Name`
  - `Member_Name`
  - `Member_ID`
  - `Effective_Date`
  - `Cycle_Year`
  - `Earner_Type` (distinguishes between FMO, agents, and agencies)


## Data Flow
1. Users upload both their raw data and an associated metadata file.
2. The system normalizes the data based on the fixed schema and business rules.
3. The processed data is stored in a SQLite database or exported as a CSV.
4. The system supports SQL-like queries to extract insights from the stored data.

---

## CLI Commands

- **upload**:
  - **Usage**: `python main.py upload <data_file> --config <yaml_config>`
  - Upload and process Excel files.

- **find_top_k_carrier**:
  - **Usage**: `python main.py find_top_k_carrier <k>`
  - Find the top K carriers based on commission.
  - **Parameters**:
    - `k`: The number of carriers to return (type: `int`).

- **find_top_k_earner**:
  - **Usage**: `python main.py find_top_k_earner <k> <period>`
  - Find the top K earners based on commission for a given period.
  - **Parameters**:
    - `k`: The number of earners to return (type: `int`).
    - `period`: The period of time (type: `str`).

- **find_top_k_plan**:
  - **Usage**: `python main.py find_top_k_plan <k>`
  - Find the top K plans based on commission.
  - **Parameters**:
    - `k`: The number of plans to return (type: `int`).

- **list_carriers**:
  - **Usage**: `python main.py list_carriers`
  - List all carriers.

- **sql_query**:
  - **Usage**: `python main.py sql_query "<SQL Query>"`
  - Execute a SQL query on the normalized dataframe.

- **export_csv**:
  - **Usage**: `python main.py export --output <path_to_csv>`
  - Export the normalized CSV to the specified file path.

---
![img.png](img.png)
![img_1.png](img_1.png)

## Assumptions on Business and Data Model
- The system supports **FMOs** (Field Marketing Organizations) as intermediaries between insurance carriers and agents.
- **Commission Data**: The core data processed includes commission payouts for agents and FMOs for specific health plan enrollments.
- **Earner Type**: Distinguishes between agents and FMOs to allow granular querying.
- **Query Logic**: When querying top agents or FMOs, the system calculates the total commission by summing up the `Commission_Amount` for each earner. Earners can be either FMOs, agents, or agencies.
- **Commission Interpretation**:
  - **Positive Commission**: Represents the earnings or profit made by the earner.
  - **Negative Commission**: Represents losses or deductions from the earner’s total commission.

---
### Extensibility, High Cohesion, and Low Coupling

- **Extensibility**: The system is designed with extensibility in mind, allowing future commands to be easily added. Each command is self-contained within its own class, and new functionalities can be added by simply creating a new class method in the `command` folder. This eliminates the need to modify the `main.py` file for adding new commands.

- **High Cohesion**: Each command class is focused on a single task, ensuring that the functionality within each class is closely related. This results in more maintainable code, where each class serves a distinct role, such as uploading files, exporting data, or executing SQL queries.

- **Low Coupling**: The system's design ensures that different components (like command classes) are loosely connected, meaning that changes in one component do not affect others. This modularity makes the system flexible and easy to extend without breaking existing functionality.

### Adding New Commands

- To add new commands to the CLI, simply create a new class under the `command` folder. Each class should inherit from a common base class and implement its own logic.

- **No changes needed to `main.py`**: The `main.py` file is designed to automatically discover and register any new commands added to the system, ensuring that new functionalities can be introduced without modifying the core logic.

For example, if you want to add a new command to calculate the average commission for a specific period, you would:

1. Create a new class in the `command` folder, e.g., `CalculateAverageCommission`.
2. Define the command’s logic within this class.
3. The new command will be automatically registered by the system and can be invoked via the CLI without altering the main program.

This design ensures that the system remains flexible, modular, and easy to maintain over time.

---
### Folder Explanation

- **data/**: Stores the input data files (Excel).
- **database/**: Stores the final output (normalized CSV).
- **src/**: Contains backend logic and processing scripts.
- **config/**: Application settings and schema configurations.
- **yaml_config/**: Stores metadata YAML files uploaded by users.


### API Design

- **Low-level API**: SQL-like query commands via CLI. This allows users to directly query the normalized data using SQL syntax for custom analysis.

- **Mid-level API**: Customizable SQL queries. Users can execute customized SQL queries based on their needs, such as retrieving top agents, carriers, or commission details for a specified period.

---
### Primary Key Handling

- **User-Provided Primary Key**: Users are required to provide a primary key in the metadata (YAML config) to uniquely identify records in their data. 

- **Generated Primary Key**: If a user does not provide a primary key in their metadata, the system will automatically generate a **composite primary key** using available columns from the fixed schema. This composite key is created by concatenating several key attributes (such as `Earner_Name`, `Commission_Amount`, `Commission_Period`, etc.), ensuring uniqueness.

- **Maintaining Clean Data**: The primary key plays a crucial role in maintaining clean and deduplicated data. If a user uploads the same Excel file multiple times, the system uses the generated or provided primary key to ensure that duplicate records are not added to the normalized CSV or SQLite database. This way, the system prevents data redundancy and ensures the integrity of the stored data.



