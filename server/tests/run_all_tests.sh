#!/bin/bash
# SyntaxMem Master Test Runner
# Simple, Uniform, Consistent testing for all modules

echo "🧪 SyntaxMem Complete Test Suite"
echo "================================="
echo ""

# Check if auth server is running
echo "📡 Checking if auth server is running..."
if ! curl -s http://localhost:8081/health > /dev/null; then
    echo "❌ Auth server not running on port 8081"
    echo "💡 Start it with: cd ../auth && python main.py"
    exit 1
fi

echo "✅ Auth server is running"
echo ""

# Activate virtual environment if it exists
if [ -d "../venv" ]; then
    echo "🐍 Using virtual environment..."
    source ../venv/bin/activate
fi

# Track overall results
TOTAL_PASSED=0
TOTAL_TESTS=0

# Run Auth Tests
echo "🔐 Running Auth Module Tests..."
cd auth
if ./run_auth_tests.sh; then
    AUTH_RESULT="PASS"
    TOTAL_PASSED=$((TOTAL_PASSED + 1))
else
    AUTH_RESULT="FAIL"
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))
cd ..
echo ""

# Future: Run Users Tests
# echo "👤 Running Users Module Tests..."
# cd users
# if ./run_users_tests.sh; then
#     USERS_RESULT="PASS"
#     TOTAL_PASSED=$((TOTAL_PASSED + 1))
# else
#     USERS_RESULT="FAIL"
# fi
# TOTAL_TESTS=$((TOTAL_TESTS + 1))
# cd ..

# Future: Run Snippets Tests
# echo "📝 Running Snippets Module Tests..."

# Future: Run Sessions Tests  
# echo "🎯 Running Sessions Module Tests..."

# Overall Results
echo "========================================="
echo "🎯 COMPLETE TEST SUITE RESULTS"
echo "========================================="
echo "Auth Module:       $AUTH_RESULT"
# echo "Users Module:      $USERS_RESULT"
# echo "Snippets Module:   $SNIPPETS_RESULT"
# echo "Sessions Module:   $SESSIONS_RESULT"
echo ""
echo "Overall: $TOTAL_PASSED/$TOTAL_TESTS modules passed"

if [ $TOTAL_PASSED -eq $TOTAL_TESTS ]; then
    echo "🎉 All test modules passed!"
    echo "✨ SyntaxMem is ready for production!"
    exit 0
else
    echo "⚠️  Some test modules failed"
    echo "🔧 Check individual module results above"
    exit 1
fi