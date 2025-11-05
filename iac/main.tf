# Terraform configuration for provisioning core AWS resources

# Configure the AWS provider
provider "aws" {
  region = "us-east-1" # You can change this to your preferred region
}

# 1. Create an S3 bucket for storing raw and processed incident data (Data Lake)
resource "aws_s3_bucket" "incident_data_lake" {
  bucket = "incident-management-data-lake-unique-name" # CHANGE THIS to a globally unique name

  tags = {
    Name    = "Incident Data Lake"
    Project = "IncidentManagement"
  }
}

# Enable versioning on the S3 bucket to prevent accidental data loss
resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.incident_data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

# 2. Create a DynamoDB table for the live application data
resource "aws_dynamodb_table" "incidents_table" {
  name           = "IncidentsTable"
  billing_mode   = "PAY_PER_REQUEST" # Serverless billing, cost-effective for variable workloads
  hash_key       = "incident_id"

  attribute {
    name = "incident_id"
    type = "S" # S for String
  }

  tags = {
    Name    = "Incidents Table"
    Project = "IncidentManagement"
  }
}

# Output the names of the created resources for easy access
output "s3_bucket_name" {
  value       = aws_s3_bucket.incident_data_lake.bucket
  description = "The name of the S3 bucket for the data lake."
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.incidents_table.name
  description = "The name of the DynamoDB table for incidents."
}
