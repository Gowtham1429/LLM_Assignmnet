# Nimbus Cloud Storage — API Reference (Core Operations)

## Rate Limits

The Nimbus API enforces a default rate limit of 3,500 PUT/COPY/POST requests per second and 5,500
GET/HEAD requests per second, per bucket. Requests beyond this limit receive an HTTP 503 response
with a `Retry-After` header. Customers on the Enterprise plan can request a higher limit by
contacting support at least 5 business days in advance of an expected traffic spike.

## Multipart Upload

Multipart upload is required for any object over 100 MB and optional for smaller objects. The
workflow is: call `InitiateMultipartUpload` to get an upload ID, upload each part with
`UploadPart` (parts must be at least 5 MB except the last one, and there is a maximum of 10,000
parts), then call `CompleteMultipartUpload` to assemble the object. Incomplete multipart uploads
are automatically aborted and their parts deleted after 7 days to avoid orphaned storage charges.

## Versioning

Bucket Versioning, when enabled, keeps every version of an object every time it is overwritten or
deleted. Deleting an object with versioning enabled adds a delete marker rather than removing the
data. Versioning cannot be disabled once enabled — it can only be suspended, which stops creating
new versions but keeps existing ones.

## Lifecycle Rules

Lifecycle rules can automatically transition objects between storage tiers or expire them after a
set number of days. For example, a rule can move objects to the Infrequent Access tier after 30
days and to the Archive tier after 90 days, then delete them after 365 days. Lifecycle rules are
evaluated once per day.

## Error Codes

Common error codes include 403 (Access Denied — the signing credentials or bucket policy do not
permit the action), 404 (Not Found — the object or bucket does not exist), and 409
(Conflict — typically returned when trying to delete a non-empty bucket without the `force` flag).
