provider "aws" {
  region = "eu-west-3"
  profile = "default"
}

data "archive_file" "lines_counter_zip" {
    type        = "zip"
    source_dir  = "./src"
    output_path = "./src/lines_counter.zip"
}

module "lines_counter" {
  filename = data.archive_file.lines_counter_zip.output_path
  source        = "../"
  hash_key      = "ID"
  hash_key_type = "S"
  table_name    = "LinesCounts"
  bucket_name   = "bpserverlessdemo"
  function_name = "LinesCounter"
  handler       = "lines_counter.lambda_handler"
  runtime       = "python3.6"
}