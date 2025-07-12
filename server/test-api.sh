#!/bin/bash

# Quick API Test Script for SyntaxMem
# Tests all local development endpoints

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🧪 Testing SyntaxMem API Endpoints${NC}"
echo "======================================"

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "Testing $name... "
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$url")
    status=$(echo "$response" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    body=$(echo "$response" | sed -e 's/HTTPSTATUS:.*//g')
    
    if [[ "$status" == "$expected_status" ]]; then
        echo -e "${GREEN}✅ OK ($status)${NC}"
        if [[ "$body" == *"healthy"* ]] || [[ "$body" == *"success"* ]]; then
            echo "   Response looks good"
        fi
    else
        echo -e "${RED}❌ FAILED ($status)${NC}"
        echo "   Expected: $expected_status, Got: $status"
        if [[ ${#body} -lt 200 ]]; then
            echo "   Response: $body"
        fi
    fi
    echo ""
}

echo -e "${YELLOW}📡 Health Checks${NC}"
echo "----------------"
test_endpoint "Auth Health" "http://localhost:8080/health"
test_endpoint "Snippets Health" "http://localhost:8081/health" 
test_endpoint "Practice Health" "http://localhost:8082/health"
test_endpoint "Leaderboard Health" "http://localhost:8083/health"
test_endpoint "Forum Health" "http://localhost:8084/health"

echo -e "${YELLOW}🔍 API Endpoints${NC}"
echo "----------------"
test_endpoint "Official Snippets" "http://localhost:8081/official"
test_endpoint "Leaderboard Stats" "http://localhost:8083/stats"
test_endpoint "Forum Posts" "http://localhost:8084/posts"

echo -e "${YELLOW}🔒 Auth Endpoints (Expected to fail without valid data)${NC}"
echo "--------------------------------------------------------"
test_endpoint "Personal Snippets (403 expected)" "http://localhost:8081/personal" 403
test_endpoint "User Profile (403 expected)" "http://localhost:8080/profile" 403

echo -e "${YELLOW}📚 API Documentation${NC}"
echo "----------------------"
echo "Visit these URLs in your browser:"
echo "• Auth API: http://localhost:8080/docs"
echo "• Snippets API: http://localhost:8081/docs"
echo "• Practice API: http://localhost:8082/docs"
echo "• Leaderboard API: http://localhost:8083/docs"
echo "• Forum API: http://localhost:8084/docs"

echo ""
echo -e "${GREEN}✨ Testing complete!${NC}"
echo ""
echo -e "${BLUE}💡 Next steps:${NC}"
echo "1. Check that all health checks passed"
echo "2. Visit the /docs URLs to see interactive API documentation"
echo "3. If all looks good, the server is ready for client integration!"