# DPP Persona-Based Heuristic Evaluation - User Guide

## Overview

This automated evaluation tool assesses your Digital Product Passport (DPP) across three components:
- **Visualization** (web interface UI/UX)
- **TTL files** (semantic data structure)
- **Dataset** (data quality and organization)

The evaluation is performed from the perspective of 4 personas against 9 heuristics, generating **automated scores**, **detailed findings**, and **actionable recommendations**.

---

## Generated Files

After running the evaluation, you'll find these files in your Documents folder:

### 1. **DPP_Evaluation_Report.md**
Complete evaluation report including:
- Executive summary with overall scores
- Detailed results for each persona
- Component-by-component analysis
- Heuristic compliance overview
- Prioritized recommendations

### 2. **DPP_Evaluation_Summary.json**
Machine-readable JSON file with:
- All scores (overall, by component, by persona, by heuristic)
- Detailed findings for programmatic access
- Can be imported into dashboards or other tools

### 3. **Persona Checklists** (4 files)
Individual evaluation checklists for:
- `Checklist_Owner___Production_Manager.md`
- `Checklist_Sustainability_assessor.md`
- `Checklist_Technical_Architect.md`
- `Checklist_Design_architect.md`

Each checklist contains:
- Specific evaluation questions tailored to that persona
- Checkboxes for manual verification
- Space for notes and observations

---

## How to Run the Evaluation

### First Time Setup
```powershell
# Already done! The tool is installed and ready
```

### Run Evaluation
```powershell
cd C:\Users\Catalina\Documents
& "C:/Users/Catalina/OneDrive - Pontificia Universidad Javeriana/Desktop/THESIS/Methodology/DPP_Hempcrete_Repostory/.venv/Scripts/python.exe" dpp_evaluator.py
```

---

## Understanding the Scores

### Score Ranges
- **85-100%** = Excellent ✓✓
- **70-84%** = Good ✓
- **50-69%** = Fair ⚠
- **0-49%** = Poor ✗

### Current Results Summary

**Overall DPP Score: 81.5%** (Good)

#### By Component:
- Visualization: 79.2% (Good)
- TTL: 82.5% (Good)
- Dataset: 82.9% (Good)

#### By Persona:
- Owner/Production Manager: 81.6%
- Sustainability Assessor: 83.2%
- Technical Architect: 83.6%
- Design Architect: 77.7%

---

## Customizing the Evaluation

### Modify Personas
Edit: `C:\Users\Catalina\Documents\Personas.txt`

Add new personas or modify existing ones. The tool will automatically detect changes.

### Modify Heuristics
Edit: `C:\Users\Catalina\Documents\Heuristics.txt`

Adjust heuristic definitions. Keep the markdown table format.

### Update Data Sources
The tool reads from:
- TTL files: `DPP_HempBlock_Element_mapped.ttl` and `DPP_HempBlock_Material_mapped.ttl`
- Dataset: `Dataset.txt`
- Visualization: Based on screenshot analysis (update `_evaluate_visualization()` method for new screenshots)

---

## Advanced Usage

### Generate Reports Programmatically

```python
from dpp_evaluator import (
    PersonaParser, HeuristicParser, TTLAnalyzer, 
    DatasetAnalyzer, HeuristicEvaluator, ReportGenerator
)

# Load your data
personas = PersonaParser.parse_personas("Personas.txt")
heuristics = HeuristicParser.parse_heuristics("Heuristics.txt")
ttl_analyzer = TTLAnalyzer(["file1.ttl", "file2.ttl"])
dataset_analyzer = DatasetAnalyzer("Dataset.txt")

# Run evaluation
evaluator = HeuristicEvaluator(personas, heuristics, ttl_analyzer, dataset_analyzer)
evaluator.evaluate_all()

# Generate specific reports
report_gen = ReportGenerator(evaluator)
report_gen.generate_full_report("custom_report.md")

# Query results
for persona in personas:
    score = evaluator.get_average_score(persona=persona)
    print(f"{persona.role}: {score*100:.1f}%")
```

### Filter Results

```python
# Get results for specific persona
owner_results = evaluator.get_results_by_persona(personas[0])

# Get results for specific component
viz_results = evaluator.get_results_by_component("visualization")

# Calculate custom scores
ttl_score = evaluator.get_average_score(component="ttl")
```

---

## Evaluation Methodology

### Automated Scoring

The tool uses rule-based heuristics to automatically score each component:

1. **Visualization** (UI/UX analysis)
   - Based on screenshot analysis
   - Evaluates navigation, clarity, data presentation
   - Checks persona-specific needs coverage

2. **TTL Files** (Semantic structure)
   - Analyzes RDF graph structure
   - Counts properties, classes, namespaces
   - Checks for required ontologies
   - Validates completeness

3. **Dataset** (Data quality)
   - Calculates completeness rate
   - Validates units and ranges
   - Checks parameter organization
   - Assesses relevance to personas

