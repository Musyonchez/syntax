#!/usr/bin/env python3
"""
Script to populate official_snippets and personal_snippets collections with test data
"""

import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE_NAME = 'syntaxmem'

async def create_test_data():
    """Create test data for both collections"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    
    # Drop existing collections to start fresh
    await db.official_snippets.drop()
    await db.personal_snippets.drop()
    print("Dropped existing snippet collections")
    
    # User IDs from your provided data
    user_musyoka = ObjectId("687445a688e3f1882cd2d161")
    user_bioagro = ObjectId("6880e811f9d50418d256c76e")
    
    # Official Snippets Data
    official_snippets = [
        {
            "_id": ObjectId(),
            "title": "Add Two Numbers",
            "language": "python",
            "difficulty": 2,
            "originalCode": "def add_numbers(a, b):\n    return a + b\n\n# Test the function\nresult = add_numbers(5, 3)\nprint(f\"Result: {result}\")",
            "status": "active",
            "authorName": "SyntaxMem Team",
            "solveCount": 45,
            "avgScore": 8.2,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        },
        {
            "_id": ObjectId(),
            "title": "Filter Even Numbers",
            "language": "python", 
            "difficulty": 5,
            "originalCode": "def filter_even(numbers):\n    return [num for num in numbers if num % 2 == 0]\n\n# Test the function\nnumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\neven_nums = filter_even(numbers)\nprint(f\"Even numbers: {even_nums}\")",
            "status": "active",
            "authorName": "SyntaxMem Team",
            "solveCount": 32,
            "avgScore": 7.8,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        },
        {
            "_id": ObjectId(),
            "title": "Recursive Factorial",
            "language": "python",
            "difficulty": 8,
            "originalCode": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\n# Test the function\nresult = factorial(5)\nprint(f\"5! = {result}\")",
            "status": "active", 
            "authorName": "SyntaxMem Team",
            "solveCount": 18,
            "avgScore": 6.9,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)  
        },
        {
            "_id": ObjectId(),
            "title": "Transform Array Elements",
            "language": "javascript",
            "difficulty": 3,
            "originalCode": "function doubleNumbers(arr) {\n    return arr.map(num => num * 2);\n}\n\n// Test the function\nconst numbers = [1, 2, 3, 4, 5];\nconst doubled = doubleNumbers(numbers);\nconsole.log('Doubled:', doubled);",
            "status": "active",
            "authorName": "SyntaxMem Team", 
            "solveCount": 38,
            "avgScore": 8.0,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        },
        {
            "_id": ObjectId(),
            "title": "Async API Call",
            "language": "javascript",
            "difficulty": 6,
            "originalCode": "async function fetchUserData(userId) {\n    try {\n        const response = await fetch(`/api/users/${userId}`);\n        const data = await response.json();\n        return data;\n    } catch (error) {\n        console.error('Error fetching user:', error);\n        throw error;\n    }\n}\n\n// Usage example\nfetchUserData(123).then(user => console.log(user));",
            "status": "active",
            "authorName": "SyntaxMem Team",
            "solveCount": 25,
            "avgScore": 7.5,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        },
        {
            "_id": ObjectId(),
            "title": "Promise.all with Error Handling", 
            "language": "javascript",
            "difficulty": 9,
            "originalCode": "async function fetchMultipleUsers(userIds) {\n    try {\n        const promises = userIds.map(id => fetch(`/api/users/${id}`));\n        const responses = await Promise.all(promises);\n        \n        const users = await Promise.all(\n            responses.map(response => {\n                if (!response.ok) throw new Error(`HTTP ${response.status}`);\n                return response.json();\n            })\n        );\n        \n        return users;\n    } catch (error) {\n        console.error('Failed to fetch users:', error);\n        throw error;\n    }\n}",
            "status": "active",
            "authorName": "SyntaxMem Team",
            "solveCount": 12,
            "avgScore": 6.8,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        }
    ]
    
    # Personal Snippets Data (for testing auth)
    personal_snippets = [
        {
            "_id": ObjectId(),
            "userId": user_musyoka,
            "title": "My String Reverser",
            "language": "python",
            "difficulty": 3,
            "originalCode": "def reverse_string(text):\n    return text[::-1]\n\n# My custom test\nreversed_text = reverse_string('Hello World')\nprint(f\"Reversed: {reversed_text}\")",
            "status": "private",
            "solveCount": 5,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        },
        {
            "_id": ObjectId(),
            "userId": user_musyoka,
            "title": "Custom Password Validator",
            "language": "javascript", 
            "difficulty": 6,
            "originalCode": "function validatePassword(password) {\n    const minLength = 8;\n    const hasUpper = /[A-Z]/.test(password);\n    const hasLower = /[a-z]/.test(password);\n    const hasNumber = /\\d/.test(password);\n    const hasSpecial = /[!@#$%^&*]/.test(password);\n    \n    return password.length >= minLength && hasUpper && hasLower && hasNumber && hasSpecial;\n}\n\nconsole.log(validatePassword('MyPass123!'));",
            "status": "shared",
            "solveCount": 3,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        },
        {
            "_id": ObjectId(),
            "userId": user_bioagro,
            "title": "Crop Yield Calculator",
            "language": "python",
            "difficulty": 4,
            "originalCode": "def calculate_yield(area_hectares, yield_per_hectare):\n    total_yield = area_hectares * yield_per_hectare\n    return {\n        'area': area_hectares,\n        'yield_per_hectare': yield_per_hectare,\n        'total_yield': total_yield,\n        'estimated_revenue': total_yield * 2.5  # $2.5 per kg\n    }\n\nresult = calculate_yield(10, 5000)\nprint(f\"Farm yield: {result}\")",
            "status": "shared",
            "solveCount": 2,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        },
        {
            "_id": ObjectId(),
            "userId": user_bioagro,
            "title": "Math Problem Solver",
            "language": "javascript",
            "difficulty": 7,
            "originalCode": "class MathSolver {\n    static solveQuadratic(a, b, c) {\n        const discriminant = b * b - 4 * a * c;\n        \n        if (discriminant < 0) {\n            return { solutions: [], type: 'no real solutions' };\n        } else if (discriminant === 0) {\n            const x = -b / (2 * a);\n            return { solutions: [x], type: 'one solution' };\n        } else {\n            const x1 = (-b + Math.sqrt(discriminant)) / (2 * a);\n            const x2 = (-b - Math.sqrt(discriminant)) / (2 * a);\n            return { solutions: [x1, x2], type: 'two solutions' };\n        }\n    }\n}\n\nconsole.log(MathSolver.solveQuadratic(1, -5, 6));",
            "status": "private",
            "solveCount": 1,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        }
    ]
    
    # Insert official snippets
    if official_snippets:
        result = await db.official_snippets.insert_many(official_snippets)
        print(f"Inserted {len(result.inserted_ids)} official snippets")
    
    # Insert personal snippets  
    if personal_snippets:
        result = await db.personal_snippets.insert_many(personal_snippets)
        print(f"Inserted {len(result.inserted_ids)} personal snippets")
    
    # Create indexes
    await db.official_snippets.create_index([("language", 1), ("difficulty", 1), ("status", 1)])
    await db.official_snippets.create_index([("status", 1), ("createdAt", -1)])
    
    await db.personal_snippets.create_index([("userId", 1), ("status", 1)])
    await db.personal_snippets.create_index([("userId", 1), ("language", 1), ("difficulty", 1)])
    
    print("Created indexes for both collections")
    
    # Close connection
    client.close()
    print("Test data creation completed!")

if __name__ == "__main__":
    asyncio.run(create_test_data())