from src.input.analysis_types import AnalysisType
from src.input.input import Input
from src.api.model import AnalysisModel
from src.parser.parser import parse_string
from src.analyzer.analyzer import Analyzer

from fastapi import FastAPI, HTTPException
import base64

app = FastAPI()

@app.post("/analysis")
async def execute_analysis(analysis: AnalysisModel):

    try:
        analysis_input = Input(AnalysisType[analysis.analysis_type], analysis.element_id)
        bpmn4frss_elements = parse_string(base64.b64decode(analysis.model))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while parsing the BPMN4FRSS model: {e}")
    
    try:
        result = Analyzer.analyze(analysis_input, bpmn4frss_elements)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {e}")