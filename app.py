import subprocess
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

class ValidateRequest(BaseModel):
    userInputs: Dict[str, str]

@app.post("/api/process_code")
async def process_code(request: CodeRequest):
    code = request.code
    result = subprocess.run(['node', 'ast_processor.js', code], capture_output=True, text=True)

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail="Error processing code")

    result_json = json.loads(result.stdout)
    blanked_code = result_json['blankedCode']
    placeholders = result_json['placeholders']
    return {"blankedCode": blanked_code, "placeholders": placeholders}

@app.post("/api/validate_code")
async def validate_code(request: ValidateRequest):
    user_inputs = request.userInputs
    # Implement validation logic based on the placeholders sent back
    pass
