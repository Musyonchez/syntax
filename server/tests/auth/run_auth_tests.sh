#!/bin/bash
# Auth Tests Runner - Simplified and Sequential
# Simple, Uniform, Consistent testing for authentication features

echo "🔐 Running Auth Tests (Sequential)"
echo "=================================="
echo ""

# Check if auth server is running
if ! curl -s http://localhost:8081/health > /dev/null; then
    echo "❌ Auth server not running on port 8081"
    echo "💡 Start it with: cd ../../auth && python main.py"
    exit 1
fi

# Track results
PASSED=0
TOTAL=0

# Sequential test files (in dependency order)
TESTS=(
    "test_01_user_creation.py"
    "test_02_token_refresh.py"
    "test_03_single_logout.py"
    "test_04_logout_all_devices.py"
    "test_05_schema_validation.py"
    "test_06_session_schema.py"
)

echo "Running tests in sequence..."
echo ""

# Run each test
for test in "${TESTS[@]}"; do
    if [ -f "$test" ]; then
        echo "Running $test..."
        if python "$test"; then
            echo "✅ $test: PASSED"
            PASSED=$((PASSED + 1))
        else
            echo "❌ $test: FAILED"
        fi
        echo ""
    else
        echo "⚠️ $test: FILE NOT FOUND"
        echo ""
    fi
    TOTAL=$((TOTAL + 1))
done

# Results summary
echo "========================="
echo "🎯 AUTH TESTS SUMMARY"
echo "========================="
echo "Passed: $PASSED/$TOTAL"

if [ $PASSED -eq $TOTAL ]; then
    echo "🎉 All auth tests passed!"
    exit 0
else
    echo "⚠️ Some auth tests failed"
    exit 1
fi