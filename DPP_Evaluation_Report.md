# DPP PERSONA-BASED HEURISTIC EVALUATION REPORT

**Report Generated:** 2025-12-04 15:39:03

---

## EXECUTIVE SUMMARY

**Overall DPP Score:** 81.5%

### Component Performance

- **Visualization:** 79.2%
- **Ttl:** 82.5%
- **Dataset:** 82.9%

### Persona Satisfaction

- **Owner / Production Manager:** 81.6%
- **Sustainability assessor:** 83.2%
- **Technical Architect:** 83.6%
- **Design architect:** 77.7%

---

## PERSONA: Owner / Production Manager

**Title:** General Manager/ Brand Manager
**Primary Goal:** Strengthen brand credibility and market access through trusted digital documentation.

**Overall Score for this Persona:** 81.6%

### H1: Clarity of Information

#### Visualization
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Clear tabbed navigation (General Info, Lifecycle, Technical Info, etc.)
- ✓ Readable parameter labels and values
- ✓ Units clearly displayed next to values
- ⚠ Some technical terms lack inline definitions (e.g., μ, CTUh)

#### Ttl
**Score:** 80.0% (GOOD)

**Findings:**
- Uses 35 standard namespaces
- ✓ Clear property naming with prefixes (dpp:, schema1:, qudt:)
- ⚠ Some URIs are lengthy and complex

#### Dataset
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Clear parameter naming convention (prefix_category_parameter)
- ✓ Units specified for each parameter
- ✓ Ranges provided for context
- Total parameters: 116

### H2: Information Relevance

#### Visualization
**Score:** 85.7% (EXCELLENT)

**Findings:**
- Visualization covers 6/7 major information categories for Owner / Production Manager

#### Ttl
**Score:** 100.0% (EXCELLENT)

**Findings:**
- 140 unique properties defined
- ✓ Covers technical, environmental, and circularity aspects

#### Dataset
**Score:** 100.0% (EXCELLENT)

**Findings:**
- 50 parameters relevant to Owner / Production Manager
- Organized in 11 categories

### H3: Consistency of Structure and Data

#### Visualization
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Consistent layout across tabs
- ✓ Uniform color coding (blue for sections)
- ✓ Standardized data presentation format

#### Ttl
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Consistent use of owl:equivalentProperty mappings
- ✓ Structured property sets (circularityPropertySet)
- ✓ 13 distinct class types

#### Dataset
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Consistent naming convention across all parameters
- ✓ Standardized data format (tab-separated)
- ✓ 11 logical category groupings

### H4: Accessibility of Key Information

#### Visualization
**Score:** 75.0% (GOOD)

**Findings:**
- ✓ Logical information hierarchy with tabs
- ✓ Key info (ID, manufacturer) prominently displayed
- ⚠ Deep nesting in some sections may hinder quick access
- ⚠ No visible search functionality

#### Ttl
**Score:** 65.0% (FAIR)

**Findings:**
- ✓ Standard RDF/Turtle format
- ⚠ Requires SPARQL knowledge to query effectively
- Total triples: 1444

#### Dataset
**Score:** 75.0% (GOOD)

**Findings:**
- ✓ Simple text format, easily opened in any spreadsheet tool
- ✓ Clear column headers (Parameter, Data, Unit, Range)
- ⚠ Requires manual search to find specific parameters

### H5: Completeness of Material Data

#### Visualization
**Score:** 88.0% (EXCELLENT)

**Findings:**
- ✓ Comprehensive lifecycle data (origin, manufacturing, use, end-of-life)
- ✓ Environmental impact visualization (GWP breakdown chart)
- ✓ Technical properties well-covered
- ⚠ Validation shows 1 missing value (98.8% complete)

#### Ttl
**Score:** 100.0% (EXCELLENT)

**Findings:**
- Data completeness: 100%
- Multiple product instances: 9

#### Dataset
**Score:** 88.8% (EXCELLENT)

**Findings:**
- Completeness: 88.8%
- Filled parameters: 103/116
- Parameters with units: 65
- Parameters with ranges: 89

### H6: Transparency of Data Sources

#### Visualization
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Data source cited: 'Manufacturer EPD'
- ✓ Last updated date shown: 15/5/2024
- ✓ EPD link available in Resources tab
- ⚠ Individual parameter sources not specified

