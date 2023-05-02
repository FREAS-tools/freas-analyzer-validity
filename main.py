import json

from analyzer.analyzer import Analyzer
from input.input import BPMN4FRSSInput
from parser.parser import parse
from results.result import ResultEncoder


def main():
    file_path = "./docs/diagrams/disputable_stored_in_same_context.bpmn"

    # # Parse the JSON input
    # input_data = request.json
    # analysis_type = input_data['analysis_type']
    # element_id = input_data.get('element_id')

    # # Get the BPMN4FRSS file data
    # bpmn_file = request.files['bpmn_file']

    analysis_input = BPMN4FRSSInput("EVIDENCE_QUALITY_ANALYSIS", "Activity_19xl907")

    try:
        bpmn4frss_elements = parse(file_path)

        # perform the analysis using the analysis_input and bpmn4frss_elements to get an instance of the Result class
        result = Analyzer.analyze(analysis_input, bpmn4frss_elements)
        print("Analysis finished")

        # result_json = json.dumps(result, indent=2, cls=ResultEncoder)
        # print(result_json)
    except Exception as e:  # TODO specify exception
        print("Error while parsing BPMN4FRSS file")
        print(e)
        return

    for error in result.errors:
        print(error.source)
        print(error.message)
    for warning in result.warnings:
        print(warning.source)
        print(warning.message)
    if result.evidence_sources is not None:
        print(result.evidence_sources.source)
        print(result.evidence_sources.message)

    # serialize the Result instance into a dictionary
    # json_result = result.to_dict()

    # send the JSON result back to the frontend
    # return jsonify(json_result)


if __name__ == "__main__":
    main()
