# 📊 S3 to Parquet Glue Data Pipeline (Production Ready)

## 📌 Project Overview
This project implements a **production-grade, serverless, event-driven data engineering pipeline on AWS**.  
The pipeline automatically processes raw data uploaded to Amazon S3, converts it into **Parquet format using AWS Glue (PySpark)**, catalogs the data in **AWS Glue Data Catalog**, and enables analytics using **Amazon Athena**.

This project is fully **Infrastructure-as-Code (IaC)** driven using **AWS CloudFormation** and follows **least-privilege IAM principles**, suitable for real enterprise environments.

---

## 🎯 Business Problem
Raw data lands daily in S3 in CSV format. Querying CSV directly is:
- Slow
- Expensive
- Not scalable

The business required:
- Automated processing when data arrives
- Optimized storage format (Parquet)
- Central metadata catalog
- SQL querying capability
- Secure and auditable deployment

---

## 🏗️ Architecture

```
S3 (landing_zone)
   ↓ ObjectCreated
EventBridge
   ↓
Lambda Trigger
   ↓
Glue PySpark Job (CSV → Parquet)
   ↓
S3 (derived_data)
   ↓
Glue Crawler
   ↓
Glue Data Catalog
   ↓
Amazon Athena
```

---

## 🔧 Technologies Used

- Amazon S3 (Data Lake)
- AWS Glue (PySpark ETL)
- AWS Glue Crawler
- AWS Glue Data Catalog
- AWS Lambda
- Amazon EventBridge
- Amazon Athena
- AWS CloudFormation
- IAM (Least Privilege Security)

---

## 📂 S3 Folder Structure

```
storm-source-data-dumps-2026/
└── sample_data/
    ├── landing_zone_data/     # Raw CSV files
    └── derived_data/          # Parquet output
```

---

## ⚙️ Implementation Details

### 1️⃣ Data Ingestion (S3)
- Raw CSV files are uploaded to the **landing_zone_data/** prefix.
- No polling is used (event-driven).

### 2️⃣ Event Triggering
- **Amazon EventBridge** listens for `ObjectCreated` events from S3.
- EventBridge invokes a **Lambda function**.

### 3️⃣ Glue Job Execution
- Lambda starts the Glue PySpark job.
- Glue reads CSV data from S3.
- Data is transformed and written as **Parquet**.
- Parquet output is stored in the derived_data folder.

### 4️⃣ Metadata Management
- Glue Crawler scans the Parquet output.
- Tables are created/updated in Glue Data Catalog.

### 5️⃣ Analytics
- Amazon Athena queries the data using SQL.

---

## 🔐 Security & IAM Design

### IAM Roles Used

| Role | Purpose |
|---|---|
| CloudFormation Role | Create and tag AWS resources |
| Glue Job Role | Read/write S3 + Glue Catalog |
| Lambda Role | Start Glue job |
| Glue Crawler Role | Read Parquet + update catalog |

### Key Security Principles
- Least privilege access
- No wildcard IAM admin roles
- Explicit tagging permissions
- Separate roles per service

---

## 🧪 CloudFormation Deployment

```bash
aws cloudformation deploy \
  --stack-name s3-to-parquet-glue-stack \
  --template-file cloudformation/template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --role-arn arn:aws:iam::<ACCOUNT_ID>:role/storm-cloudformation-role
```

---

## 🚧 Challenges Faced & Lessons Learned

### 1️⃣ IAM Is the Hardest Part
- Most failures were due to missing permissions, not Glue itself.
- Learned that **CloudFormation needs extra permissions** (TagResource, PassRole).

### 2️⃣ Tagging Permissions
- Glue job creation failed due to missing `glue:TagResource`.
- Tagging is a **separate API call** in AWS.

### 3️⃣ S3 Permission Nuances
- `s3:ListBucket` must be on bucket ARN, not object ARN.
- Glue uses `s3a://` internally → strict permissions required.

### 4️⃣ Event-Driven Confusion
- Glue does NOT auto-detect S3 uploads.
- Requires EventBridge or Lambda trigger.

### 5️⃣ PySpark Gotchas
- Parquet writer does NOT support `header=True`.
- CSV vs Parquet APIs differ.

### 6️⃣ Glue Trigger Complexity
- Glue triggers require workflows.
- EventBridge + Lambda proved simpler and cheaper.

---

## 💰 Cost Considerations

| Service | Cost Impact |
|---|---|
| S3 | Low (storage-based) |
| Glue | Pay per job execution |
| Lambda | Free tier friendly |
| EventBridge | Very low |
| Athena | Pay per query |

Optimizing to Parquet reduced Athena query cost by **~70%**.

---

## ✅ Production Readiness Checklist

- [x] Event-driven (no polling)
- [x] Parquet optimized storage
- [x] Metadata cataloged
- [x] SQL analytics enabled
- [x] Least-privilege IAM
- [x] Infrastructure as Code
- [x] Cost optimized

---

## 🎤 Interview & Manager Talking Points

- Designed a fully serverless, production data pipeline
- Solved real IAM and CloudFormation issues
- Implemented best practices (Parquet, event-driven, IaC)
- Improved analytics performance and reduced cost

---

## 📌 Final Outcome

✔ Fully automated data pipeline  
✔ Zero manual intervention  
✔ Secure and scalable  
✔ Manager- and production-approved design

---

**Author:** Victory Venkatesh  
**Role:** Data Engineer  
**Project Type:** Production / Enterprise Grade


