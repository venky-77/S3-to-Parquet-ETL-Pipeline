# Project Errors, Challenges & Learnings

This document captures **all the errors, issues, and challenges** faced during the implementation of the **S3 → EventBridge → Lambda → Glue → Parquet → Crawler** pipeline.

This is included intentionally to demonstrate **real-world AWS troubleshooting experience**, not just happy-path development.

---

## 1. CloudFormation Template Validation Errors

### Error
```
An error occurred (ValidationError) when calling the CreateChangeSet operation:
[/Resources/GlueJob/GlueTrigger/Properties/Predicate] 'null' values are not allowed in templates
```

### Caused By
- Passing `null` values explicitly in CloudFormation properties

### Issue With
- CloudFormation strict validation rules

### Solution
- Removed `Predicate` entirely when not required
- Used `!Ref AWS::NoValue` for optional properties

---

## 2. Glue Trigger CREATE_FAILED – Workflow Name Missing

### Error
```
Workflow name cannot be null or empty
```

### Caused By
- Glue Trigger was created without linking to a Workflow

### Issue With
- Glue Trigger configuration

### Solution
- Explicitly created `AWS::Glue::Workflow`
- Attached `WorkflowName` to Glue Trigger

---

## 3. Glue Trigger Entity Not Found

### Error
```
Entity not found (Service: Glue)
```

### Caused By
- Trigger referencing a Glue Job that was not created yet

### Issue With
- Resource creation order

### Solution
- Used `DependsOn` to enforce correct creation sequence

---

## 4. CloudFormation Access Denied – Glue Permissions

### Error
```
not authorized to perform: glue:CreateWorkflow
```

### Caused By
- CloudFormation execution role missing Glue permissions

### Issue With
- IAM Role used by CloudFormation

### Solution
- Added required permissions:
  - `glue:CreateWorkflow`
  - `glue:CreateDatabase`
  - `glue:CreateJob`

---

## 5. Glue Job CREATE_FAILED – Tagging Error

### Error
```
not authorized to perform: glue:TagResource
```

### Caused By
- CloudFormation automatically applies tags

### Issue With
- Missing tagging permissions

### Solution
- Added tagging permissions:
  - `glue:TagResource`
  - `glue:UntagResource`
  - `glue:GetTags`

---

## 6. Glue Database CREATE_FAILED – Access Denied

### Error
```
not authorized to perform: glue:CreateDatabase on catalog
```

### Caused By
- Glue Catalog permissions missing

### Issue With
- CloudFormation execution role

### Solution
- Added:
  - `glue:CreateDatabase`
  - `glue:GetDatabase`

---

## 7. EventBridge Rule Not Triggering Glue Job

### Error
- File uploaded but Glue Job not triggered

### Caused By
- EventBridge pattern mismatch

### Issue With
- S3 event filtering

### Solution
- Corrected:
  - `detail-type: Object Created`
  - Bucket name
  - Prefix path

---

## 8. S3 403 Forbidden – Glue Job Read Error

### Error
```
AmazonS3Exception: Forbidden (403)
```

### Caused By
- Glue Job role missing S3 read permissions

### Issue With
- IAM role for Glue Job

### Solution
- Added:
  - `s3:GetObject`
  - `s3:ListBucket`

---

## 9. PySpark Error – parquet() Header Argument

### Error
```
DataFrameWriter.parquet() got an unexpected keyword argument 'header'
```

### Caused By
- `header` option is valid only for CSV, not Parquet

### Issue With
- Spark API misuse

### Solution
- Removed `header=True` from Parquet write

---

## 10. Glue Script Not Found in S3

### Error
```
Error retrieving script: NoSuchKey
```

### Caused By
- Incorrect S3 path for Glue script

### Issue With
- Glue Job configuration

### Solution
- Verified script upload path
- Updated `ScriptLocation`

---

## 11. Glue Crawler Access Denied

### Error
```
User does not have access to target s3://.../derived_data/
```

### Caused By
- Glue Crawler role missing S3 write/read permissions

### Issue With
- Crawler IAM role

### Solution
- Added:
  - `s3:GetObject`
  - `s3:PutObject`
  - `s3:ListBucket`

---

## Key Learnings

- IAM permissions are the **#1 cause of AWS failures**
- CloudFormation requires **tagging permissions by default**
- Event-driven systems need **precise event patterns**
- Glue uses **multiple roles** (Job, Crawler, CloudFormation)
- Debugging AWS errors is a **core data engineer skill**

---

## Final Outcome

Despite multiple failures, this project resulted in:
- Fully automated S3 → Glue ETL pipeline
- Least-privilege IAM roles
- Production-grade CloudFormation templates
- Strong hands-on AWS troubleshooting experience

---

**This document is intentionally included to show real-world engineering challenges and resolutions.**

