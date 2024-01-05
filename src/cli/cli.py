import click

from src.analysis_input.analysis_types import AnalysisType
from src.analysis_input.input import Input
from dataclasses import dataclass

@dataclass
class Args:
    """Class for returning the arguments."""
    input: Input
    model_path: str

def cli() -> Args:
    """Wrapper for calling the cli. Returns the arguments object"""
    return base(standalone_mode=False)

@click.group()
@click.pass_context
@click.argument('MODEL_PATH', type=click.Path(exists=True))
def base(ctx, model_path):
    """Performs the analysis.
    See the available commands for a specific analysis.

    MODEL_PATH is path to the BPMN4FRSS model file.
    """
    ctx.ensure_object(dict)
    ctx.obj["MODEL_PATH"] = model_path

@base.command()
@click.pass_context
def rules(ctx):
    """Performs the Semantic Rules Analysis.
    
    """
    return Args(
        input=Input(AnalysisType.SEMANTIC_RULES, None),
        model_path=ctx.obj["MODEL_PATH"])

@base.command()
@click.pass_context
def hints(ctx):
    """Performs the Semantic Hints Analysis.

    """
    return Args(
        input=Input(AnalysisType.SEMANTIC_HINTS, None),
        model_path=ctx.obj["MODEL_PATH"])

@base.command()
@click.pass_context
@click.argument("ELEMENT_ID")
def evidence_quality(ctx, element_id):
    """Performs the Evidence Quality Analysis.

    ELEMENT_ID is element ID for the analysis.
    """
    return Args(
        input=Input(AnalysisType.EVIDENCE_QUALITY_ANALYSIS, element_id),
        model_path=ctx.obj["MODEL_PATH"])
