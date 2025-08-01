#!/bin/bash
# Snippets Module Test Runner
# Simple, Uniform, Consistent testing for snippets functionality

echo "📝 Running Snippets Module Tests"
echo "================================"

# Track results
PASSED=0
TOTAL=0

# Test files to run (in dependency order)
TESTS=(
    "test_01_personal_create.py"
    "test_02_personal_get.py"
    "test_03_personal_update.py"
    "test_04_personal_delete.py"
    "test_05_admin_create_official.py"
    "test_06_official_get.py"
    "test_07_auth_required.py"
    "test_08_schema_validation.py"
)

# Run each test
for test in "${TESTS[@]}"; do
    echo ""
    echo "Running $test..."
    if python "$test"; then
        echo "✅ $test: PASSED"
        PASSED=$((PASSED + 1))
    else
        echo "❌ $test: FAILED"
    fi
    TOTAL=$((TOTAL + 1))
done

echo ""
echo "📊 Snippets Module Results: $PASSED/$TOTAL tests passed"

if [ $PASSED -eq $TOTAL ]; then
    echo "🎉 All snippets tests passed!"
    exit 0
else
    echo "⚠️  Some snippets tests failed"
    exit 1
fi