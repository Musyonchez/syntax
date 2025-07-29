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

echo "=== CORE AUTH FLOW TESTS ==="

# Test 1: Login/Register Flow
echo "Test 1: Login/Register Flow"
if python test_login_register.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# Test 2: Token Refresh Flow
echo "Test 2: Token Refresh Flow"
if python test_token_refresh.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# Test 3: Schema Validation
echo "Test 3: Schema Validation"
if python test_schema_validation.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

echo "=== SESSION MANAGEMENT TESTS ==="

# Test 4: Token Cleanup
echo "Test 4: Token Cleanup"
if python test_token_cleanup.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# Test 5: Single Device Logout
echo "Test 5: Single Device Logout"
if python test_logout.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# Test 6: Logout All Devices  
echo "Test 6: Logout All Devices"
if python test_logout_all.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# Test 7: Session Limits
echo "Test 7: Session Limits"
if python test_session_limits.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

echo "=== EDGE CASE TESTS ==="

# Test 8: Invalid Token Handling
echo "Test 8: Invalid Token Handling"
if python test_invalid_tokens.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# Test 9: Concurrent Login Handling
echo "Test 9: Concurrent Login Handling"
if python test_concurrent_logins.py; then
    PASSED=$((PASSED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

echo "=== SECURITY TESTS ==="

# Test 10: Security Validation
echo "Test 10: Security Validation"
if python test_security.py; then
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