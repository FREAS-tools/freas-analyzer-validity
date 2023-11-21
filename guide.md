# Quick Guide

FREAS is an analysis tool for forensic-ready software systems. The tool allows users to import or model business processes using the BPMN for Forensic-Ready Systems (BPMN4FRSS) notation. On the provided BPMN4FRSS model, users can run different types of analysis to evaluate the extent to which the modeled system complies with forensic readiness requirements. Furthermore, users can assess the system's ability to provide evidence with high evidentiary value in case of an incident. 
As a result, the tool allows users to inspect the possible model insufficiencies and offers hints to remedy the issue. 


## BPMN4FRSS Analysis

Clicking on the "Show validation" displays a right sidebar where the analysis type can be specified and validation executed.
The validation result is shown in the form of a message next to the corresponding elements.

Three types of analysis are available:

* Semantic Rules Analysis
* Semantic Hints Analysis
* Evidence Quality Analysis


**Semantic Rules Analysis**
  * verifies if the provided model is in accordance with BPMN4FRSS semantic rules. If the model violates any of the rules, the tool displayes **Error** messages that indicate the concrete problem and can help users fix the issue.

**Semantic Hints Analysis** 
  * provides recommendations for improving the model. Violating these rules results in **Warnings** but does not affect the model's validity. Nevertheless, compliance with these rules is highly recommended, as their violation can indicate potential weaknesses.

**Evidence Quality Analysis**
  * checks whether the employed forensic-ready controls are sufficient to yield reliable and relevant potential evidence in case of an incident that compromises concrete **Data Store** or a **Flow Object** (Task or Event).
  To simulate an incident, the user must mark a corresponding element from the model as compromised, i.e., select the **id** of the element in the sidebar. \
  In both cases, as a result, analysis marks all Data Store elements that contain potential evidence connected to the incident. Stored potential evidence can hold information to help detect the inconsistency between the data.


## Modeling Guidelines

* Models can be exported as *.bpmn and *.svg files.
* Selecting the individual elements displays the selected element's properties and allows the user to change them.
* To specify potential evidence stored in evidence store, a user must select them in the data store properties in the sidebar.
* To mark a task as integrity or authenticity computation, or data transfer, the task must have at least one input and one output being a potential evidence object.
