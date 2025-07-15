#!/bin/bash

# SyntaxMem Local Development Server
# Runs all Cloud Functions locally for development and testing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function definitions
FUNCTIONS=(
    "auth:8080:Authentication Service"
    "snippets:8081:Snippets Management"
    "practice:8082:Practice Sessions"
    "leaderboard:8083:Leaderboard & Rankings"
    "forum:8084:Forum & Comments"
)

# PIDs of running processes
declare -a PIDS=()
declare -a PORTS=()

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down development servers...${NC}"
    
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            echo "Stopping process $pid..."
            kill "$pid" 2>/dev/null || true
        fi
    done
    
    # Wait a moment for graceful shutdown
    sleep 2
    
    # Force kill if still running
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            echo "Force stopping process $pid..."
            kill -9 "$pid" 2>/dev/null || true
        fi
    done
    
    echo -e "${GREEN}✅ All servers stopped${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check if .env file exists
check_env() {
    if [[ ! -f ".env" ]]; then
        echo -e "${RED}❌ .env file not found${NC}"
        echo -e "${YELLOW}💡 Please copy .env.example to .env and configure it:${NC}"
        echo "   cp .env.example .env"
        echo "   # Edit .env with your MongoDB URI, JWT secret, etc."
        exit 1
    fi
    echo -e "${GREEN}✅ Environment file found${NC}"
}

# Check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}❌ Port $port is already in use${NC}"
        echo "Please stop the process using port $port or choose a different port"
        exit 1
    fi
}

# Install dependencies for a function
install_deps() {
    local func_name=$1
    local func_dir="functions/$func_name"
    
    if [[ ! -d "$func_dir" ]]; then
        echo -e "${RED}❌ Function directory $func_dir not found${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📦 Installing dependencies for $func_name...${NC}"
    
    # Check if virtual environment exists, create if not
    if [[ ! -d "$func_dir/venv" ]]; then
        echo "Creating virtual environment for $func_name..."
        python3 -m venv "$func_dir/venv"
    fi
    
    # Activate virtual environment and install dependencies
    source "$func_dir/venv/bin/activate"
    pip install -q -r "$func_dir/requirements.txt"
    deactivate
    
    echo -e "${GREEN}✅ Dependencies installed for $func_name${NC}"
}

# Start a function server
start_function() {
    local func_name=$1
    local port=$2
    local description=$3
    local func_dir="functions/$func_name"
    
    echo -e "${YELLOW}🚀 Starting $description on port $port...${NC}"
    
    # Check if function directory exists
    if [[ ! -d "$func_dir" ]]; then
        echo -e "${RED}❌ Function directory $func_dir not found${NC}"
        return 1
    fi
    
    # Install dependencies
    install_deps "$func_name"
    
    # Start the function in background
    cd "$func_dir"
    source venv/bin/activate
    
    # Start functions framework
    functions-framework --target=main --port=$port --debug 2>&1 | while IFS= read -r line; do
        echo -e "${CYAN}[$func_name:$port]${NC} $line"
    done &
    
    local pid=$!
    PIDS+=($pid)
    PORTS+=($port)
    
    cd - > /dev/null
    
    echo -e "${GREEN}✅ $description started (PID: $pid)${NC}"
    return 0
}

# Wait for server to be ready
wait_for_server() {
    local port=$1
    local func_name=$2
    local max_attempts=30
    local attempt=1
    
    echo -n "Waiting for $func_name to be ready"
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
            echo -e " ${GREEN}✅${NC}"
            return 0
        fi
        
        echo -n "."
        sleep 1
        ((attempt++))
    done
    
    echo -e " ${RED}❌ Timeout${NC}"
    return 1
}

# Test all endpoints
test_endpoints() {
    echo ""
    echo -e "${BLUE}🧪 Testing API endpoints...${NC}"
    echo ""
    
    for func_port in "${FUNCTIONS[@]}"; do
        IFS=':' read -r func_name port description <<< "$func_port"
        
        echo -e "${CYAN}Testing $description (http://localhost:$port)${NC}"
        
        # Test health endpoint
        if curl -s "http://localhost:$port/health" | grep -q "healthy"; then
            echo -e "  ✅ Health check: ${GREEN}OK${NC}"
        else
            echo -e "  ❌ Health check: ${RED}FAILED${NC}"
        fi
        
        echo ""
    done
}

