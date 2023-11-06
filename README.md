# BPMN4FRSS Analysis Tool Utilizing Z3 SMT Solver

The tool analyzes BPMN4FRSS models representing a forensic-ready software system. The analysis process utilizes Z3 SMT Solver to evaluate the extent to which a system complies with forensic readiness requirements. Furthermore, it assesses system's ability to provide evidence with high evidentiary value in case of an incident. As a result, the implemented tool allows software engineers to inspect the possible model insufficiencies and offers hints to remedy the issue.

## Analysis Types
Forensic readiness requirements are captured in the form of rules.
The rules are divided into three categories depending on the type of analysis they perform:

**Semantic Rules Analysis** 
  * Verifies if the provided model is in accordance with BPMN4FRSS semantic rules. If the model is not valid, the tool returns **Errors** that indicate the concrete problem and can help users to remedy the issue.

**Semantic Hints Analysis** 
  * Provides recommendations during the design process. Violating these rules results in **Warnings**, but it does not affect model's validity. Nevertheless, compliance with these rules is highly recommended, as their violation can indicate potential weaknesses. 

**Evidence Quality Analysis**
  * Check whether the employed forensic-ready controls are sufficient to yield reliable and relevant potential evidence in case of an incident. 
  To simulate an incident, the user can mark a concrete **Data Store** or a **Flow Object** from the model as compromised, i.e., provide the **id** of a specific element within the analysis input.
  * In both cases, analysis output is a list of Data Store elements that contain potential evidence. Stored potential evidence can hold information to help detect the inconsistency between incident evidence data.
  The result of this analysis can help the software engineers assess the availability of relevant potential evidence, directly affecting the system’s forensic readiness state.

## Running the Analysis
Analysis input requires **file path** to the BPMN4FRSS model, **analysis type** and in case of Evidence Quality Analysis, the **compromised element id**.

To manually set the analysis input, the user can change the details of the `src/input/input_example.json` file or 
use one of the examples from the `src/input/examples.json`. 

To run the analysis, run one of the following commands in the root directory of the project:
  - `python main.py`
  - `poetry run main.py `

## Running the Tests
To run all tests, run one of the following commands in the root directory of the project:
  - `pytest`
  - `poetry run pytest`

To run just unit or integration tests, run one of the following commands in the root directory of the project:
  - `pytest tests/test_unit`
  - `pytest tests/test_integration`
  - `poetry run pytest tests/test_unit`
  - `poetry run pytest tests/test_integration`

## Requirements

To install the dependencies:
- `poetry install`

## License
MIT