## 1️⃣ IAM & Permission Errors (Most Common)
| Error Message                                  | Caused By                             | Issue With              | Solution                                             |
| ---------------------------------------------- | ------------------------------------- | ----------------------- | ---------------------------------------------------- |
| `AccessDenied: s3:ListBucket`                  | Bucket-level permission missing       | IAM User / Role         | Add `s3:ListBucket` on **bucket ARN** (not `/*`)     |
| `403 Forbidden (s3a://...)`                    | Glue job role cannot read source data | Glue Job Role           | Add `s3:GetObject`, `s3:ListBucket` on source bucket |
| `User does not have access to target s3://...` | No write permission to target         | Glue Job / Crawler Role | Add `s3:PutObject`, `s3:ListBucket` on target bucket |
| `iam:PassRole is not authorized`               | CFN role can’t pass IAM roles         | CloudFormation Role     | Add `iam:PassRole` for Glue/Lambda roles             |
| `Role is invalid or cannot be assumed`         | Wrong trust policy                    | Glue Role               | Trust policy must allow `glue.amazonaws.com`         |
| `glue:CreateJob denied`                        | Missing Glue permissions              | CloudFormation Role     | Add `glue:CreateJob`                                 |
| `glue:CreateDatabase denied`                   | Missing Glue catalog permissions      | CloudFormation Role     | Add `glue:CreateDatabase`                            |
| `glue:CreateWorkflow denied`                   | Missing workflow permissions          | CloudFormation Role     | Add `glue:CreateWorkflow`                            |
| `glue:CreateTrigger denied`                    | Missing trigger permission            | CloudFormation Role     | Add `glue:CreateTrigger`                             |
| `UnauthorizedTaggingOperation`                 | Tag permissions missing               | CloudFormation Role     | Add `glue:TagResource`, `glue:UntagResource`         |
| `events:DescribeRule denied`                   | CFN validating EventBridge rule       | CloudFormation Role     | Add `events:DescribeRule`                            |


## 2️⃣ CloudFormation Template Errors

| Error Message                                  | Caused By                             | Issue With              | Solution                                             |
| ---------------------------------------------- | ------------------------------------- | ----------------------- | ---------------------------------------------------- |
| `AccessDenied: s3:ListBucket`                  | Bucket-level permission missing       | IAM User / Role         | Add `s3:ListBucket` on **bucket ARN** (not `/*`)     |
| `403 Forbidden (s3a://...)`                    | Glue job role cannot read source data | Glue Job Role           | Add `s3:GetObject`, `s3:ListBucket` on source bucket |
| `User does not have access to target s3://...` | No write permission to target         | Glue Job / Crawler Role | Add `s3:PutObject`, `s3:ListBucket` on target bucket |
| `iam:PassRole is not authorized`               | CFN role can’t pass IAM roles         | CloudFormation Role     | Add `iam:PassRole` for Glue/Lambda roles             |
| `Role is invalid or cannot be assumed`         | Wrong trust policy                    | Glue Role               | Trust policy must allow `glue.amazonaws.com`         |
| `glue:CreateJob denied`                        | Missing Glue permissions              | CloudFormation Role     | Add `glue:CreateJob`                                 |
| `glue:CreateDatabase denied`                   | Missing Glue catalog permissions      | CloudFormation Role     | Add `glue:CreateDatabase`                            |
| `glue:CreateWorkflow denied`                   | Missing workflow permissions          | CloudFormation Role     | Add `glue:CreateWorkflow`                            |
| `glue:CreateTrigger denied`                    | Missing trigger permission            | CloudFormation Role     | Add `glue:CreateTrigger`                             |
| `UnauthorizedTaggingOperation`                 | Tag permissions missing               | CloudFormation Role     | Add `glue:TagResource`, `glue:UntagResource`         |
| `events:DescribeRule denied`                   | CFN validating EventBridge rule       | CloudFormation Role     | Add `events:DescribeRule`                            |


## 3️⃣ EventBridge & Trigger Errors

| Error Message                           | Caused By                             | Issue With       | Solution                                       |
| --------------------------------------- | ------------------------------------- | ---------------- | ---------------------------------------------- |
| `Provided Arn is not in correct format` | Glue Job ARN used incorrectly         | EventBridge Rule | EventBridge → Glue needs **job name**, not ARN |
| `No trigger happened after upload`      | S3 doesn’t natively trigger Glue      | Architecture     | Use EventBridge or Lambda trigger              |
| `Rule CREATE_FAILED`                    | Missing permissions during validation | CFN Role         | Add `events:*` describe permissions            |

## 4️⃣ Glue Script & Runtime Errors

| Error Message                                          | Caused By                   | Issue With    | Solution                         |
| ------------------------------------------------------ | --------------------------- | ------------- | -------------------------------- |
| `Error retrieving script: NoSuchKey`                   | Wrong script S3 path        | Glue Job      | Correct `ScriptLocation` S3 URI  |
| `TypeError: parquet() got unexpected keyword 'header'` | CSV option used for parquet | PySpark Code  | Remove `header=True` for parquet |
| `getFileStatus Forbidden`                              | Glue role lacks S3 access   | Glue Job Role | Add proper S3 permissions        |
| `Error while calling o104.csv`                         | Same S3 permission issue    | Glue Job Role | Fix IAM policy                   |

## 5️⃣ Glue Crawler Errors

| Error Message                            | Caused By                        | Issue With     | Solution                            |
| ---------------------------------------- | -------------------------------- | -------------- | ----------------------------------- |
| `User does not have access to target S3` | Crawler role missing permissions | Crawler Role   | Add `s3:GetObject`, `s3:ListBucket` |
| `Crawler runs but no tables created`     | No data or wrong prefix          | Crawler Config | Verify S3 path & data format        |

## 6️⃣ Design / Architecture Learnings (Not Errors, but Confusions)

| Confusion                       | Clarification                                 |
| ------------------------------- | --------------------------------------------- |
| “How Glue knows file arrived?”  | Glue **does not auto-detect** S3 uploads      |
| “Can S3 trigger Glue directly?” | ❌ No (must use EventBridge or Lambda)         |
| “Is EventBridge expensive?”     | Very cheap (near zero cost)                   |
| “Can everything be in one CFT?” | Yes, but better split for production          |
| “Why so many IAM errors?”       | Least-privilege + CFN needs extra permissions |
