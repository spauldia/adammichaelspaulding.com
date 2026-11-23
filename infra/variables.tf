variable "aws_account_id" {
  description = "Personal AWS account ID. Terraform refuses to run against any other account."
  type        = string
}

variable "aws_region" {
  description = "AWS region for every resource."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name used for the Lambda function, table, role and parameters."
  type        = string
  default     = "site-chat"
}

variable "allowed_origins" {
  description = "Browser origins allowed to call the function URL."
  type        = list(string)
  default     = ["https://adammichaelspaulding.com", "http://localhost:4321"]
}

variable "github_oidc_subject_prefix" {
  description = "OIDC subject prefix of the repository allowed to deploy, from GitHub's actions/oidc/customization/sub API."
  type        = string
  default     = "repo:spauldia@104309279/adammichaelspaulding.com@1442312390"
}

variable "alert_email" {
  description = "Email address for AWS cost alerts."
  type        = string
}

variable "monthly_budget_usd" {
  description = "Monthly Claude spend at which the chat stops answering."
  type        = number
  default     = 4.5
}
