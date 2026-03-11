SystemLens :

AI Copilot for Understanding Enterprise Systems and Legacy Code

SystemLens is an experimental AI prototype designed to help engineers, product managers, and technical program managers understand complex enterprise systems faster.

Large enterprise platforms often accumulate significant technical complexity over time. Understanding system behavior, dependencies, and legacy code logic can take days or even weeks for new engineers.

SystemLens explores how AI can accelerate this process by converting technical artifacts into structured, human-readable insights.

Problem :

Enterprise systems—especially in banking, telecom, and large-scale platforms—often suffer from:

• outdated or incomplete documentation
• tightly coupled modules and hidden dependencies
• legacy codebases that are difficult to interpret
• high risk when modifying production-critical workflows

Engineers and product teams frequently spend significant time simply understanding how a system works before making any changes.

Solution :

SystemLens uses AI to analyze technical artifacts and generate structured explanations that help teams quickly build a mental model of the system.

Instead of manually interpreting code or documentation, users can upload artifacts and receive insights such as:

• system/module summaries
• workflow explanations
• dependency insights
• potential change impacts
• onboarding-friendly system explanations

For legacy COBOL programs, SystemLens can also translate program logic into business-readable explanations.

Demo :

<img width="1107" height="661" alt="image" src="https://github.com/user-attachments/assets/a00b19a0-acd5-4251-b7e3-4e6cc9309735" />

Key Features :
Explain Technical Artifacts

Upload architecture notes, documentation, or code snippets and generate structured system explanations.

Dependency Awareness

Identify possible upstream and downstream impacts when modifying a component.

Change Impact Assessment

Highlight areas that may be affected by a system change.

Onboarding Summaries

Generate simplified explanations for engineers who are new to the system.

COBOL Program Breakdown

Translate legacy COBOL code into structured insights including:

• program purpose
• high-level logic flow
• key sections and variables
• inputs and outputs
• business rules
• modernization suggestions

This helps teams understand legacy programs before refactoring or modernization.

Tech Stack :

Python
Streamlit
LLM APIs
PDF / DOCX document parsing libraries

Example Use Cases :

SystemLens can assist teams with:

Legacy system onboarding
Helping engineers understand existing enterprise platforms faster.

Impact analysis before releases
Understanding potential downstream risks before modifying production code.

Legacy modernization initiatives
Breaking down COBOL logic before redesigning workflows in modern architectures.

Cross-functional understanding
Helping TPMs, PMs, and architects understand system behavior without reading large codebases.

Why I Built This :

Having worked with complex enterprise systems, I have seen how difficult it can be to understand legacy platforms—especially when documentation is limited and system behavior is spread across multiple components.

This project explores how AI can help engineers and product teams:

• reduce time spent understanding systems
• surface hidden dependencies
• translate legacy code into understandable logic

The goal is not just automation, but improving how teams reason about complex systems.

Future Experiments :

Ideas I plan to explore next

• multi-file dependency analysis
• automatic architecture diagram generation
• copybook and file structure understanding for COBOL
• cross-artifact system reasoning
• modernization recommendations for legacy modules

Project Status :

⚠️ Prototype — built as an exploration of how AI can assist engineers working with complex enterprise systems.

Repository Structure
app.py              → Streamlit application
requirements.txt    → Dependencies
README.md           → Project documentation

License :
MIT License
