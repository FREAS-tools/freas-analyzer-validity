import json

from src.parser.parser import parse_file
from src.analyzer.analyzer import Analyzer
from src.analysis_input.input import AnalysisType
from src.analysis_input.input import Input
from src.analysis_output.output import OutputEncoder


def main():
    # Define the input file name
    input_path = 'src/analysis_input/input_example.json'

    # Load the JSON file
    with open(input_path, 'r') as file:
        data = json.load(file)

    # Extract information from the JSON data
    if "bpmn4frss_model" not in data or "analysis_type" not in data or "element_id" not in data:
        print("Error: Invalid JSON file")
        return

    file_path = data['bpmn4frss_model']
    analysis_type = data['analysis_type']
    element_id = data['element_id']

    print("JSON file loaded")
    print()
    print("File path: " + file_path)
    print("Analysis type: " + analysis_type)
    print("Element ID: " + (str(element_id) if element_id is not None else "None"))
    print()

    try:
        analysis_input = Input(AnalysisType[analysis_type], element_id)
        bpmn4frss_elements = parse_file(file_path)
    except Exception as e:
        print("Error while parsing the BPMN4FRSS model: " + str(e))
        return

    # Perform the analysis using the analysis_input and bpmn4frss_elements to get an instance of the Result class
    result = Analyzer.analyze(analysis_input, bpmn4frss_elements)
    result_json = json.dumps(result, indent=2, cls=OutputEncoder)

    print("Analysis result:")
    print(result_json)


if __name__ == "__main__":
    main()
