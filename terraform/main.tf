provider "aws" {
  region = "eu-north-1"
  default_tags {
    tags = {
      hashicorp-learn = "resource-targeting"
    }
  }
}

module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "4.1.1"

  bucket = "terraform-hesamzkr-s3-website"
  acl    = "private"

  control_object_ownership = true
  object_ownership         = "BucketOwnerPreferred"

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_object" "index_html" {
  acl          = "public-read"
  key          = "index.html"
  bucket       = module.s3_bucket.s3_bucket_id
  source       = "../index.html"
  content_type = "text/html"
}