# Main function
main() {
    echo "======================================"
    echo -e "${PURPLE}🎯 SyntaxMem Development Server${NC}"
    echo "======================================"
    echo ""
    
    # Pre-flight checks
    check_env
    
    # Check if all ports are available
    for func_port in "${FUNCTIONS[@]}"; do
        IFS=':' read -r func_name port description <<< "$func_port"
        check_port "$port"
    done
    
    echo ""
    echo -e "${BLUE}🚀 Starting all functions...${NC}"
    echo ""
    
    # Start all functions
    for func_port in "${FUNCTIONS[@]}"; do
        IFS=':' read -r func_name port description <<< "$func_port"
        
        if start_function "$func_name" "$port" "$description"; then
            sleep 2  # Give each function time to start
        else
            echo -e "${RED}❌ Failed to start $func_name${NC}"
            cleanup
            exit 1
        fi
    done
    
    echo ""
    echo -e "${GREEN}🎉 All functions started successfully!${NC}"
    echo ""
    
    # Wait for all servers to be ready
    echo -e "${BLUE}⏳ Waiting for all servers to be ready...${NC}"
    for func_port in "${FUNCTIONS[@]}"; do
        IFS=':' read -r func_name port description <<< "$func_port"
        wait_for_server "$port" "$func_name"
    done
    
    # Test endpoints
    test_endpoints
    
    # Show running services
    echo "======================================"
    echo -e "${GREEN}🌟 SyntaxMem API Development Server${NC}"
    echo "======================================"
    echo ""
    echo -e "${YELLOW}📡 Running Services:${NC}"
    
    for func_port in "${FUNCTIONS[@]}"; do
        IFS=':' read -r func_name port description <<< "$func_port"
        echo -e "  🔹 $description"
        echo -e "     ${CYAN}http://localhost:$port${NC}"
        echo ""
    done
    
    echo -e "${YELLOW}🧪 Quick Test Commands:${NC}"
    echo "  # Test auth health"
    echo -e "  ${CYAN}curl http://localhost:8080/health${NC}"
    echo ""
    echo "  # Test snippets"
    echo -e "  ${CYAN}curl http://localhost:8081/official${NC}"
    echo ""
    echo "  # Test leaderboard"
    echo -e "  ${CYAN}curl http://localhost:8083/stats${NC}"
    echo ""
    
    echo -e "${YELLOW}💡 Tips:${NC}"
    echo "  • Press ${RED}Ctrl+C${NC} to stop all servers"
    echo "  • Logs are shown with colored prefixes"
    echo "  • Each function runs in its own virtual environment"
    echo "  • Changes require restart (no hot reload)"
    echo ""
    
    # Keep script running
    echo -e "${GREEN}✨ Development server is running... Press Ctrl+C to stop${NC}"
    echo ""
    
    # Wait for user to stop
    while true; do
        sleep 1
    done
}

# Handle script arguments
case "${1:-}" in
    "install")
        echo -e "${BLUE}📦 Installing dependencies for all functions...${NC}"
        for func_port in "${FUNCTIONS[@]}"; do
            IFS=':' read -r func_name port description <<< "$func_port"
            install_deps "$func_name"
        done
        echo -e "${GREEN}✅ All dependencies installed${NC}"
        ;;
    "test")
        echo -e "${BLUE}🧪 Testing endpoints only...${NC}"
        test_endpoints
        ;;
    "clean")
        echo -e "${BLUE}🧹 Cleaning virtual environments...${NC}"
        for func_port in "${FUNCTIONS[@]}"; do
            IFS=':' read -r func_name port description <<< "$func_port"
            if [[ -d "functions/$func_name/venv" ]]; then
                echo "Removing venv for $func_name..."
                rm -rf "functions/$func_name/venv"
            fi
        done
        echo -e "${GREEN}✅ Virtual environments cleaned${NC}"
        ;;
    "help"|"-h"|"--help")
        echo "SyntaxMem Development Server"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  (no args)  Start all development servers"
        echo "  install    Install dependencies for all functions"
        echo "  test       Test all endpoints"
        echo "  clean      Remove all virtual environments"
        echo "  help       Show this help message"
        echo ""
        echo "The script will start these services:"
        for func_port in "${FUNCTIONS[@]}"; do
            IFS=':' read -r func_name port description <<< "$func_port"
            echo "  • $description: http://localhost:$port"
        done
        ;;
    *)
        main
        ;;
esac