#### Ttl
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Includes prov: namespace for provenance
- ✓ dcterms: for metadata
- ⚠ Data source attribution could be more explicit

#### Dataset
**Score:** 50.0% (FAIR)

**Findings:**
- ⚠ No explicit data source column
- ⚠ No timestamp or version information
- ✓ Ranges provide validation context

### H7: Alignment with Circularity Requirements

#### Visualization
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Dedicated circularity profile visualization (radar chart)
- ✓ End-of-life recommendations clearly stated
- ✓ Disassembly instructions included
- ✓ Secondary use scenarios described

#### Ttl
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Dedicated circularityPropertySet class
- ✓ Multiple circularity instances defined

#### Dataset
**Score:** 100.0% (EXCELLENT)

**Findings:**
- ✓ 15 dedicated circularity parameters
- ✓ Includes disassembly, reusability, recycling metrics

### H8: Compatibility with Digital Workflows

#### Visualization
**Score:** 60.0% (FAIR)

**Findings:**
- ✓ Download options for TTL and IFC files
- ⚠ Downloads marked as 'N/A' in current state
- ⚠ No direct API access visible

#### Ttl
**Score:** 95.0% (EXCELLENT)

**Findings:**
- ✓ Uses widely-adopted ontologies (BOT, BPO, Schema.org)
- ✓ QUDT for units and quantities
- ✓ RDF format enables SPARQL queries
- ✓ Semantic web standards compliance

#### Dataset
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Tab-separated format, easy to import
- ✓ Can be converted to CSV, JSON, or database
- ⚠ Not directly machine-readable (requires parsing)

### H9: User-Centred Orientation

#### Visualization
**Score:** 80.0% (GOOD)

**Findings:**
- Interface alignment with Owner / Production Manager needs: 80%
- ✓ Cost information readily available
- ✓ Summary metrics for client communication

#### Ttl
**Score:** 40.0% (POOR)

**Findings:**
- ⚠ Requires technical expertise to use

#### Dataset
**Score:** 100.0% (EXCELLENT)

**Findings:**
- 27 parameters align with Owner / Production Manager data needs


---

## PERSONA: Sustainability assessor

**Title:** Sustainability and Certification Manager
**Primary Goal:** Ensure environmental transparency and regulatory compliance through structured, verifiable data.

**Overall Score for this Persona:** 83.2%

### H1: Clarity of Information

#### Visualization
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Clear tabbed navigation (General Info, Lifecycle, Technical Info, etc.)
- ✓ Readable parameter labels and values
- ✓ Units clearly displayed next to values
- ⚠ Some technical terms lack inline definitions (e.g., μ, CTUh)

#### Ttl
**Score:** 80.0% (GOOD)

**Findings:**
- Uses 35 standard namespaces
- ✓ Clear property naming with prefixes (dpp:, schema1:, qudt:)
- ⚠ Some URIs are lengthy and complex

#### Dataset
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Clear parameter naming convention (prefix_category_parameter)
- ✓ Units specified for each parameter
- ✓ Ranges provided for context
- Total parameters: 116

### H2: Information Relevance

#### Visualization
**Score:** 85.7% (EXCELLENT)

**Findings:**
- Visualization covers 6/7 major information categories for Sustainability assessor

#### Ttl
**Score:** 100.0% (EXCELLENT)

**Findings:**
- 140 unique properties defined
- ✓ Covers technical, environmental, and circularity aspects

#### Dataset
**Score:** 100.0% (EXCELLENT)

**Findings:**
- 41 parameters relevant to Sustainability assessor
- Organized in 11 categories

### H3: Consistency of Structure and Data

#### Visualization
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Consistent layout across tabs
- ✓ Uniform color coding (blue for sections)
- ✓ Standardized data presentation format

#### Ttl
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Consistent use of owl:equivalentProperty mappings
- ✓ Structured property sets (circularityPropertySet)
- ✓ 13 distinct class types

#### Dataset
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Consistent naming convention across all parameters
- ✓ Standardized data format (tab-separated)
- ✓ 11 logical category groupings

### H4: Accessibility of Key Information

#### Visualization
**Score:** 75.0% (GOOD)

**Findings:**
- ✓ Logical information hierarchy with tabs
- ✓ Key info (ID, manufacturer) prominently displayed
- ⚠ Deep nesting in some sections may hinder quick access
- ⚠ No visible search functionality

