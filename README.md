# Digital Product Passport (DPP) Hempcrete Repository

A comprehensive toolkit for converting IFC building models to Linked Building Data (LBD) with Digital Product Passport (DPP) integration, ontology mapping, validation, and dataset comparison capabilities.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Core Tools](#core-tools)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [File Formats](#file-formats)
- [Ontologies Used](#ontologies-used)
- [Troubleshooting](#troubleshooting)
- [Requirements](#requirements)

---

## 🎯 Overview

This repository provides a complete workflow for:

1. **IFC to RDF Conversion**: Convert Industry Foundation Classes (IFC) building models to RDF/Turtle format with BOT (Building Topology Ontology) structure
2. **Excel Export**: Generate parallel Excel spreadsheets with all extracted parameters, values, and units
3. **Ontology Mapping**: Map custom properties to multiple standard ontologies (BOT, DPP, BPO, Schema.org, QUDT, etc.)
4. **SHACL Validation**: Validate data against multi-ontology SHACL shapes
5. **Dataset Comparison**: Compare base DPP datasets with IFC conversion outputs to assess data completeness and quality

---

## 📁 Project Structure

```
DPP_Hempcrete_Repository/
├── IFCtoLBD.py                    # Main IFC to RDF/Excel converter
├── map_to_ontology.py             # Multi-ontology property mapper
├── compare_excel_datasets.py      # Dataset comparison & validation tool
├── NEWValidationtool_DPP.py       # SHACL validation tool
├── Namespace.py                   # Namespace definitions
├── SHACL_MultiOntology.ttl        # Multi-ontology SHACL shapes
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── README_THESIS_WORKFLOW.md      # Detailed workflow documentation
└── Pyrevit Parameters tool/       # Revit parameter management extension
    └── TestTool.extension/
```

---

## 🛠️ Core Tools

### 1. IFCtoLBD.py - IFC to Linked Building Data Converter

**Purpose**: Converts IFC building models to RDF (Turtle format) with BOT structure and generates parallel Excel spreadsheets.

**Key Features**:
- ✅ Interactive file selection dialogs
- ✅ Element type filtering (Sites, Buildings, Storeys, Spaces, Elements, etc.)
- ✅ Dual output: `.ttl` (RDF/Turtle) + `.xlsx` (Excel)
- ✅ Smart unit extraction from parameter names (kgCO₂eq, mm, EUR, etc.)
- ✅ Progress feedback during processing
- ✅ Custom property namespace (`props:`) for IFC parameters

**Input**: 
- IFC file (`.ifc`) - Building Information Model

**Output**:
1. **Turtle file** (`.ttl`): RDF graph with BOT structure
   - Building hierarchy (Building → Storey → Space → Element)
   - Element properties with `props:` namespace
   - GUID tracking with `bot:hasGuid` and `props:hasCompressedGuid`

2. **Excel file** (`.xlsx`): Tabular data with 7 columns
   - Element ID
   - Element Type
   - Element Name
   - Parameter
   - Value
   - Data Type
   - Unit

**Usage**:
```bash
python IFCtoLBD.py
```

**Interactive Steps**:
1. Select input IFC file
2. Choose element types to process (checkbox dialog)
3. Enter output filename
4. Select output directory
5. Wait for processing (progress shown in console)

**Example Output Structure**:

*Turtle (.ttl):*
```turtle
@prefix bot: <https://w3id.org/bot#> .
@prefix props: <https://w3id.org/props#> .

<element_12345> a bot:Element ;
    rdfs:label "Hemp Block Wall" ;
    bot:hasGuid "2O2Fr$t4X7Zf8NOew3FLxx" ;
    props:hasCompressedGuid "2O2Fr$t4X7Zf8NOew3FLxx" ;
    props:Category "Walls" ;
    props:Dpp_Mat_Material "Hemp Concrete" ;
    props:Dpp_Dim_Height_Mm "3000"^^xsd:decimal ;
    props:Dpp_End_Embodiedcarbon_Kgco₂Eq "-25.5"^^xsd:decimal .
```

*Excel (.xlsx):*
| Element ID | Element Type | Element Name | Parameter | Value | Data Type | Unit |
|------------|-------------|--------------|-----------|-------|-----------|------|
| element_12345 | Wall | Hemp Block Wall | Dpp_Mat_Material | Hemp Concrete | string | |
| element_12345 | Wall | Hemp Block Wall | Dpp_Dim_Height_Mm | 3000 | decimal | mm |
| element_12345 | Wall | Hemp Block Wall | Dpp_End_Embodiedcarbon_Kgco₂Eq | -25.5 | decimal | kgCO₂eq |

---

### 2. map_to_ontology.py - Multi-Ontology Property Mapper

**Purpose**: Maps custom `props:` properties to multiple standard ontology vocabularies for maximum interoperability.

**Key Features**:
- ✅ Maps to 10+ ontologies (BOT, DPP, BPO, BMP, Schema.org, QUDT, DCTERMS, PROV, etc.)
- ✅ Creates redundant mappings (one property → multiple ontologies)
- ✅ Generates OWL `equivalentProperty` statements
- ✅ Creates circularity property sets for DPP circularity metrics
- ✅ Preserves building hierarchy and unmapped properties

**Input**: 
- Turtle file from `IFCtoLBD.py` (e.g., `Project1.ttl`)

**Output**:
- Mapped Turtle file (e.g., `Project1_mapped.ttl`)

**Usage**:
```bash
python map_to_ontology.py Project1.ttl Project1_mapped.ttl
```

**Mapping Examples**:

| Original Property | Mapped To |
|------------------|-----------|
| `props:Dpp_Mat_Material` | `dpp:hasMaterial`, `schema:material`, `bpo:consistsOf` |
| `props:Dpp_Dim_Height_Mm` | `qudt:hasHeight`, `schema:height`, `dpp:hasHeight` |
| `props:Dpp_End_Gwp_Kgco₂Eq` | `dpp:hasGlobalWarmingPotential`, `schema:emissionsCO2` |
| `props:Dpp_Cod_Unitcost_Eur` | `dpp:hasUnitCost`, `schema:price` |
| `props:hasCompressedGuid` | `dpp:hasGuid`, `dcterms:identifier` |

**Ontologies Supported**:
- **BOT**: Building Topology Ontology (spatial structure)
- **DPP**: Digital Product Passport ontology
- **BPO**: Building Product Ontology
- **BMP**: Building Material Properties
- **Schema.org**: General-purpose vocabulary
- **QUDT**: Quantities, Units, Dimensions, and Types
- **DCTERMS**: Dublin Core metadata terms
- **PROV**: Provenance ontology
- **OWL**: Web Ontology Language (for equivalences)

**Output Example**:
```turtle
<element_12345> a bot:Element, dpp:product, bpo:Product ;
    rdfs:label "Hemp Block Wall" ;
    dpp:hasMaterial "Hemp Concrete" ;
    schema:material "Hemp Concrete" ;
    bpo:consistsOf "Hemp Concrete" ;
    qudt:hasHeight "3000"^^xsd:decimal ;
    schema:height "3000"^^xsd:decimal ;
    dpp:hasCircularityPropertySet <circularity_12345> .

<circularity_12345> a dpp:circularityPropertySet ;
    dpp:hasRecyclingPotential "High" ;
    dpp:hasReusabilityPotential "Medium" ;
    dpp:hasCircularityIndex "0.85"^^xsd:decimal .
```

---

### 3. compare_excel_datasets.py - Dataset Comparison Tool

**Purpose**: Compares a base DPP dataset with IFC conversion output to assess data completeness, value accuracy, and unit consistency.

**Key Features**:
- ✅ Interactive file selection dialogs
- ✅ Smart parameter name normalization (handles prefixes like "DPP_HempBlock_Material:Typ:")
- ✅ Numeric value comparison with 10% tolerance
- ✅ Intelligent value equivalents (Yes ≈ True, No ≈ False)
- ✅ Unit normalization (treats dashes as "no unit")
- ✅ Reads calculated values from Excel formulas
- ✅ Dual output: Color-coded Excel + PDF reports
- ✅ Completeness percentage calculation
- ✅ Formula injection prevention

**Input**:
1. **Base Dataset** (Excel): DPP template with 4 columns
   - Column A: Parameter
   - Column B: Data (can contain formulas)
   - Column C: Unit (can use — for "no unit")
   - Column D: Range (optional)

2. **Converted Dataset** (Excel): IFC conversion output with 7 columns
   - From `IFCtoLBD.py` output

**Output**:
1. **Excel Report** (`.xlsx`): Color-coded comparison spreadsheet
2. **PDF Report** (`.pdf`): Professional comparison report

**Usage**:
```bash
python compare_excel_datasets.py
```

**Interactive Steps**:
1. Select BASE dataset (DPP template)
2. Select CONVERTED dataset (IFC output)
3. Enter output filename
4. Select output directory
5. Review results in console and reports

**Comparison Logic**:

| Aspect | Method |
|--------|--------|
| **Parameter Matching** | Normalize: remove spaces, underscores, case; extract after last colon |
| **Value Comparison** | Numbers: 10% tolerance; Strings: case-insensitive; Equivalents: Yes↔True, No↔False |
| **Unit Comparison** | Normalize units (mm, kgCO₂eq, etc.); treat —, -, –, ― as empty |
| **Completeness** | (Matched Parameters / Total Parameters) × 100% |

**Report Format**:

*Excel Report Features*:
- 🟦 Blue header row (white text)
- 🟢 Green summary (≥90% completeness) / 🟡 Gold (70-89%) / 🔴 Light salmon (<70%)
- ✅ Green cells for matches, ❌ Light salmon for mismatches
- 📊 8 columns: Parameter, Base Value, Base Unit, Converted Value, Converted Unit, Value Match, Unit Match, Status

*PDF Report Features*:
- Professional header with completeness score
- Color-coded table rows:
  - 🟢 Green: Full match (value + unit)
  - 🟡 Yellow: Partial mismatch
  - 🔴 Red: Missing in converted dataset
- Legend explaining color codes

**Example Console Output**:
```
============================================================
EXCEL DATASET COMPARISON TOOL
============================================================

Step 1: Select the BASE dataset (DPP template format)
✓ Base dataset: DPP_Template.xlsx

Step 2: Select the CONVERTED dataset (IFC conversion output)
✓ Converted dataset: Project1_converted.xlsx

Step 3: Enter output file name
Step 4: Select output folder
✓ Output directory: C:\Reports

============================================================
PROCESSING...
============================================================

[1/5] Loading base dataset...
  ✓ Loaded 45 parameters from base dataset

[2/5] Loading converted dataset...
  ✓ Loaded 38 parameters from converted dataset

[3/5] Comparing datasets...
  ✓ Comparison complete: 84.4% match rate

[4/5] Generating Excel report...
  ✓ Excel report saved

[5/5] Generating PDF report...
  ✓ PDF report saved

============================================================
COMPARISON COMPLETE!
============================================================

Results:
  Total parameters: 45
  Matched: 38
  Completeness: 84.4%

Reports saved:
  Excel: C:\Reports\comparison_report.xlsx
  PDF: C:\Reports\comparison_report.pdf
============================================================
```

**Status Flags**:
- ✅ **Match**: Value and unit both match
- ⚠️ **Value Mismatch**: Unit matches but value differs
- ⚠️ **Unit Mismatch**: Value matches but unit differs
- ⚠️ **Value & Unit Mismatch**: Both differ
- ❌ **Missing in Converted**: Parameter not found in IFC output

---

### 4. NEWValidationtool_DPP.py - SHACL Validation Tool

**Purpose**: Validates RDF data against SHACL (Shapes Constraint Language) shapes to ensure data quality and compliance.

**Input**:
- RDF data file (Turtle format)
- SHACL shapes file (`SHACL_MultiOntology.ttl`)

**Output**:
- Validation report (console)
- Detailed constraint violations

**Usage**:
```bash
python NEWValidationtool_DPP.py
```

---

## 💾 Installation

### Prerequisites
- Python 3.7 or higher
- Windows/Linux/macOS

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/catalinacadena-boop/DPP_Hempcrete_Repostory.git
cd DPP_Hempcrete_Repostory
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

**Dependencies installed**:
- `ifcopenshell >= 0.7.0` - IFC file parsing
- `rdflib >= 6.0.0` - RDF graph manipulation
- `pyshacl >= 0.21.0` - SHACL validation
- `openpyxl >= 3.1.0` - Excel file generation
- `reportlab >= 4.0.0` - PDF report generation

3. **Verify installation**:
```bash
python -c "import ifcopenshell, rdflib, openpyxl, reportlab; print('✓ All dependencies installed')"
```

---

## 📖 Usage Guide

### Complete Workflow Example

**Scenario**: Convert an IFC hempcrete building model to RDF, map to ontologies, and compare with DPP template.

#### Step 1: Convert IFC to RDF + Excel

```bash
python IFCtoLBD.py
```

1. Select: `HempcreteBuilding.ifc`
2. Filter: Check ✅ Buildings, ✅ Elements
3. Name: `HempBuilding_converted`
4. Save to: `C:\Projects\Output`

**Result**: 
- `HempBuilding_converted.ttl` (RDF graph)
- `HempBuilding_converted.xlsx` (Excel spreadsheet)

#### Step 2: Map to Ontologies

```bash
python map_to_ontology.py HempBuilding_converted.ttl HempBuilding_mapped.ttl
```

**Result**: 
- `HempBuilding_mapped.ttl` (multi-ontology RDF)

#### Step 3: Compare with DPP Template

```bash
python compare_excel_datasets.py
```

1. Select BASE: `DPP_HempBlock_Template.xlsx`
2. Select CONVERTED: `HempBuilding_converted.xlsx`
3. Name: `Quality_Assessment`
4. Save to: `C:\Projects\Reports`

**Result**:
- `Quality_Assessment.xlsx` (Excel comparison)
- `Quality_Assessment.pdf` (PDF report)
- Console output showing 84.4% completeness

#### Step 4: Validate with SHACL

```bash
python NEWValidationtool_DPP.py
```

Select: `HempBuilding_mapped.ttl`

**Result**: Validation report showing constraint compliance

---

## 📄 File Formats

### IFC Files (.ifc)
- Industry Foundation Classes
- Standard format for BIM (Building Information Modeling)
- Contains geometry, properties, and relationships

### Turtle Files (.ttl)
- RDF serialization format
- Human-readable triples (Subject-Predicate-Object)
- Used for Linked Data and ontologies

### Excel Files (.xlsx)
- Spreadsheet format for tabular data
- Used for both conversion output and comparison input
- Can contain formulas (calculated values extracted)

### PDF Files (.pdf)
- Portable Document Format
- Professional comparison reports
- Color-coded tables with legends

---

## 🌐 Ontologies Used

| Ontology | Prefix | URI | Purpose |
|----------|--------|-----|---------|
| BOT | `bot:` | https://w3id.org/bot# | Building topology (spaces, elements) |
| DPP | `dpp:` | Custom DPP namespace | Digital Product Passport properties |
| BPO | `bpo:` | https://w3id.org/bpo# | Building products |
| Schema.org | `schema:` | http://schema.org/ | General-purpose vocabulary |
| QUDT | `qudt:` | http://qudt.org/schema/qudt/ | Quantities and units |
| DCTERMS | `dcterms:` | http://purl.org/dc/terms/ | Metadata terms |
| PROV | `prov:` | http://www.w3.org/ns/prov# | Provenance tracking |
| OWL | `owl:` | http://www.w3.org/2002/07/owl# | Ontology relationships |

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: Excel file shows corruption warning
- **Cause**: Formula injection or invalid cell values
- **Solution**: Tool now sanitizes all cell values automatically

**Issue**: Low completeness percentage in comparison
- **Cause**: Parameter name mismatch (prefixes like "Material:Typ:")
- **Solution**: Tool normalizes parameter names (extracts after last colon)

**Issue**: Units don't match (— vs empty)
- **Cause**: Different representations of "no unit"
- **Solution**: Tool treats all dashes (—, -, –, ―) as empty

**Issue**: Values don't match (200 vs 200.0000000000082)
- **Cause**: Floating-point precision differences
- **Solution**: Tool uses 10% tolerance for numeric comparisons

**Issue**: IFC file won't open
- **Cause**: Incompatible IFC version or corrupted file
- **Solution**: Re-export from Revit/ArchiCAD using IFC 2x3 or IFC4

**Issue**: Missing units in Excel output
- **Cause**: Units not detected in parameter names
- **Solution**: Use standardized naming (e.g., `Dpp_Dim_Height_Mm`)

---

## 📋 Requirements

### Python Packages (requirements.txt)

```
ifcopenshell>=0.7.0
rdflib>=6.0.0
pyshacl>=0.21.0
openpyxl>=3.1.0
reportlab>=4.0.0
```

### System Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: 4GB minimum (8GB recommended for large IFC files)
- **Storage**: 500MB for dependencies + space for IFC/output files
- **Python**: 3.7 - 3.11 (tkinter included)

---

## 📝 Parameter Naming Conventions

The tools recognize these parameter patterns:

### Dimension Parameters
- `Dpp_Dim_Height_Mm` → Height in millimeters
- `Dpp_Dim_Length_Mm` → Length in millimeters
- `Dpp_Dim_Width_Mm` → Width in millimeters

### Material Parameters
- `Dpp_Mat_Material` → Material name
- `Dpp_Aut_Materialtype` → Material type/category

### Environmental Parameters
- `Dpp_End_Gwp_Kgco₂Eq` → Global Warming Potential (kg CO₂ equivalent)
- `Dpp_End_Embodiedcarbon_Kgco₂Eq` → Embodied carbon
- `Dpp_End_Biogeniccarbon_Kgco₂Eq` → Biogenic carbon
- `Dpp_End_Penrt_Mjkg` → Primary Energy Non-Renewable (MJ/kg)
- `Dpp_End_Pert_Mjkg` → Primary Energy Renewable (MJ/kg)

### Circularity Parameters
- `Dpp_Cir_Recyclingpotential` → Recycling potential score
- `Dpp_Cir_Reusabilitypotential` → Reusability score
- `Dpp_Cir_Circularityindex` → Overall circularity index
- `Dpp_Cir_Deconstructabilityscore` → Ease of deconstruction

### Safety Parameters
- `Dpp_Sad_Fire_Class` → Fire classification
- `Dpp_Sad_Fireresistance` → Fire resistance rating
- `Dpp_Sad_Toxicity` → Toxicity assessment
- `Dpp_Sad_Compliance` → Regulatory compliance

### Cost Parameters
- `Dpp_Cod_Unitcost_Eur` → Unit cost in EUR
- `Dpp_Cod_Replacement_Eur` → Replacement cost in EUR
- `Dpp_Cod_Circularbenefit_Eur` → Circular economy benefit

### Temporal Parameters
- `Dpp_Tmp_Servicelife_Years` → Service life in years
- `Dpp_Tmp_Warranty` → Warranty period

---

## 🎓 Academic Context

This repository is part of a master's thesis on **Digital Product Passports for Hemp-based Building Materials** at Politecnico di Torino.

**Research Focus**:
- Circular economy in construction
- Hempcrete material characterization
- BIM-to-Linked Data workflows
- Multi-criteria sustainability assessment

---

## 📧 Contact & Support

**Author**: Catalina Cadena  
**Institution**: Politecnico di Torino
**Repository**: https://github.com/catalinacadena-boop/DPP_Hempcrete_Repostory

For issues or questions, please open an issue on GitHub.

---

## 📜 License

This project is part of academic research. Please cite appropriately if used in academic work.

---

## 🔄 Version History

- **v3.4** (Current): Added comparison tool with color-coded reports, formula value extraction, parameter normalization
- **v3.3**: Added Excel export functionality to IFC converter
- **v3.2**: Improved unit extraction with regex patterns
- **v3.1**: Added interactive element filtering
- **v3.0**: Multi-ontology mapping implementation
- **v2.0**: SHACL validation integration
- **v1.0**: Initial IFC to RDF converter

---

## 🚀 Future Enhancements

- [ ] Web-based interface for comparison tool
- [ ] Automated report generation pipeline
- [ ] Support for multiple IFC files batch processing
- [ ] Database integration for historical comparisons
- [ ] Machine learning for parameter matching suggestions
- [ ] 3D visualization of validated elements

---

*Last Updated: November 13, 2025*
