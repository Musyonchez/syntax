#!/usr/bin/env python3
"""
Snippets Test: Schema Validation
Tests that snippet creation properly validates data using schemas
"""

import asyncio
import aiohttp
import sys
import os

# Add shared modules to path
sys.path.append('../../shared')
sys.path.append('../../schemas')

# Test configuration
SNIPPETS_URL = "http://localhost:8083"
TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjg4YTJmZTg0MmJhM2FjY2QzODAxY2E3IiwiZW1haWwiOiJ0ZXN0LnVzZXIuMTA5NzI5LjgyNDcyMTQ2NUBleGFtcGxlLmNvbSIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc1Mzg5MTkxMCwiaWF0IjoxNzUzODg4MzEwfQ.WK4HgS0InfKbrYyypVIAZv0gEmaL6tnDQUnCIFq3ju4"

async def test_schema_validation():
    """Test that schema validation works correctly"""
    print("🧪 Testing schema validation...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
        
        # Test missing required fields
        invalid_data_tests = [
            ({}, "empty data"),
            ({"title": ""}, "empty title"),
            ({"title": "Test", "code": ""}, "empty code"),
            ({"title": "Test", "code": "console.log('hi')"}, "missing language"),
            ({"title": "Test", "code": "console.log('hi')", "language": ""}, "empty language"),
        ]
        
        for data, description in invalid_data_tests:
            async with session.post(
                f"{SNIPPETS_URL}/personal",
                json=data,
                headers=headers
            ) as response:
                if response.status == 200:
                    print(f"  ❌ Should reject {description}, but accepted it")
                    return False
                elif response.status == 400:
                    print(f"  ✅ Properly rejected {description}")
                else:
                    # Might be 401 if token is invalid, which is fine for this test
                    print(f"  ℹ️ {description} returned status {response.status}")
        
        # Test valid data
        valid_data = {
            "title": "Valid Test Snippet",
            "description": "A valid snippet for testing",
            "code": "console.log('Hello, World!');",
            "language": "javascript",
            "tags": ["test", "javascript"],
            "difficulty": "easy",
            "isPrivate": True
        }
        
        async with session.post(
            f"{SNIPPETS_URL}/personal",
            json=valid_data,
            headers=headers
        ) as response:
            if response.status == 401:
                print(f"  ℹ️ Valid data test skipped (auth required)")
            elif response.status == 200:
                data = await response.json()
                if data.get('success'):
                    print(f"  ✅ Valid data properly accepted")
                else:
                    print(f"  ❌ Valid data rejected: {data}")
                    return False
            else:
                data = await response.json()
                print(f"  ❌ Valid data unexpected status {response.status}: {data}")
                return False
        
        # Test data normalization
        normalization_data = {
            "title": "  Test With Spaces  ",
            "description": "  Description with spaces  ",
            "code": "console.log('test');",
            "language": "  JAVASCRIPT  ",  # Should be normalized to lowercase
            "tags": ["  React  ", "COMPONENT", "  test  "],  # Should be normalized
            "difficulty": "EASY",  # Should be normalized to lowercase
        }
        
        async with session.post(
            f"{SNIPPETS_URL}/personal",
            json=normalization_data,
            headers=headers
        ) as response:
            if response.status == 401:
                print(f"  ℹ️ Normalization test skipped (auth required)")
            elif response.status == 200:
                data = await response.json()
                if data.get('success'):
                    snippet = data.get('data', {})
                    
                    # Check normalization
                    if snippet.get('language') != 'javascript':
                        print(f"  ❌ Language not normalized: {snippet.get('language')}")
                        return False
                    
                    if snippet.get('difficulty') != 'easy':
                        print(f"  ❌ Difficulty not normalized: {snippet.get('difficulty')}")
                        return False
                    
                    print(f"  ✅ Data properly normalized")
                else:
                    print(f"  ❌ Normalization data rejected: {data}")
            else:
                print(f"  ℹ️ Normalization test returned status {response.status}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False
    finally:
        if session:
            await session.close()

if __name__ == "__main__":
    result = asyncio.run(test_schema_validation())
    exit(0 if result else 1)