#### Ttl
**Score:** 65.0% (FAIR)

**Findings:**
- ✓ Standard RDF/Turtle format
- ⚠ Requires SPARQL knowledge to query effectively
- Total triples: 1444

#### Dataset
**Score:** 75.0% (GOOD)

**Findings:**
- ✓ Simple text format, easily opened in any spreadsheet tool
- ✓ Clear column headers (Parameter, Data, Unit, Range)
- ⚠ Requires manual search to find specific parameters

### H5: Completeness of Material Data

#### Visualization
**Score:** 88.0% (EXCELLENT)

**Findings:**
- ✓ Comprehensive lifecycle data (origin, manufacturing, use, end-of-life)
- ✓ Environmental impact visualization (GWP breakdown chart)
- ✓ Technical properties well-covered
- ⚠ Validation shows 1 missing value (98.8% complete)

#### Ttl
**Score:** 100.0% (EXCELLENT)

**Findings:**
- Data completeness: 100%
- Multiple product instances: 9

#### Dataset
**Score:** 88.8% (EXCELLENT)

**Findings:**
- Completeness: 88.8%
- Filled parameters: 103/116
- Parameters with units: 65
- Parameters with ranges: 89

### H6: Transparency of Data Sources

#### Visualization
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Data source cited: 'Manufacturer EPD'
- ✓ Last updated date shown: 15/5/2024
- ✓ EPD link available in Resources tab
- ⚠ Individual parameter sources not specified

#### Ttl
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Includes prov: namespace for provenance
- ✓ dcterms: for metadata
- ⚠ Data source attribution could be more explicit

#### Dataset
**Score:** 50.0% (FAIR)

**Findings:**
- ⚠ No explicit data source column
- ⚠ No timestamp or version information
- ✓ Ranges provide validation context

### H7: Alignment with Circularity Requirements

#### Visualization
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Dedicated circularity profile visualization (radar chart)
- ✓ End-of-life recommendations clearly stated
- ✓ Disassembly instructions included
- ✓ Secondary use scenarios described

#### Ttl
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Dedicated circularityPropertySet class
- ✓ Multiple circularity instances defined

#### Dataset
**Score:** 100.0% (EXCELLENT)

**Findings:**
- ✓ 15 dedicated circularity parameters
- ✓ Includes disassembly, reusability, recycling metrics

### H8: Compatibility with Digital Workflows

#### Visualization
**Score:** 60.0% (FAIR)

**Findings:**
- ✓ Download options for TTL and IFC files
- ⚠ Downloads marked as 'N/A' in current state
- ⚠ No direct API access visible

#### Ttl
**Score:** 95.0% (EXCELLENT)

**Findings:**
- ✓ Uses widely-adopted ontologies (BOT, BPO, Schema.org)
- ✓ QUDT for units and quantities
- ✓ RDF format enables SPARQL queries
- ✓ Semantic web standards compliance

#### Dataset
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Tab-separated format, easy to import
- ✓ Can be converted to CSV, JSON, or database
- ⚠ Not directly machine-readable (requires parsing)

### H9: User-Centred Orientation

#### Visualization
**Score:** 90.0% (EXCELLENT)

**Findings:**
- Interface alignment with Sustainability assessor needs: 90%

#### Ttl
**Score:** 75.0% (GOOD)

**Findings:**
- ✓ Suitable for BIM integration workflows

#### Dataset
**Score:** 100.0% (EXCELLENT)

**Findings:**
- 27 parameters align with Sustainability assessor data needs


---

## PERSONA: Technical Architect

**Title:** Project Architect
**Primary Goal:** Access accurate, comparable technical and environmental data to support design and procurement decisions.

**Overall Score for this Persona:** 83.6%

### H1: Clarity of Information

#### Visualization
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Clear tabbed navigation (General Info, Lifecycle, Technical Info, etc.)
- ✓ Readable parameter labels and values
- ✓ Units clearly displayed next to values
- ⚠ Some technical terms lack inline definitions (e.g., μ, CTUh)

#### Ttl
**Score:** 80.0% (GOOD)

**Findings:**
- Uses 35 standard namespaces
- ✓ Clear property naming with prefixes (dpp:, schema1:, qudt:)
- ⚠ Some URIs are lengthy and complex

