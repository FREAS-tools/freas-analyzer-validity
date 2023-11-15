from src.input.analysis_types import AnalysisType
from src.input.input import Input
from src.api.model import AnalysisModel
from src.parser.parser import parse_string
from src.analyzer.analyzer import Analyzer
from src.result.result import ResultEncoder

from base64 import b64decode
from json import dumps
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"]
)

@app.post("/analysis")
async def execute_analysis(analysis: AnalysisModel):

    try:
        analysis_input = Input(AnalysisType[analysis.analysis_type], analysis.element_id)
        bpmn4frss_elements = parse_string(b64decode(analysis.model))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while parsing the BPMN4FRSS model: {e}")
    
    try:
        result = Analyzer.analyze(analysis_input, bpmn4frss_elements)
        json_result = dumps(result, cls=ResultEncoder).encode('utf-8')
        return Response(media_type="application/json", content=json_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {e}")