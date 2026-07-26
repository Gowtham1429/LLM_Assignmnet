# Nimbus Cloud Storage — Security and Access Policy

## Authentication

All API requests to Nimbus must be signed using an HMAC-SHA256 signature derived from an access key and secret key pair. Access keys are issued through the Nimbus console and can be rotated at any time. Nimbus does not support unsigned or anonymous write requests; anonymous read access can be enabled per-bucket by an administrator.

## Encryption

Data is encrypted at rest using AES-256 by default, with no additional configuration required. Customers may optionally supply their own encryption keys through the Customer-Managed Key (CMK) feature, which is available only on the Business and Enterprise plans.

In transit, all data is encrypted using TLS 1.2 or higher. Nimbus rejects connections that attempt to negotiate TLS 1.1 or earlier.

## Access Control

Access to buckets is controlled through Bucket Policies, written in a JSON-based policy language similar to IAM policies. Policies can grant or deny actions such as GetObject, PutObject, DeleteObject, and ListBucket, and can be scoped to specific IP ranges or VPC endpoints.

By default, all newly created buckets are private. Public read access must be explicitly enabled in the bucket policy.

## Audit Logging

Every API call can be logged to an Access Log bucket, which records the requester identity, timestamp, source IP, action taken, and response status. Access logging is disabled by default and must be turned on per bucket. Logs are retained for 90 days unless the customer configures a longer retention period.

## Compliance

Nimbus maintains SOC 2 Type II certification, renewed annually. It does not currently offer a HIPAA-compliant storage tier.
