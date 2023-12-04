import logging

from src.analysis_input.analysis_types import AnalysisType
from src.analysis_input.input import Input
from src.api.model import AnalysisModel
from src.parser.parser import Parser
from src.analyzer.analyzer import Analyzer
from src.analysis_output.output import OutputEncoder

from sys import stdout
from base64 import b64decode
from json import dumps
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

# Setup logging
logging.basicConfig(stream=stdout)

# Setup API
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
        parser = Parser()
        bpmn4frss_elements = parser.parse_string(b64decode(analysis.model))
    except Exception as e:
        logging.error('Error while parsing the BPMN4FRSS model: %s', e)
        raise HTTPException(status_code=400, detail=f"Error while parsing the BPMN4FRSS model: {e}")

    try:
        analysis_output = Analyzer.analyze(analysis_input, bpmn4frss_elements)
        json_output = dumps(analysis_output, cls=OutputEncoder).encode('utf-8')
        return Response(media_type="application/json", content=json_output)
    except Exception as e:
        logging.error('Analysis error: %s', e)
        raise HTTPException(status_code=500, detail=f"Analysis error: {e}")
