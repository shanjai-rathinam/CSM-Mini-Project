# Mini-Project: Legacy IT Systems Migration to Cloud

This repository contains a complete mini-project outlining the strategy, design, and implementation steps for migrating a legacy IT incident management system to a modern, cloud-native architecture.

## 1. Project Overview & Scenario

### The Legacy System
The project simulates the migration of an on-premise IT Service Management (ITSM) system. This legacy system is characterized by:
- A monolithic architecture, making updates slow and risky.
- High operational and maintenance costs for on-premise servers.
- Limited scalability, leading to performance issues during high-load periods.
- Data siloed in a traditional relational database, making modern analytics difficult.

The data from this system is represented by the `legacy_incidents_data.csv` file (sourced from the AIOps Kaggle Dataset), which contains historical IT incident records.

### The Goal
The primary objective is to re-architect this system into a scalable, cost-efficient, and intelligent cloud-native solution. This will improve agility, enhance reliability, and unlock the value of our data through analytics.

## 2. Proposed Cloud-Native Architecture

The new architecture will be built on AWS and will be event-driven and serverless to maximize scalability and minimize operational overhead.

![Architecture Diagram](architecture.png)
*(A sample diagram image named `architecture.png` should be placed here. You can create one using tools like diagrams.net and add it to the repository.)*

**Core Components:**

1.  **Data Ingestion (API Gateway & AWS Lambda):** New incidents are reported via a REST API endpoint hosted on API Gateway. This triggers a Lambda function (`IncidentIngestionFunction`) to process and validate the incoming data.
2.  **Data Storage (Amazon S3 & Amazon DynamoDB):**
    -   Raw, validated incident data is stored in an **Amazon S3 Bucket** (`incident-data-lake`) for long-term archival and as a source for big data analytics.
    -   Hot, queryable data for the live application is stored in **Amazon DynamoDB** (`IncidentsTable`), a NoSQL database providing single-digit millisecond latency.
3.  **Data Processing & Analytics (AWS Glue & Amazon SageMaker):**
    -   **AWS Glue** is used to run an ETL (Extract, Transform, Load) job that processes the historical data from the legacy system (now in S3) and loads it into the new cloud databases.
    -   **Amazon SageMaker** will be used to train a machine learning model on the historical data to automatically classify new incidents, reducing manual effort.
4.  **Monitoring & Logging (Amazon CloudWatch):** All services will send logs and metrics to CloudWatch for centralized monitoring, alerting, and dashboarding.

## 3. Data Migration Strategy

The migration follows the **Extract, Transform, Load (ETL)** pattern.

-   **Extract:** The historical data is exported from the legacy system into a `csv` format (`legacy_incidents_data.csv`).
-   **Transform:** A Python script (`data_processing/transform_legacy_data.py`) is used to clean, format, and enrich the data to make it compatible with the new DynamoDB schema. This includes standardizing date formats, cleaning text, and categorizing incident types.
-   **Load:** The transformed data is uploaded to the S3 data lake and then loaded into the DynamoDB table for application use.

## 4. Cloud Systems Management Plan

-   **Monitoring:** CloudWatch Dashboards will be set up to monitor key metrics like Lambda invocation counts, API latency, DynamoDB read/write capacity, and error rates.
-   **Security:** Access to all resources will be controlled via strict **IAM (Identity and Access Management)** roles and policies. Data in S3 and DynamoDB will be encrypted at rest.
-   **Cost Management:** All resources will be tagged with a `Project: IncidentManagement` tag. AWS Budgets will be configured to send alerts if spending exceeds predefined thresholds. The serverless nature of the architecture ensures we only pay for what we use.

## 5. How to Run This Project

### Prerequisites
- Python 3.8+
- An AWS Account (optional, for IaC deployment)
- Terraform (optional, for IaC deployment)

### 1. Set Up the Environment
Clone the repository and install the required Python packages.
```bash
git clone <your-repo-url>
cd cloud-migration-project
pip install -r requirements.txt
```

### 2. Run the Data Transformation Script
This script simulates the "Transform" step of our ETL process. It reads the raw legacy data, cleans it, and outputs a cloud-ready JSON file.

```bash
python data_processing/transform_legacy_data.py
```
This will generate a `cloud_ready_incidents.json` file in the `data/` directory.

### 3. Deploy Infrastructure (Optional)
The `iac/` directory contains Terraform code to provision the basic AWS resources (the S3 bucket and DynamoDB table) for this project.

```bash
# Navigate to the iac directory
cd iac

# Initialize Terraform
terraform init

# Preview the changes
terraform plan

# Apply the changes to create the resources in your AWS account
terraform apply
```
---
