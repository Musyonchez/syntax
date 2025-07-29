# SyntaxMem Schemas

**Simple, Uniform, Consistent** data validation for all database operations.

## 🎯 Purpose

Schemas provide:
- **Input validation** - Prevent bad data from entering the database
- **Data sanitization** - Clean and normalize input data  
- **Structure documentation** - Clear data contracts for all collections
- **Consistent patterns** - Same validation approach everywhere

## 📁 Schema Files

Each collection gets its own schema file:

```
schemas/
├── users.py      # User authentication and profile data
├── tokens.py     # JWT refresh token validation
├── snippets.py   # Code snippet data validation
├── sessions.py   # Practice session tracking
├── leaderboard.py (future)
├── forums.py     (future)
└── __init__.py   # Import all schemas
```

## 🚨 Schema Rules

### The Sacred Laws (NEVER BREAK)

1. **One Schema Per Collection** - Each MongoDB collection gets exactly one schema file
2. **Simple Validation Only** - No complex business logic, just data validation
3. **Static Methods Only** - No class instances, just `ClassName.validate_create(data)`
4. **Consistent Naming** - All schemas follow same method naming pattern
5. **Fail Fast** - Raise `ValueError` immediately for invalid data

### Method Patterns (UNIFORM)

Every schema MUST have these methods:

```python
class ExampleSchema:
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for creating new record"""
        # 1. Check required fields
        # 2. Validate data types
        # 3. Set defaults
        # 4. Add timestamps
        # 5. Return clean data
        
    @staticmethod  
    def validate_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for updating existing record"""
        # 1. Check optional fields only
        # 2. Validate changed data
        # 3. Return only changed fields
```

### Error Handling (CONSISTENT)

All validation errors MUST use `ValueError`:

```python
# ✅ CORRECT
if not email or '@' not in email:
    raise ValueError("Valid email is required")

# ❌ WRONG - don't use custom exceptions
if not email:
    raise CustomValidationError("Email missing")
```

### Data Types (SIMPLE)

Only use basic Python types:

```python
# ✅ CORRECT
return {
    'name': str,
    'age': int, 
    'active': bool,
    'tags': list,
    'metadata': dict,
    'createdAt': datetime
}

# ❌ WRONG - no complex objects
return SomeCustomClass(data)
```

## 📋 Usage Patterns

### Import Schema
```python
# In any function
import sys
sys.path.append('../schemas')
from users import UserSchema
```

### Validate New Data
```python
# Creating new record
try:
    clean_data = UserSchema.validate_create(request_data)
    result = await collection.insert_one(clean_data)
except ValueError as e:
    return create_error_response(str(e), 400)
```

### Validate Updates
```python
# Updating existing record
try:
    update_data = UserSchema.validate_update(request_data)
    if update_data:  # Only update if there are changes
        await collection.update_one({"_id": user_id}, {"$set": update_data})
except ValueError as e:
    return create_error_response(str(e), 400)
```

## 🔧 Required Fields

Every schema MUST include these fields:

### For New Records (`validate_create`)
```python
{
    'createdAt': datetime.now(timezone.utc),
    'updatedAt': datetime.now(timezone.utc),
    # ... other fields
}
```

### For Updates (`validate_update`)
```python
# Only add updatedAt if data actually changed
if update_fields:
    update_fields['updatedAt'] = datetime.now(timezone.utc)
```

## 🚫 What NOT to Do

### Forbidden Complexity
- ❌ Database queries inside schemas
- ❌ Business logic in validation
- ❌ Complex inheritance hierarchies  
- ❌ External API calls
- ❌ File system operations

### Forbidden Patterns
- ❌ Schemas that return database records
- ❌ Schemas that modify global state
- ❌ Schemas with side effects
- ❌ Async schema methods
- ❌ Schema methods that can fail silently

## ✅ Schema Checklist

Before committing any schema:

- [ ] File named after collection (users.py for users collection)
- [ ] Contains `validate_create()` method
- [ ] Contains `validate_update()` method  
- [ ] Uses only `ValueError` for validation errors
- [ ] Adds `createdAt` and `updatedAt` timestamps
- [ ] Imported in `__init__.py`
- [ ] Follows exact same pattern as existing schemas
- [ ] No database operations inside validation
- [ ] No business logic mixed with validation

## 🎯 Success Metrics

You know schemas are working when:

- **Zero invalid data** reaches the database
- **Same validation pattern** used everywhere
- **Clear error messages** for all validation failures
- **No duplicate validation code** across functions
- **New schemas take minutes to write** (copy existing pattern)

---

**Remember**: Schemas are data gatekeepers, not business logic. Keep them simple, uniform, and consistent. 🎯

*If your schema does more than validate and clean data, it's too complex.*