locals {
  notes_key = "notes.md"
}

resource "aws_s3_bucket" "notes" {
  bucket = "${var.project_name}-notes-${var.aws_account_id}"
}

resource "aws_s3_bucket_versioning" "notes" {
  bucket = aws_s3_bucket.notes.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "notes" {
  bucket                  = aws_s3_bucket.notes.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
