# MinIO Buckets Documentation

This document explains the purpose of each MinIO bucket in the Vision-to-Vintage system.

## Buckets Overview

The system uses the following buckets to store different types of data:

### 1. `drift` Bucket

**Purpose**: Store data related to model drift detection

This bucket contains:
- Reference datasets representing the expected distribution of data
- Current production data samples for comparison 
- Drift reports and metrics over time
- Visualization data for drift dashboards

When the system detects drift between the original training data distribution and current production data, it stores these metrics and samples to help data scientists diagnose the issue.

### 2. `feedback` Bucket

**Purpose**: Store user feedback data for model improvement

This bucket contains:
- Feedback metadata (ratings, comments, timestamps)
- Images with poor feedback ratings (marked for retraining)
- Aggregate feedback statistics for reporting
- User sentiment analysis 

The feedback system specifically collects detailed metrics about:
- Color accuracy
- Style capture
- Detail preservation
- Artistic quality

Images with negative feedback are automatically stored in the `feedback/retraining` subfolder for potential model retraining.

### 3. `metrics` Bucket

**Purpose**: Store detailed system metrics beyond what Prometheus keeps

This bucket contains:
- Detailed performance reports (latency, throughput)
- Resource utilization statistics
- Error logs and analysis
- A/B test results
- Batch processing metrics

These metrics help with system optimization, long-term trend analysis, and capacity planning.

### 4. `mlflow-artifacts` Bucket

**Purpose**: Store MLflow experiment artifacts

This bucket contains:
- Trained model files
- Dataset snapshots
- Evaluation reports
- Parameter logs
- Performance visualization data

MLflow uses this bucket to maintain experiment lineage, enable model versioning, and support reproducibility.

## Best Practices

- **Data Lifecycle**: Regular cleanup jobs should be implemented to remove outdated metrics and data that are no longer needed.
- **Access Control**: Access to sensitive buckets should be restricted to relevant personnel.
- **Versioning**: Consider enabling versioning on the `mlflow-artifacts` bucket to track model changes over time.
- **Backup**: Implement regular backups of critical MinIO buckets to prevent data loss. 