#### Dataset
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Clear parameter naming convention (prefix_category_parameter)
- ✓ Units specified for each parameter
- ✓ Ranges provided for context
- Total parameters: 116

### H2: Information Relevance

#### Visualization
**Score:** 100.0% (EXCELLENT)

**Findings:**
- Visualization covers 7/7 major information categories for Technical Architect

#### Ttl
**Score:** 100.0% (EXCELLENT)

**Findings:**
- 140 unique properties defined
- ✓ Covers technical, environmental, and circularity aspects

#### Dataset
**Score:** 100.0% (EXCELLENT)

**Findings:**
- 50 parameters relevant to Technical Architect
- Organized in 11 categories

### H3: Consistency of Structure and Data

#### Visualization
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Consistent layout across tabs
- ✓ Uniform color coding (blue for sections)
- ✓ Standardized data presentation format

#### Ttl
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Consistent use of owl:equivalentProperty mappings
- ✓ Structured property sets (circularityPropertySet)
- ✓ 13 distinct class types

#### Dataset
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Consistent naming convention across all parameters
- ✓ Standardized data format (tab-separated)
- ✓ 11 logical category groupings

### H4: Accessibility of Key Information

#### Visualization
**Score:** 75.0% (GOOD)

**Findings:**
- ✓ Logical information hierarchy with tabs
- ✓ Key info (ID, manufacturer) prominently displayed
- ⚠ Deep nesting in some sections may hinder quick access
- ⚠ No visible search functionality

#### Ttl
**Score:** 65.0% (FAIR)

**Findings:**
- ✓ Standard RDF/Turtle format
- ⚠ Requires SPARQL knowledge to query effectively
- Total triples: 1444

#### Dataset
**Score:** 75.0% (GOOD)

**Findings:**
- ✓ Simple text format, easily opened in any spreadsheet tool
- ✓ Clear column headers (Parameter, Data, Unit, Range)
- ⚠ Requires manual search to find specific parameters

### H5: Completeness of Material Data

#### Visualization
**Score:** 88.0% (EXCELLENT)

**Findings:**
- ✓ Comprehensive lifecycle data (origin, manufacturing, use, end-of-life)
- ✓ Environmental impact visualization (GWP breakdown chart)
- ✓ Technical properties well-covered
- ⚠ Validation shows 1 missing value (98.8% complete)

#### Ttl
**Score:** 100.0% (EXCELLENT)

**Findings:**
- Data completeness: 100%
- Multiple product instances: 9

#### Dataset
**Score:** 88.8% (EXCELLENT)

**Findings:**
- Completeness: 88.8%
- Filled parameters: 103/116
- Parameters with units: 65
- Parameters with ranges: 89

### H6: Transparency of Data Sources

#### Visualization
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Data source cited: 'Manufacturer EPD'
- ✓ Last updated date shown: 15/5/2024
- ✓ EPD link available in Resources tab
- ⚠ Individual parameter sources not specified

#### Ttl
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Includes prov: namespace for provenance
- ✓ dcterms: for metadata
- ⚠ Data source attribution could be more explicit

#### Dataset
**Score:** 50.0% (FAIR)

**Findings:**
- ⚠ No explicit data source column
- ⚠ No timestamp or version information
- ✓ Ranges provide validation context

### H7: Alignment with Circularity Requirements

#### Visualization
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Dedicated circularity profile visualization (radar chart)
- ✓ End-of-life recommendations clearly stated
- ✓ Disassembly instructions included
- ✓ Secondary use scenarios described

#### Ttl
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Dedicated circularityPropertySet class
- ✓ Multiple circularity instances defined

#### Dataset
**Score:** 100.0% (EXCELLENT)

**Findings:**
- ✓ 15 dedicated circularity parameters
- ✓ Includes disassembly, reusability, recycling metrics

### H8: Compatibility with Digital Workflows

#### Visualization
**Score:** 60.0% (FAIR)

**Findings:**
- ✓ Download options for TTL and IFC files
- ⚠ Downloads marked as 'N/A' in current state
- ⚠ No direct API access visible

#### Ttl
**Score:** 95.0% (EXCELLENT)

**Findings:**
- ✓ Uses widely-adopted ontologies (BOT, BPO, Schema.org)
- ✓ QUDT for units and quantities
- ✓ RDF format enables SPARQL queries
- ✓ Semantic web standards compliance

