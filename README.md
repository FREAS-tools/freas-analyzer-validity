# BPMN4FRSS Analysis Tool

The tool analyzes BPMN4FRSS models representing forensic-ready software systems. The analysis process utilizes **Z3 SMT Solver** to evaluate the extent to which a system complies with forensic readiness requirements. Furthermore, it assesses system's ability to provide evidence with high evidentiary value in case of an incident. As a result, the implemented tool allows software engineers to inspect the possible model insufficiencies and offers hints to remedy the issue.

## Analysis Types
Forensic readiness requirements are captured in the form of rules.
The rules are divided into three categories depending on the type of analysis they perform:

**Semantic Rules Analysis** 
  * verifies if the provided model is in accordance with BPMN4FRSS semantic rules. If the model violates any of the rules, the tool returns **Errors** that indicate the concrete problem and can help users fix the issue.

**Semantic Hints Analysis** 
  * provides recommendations for improving the model. Violating these rules results in **Warnings** but does not affect the model's validity. Nevertheless, compliance with these rules is highly recommended, as their violation can indicate potential weaknesses.

**Evidence Quality Analysis**
  * checks whether the employed forensic-ready controls are sufficient to yield reliable and relevant potential evidence in case of an incident. 
  To simulate an incident, the user can mark a concrete **Data Store** or a **Flow Object** (Task or Event) from the model as compromised, i.e., provide the **id** of a specific element within the analysis input. \
  In both cases, analysis output is a list of Data Store elements that contain potential evidence. Stored potential evidence can hold information to help detect the inconsistency between incident related data.


## Running the Analysis
Analysis input requires **model path** to the BPMN4FRSS model, **command** representing the analysis type and in case of Evidence Quality Analysis, the **compromised element id** as an argument.

To run the analysis, run one of the following commands in the root directory of the project:
  - `python main.py [OPTIONS] MODEL_PATH COMMAND [ARGS]`
  - `poetry run main.py [OPTIONS] MODEL_PATH COMMAND [ARGS]`

Use `--help` for more details.

## Running the Tests
To run all tests, run one of the following commands in the root directory of the project:
  - `pytest`
  - `poetry run pytest`

or to run just unit or integration tests:
  - `pytest tests/test_unit`
  - `pytest tests/test_integration`

## Run the API
To run the analysis exposed as REST API, run the following command:
 - `poetry run uvicorn src.api.api:app --reload`

## Requirements

To install the dependencies:
- `poetry install`

## License
MIT
