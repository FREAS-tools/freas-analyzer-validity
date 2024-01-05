import json

from src.parser.parser import Parser
from src.analyzer.analyzer import Analyzer
from src.analysis_output.output import OutputEncoder

from src.cli.cli import cli

def main():
    # Load arguments from CLI
    args = cli()
    if not args:
        exit()

    print("File path: " + args.model_path)
    print("Analysis type: " + str(args.input.analysis_type))
    print("Element ID: " + (str(args.input.element_id)))
    print()

    parser = Parser()
    bpmn4frss_elements = parser.parse_file(args.model_path)

    # Perform the analysis using the analysis_input and bpmn4frss_elements to get an instance of the Result class
    result = Analyzer.analyze(args.input, bpmn4frss_elements)
    result_json = json.dumps(result, indent=2, cls=OutputEncoder)

    print("Analysis result:")
    print(result_json)

if __name__ == "__main__":
    main()
