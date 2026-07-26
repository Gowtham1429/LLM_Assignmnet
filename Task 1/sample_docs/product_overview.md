# Nimbus Cloud Storage — Product Overview

Nimbus Cloud Storage is an object storage service for developers and small businesses. It was launched in 2021 and is designed as a low-cost alternative to large managed storage providers.

## Storage Tiers

Nimbus offers three storage tiers: Standard, Infrequent Access, and Archive.

The Standard tier costs $0.021 per GB per month and is meant for data accessed frequently.

The Infrequent Access tier costs $0.012 per GB per month, with a minimum storage duration of 30 days and a retrieval fee of $0.01 per GB.

The Archive tier costs $0.004 per GB per month, but retrieval requests take up to 12 hours to complete and the minimum storage duration is 90 days.

## Regions

Nimbus operates in four regions: us-east-1, us-west-2, eu-central-1, and ap-southeast-1. Data does not automatically replicate across regions unless the customer enables Cross-Region Replication, which is a paid add-on billed at $0.02 per GB transferred.

## File Size Limits

A single object can be up to 5 terabytes in size. Objects larger than 100 megabytes must be uploaded using the multipart upload API, which splits the file into parts of at least 5 megabytes each, except for the final part.

## Durability and Availability

Nimbus advertises 99.999999999% (eleven nines) durability for the Standard and Infrequent Access tiers, and 99.9% availability for the Standard tier.
