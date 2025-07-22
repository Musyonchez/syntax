#!/usr/bin/env python3
"""
Database Seeding Script for SyntaxMem
Adds sample official snippets for development and testing
"""

import asyncio
import sys
import os
from datetime import datetime

# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from shared.database import get_snippets_collection
from shared.utils import generate_id, current_timestamp

# Sample official snippets
SAMPLE_SNIPPETS = [
    {
        "title": "Hello World Function",
        "content": '''def greet(name):
    """Return a greeting message"""
    return f"Hello, {name}!"

# Usage
message = greet("World")
print(message)''',
        "language": "python",
        "difficulty": 1,
        "description": "A simple function that returns a greeting message"
    },
    {
        "title": "List Comprehension Basics",
        "content": '''numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Square all even numbers
even_squares = [x**2 for x in numbers if x % 2 == 0]

print(even_squares)  # [4, 16, 36, 64, 100]''',
        "language": "python",
        "difficulty": 3,
        "description": "Practice with list comprehensions and filtering"
    },
    {
        "title": "Simple Calculator",
        "content": '''def calculator(a, b, operation):
    """Simple calculator function"""
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        return a / b if b != 0 else "Cannot divide by zero"
    else:
        return "Invalid operation"

# Test the calculator
result = calculator(10, 5, '+')
print(f"Result: {result}")''',
        "language": "python",
        "difficulty": 2,
        "description": "A basic calculator with arithmetic operations"
    },
    {
        "title": "Array Methods Practice",
        "content": '''const numbers = [1, 2, 3, 4, 5];

// Double each number
const doubled = numbers.map(x => x * 2);

// Filter even numbers
const evens = numbers.filter(x => x % 2 === 0);

// Sum all numbers
const sum = numbers.reduce((acc, x) => acc + x, 0);

console.log("Doubled:", doubled);
console.log("Evens:", evens);
console.log("Sum:", sum);''',
        "language": "javascript",
        "difficulty": 3,
        "description": "Working with array methods: map, filter, reduce"
    },
    {
        "title": "Basic Function",
        "content": '''function greetUser(name) {
    return `Hello, ${name}! Welcome to JavaScript.`;
}

// Call the function
const greeting = greetUser("Developer");
console.log(greeting);''',
        "language": "javascript",
        "difficulty": 1,
        "description": "A simple JavaScript function with template literals"
    },
    {
        "title": "Class Definition",
        "content": '''class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# Create instance and use methods
rect = Rectangle(5, 3)
print(f"Area: {rect.area()}")
print(f"Perimeter: {rect.perimeter()}")''',
        "language": "python",
        "difficulty": 4,
        "description": "Object-oriented programming with classes and methods"
    }
]

async def seed_database():
    """Add sample official snippets to the database"""
    try:
        print("🌱 Starting database seeding...")
        
        snippets_collection = await get_snippets_collection()
        
        # Check if we already have official snippets
        existing_count = await snippets_collection.count_documents({
            "type": "official",
            "status": "active"
        })
        
        if existing_count > 0:
            print(f"   ℹ️  Found {existing_count} existing official snippets")
            response = input("   Do you want to add more sample snippets? (y/N): ")
            if response.lower() != 'y':
                print("   Skipping seeding.")
                return
        
        # Add sample snippets
        admin_user_id = "admin"  # Default admin user ID
        added_count = 0
        
        for snippet_data in SAMPLE_SNIPPETS:
            # Check if this snippet already exists
            existing = await snippets_collection.find_one({
                "title": snippet_data["title"],
                "type": "official"
            })
            
            if existing:
                print(f"   ⏭️  Skipping '{snippet_data['title']}' (already exists)")
                continue
            
            # Create new snippet document
            snippet_doc = {
                "_id": generate_id(),
                "title": snippet_data["title"],
                "content": snippet_data["content"],
                "language": snippet_data["language"],
                "difficulty": snippet_data["difficulty"],
                "type": "official",
                "status": "active",
                "author": admin_user_id,
                "description": snippet_data.get("description", ""),
                "solveCount": 0,
                "avgScore": 0.0,
                "createdAt": current_timestamp(),
                "updatedAt": current_timestamp()
            }
            
            await snippets_collection.insert_one(snippet_doc)
            added_count += 1
            print(f"   ✅ Added '{snippet_data['title']}' ({snippet_data['language']}, difficulty {snippet_data['difficulty']})")
        
        print(f"\n🎉 Successfully added {added_count} official snippets to the database!")
        
        # Show summary
        total_official = await snippets_collection.count_documents({
            "type": "official",
            "status": "active"
        })
        print(f"📊 Total official snippets in database: {total_official}")
        
        # Show by language
        for language in ["python", "javascript"]:
            count = await snippets_collection.count_documents({
                "type": "official",
                "status": "active",
                "language": language
            })
            print(f"   • {language.title()}: {count} snippets")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("SyntaxMem Database Seeding Script")
    print("=================================")
    asyncio.run(seed_database())