#### Dataset
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Tab-separated format, easy to import
- ✓ Can be converted to CSV, JSON, or database
- ⚠ Not directly machine-readable (requires parsing)

### H9: User-Centred Orientation

#### Visualization
**Score:** 85.0% (EXCELLENT)

**Findings:**
- Interface alignment with Technical Architect needs: 85%
- ✓ Technical specifications well-organized
- ✓ Environmental data accessible for LCA

#### Ttl
**Score:** 75.0% (GOOD)

**Findings:**
- ✓ Suitable for BIM integration workflows

#### Dataset
**Score:** 100.0% (EXCELLENT)

**Findings:**
- 27 parameters align with Technical Architect data needs


---

## PERSONA: Design architect

**Title:** Design Architect
**Primary Goal:** Understand the sensory, aesthetic, and narrative qualities of materials through accessible information.

**Overall Score for this Persona:** 77.7%

### H1: Clarity of Information

#### Visualization
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Clear tabbed navigation (General Info, Lifecycle, Technical Info, etc.)
- ✓ Readable parameter labels and values
- ✓ Units clearly displayed next to values
- ⚠ Some technical terms lack inline definitions (e.g., μ, CTUh)

#### Ttl
**Score:** 80.0% (GOOD)

**Findings:**
- Uses 35 standard namespaces
- ✓ Clear property naming with prefixes (dpp:, schema1:, qudt:)
- ⚠ Some URIs are lengthy and complex

#### Dataset
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Clear parameter naming convention (prefix_category_parameter)
- ✓ Units specified for each parameter
- ✓ Ranges provided for context
- Total parameters: 116

### H2: Information Relevance

#### Visualization
**Score:** 42.9% (POOR)

**Findings:**
- Visualization covers 3/7 major information categories for Design architect

#### Ttl
**Score:** 100.0% (EXCELLENT)

**Findings:**
- 140 unique properties defined
- ✓ Covers technical, environmental, and circularity aspects

#### Dataset
**Score:** 93.3% (EXCELLENT)

**Findings:**
- 28 parameters relevant to Design architect
- Organized in 11 categories

### H3: Consistency of Structure and Data

#### Visualization
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Consistent layout across tabs
- ✓ Uniform color coding (blue for sections)
- ✓ Standardized data presentation format

#### Ttl
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Consistent use of owl:equivalentProperty mappings
- ✓ Structured property sets (circularityPropertySet)
- ✓ 13 distinct class types

#### Dataset
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Consistent naming convention across all parameters
- ✓ Standardized data format (tab-separated)
- ✓ 11 logical category groupings

### H4: Accessibility of Key Information

#### Visualization
**Score:** 75.0% (GOOD)

**Findings:**
- ✓ Logical information hierarchy with tabs
- ✓ Key info (ID, manufacturer) prominently displayed
- ⚠ Deep nesting in some sections may hinder quick access
- ⚠ No visible search functionality

#### Ttl
**Score:** 65.0% (FAIR)

**Findings:**
- ✓ Standard RDF/Turtle format
- ⚠ Requires SPARQL knowledge to query effectively
- Total triples: 1444

#### Dataset
**Score:** 75.0% (GOOD)

**Findings:**
- ✓ Simple text format, easily opened in any spreadsheet tool
- ✓ Clear column headers (Parameter, Data, Unit, Range)
- ⚠ Requires manual search to find specific parameters

### H5: Completeness of Material Data

#### Visualization
**Score:** 88.0% (EXCELLENT)

**Findings:**
- ✓ Comprehensive lifecycle data (origin, manufacturing, use, end-of-life)
- ✓ Environmental impact visualization (GWP breakdown chart)
- ✓ Technical properties well-covered
- ⚠ Validation shows 1 missing value (98.8% complete)

#### Ttl
**Score:** 100.0% (EXCELLENT)

**Findings:**
- Data completeness: 100%
- Multiple product instances: 9

#### Dataset
**Score:** 88.8% (EXCELLENT)

**Findings:**
- Completeness: 88.8%
- Filled parameters: 103/116
- Parameters with units: 65
- Parameters with ranges: 89

### H6: Transparency of Data Sources

