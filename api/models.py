from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CodeReviewFinding(BaseModel):
    type: str
    severity: str
    description: str
    suggested_fix: Optional[str] = None

class CodeReviewResult(BaseModel):
    code_style: List[CodeReviewFinding]
    potential_bugs: List[CodeReviewFinding]
    performance: List[CodeReviewFinding]
    best_practices: List[CodeReviewFinding]
    overall_assessment: str