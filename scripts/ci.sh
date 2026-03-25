#!/bin/bash
set -e

echo "Running pyright..."
pyright core feature_requests

echo "Running pylint..."
pylint core feature_requests

echo "Running pytest..."
pytest core/
