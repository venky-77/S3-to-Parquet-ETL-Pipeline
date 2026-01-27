# AWS CloudFormation CLI Commands

This document contains AWS CLI commands to **create stacks**, **update stacks**, **create & execute change sets**, and **delete stacks** for the following CloudFormation stacks:

- Glue-Job
- Lambda-event-Job
- Glue-catalog-crawler

---

## Common Configuration

```bash
REGION=us-east-1
PROFILE=default
ROLE_ARN=arn:aws:iam::297041784012:role/storm-cloudformation-role
CAPABILITIES="CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM"
```

---

## Glue-Job Stack

**Template:** `cloudformation/gluejob.yaml`

### Create Stack
```bash
aws cloudformation create-stack \
  --profile $PROFILE \
  --region $REGION \
  --role-arn $ROLE_ARN \
  --stack-name Glue-Job \
  --template-body file://cloudformation/gluejob.yaml \
  --capabilities $CAPABILITIES
```

### Update Stack
```bash
aws cloudformation update-stack \
  --profile $PROFILE \
  --region $REGION \
  --role-arn $ROLE_ARN \
  --stack-name Glue-Job \
  --template-body file://cloudformation/gluejob.yaml \
  --capabilities $CAPABILITIES
```

### Create Change Set
```bash
aws cloudformation create-change-set \
  --profile $PROFILE \
  --region $REGION \
  --role-arn $ROLE_ARN \
  --stack-name Glue-Job \
  --change-set-name Glue-Job-changeset \
  --template-body file://cloudformation/gluejob.yaml \
  --capabilities $CAPABILITIES
```

### Execute Change Set
```bash
aws cloudformation execute-change-set \
  --profile $PROFILE \
  --region $REGION \
  --stack-name Glue-Job \
  --change-set-name Glue-Job-changeset
```

### Delete Stack
```bash
aws cloudformation delete-stack \
  --profile $PROFILE \
  --region $REGION \
  --stack-name Glue-Job
```

---

## Lambda-event-Job Stack

**Template:** `cloudformation/lambda_event_trigger.yaml`

### Create Stack
```bash
aws cloudformation create-stack \
  --profile $PROFILE \
  --region $REGION \
  --role-arn $ROLE_ARN \
  --stack-name Lambda-event-Job \
  --template-body file://cloudformation/lambda_event_trigger.yaml \
  --capabilities $CAPABILITIES
```

### Update Stack
```bash
aws cloudformation update-stack \
  --profile $PROFILE \
  --region $REGION \
  --role-arn $ROLE_ARN \
  --stack-name Lambda-event-Job \
  --template-body file://cloudformation/lambda_event_trigger.yaml \
  --capabilities $CAPABILITIES
```

### Create Change Set
```bash
aws cloudformation create-change-set \
  --profile $PROFILE \
  --region $REGION \
  --role-arn $ROLE_ARN \
  --stack-name Lambda-event-Job \
  --change-set-name Lambda-event-Job-changeset \
  --template-body file://cloudformation/lambda_event_trigger.yaml \
  --capabilities $CAPABILITIES
```

### Execute Change Set
```bash
aws cloudformation execute-change-set \
  --profile $PROFILE \
  --region $REGION \
  --stack-name Lambda-event-Job \
  --change-set-name Lambda-event-Job-changeset
```

### Delete Stack
```bash
aws cloudformation delete-stack \
  --profile $PROFILE \
  --region $REGION \
  --stack-name Lambda-event-Job
```

---

## Glue-catalog-crawler Stack

**Template:** `cloudformation/glue_catalog_crawler.yaml`

### Create Stack
```bash
aws cloudformation create-stack \
  --profile $PROFILE \
  --region $REGION \
  --role-arn $ROLE_ARN \
  --stack-name Glue-catalog-crawler \
  --template-body file://cloudformation/glue_catalog_crawler.yaml \
  --capabilities $CAPABILITIES
```

### Update Stack
```bash
aws cloudformation update-stack \
  --profile $PROFILE \
  --region $REGION \
  --role-arn $ROLE_ARN \
  --stack-name Glue-catalog-crawler \
  --template-body file://cloudformation/glue_catalog_crawler.yaml \
  --capabilities $CAPABILITIES
```

### Create Change Set
```bash
aws cloudformation create-change-set \
  --profile $PROFILE \
  --region $REGION \
  --role-arn $ROLE_ARN \
  --stack-name Glue-catalog-crawler \
  --change-set-name Glue-catalog-crawler-changeset \
  --template-body file://cloudformation/glue_catalog_crawler.yaml \
  --capabilities $CAPABILITIES
```

### Execute Change Set
```bash
aws cloudformation execute-change-set \
  --profile $PROFILE \
  --region $REGION \
  --stack-name Glue-catalog-crawler \
  --change-set-name Glue-catalog-crawler-changeset
```

### Delete Stack
```bash
aws cloudformation delete-stack \
  --profile $PROFILE \
  --region $REGION \
  --stack-name Glue-catalog-crawler
```

---

## Notes
- Use **change sets** for safe review before deployment.
- `deploy` can be used for simplified workflows, but `create-stack` and `update-stack` give more control.
- Add `aws cloudformation wait stack-*-complete` if scripting automation.