#### Visualization
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Data source cited: 'Manufacturer EPD'
- ✓ Last updated date shown: 15/5/2024
- ✓ EPD link available in Resources tab
- ⚠ Individual parameter sources not specified

#### Ttl
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Includes prov: namespace for provenance
- ✓ dcterms: for metadata
- ⚠ Data source attribution could be more explicit

#### Dataset
**Score:** 50.0% (FAIR)

**Findings:**
- ⚠ No explicit data source column
- ⚠ No timestamp or version information
- ✓ Ranges provide validation context

### H7: Alignment with Circularity Requirements

#### Visualization
**Score:** 85.0% (EXCELLENT)

**Findings:**
- ✓ Dedicated circularity profile visualization (radar chart)
- ✓ End-of-life recommendations clearly stated
- ✓ Disassembly instructions included
- ✓ Secondary use scenarios described

#### Ttl
**Score:** 90.0% (EXCELLENT)

**Findings:**
- ✓ Dedicated circularityPropertySet class
- ✓ Multiple circularity instances defined

#### Dataset
**Score:** 100.0% (EXCELLENT)

**Findings:**
- ✓ 15 dedicated circularity parameters
- ✓ Includes disassembly, reusability, recycling metrics

### H8: Compatibility with Digital Workflows

#### Visualization
**Score:** 60.0% (FAIR)

**Findings:**
- ✓ Download options for TTL and IFC files
- ⚠ Downloads marked as 'N/A' in current state
- ⚠ No direct API access visible

#### Ttl
**Score:** 95.0% (EXCELLENT)

**Findings:**
- ✓ Uses widely-adopted ontologies (BOT, BPO, Schema.org)
- ✓ QUDT for units and quantities
- ✓ RDF format enables SPARQL queries
- ✓ Semantic web standards compliance

#### Dataset
**Score:** 70.0% (GOOD)

**Findings:**
- ✓ Tab-separated format, easy to import
- ✓ Can be converted to CSV, JSON, or database
- ⚠ Not directly machine-readable (requires parsing)

### H9: User-Centred Orientation

#### Visualization
**Score:** 70.0% (GOOD)

**Findings:**
- Interface alignment with Design architect needs: 70%

#### Ttl
**Score:** 40.0% (POOR)

**Findings:**
- ⚠ Requires technical expertise to use

#### Dataset
**Score:** 56.0% (FAIR)

**Findings:**
- 14 parameters align with Design architect data needs


---

## HEURISTIC COMPLIANCE OVERVIEW

### H1: Clarity of Information
**Average Score:** 83.3%
**Description:** Information in the DPP should be understandable without specialist interpretation. Terminology, units, and definitions should be clear and unambiguous.

- Visualization: 85.0%
- Ttl: 80.0%
- Dataset: 85.0%

### H2: Information Relevance
**Average Score:** 92.3%
**Description:** The parameters included should be meaningful for assessing the environmental, technical, and circular performance of hempcrete. Redundant or irrelevant data should be avoided.

- Visualization: 78.6%
- Ttl: 100.0%
- Dataset: 98.3%

### H3: Consistency of Structure and Data
**Average Score:** 88.3%
**Description:** The DPP should maintain a coherent internal structure, with consistent data fields, naming conventions, and categorisation.

- Visualization: 90.0%
- Ttl: 85.0%
- Dataset: 90.0%

### H4: Accessibility of Key Information
**Average Score:** 71.7%
**Description:** Essential information (e.g., composition, performance indicators, sourcing, LCA values) should be easy to locate, without requiring prior system knowledge.

- Visualization: 75.0%
- Ttl: 65.0%
- Dataset: 75.0%

### H5: Completeness of Material Data
**Average Score:** 92.3%
**Description:** The DPP should provide sufficient technical and environmental information to support design, specification, and lifecycle-related decisions.

- Visualization: 88.0%
- Ttl: 100.0%
- Dataset: 88.8%

### H6: Transparency of Data Sources
**Average Score:** 63.3%
**Description:** Each parameter should clearly indicate its origin (manufacturer data, laboratory tests, literature), enabling users to assess data reliability and update needs.

- Visualization: 70.0%
- Ttl: 70.0%
- Dataset: 50.0%

### H7: Alignment with Circularity Requirements
**Average Score:** 91.7%
**Description:** The DPP should support circular workflows by including information on reuse, disassembly, biodegradation, repair options, and end-of-life strategies.