### Heuristics Applied

1. **Clarity of Information** - Understandability without specialist knowledge
2. **Information Relevance** - Meaningful parameters, no redundancy
3. **Consistency** - Coherent structure and naming
4. **Accessibility** - Easy to locate essential information
5. **Completeness** - Sufficient technical and environmental data
6. **Transparency** - Clear data sources and provenance
7. **Circularity Alignment** - Support for circular workflows
8. **Digital Compatibility** - Interoperability with BIM/LCA tools
9. **User-Centered Design** - Tailored to different user profiles

---

## Interpreting the Reports

### Main Report Structure

```
EXECUTIVE SUMMARY
├── Overall Score
├── Component Scores
└── Persona Satisfaction

PERSONA SECTIONS (4x)
├── Persona Profile
├── Overall Score for Persona
└── For Each Heuristic (9x)
    ├── Visualization Score & Findings
    ├── TTL Score & Findings
    └── Dataset Score & Findings

HEURISTIC COMPLIANCE OVERVIEW
├── Average Score per Heuristic
└── Breakdown by Component

RECOMMENDATIONS
├── Priority 1: Lowest scoring areas
├── Priority 2: Medium improvements
└── Priority 3: Minor enhancements
```

### Checklist Usage

Use persona checklists for:
- **Manual verification** of automated scores
- **User testing** with real stakeholders
- **Iterative improvements** tracking
- **Documentation** of design decisions

---

## Key Findings from Current Evaluation

### Strengths ✓
- Strong technical data completeness (82.9%)
- Excellent semantic structure in TTL files (82.5%)
- Good circularity information coverage
- Comprehensive environmental impact data
- Well-organized lifecycle information

### Areas for Improvement ⚠

#### Visualization (79.2%)
- Add inline definitions for technical terms
- Implement search functionality
- Enable TTL/IFC file downloads (currently N/A)
- Improve deep navigation paths

#### TTL Files (82.5%)
- Add more explicit data source attribution
- Include examples/documentation
- Simplify URIs where possible

#### Dataset (82.9%)
- Add data source column
- Include timestamp/version information
- Reduce NA values

### Recommendations by Priority

**Priority 1:** Digital Workflow Compatibility (60% score)
- Enable TTL and IFC file downloads
- Provide API access documentation
- Add export functionality

**Priority 2:** Data Source Transparency (50-70% scores)
- Add source attribution to dataset
- Document update history
- Link to test reports

**Priority 3:** Accessibility Enhancements (75% score)
- Add search functionality to visualization
- Provide glossary for technical terms
- Simplify navigation depth

---

## FAQ

### Q: How often should I run the evaluation?
**A:** Run after any major data updates, when adding new features, or before stakeholder reviews.

### Q: Can I add more personas?
**A:** Yes! Edit `Personas.txt` following the existing format. The tool will automatically include them.

### Q: How do I update the visualization scores?
**A:** Take new screenshots and update the `_evaluate_visualization()` method in `dpp_evaluator.py` with observations from the new interface.

### Q: Can I export results to Excel?
**A:** Use the JSON file (`DPP_Evaluation_Summary.json`) and import it to Excel, or modify the `ReportGenerator` class to add CSV/Excel export.

### Q: What if I want different scoring weights?
**A:** Modify the scoring logic in the `_evaluate_*()` methods within the `HeuristicEvaluator` class.

---

## Technical Details

### Requirements
- Python 3.12+
- rdflib (for TTL parsing)

### File Structure
```
C:\Users\Catalina\Documents\
├── dpp_evaluator.py          # Main tool
├── Personas.txt               # Input: persona definitions
├── Heuristics.txt             # Input: evaluation criteria
├── Dataset.txt                # Input: DPP data
├── DPP_Evaluation_Report.md   # Output: main report
├── DPP_Evaluation_Summary.json # Output: JSON data
└── Checklist_*.md             # Output: persona checklists (4x)
```

### Classes Overview
- **PersonaParser** - Parses persona definitions
- **HeuristicParser** - Parses heuristic criteria
- **TTLAnalyzer** - Analyzes RDF/Turtle files
- **DatasetAnalyzer** - Analyzes dataset quality
- **HeuristicEvaluator** - Main evaluation engine
- **ReportGenerator** - Creates reports and checklists
- **EvaluationResult** - Stores individual results

---

## Next Steps

1. ✓ Review `DPP_Evaluation_Report.md` for comprehensive findings
2. ✓ Check persona-specific checklists for detailed questions
3. ✓ Prioritize improvements based on recommendations
4. ⚡ Conduct user testing with checklists
5. ⚡ Re-run evaluation after implementing changes
6. ⚡ Track progress over time using JSON summaries

---

## Support

For issues or customization requests, review the code in `dpp_evaluator.py`. The code is well-documented with docstrings explaining each function.

---

**Generated by:** DPP Heuristic Evaluation Tool v1.0
**Last Updated:** December 4, 2025
