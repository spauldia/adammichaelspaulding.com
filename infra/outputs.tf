output "function_url" {
  description = "Public URL of the chat API. The chat endpoint is this URL plus \"chat\"."
  value       = aws_lambda_function_url.chat.function_url
}

output "function_name" {
  description = "Lambda function name."
  value       = aws_lambda_function.chat.function_name
}

output "github_deploy_role_arn" {
  description = "Role GitHub Actions assumes to deploy new code."
  value       = aws_iam_role.github_deploy.arn
}

output "notes_bucket" {
  description = "Private S3 bucket holding notes.md."
  value       = aws_s3_bucket.notes.bucket
}

output "table_name" {
  description = "DynamoDB table holding rate limits and monthly spend."
  value       = aws_dynamodb_table.chat.name
}