- Visualization: 85.0%
- Ttl: 90.0%
- Dataset: 100.0%

### H8: Compatibility with Digital Workflows
**Average Score:** 75.0%
**Description:** The DPP structure should support interoperability, enabling integration with BIM and other digital systems.

- Visualization: 60.0%
- Ttl: 95.0%
- Dataset: 70.0%

### H9: User-Centred Orientation
**Average Score:** 75.9%
**Description:** The DPP should address the needs of different user profiles (e.g., designer, contractor, LCA analyst), reflecting how each interacts with material data.

- Visualization: 81.2%
- Ttl: 57.5%
- Dataset: 89.0%


---

## RECOMMENDATIONS

### Visualization Improvements

**Priority 1:** H2: Information Relevance (Score: 42.9%)
- Affects: Design architect (Design Architect)
- Issues:

**Priority 2:** H8: Compatibility with Digital Workflows (Score: 60.0%)
- Affects: Owner / Production Manager (General Manager/ Brand Manager)
- Issues:
  - ⚠ Downloads marked as 'N/A' in current state
  - ⚠ No direct API access visible

**Priority 3:** H8: Compatibility with Digital Workflows (Score: 60.0%)
- Affects: Sustainability assessor (Sustainability and Certification Manager)
- Issues:
  - ⚠ Downloads marked as 'N/A' in current state
  - ⚠ No direct API access visible

**Priority 4:** H8: Compatibility with Digital Workflows (Score: 60.0%)
- Affects: Technical Architect (Project Architect)
- Issues:
  - ⚠ Downloads marked as 'N/A' in current state
  - ⚠ No direct API access visible

**Priority 5:** H8: Compatibility with Digital Workflows (Score: 60.0%)
- Affects: Design architect (Design Architect)
- Issues:
  - ⚠ Downloads marked as 'N/A' in current state
  - ⚠ No direct API access visible

### Ttl Improvements

**Priority 6:** H9: User-Centred Orientation (Score: 40.0%)
- Affects: Owner / Production Manager (General Manager/ Brand Manager)
- Issues:
  - ⚠ Requires technical expertise to use

**Priority 7:** H9: User-Centred Orientation (Score: 40.0%)
- Affects: Design architect (Design Architect)
- Issues:
  - ⚠ Requires technical expertise to use

**Priority 8:** H4: Accessibility of Key Information (Score: 65.0%)
- Affects: Owner / Production Manager (General Manager/ Brand Manager)
- Issues:
  - ⚠ Requires SPARQL knowledge to query effectively

**Priority 9:** H4: Accessibility of Key Information (Score: 65.0%)
- Affects: Sustainability assessor (Sustainability and Certification Manager)
- Issues:
  - ⚠ Requires SPARQL knowledge to query effectively

**Priority 10:** H4: Accessibility of Key Information (Score: 65.0%)
- Affects: Technical Architect (Project Architect)
- Issues:
  - ⚠ Requires SPARQL knowledge to query effectively

**Priority 11:** H4: Accessibility of Key Information (Score: 65.0%)
- Affects: Design architect (Design Architect)
- Issues:
  - ⚠ Requires SPARQL knowledge to query effectively

### Dataset Improvements

**Priority 12:** H6: Transparency of Data Sources (Score: 50.0%)
- Affects: Owner / Production Manager (General Manager/ Brand Manager)
- Issues:
  - ⚠ No explicit data source column
  - ⚠ No timestamp or version information

**Priority 13:** H6: Transparency of Data Sources (Score: 50.0%)
- Affects: Sustainability assessor (Sustainability and Certification Manager)
- Issues:
  - ⚠ No explicit data source column
  - ⚠ No timestamp or version information

**Priority 14:** H6: Transparency of Data Sources (Score: 50.0%)
- Affects: Technical Architect (Project Architect)
- Issues:
  - ⚠ No explicit data source column
  - ⚠ No timestamp or version information

**Priority 15:** H6: Transparency of Data Sources (Score: 50.0%)
- Affects: Design architect (Design Architect)
- Issues:
  - ⚠ No explicit data source column
  - ⚠ No timestamp or version information

**Priority 16:** H9: User-Centred Orientation (Score: 56.0%)
- Affects: Design architect (Design Architect)
- Issues:

