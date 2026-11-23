#!/usr/bin/env bash
# Build dist/lambda.zip for the arm64 Python 3.13 Lambda runtime.
set -euo pipefail

cd "$(dirname "$0")/.."
rm -rf build dist
mkdir -p build/package dist

uv export --frozen --no-dev --no-hashes --no-emit-project --output-file build/requirements.txt
uv pip install \
  --requirement build/requirements.txt \
  --target build/package \
  --python-platform aarch64-manylinux2014 \
  --python-version 3.13 \
  --only-binary :all:

cp -R app build/package/
find build/package -name "__pycache__" -type d -prune -exec rm -rf {} +
(cd build/package && zip -qr ../../dist/lambda.zip .)

echo "Built dist/lambda.zip ($(du -h dist/lambda.zip | cut -f1))"
