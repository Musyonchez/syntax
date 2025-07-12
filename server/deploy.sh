#!/bin/bash

# SyntaxMem Cloud Functions Deployment Script
# Deploy all serverless functions to Google Cloud

set -e  # Exit on any error

echo "🚀 Starting SyntaxMem Cloud Functions Deployment..."

# Configuration
PROJECT_ID="syntaxmem"
REGION="us-central1"
RUNTIME="python311"

# Function definitions: name:directory
FUNCTIONS=(
    "auth-verify:auth"
    "snippets-official:snippets"
    "snippets-personal:snippets"
    "snippets-mask:snippets"
    "snippets-submit:snippets"
    "practice-start:practice"
    "practice-submit:practice"
    "leaderboard-get:leaderboard"
    "forum-posts:forum"
    "forum-comments:forum"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gcloud is installed and authenticated
check_gcloud() {
    if ! command -v gcloud &> /dev/null; then
        echo -e "${RED}❌ gcloud CLI not found. Please install it first.${NC}"
        echo "Visit: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        echo -e "${RED}❌ Not authenticated with gcloud. Please run 'gcloud auth login'${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ gcloud CLI authenticated${NC}"
}

# Set project
set_project() {
    echo -e "${BLUE}📋 Setting project to $PROJECT_ID...${NC}"
    gcloud config set project $PROJECT_ID
    
    # Verify project exists
    if ! gcloud projects describe $PROJECT_ID &> /dev/null; then
        echo -e "${RED}❌ Project $PROJECT_ID not found or not accessible${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Project set to $PROJECT_ID${NC}"
}

# Enable required APIs
enable_apis() {
    echo -e "${BLUE}🔧 Enabling required APIs...${NC}"
    
    APIS=(
        "cloudfunctions.googleapis.com"
        "cloudbuild.googleapis.com"
        "cloudresourcemanager.googleapis.com"
    )
    
    for api in "${APIS[@]}"; do
        echo "Enabling $api..."
        gcloud services enable $api
    done
    
    echo -e "${GREEN}✅ APIs enabled${NC}"
}

# Deploy a single function
deploy_function() {
    local func_name=$1
    local func_dir=$2
    
    echo -e "${YELLOW}🔄 Deploying $func_name...${NC}"
    
    # Check if function directory exists
    if [[ ! -d "./functions/$func_dir" ]]; then
        echo -e "${RED}❌ Function directory ./functions/$func_dir not found${NC}"
        return 1
    fi
    
    # Check if .env file exists
    if [[ ! -f ".env" ]]; then
        echo -e "${RED}❌ .env file not found. Please create it from .env.example${NC}"
        return 1
    fi
    
    # Deploy function with environment variables from .env file
    gcloud functions deploy $func_name \
        --runtime $RUNTIME \
        --trigger-http \
        --allow-unauthenticated \
        --source=./functions/$func_dir \
        --entry-point=main \
        --region=$REGION \
        --memory=512MB \
        --timeout=540s \
        --env-vars-file=.env \
        --quiet
    
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ $func_name deployed successfully${NC}"
        
        # Get function URL
        local func_url=$(gcloud functions describe $func_name --region=$REGION --format="value(httpsTrigger.url)")
        echo -e "${BLUE}🔗 URL: $func_url${NC}"
        echo ""
    else
        echo -e "${RED}❌ Failed to deploy $func_name${NC}"
        return 1
    fi
}

# Deploy all functions
deploy_all_functions() {
    echo -e "${BLUE}🚀 Deploying all functions...${NC}"
    echo ""
    
    local success_count=0
    local total_count=${#FUNCTIONS[@]}
    
    for func in "${FUNCTIONS[@]}"; do
        IFS=':' read -r name dir <<< "$func"
        
        if deploy_function "$name" "$dir"; then
            ((success_count++))
        else
            echo -e "${RED}⚠️  Continuing with next function...${NC}"
            echo ""
        fi
    done
    
    echo "======================================"
    echo -e "${BLUE}📊 Deployment Summary${NC}"
    echo "======================================"
    echo -e "✅ Successful: ${GREEN}$success_count${NC}/$total_count"
    echo -e "❌ Failed: ${RED}$((total_count - success_count))${NC}/$total_count"
    echo ""
    
    if [[ $success_count -eq $total_count ]]; then
        echo -e "${GREEN}🎉 All functions deployed successfully!${NC}"
        echo ""
        echo -e "${BLUE}🔗 Your API endpoints:${NC}"
        echo "Auth: https://$REGION-$PROJECT_ID.cloudfunctions.net/auth-verify"
        echo "Snippets: https://$REGION-$PROJECT_ID.cloudfunctions.net/snippets-official"
        echo "Practice: https://$REGION-$PROJECT_ID.cloudfunctions.net/practice-start"
        echo "Leaderboard: https://$REGION-$PROJECT_ID.cloudfunctions.net/leaderboard-get"
        echo "Forum: https://$REGION-$PROJECT_ID.cloudfunctions.net/forum-posts"
        echo ""
        echo -e "${YELLOW}💡 Remember to configure your Next.js client with these URLs!${NC}"
    else
        echo -e "${YELLOW}⚠️  Some functions failed to deploy. Check the errors above.${NC}"
        exit 1
    fi
}

# Validate environment file
validate_env() {
    echo -e "${BLUE}🔐 Validating environment variables...${NC}"
    
    if [[ ! -f ".env" ]]; then
        echo -e "${RED}❌ .env file not found${NC}"
        echo -e "${YELLOW}💡 Please copy .env.example to .env and fill in your values:${NC}"
        echo "   cp .env.example .env"
        echo "   # Then edit .env with your actual values"
        return 1
    fi
    
    # Check for required variables
    local required_vars=("MONGODB_URI" "JWT_SECRET" "DATABASE_NAME")
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if ! grep -q "^${var}=" .env || grep -q "^${var}=$" .env || grep -q "^${var}=your-" .env; then
            missing_vars+=("$var")
        fi
    done
    
    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        echo -e "${RED}❌ Missing or incomplete environment variables:${NC}"
        for var in "${missing_vars[@]}"; do
            echo "   - $var"
        done
        echo -e "${YELLOW}💡 Please update your .env file with actual values${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ Environment variables validated${NC}"
}

# List deployed functions
list_functions() {
    echo -e "${BLUE}📋 Currently deployed functions:${NC}"
    gcloud functions list --regions=$REGION --format="table(name,status,trigger.httpsTrigger.url)"
}

# Main execution
main() {
    echo "======================================"
    echo -e "${BLUE}🎯 SyntaxMem Deployment Script${NC}"
    echo "======================================"
    echo ""
    
    # Run checks and setup
    check_gcloud
    set_project
    enable_apis
    validate_env
    
    echo ""
    echo "======================================"
    echo -e "${BLUE}🚀 Starting Function Deployment${NC}"
    echo "======================================"
    echo ""
    
    # Deploy functions
    deploy_all_functions
    
    echo ""
    echo "======================================"
    echo -e "${BLUE}📋 Final Status${NC}"
    echo "======================================"
    list_functions
    
    echo ""
    echo -e "${GREEN}🎉 Deployment completed!${NC}"
}

# Handle script arguments
case "${1:-}" in
    "list")
        list_functions
        ;;
    "validate")
        check_gcloud
        set_project
        validate_env
        ;;
    "single")
        if [[ -z "$2" || -z "$3" ]]; then
            echo "Usage: $0 single <function-name> <function-dir>"
            echo "Example: $0 single auth-verify auth"
            exit 1
        fi
        check_gcloud
        set_project
        validate_env
        deploy_function "$2" "$3"
        ;;
    *)
        main
        ;;
esac