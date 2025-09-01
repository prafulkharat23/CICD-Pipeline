#!/bin/bash

# Script to verify all GitHub Actions are using latest versions

echo "🔍 Checking GitHub Actions versions in workflow files..."
echo "=================================================="

WORKFLOW_FILE=".github/workflows/ci-cd.yml"

if [ ! -f "$WORKFLOW_FILE" ]; then
    echo "❌ Workflow file not found: $WORKFLOW_FILE"
    exit 1
fi

echo "📁 Checking file: $WORKFLOW_FILE"
echo ""

# Check for deprecated actions
echo "🚨 Checking for deprecated actions:"
echo "-----------------------------------"

# Check for v3 artifact actions (deprecated)
if grep -n "upload-artifact@v3\|download-artifact@v3" "$WORKFLOW_FILE"; then
    echo "❌ Found deprecated artifact actions (v3)"
else
    echo "✅ No deprecated artifact actions found"
fi

# Check for v2 CodeQL actions (deprecated)
if grep -n "codeql-action.*@v2" "$WORKFLOW_FILE"; then
    echo "❌ Found deprecated CodeQL actions (v2)"
else
    echo "✅ No deprecated CodeQL actions found"
fi

echo ""
echo "📋 Current action versions:"
echo "---------------------------"

# Extract all action versions
grep -n "uses:" "$WORKFLOW_FILE" | while read -r line; do
    echo "$line"
done

echo ""
echo "✅ Recommended latest versions:"
echo "------------------------------"
echo "actions/checkout@v4"
echo "actions/setup-python@v5"
echo "actions/cache@v4"
echo "actions/upload-artifact@v4"
echo "actions/download-artifact@v4"
echo "codecov/codecov-action@v4"
echo "github/codeql-action/upload-sarif@v3"
echo "aquasecurity/trivy-action@0.28.0"

echo ""
echo "🔧 If you see any deprecated versions, update them and commit:"
echo "git add .github/workflows/"
echo "git commit -m 'Update GitHub Actions to latest versions'"
echo "git push origin main"
