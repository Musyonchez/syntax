#!/bin/bash
# Auth Tests Runner
# Simple, Uniform, Consistent testing for authentication features

echo "🔐 Running Auth Tests"
echo "===================="
echo ""

# Check if we're in the right directory
if [ ! -f "test_token_cleanup.py" ]; then
    echo "❌ Run this script from the tests/auth directory"
    exit 1
fi

# Check if auth server is running
if ! curl -s http://localhost:8081/health > /dev/null; then
    echo "❌ Auth server not running on port 8081"
    echo "💡 Start it with: cd ../../auth && python main.py"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "../../venv" ]; then
    source ../../venv/bin/activate
fi

# Run individual auth tests
echo "🧪 Running individual auth tests..."
echo ""

# Track results
PASSED=0
TOTAL=0

# Test 1: Token Cleanup
echo "Test 1: Token Cleanup"
if python test_token_cleanup.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# Test 2: Single Device Logout
echo "Test 2: Single Device Logout"
if python test_logout.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# Test 3: Logout All Devices  
echo "Test 3: Logout All Devices"
if python test_logout_all.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# Test 4: Session Limits
echo "Test 4: Session Limits"
if python test_session_limits.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# Results summary
echo "========================="
echo "🎯 AUTH TESTS SUMMARY"
echo "========================="
echo "Passed: $PASSED/$TOTAL"

if [ $PASSED -eq $TOTAL ]; then
    echo "🎉 All auth tests passed!"
    exit 0
else
    echo "⚠️  Some auth tests failed"
    exit 1
fi