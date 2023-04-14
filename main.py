from analyzer.analyzer import Analyzer
from parser.parser import parse


def main():
    file_path = "../docs/diagrams/semantics_bad.bpmn"
    elements = parse(file_path)
    result = Analyzer.analyze(elements)


if __name__ == "__main__":
    main()
