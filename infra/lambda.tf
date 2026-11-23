locals {
  anthropic_key_param = "/${var.project_name}/anthropic-api-key"
  ip_salt_param       = "/${var.project_name}/ip-salt"
  parameter_arn       = "arn:aws:ssm:${var.aws_region}:${var.aws_account_id}:parameter/${var.project_name}/*"
}

resource "aws_iam_role" "lambda" {
  name = "${var.project_name}-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_access" {
  name = "${var.project_name}-access"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["dynamodb:GetItem", "dynamodb:UpdateItem"]
        Resource = aws_dynamodb_table.chat.arn
      },
      {
        Effect   = "Allow"
        Action   = "ssm:GetParameter"
        Resource = local.parameter_arn
      },
      {
        Effect   = "Allow"
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.notes.arn}/${local.notes_key}"
      },
      {
        Effect   = "Allow"
        Action   = "s3:ListBucket"
        Resource = aws_s3_bucket.notes.arn
      },
    ]
  })
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.project_name}"
  retention_in_days = 14
}

resource "aws_lambda_function" "chat" {
  function_name = var.project_name
  role          = aws_iam_role.lambda.arn
  runtime       = "python3.13"
  architectures = ["arm64"]
  handler       = "app.main.handler"
  filename      = "${path.module}/../api/dist/lambda.zip"
  memory_size   = 512
  timeout       = 30

  environment {
    variables = {
      CHAT_TABLE_NAME          = aws_dynamodb_table.chat.name
      CHAT_ANTHROPIC_KEY_PARAM = local.anthropic_key_param
      CHAT_IP_SALT_PARAM       = local.ip_salt_param
      CHAT_NOTES_BUCKET        = aws_s3_bucket.notes.bucket
      CHAT_NOTES_KEY           = local.notes_key
      CHAT_MONTHLY_BUDGET_USD  = tostring(var.monthly_budget_usd)
    }
  }

  depends_on = [aws_cloudwatch_log_group.lambda, aws_iam_role_policy_attachment.lambda_logs]

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}

resource "aws_lambda_function_url" "chat" {
  function_name      = aws_lambda_function.chat.function_name
  authorization_type = "NONE"

  cors {
    allow_origins = var.allowed_origins
    allow_methods = ["POST"]
    allow_headers = ["content-type"]
    max_age       = 3600
  }
}

resource "aws_lambda_permission" "public_url" {
  statement_id           = "AllowPublicFunctionUrl"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.chat.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}

resource "aws_lambda_permission" "public_invoke_via_url" {
  statement_id             = "AllowPublicInvokeViaFunctionUrl"
  action                   = "lambda:InvokeFunction"
  function_name            = aws_lambda_function.chat.function_name
  principal                = "*"
  invoked_via_function_url = true
}
