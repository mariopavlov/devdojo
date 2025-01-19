from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.code_runner import CodeRunner

router = APIRouter()

class CodeRequest(BaseModel):
    source_code: str
    test_code: Optional[str] = None

class CodeResponse(BaseModel):
    success: bool
    output: str
    error_message: Optional[str] = None

@router.post("/validate")
async def validate_code(request: CodeRequest) -> CodeResponse:
    result = CodeRunner.validate_syntax(request.source_code)
    return CodeResponse(
        success=result.success,
        output=result.output,
        error_message=result.error_message
    )

@router.post("/run-tests")
async def run_tests(request: CodeRequest) -> CodeResponse:
    if not request.test_code:
        raise HTTPException(status_code=400, detail="Test code is required")
    
    result = CodeRunner.run_tests(request.source_code, request.test_code)
    return CodeResponse(
        success=result.success,
        output=result.output,
        error_message=result.error_message
    )

@router.post("/execute")
async def execute_code(request: CodeRequest) -> CodeResponse:
    result = CodeRunner.execute_code(request.source_code)
    return CodeResponse(
        success=result.success,
        output=result.output,
        error_message=result.error_message
    )
