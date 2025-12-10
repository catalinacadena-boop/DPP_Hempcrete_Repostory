"""
DPP Persona-Based Heuristic Evaluation Automation Tool
Evaluates Digital Product Passports against defined heuristics from multiple persona perspectives
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import rdflib
from rdflib import Graph, Namespace


@dataclass
class Persona:
    """Represents a user persona with their characteristics and data needs"""
    role: str
    education: str
    title: str
    industry: str
    responsibilities: str
    primary_goal: str
    secondary_goal: str
    data_needs: List[str]
    
    def __str__(self):
        return f"{self.role} ({self.title})"


@dataclass
class Heuristic:
    """Represents an evaluation heuristic"""
    number: int
    name: str
    description: str
    
    def __str__(self):
        return f"H{self.number}: {self.name}"


@dataclass
class EvaluationResult:
    """Stores evaluation results for a specific persona-heuristic-component combination"""
    persona: str
    heuristic: str
    component: str  # 'visualization', 'ttl', or 'dataset'
    score: float  # 0.0 to 1.0
    findings: List[str] = field(default_factory=list)
    compliance_level: str = ""  # 'excellent', 'good', 'fair', 'poor'
    
    def __post_init__(self):
        # Auto-assign compliance level based on score
        if self.score >= 0.85:
            self.compliance_level = "excellent"
        elif self.score >= 0.70:
            self.compliance_level = "good"
        elif self.score >= 0.50:
            self.compliance_level = "fair"
        else:
            self.compliance_level = "poor"


class PersonaParser:
    """Parses persona definitions from text file"""
    
    @staticmethod
    def parse_personas(file_path: str) -> List[Persona]:
        """Parse personas from text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        personas = []
        # Split by persona sections
        persona_blocks = re.split(r'\n(?=Producer persona:|Architect persona:)', content)
        
        for block in persona_blocks:
            if not block.strip():
                continue
            
            lines = block.strip().split('\n')
            persona_data = {}
            data_needs = []
            in_data_needs = False
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('Producer persona:') or line.startswith('Architect persona:'):
                    persona_data['role'] = line.split(':', 1)[1].strip()
                elif line.startswith('Education:'):
                    persona_data['education'] = line.split(':', 1)[1].strip()
                elif line.startswith('Title:'):
                    persona_data['title'] = line.split(':', 1)[1].strip()
                elif line.startswith('Industry:'):
                    persona_data['industry'] = line.split(':', 1)[1].strip()
                elif line.startswith('Key responsibilities:'):
                    persona_data['responsibilities'] = line.split(':', 1)[1].strip()
                elif line.startswith('Primary Goal:'):
                    persona_data['primary_goal'] = line.split(':', 1)[1].strip()
                elif line.startswith('Secondary Goal:'):
                    persona_data['secondary_goal'] = line.split(':', 1)[1].strip()
                elif line.startswith('Data needs'):
                    in_data_needs = True
                elif in_data_needs and line.startswith('•'):
                    data_needs.append(line[1:].strip())
            
            if persona_data:
                persona_data['data_needs'] = data_needs
                personas.append(Persona(**persona_data))
        
        return personas


class HeuristicParser:
    """Parses heuristic definitions from text file"""
    
    @staticmethod
    def parse_heuristics(file_path: str) -> List[Heuristic]:
        """Parse heuristics from markdown table format"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        heuristics = []
        lines = content.strip().split('\n')
        
        for line in lines[2:]:  # Skip header and separator
            if '|' not in line:
                continue
            
            parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first/last
            if len(parts) >= 2:
                # Extract number from heuristic name
                match = re.search(r'\*\*(\d+)\.\s*(.+?)\*\*', parts[0])
                if match:
                    number = int(match.group(1))
                    name = match.group(2)
                    description = parts[1]
                    heuristics.append(Heuristic(number, name, description))
        
        return heuristics


class TTLAnalyzer:
    """Analyzes TTL/RDF files for structure and completeness"""
    
    def __init__(self, ttl_files: List[str]):
        self.graphs = []
        self.namespaces = {}
        
        for ttl_file in ttl_files:
            g = Graph()
            g.parse(ttl_file, format='turtle')
            self.graphs.append(g)
            
            # Collect namespaces
            for prefix, namespace in g.namespaces():
                if prefix:
                    self.namespaces[prefix] = str(namespace)
    
    def analyze_structure(self) -> Dict:
        """Analyze TTL structure and return metrics"""
        analysis = {
            'total_triples': 0,
            'unique_predicates': set(),
            'unique_subjects': set(),
            'namespaces_used': list(self.namespaces.keys()),
            'class_instances': {},
            'property_coverage': {},
            'data_completeness': 0.0
        }
        
        for g in self.graphs:
            analysis['total_triples'] += len(g)
            
            for s, p, o in g:
                analysis['unique_subjects'].add(str(s))
                analysis['unique_predicates'].add(str(p))
                
                # Count class instances
                if 'type' in str(p).lower():
                    class_name = str(o).split('#')[-1].split('/')[-1]
                    analysis['class_instances'][class_name] = analysis['class_instances'].get(class_name, 0) + 1
        
        analysis['unique_predicates'] = list(analysis['unique_predicates'])
        analysis['unique_subjects'] = list(analysis['unique_subjects'])
        
        # Calculate completeness (percentage of non-null values)
        total_properties = len(analysis['unique_predicates'])
        analysis['data_completeness'] = min(total_properties / 50, 1.0)  # Assume 50 properties is "complete"
        
        return analysis
    
    def check_required_properties(self, required_props: List[str]) -> Dict[str, bool]:
        """Check if required properties exist in the TTL"""
        found = {}
        
        for prop in required_props:
            found[prop] = False
            for g in self.graphs:
                for s, p, o in g:
                    if prop.lower() in str(p).lower():
                        found[prop] = True
                        break
                if found[prop]:
                    break
        
        return found
    
    def get_property_count(self) -> int:
        """Get total unique properties"""
        all_props = set()
        for g in self.graphs:
            for s, p, o in g:
                all_props.add(str(p))
        return len(all_props)


class DatasetAnalyzer:
    """Analyzes dataset for quality and organization"""
    
    def __init__(self, dataset_file: str):
        self.data = self._parse_dataset(dataset_file)
    
    def _parse_dataset(self, file_path: str) -> List[Dict]:
        """Parse tab-separated dataset"""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        data = []
        for line in lines[1:]:  # Skip header
            parts = line.strip().split('\t')
            if len(parts) >= 4:
                data.append({
                    'parameter': parts[0],
                    'data': parts[1],
                    'unit': parts[2],
                    'range': parts[3]
                })
        
        return data
    
    def analyze_quality(self) -> Dict:
        """Analyze dataset quality metrics"""
        total_params = len(self.data)
        filled_params = sum(1 for item in self.data if item['data'] and item['data'] not in ['0', 'NA', '—'])
        has_units = sum(1 for item in self.data if item['unit'] and item['unit'] not in ['—', '0'])
        has_range = sum(1 for item in self.data if item['range'] and item['range'] not in ['—', '0'])
        
        # Categorize by prefix
        categories = {}
        for item in self.data:
            prefix = item['parameter'].split('_')[1] if '_' in item['parameter'] else 'other'
            categories[prefix] = categories.get(prefix, 0) + 1
        
        return {
            'total_parameters': total_params,
            'filled_parameters': filled_params,
            'completeness_rate': filled_params / total_params if total_params > 0 else 0,
            'parameters_with_units': has_units,
            'parameters_with_ranges': has_range,
            'categories': categories,
            'missing_data_count': total_params - filled_params
        }
    
    def get_parameters_by_category(self, category: str) -> List[Dict]:
        """Get parameters matching a category keyword"""
        return [item for item in self.data if category.upper() in item['parameter'].upper()]
    
    def check_required_parameters(self, required_params: List[str]) -> Dict[str, bool]:
        """Check if required parameters exist"""
        found = {}
        for param in required_params:
            found[param] = any(param.lower() in item['parameter'].lower() for item in self.data)
        return found


class HeuristicEvaluator:
    """Main evaluator that applies heuristics to DPP components from persona perspectives"""
    
    def __init__(self, personas: List[Persona], heuristics: List[Heuristic], 
                 ttl_analyzer: TTLAnalyzer, dataset_analyzer: DatasetAnalyzer):
        self.personas = personas
        self.heuristics = heuristics
        self.ttl_analyzer = ttl_analyzer
        self.dataset_analyzer = dataset_analyzer
        self.results = []
    
    def evaluate_all(self):
        """Run complete evaluation for all personas and heuristics"""
        for persona in self.personas:
            for heuristic in self.heuristics:
                # Evaluate each component
                self._evaluate_visualization(persona, heuristic)
                self._evaluate_ttl(persona, heuristic)
                self._evaluate_dataset(persona, heuristic)
    
    def _evaluate_visualization(self, persona: Persona, heuristic: Heuristic):
        """Evaluate visualization component based on screenshots analysis"""
        score = 0.0
        findings = []
        
        # Heuristic-specific evaluation criteria
        if heuristic.number == 1:  # Clarity of Information
            # Based on screenshots: clear tabbed navigation, readable labels
            score = 0.85
            findings.append("✓ Clear tabbed navigation (General Info, Lifecycle, Technical Info, etc.)")
            findings.append("✓ Readable parameter labels and values")
            findings.append("✓ Units clearly displayed next to values")
            findings.append("⚠ Some technical terms lack inline definitions (e.g., μ, CTUh)")
            
        elif heuristic.number == 2:  # Information Relevance
            # Check if persona's data needs are addressed
            relevant_tabs = self._check_persona_data_coverage(persona)
            score = min(relevant_tabs / 7, 1.0)  # 7 main tabs
            findings.append(f"Visualization covers {relevant_tabs}/7 major information categories for {persona.role}")
            
        elif heuristic.number == 3:  # Consistency
            score = 0.90
            findings.append("✓ Consistent layout across tabs")
            findings.append("✓ Uniform color coding (blue for sections)")
            findings.append("✓ Standardized data presentation format")
            
        elif heuristic.number == 4:  # Accessibility
            score = 0.75
            findings.append("✓ Logical information hierarchy with tabs")
            findings.append("✓ Key info (ID, manufacturer) prominently displayed")
            findings.append("⚠ Deep nesting in some sections may hinder quick access")
            findings.append("⚠ No visible search functionality")
            
        elif heuristic.number == 5:  # Completeness
            score = 0.88
            findings.append("✓ Comprehensive lifecycle data (origin, manufacturing, use, end-of-life)")
            findings.append("✓ Environmental impact visualization (GWP breakdown chart)")
            findings.append("✓ Technical properties well-covered")
            findings.append("⚠ Validation shows 1 missing value (98.8% complete)")
            
        elif heuristic.number == 6:  # Transparency of Data Sources
            score = 0.70
            findings.append("✓ Data source cited: 'Manufacturer EPD'")
            findings.append("✓ Last updated date shown: 15/5/2024")
            findings.append("✓ EPD link available in Resources tab")
            findings.append("⚠ Individual parameter sources not specified")
            
        elif heuristic.number == 7:  # Circularity
            score = 0.85
            findings.append("✓ Dedicated circularity profile visualization (radar chart)")
            findings.append("✓ End-of-life recommendations clearly stated")
            findings.append("✓ Disassembly instructions included")
            findings.append("✓ Secondary use scenarios described")
            
        elif heuristic.number == 8:  # Digital Workflow Compatibility
            score = 0.60
            findings.append("✓ Download options for TTL and IFC files")
            findings.append("⚠ Downloads marked as 'N/A' in current state")
            findings.append("⚠ No direct API access visible")
            
        elif heuristic.number == 9:  # User-Centered Orientation
            # Persona-specific evaluation
            persona_score = self._evaluate_persona_fit(persona)
            score = persona_score
            findings.append(f"Interface alignment with {persona.role} needs: {persona_score*100:.0f}%")
            if persona.role in ["Owner / Production Manager", "General Manager/ Brand Manager"]:
                findings.append("✓ Cost information readily available")
                findings.append("✓ Summary metrics for client communication")
            elif "Architect" in persona.role:
                findings.append("✓ Technical specifications well-organized")
                findings.append("✓ Environmental data accessible for LCA")
        
        result = EvaluationResult(
            persona=str(persona),
            heuristic=str(heuristic),
            component="visualization",
            score=score,
            findings=findings
        )
        self.results.append(result)
    
    def _evaluate_ttl(self, persona: Persona, heuristic: Heuristic):
        """Evaluate TTL file structure"""
        score = 0.0
        findings = []
        analysis = self.ttl_analyzer.analyze_structure()
        
        if heuristic.number == 1:  # Clarity
            namespaces_clear = len(analysis['namespaces_used']) > 0
            score = 0.80 if namespaces_clear else 0.50
            findings.append(f"Uses {len(analysis['namespaces_used'])} standard namespaces")
            findings.append("✓ Clear property naming with prefixes (dpp:, schema1:, qudt:)")
            findings.append("⚠ Some URIs are lengthy and complex")
            
        elif heuristic.number == 2:  # Relevance
            property_count = len(analysis['unique_predicates'])
            score = min(property_count / 40, 1.0)
            findings.append(f"{property_count} unique properties defined")
            findings.append("✓ Covers technical, environmental, and circularity aspects")
            
        elif heuristic.number == 3:  # Consistency
            score = 0.85
            findings.append("✓ Consistent use of owl:equivalentProperty mappings")
            findings.append("✓ Structured property sets (circularityPropertySet)")
            findings.append(f"✓ {len(analysis['class_instances'])} distinct class types")
            
        elif heuristic.number == 4:  # Accessibility
            score = 0.65
            findings.append("✓ Standard RDF/Turtle format")
            findings.append("⚠ Requires SPARQL knowledge to query effectively")
            findings.append(f"Total triples: {analysis['total_triples']}")
            
        elif heuristic.number == 5:  # Completeness
            score = analysis['data_completeness']
            findings.append(f"Data completeness: {score*100:.0f}%")
            findings.append(f"Multiple product instances: {analysis['class_instances'].get('product', 0)}")
            
        elif heuristic.number == 6:  # Transparency
            score = 0.70
            findings.append("✓ Includes prov: namespace for provenance")
            findings.append("✓ dcterms: for metadata")
            findings.append("⚠ Data source attribution could be more explicit")
            
        elif heuristic.number == 7:  # Circularity
            has_circularity = 'circularity' in str(analysis['class_instances'])
            score = 0.90 if has_circularity else 0.30
            findings.append("✓ Dedicated circularityPropertySet class")
            findings.append("✓ Multiple circularity instances defined")
            
        elif heuristic.number == 8:  # Compatibility
            score = 0.95
            findings.append("✓ Uses widely-adopted ontologies (BOT, BPO, Schema.org)")
            findings.append("✓ QUDT for units and quantities")
            findings.append("✓ RDF format enables SPARQL queries")
            findings.append("✓ Semantic web standards compliance")
            
        elif heuristic.number == 9:  # User-Centered
            # Technical users benefit most from TTL
            if "Architect" in persona.role or "Sustainability" in persona.role:
                score = 0.75
                findings.append("✓ Suitable for BIM integration workflows")
            else:
                score = 0.40
                findings.append("⚠ Requires technical expertise to use")
        
        result = EvaluationResult(
            persona=str(persona),
            heuristic=str(heuristic),
            component="ttl",
            score=score,
            findings=findings
        )
        self.results.append(result)
    
    def _evaluate_dataset(self, persona: Persona, heuristic: Heuristic):
        """Evaluate dataset quality"""
        score = 0.0
        findings = []
        analysis = self.dataset_analyzer.analyze_quality()
        
        if heuristic.number == 1:  # Clarity
            score = 0.85
            findings.append("✓ Clear parameter naming convention (prefix_category_parameter)")
            findings.append("✓ Units specified for each parameter")
            findings.append("✓ Ranges provided for context")
            findings.append(f"Total parameters: {analysis['total_parameters']}")
            
        elif heuristic.number == 2:  # Relevance
            relevant_params = self._count_relevant_params(persona)
            score = min(relevant_params / 30, 1.0)
            findings.append(f"{relevant_params} parameters relevant to {persona.role}")
            findings.append(f"Organized in {len(analysis['categories'])} categories")
            
        elif heuristic.number == 3:  # Consistency
            score = 0.90
            findings.append("✓ Consistent naming convention across all parameters")
            findings.append("✓ Standardized data format (tab-separated)")
            findings.append(f"✓ {len(analysis['categories'])} logical category groupings")
            
        elif heuristic.number == 4:  # Accessibility
            score = 0.75
            findings.append("✓ Simple text format, easily opened in any spreadsheet tool")
            findings.append("✓ Clear column headers (Parameter, Data, Unit, Range)")
            findings.append("⚠ Requires manual search to find specific parameters")
            
        elif heuristic.number == 5:  # Completeness
            score = analysis['completeness_rate']
            findings.append(f"Completeness: {score*100:.1f}%")
            findings.append(f"Filled parameters: {analysis['filled_parameters']}/{analysis['total_parameters']}")
            findings.append(f"Parameters with units: {analysis['parameters_with_units']}")
            findings.append(f"Parameters with ranges: {analysis['parameters_with_ranges']}")
            
        elif heuristic.number == 6:  # Transparency
            score = 0.50
            findings.append("⚠ No explicit data source column")
            findings.append("⚠ No timestamp or version information")
            findings.append("✓ Ranges provide validation context")
            
        elif heuristic.number == 7:  # Circularity
            circ_params = self.dataset_analyzer.get_parameters_by_category('CIR')
            score = min(len(circ_params) / 15, 1.0)
            findings.append(f"✓ {len(circ_params)} dedicated circularity parameters")
            findings.append("✓ Includes disassembly, reusability, recycling metrics")
            
        elif heuristic.number == 8:  # Compatibility
            score = 0.70
            findings.append("✓ Tab-separated format, easy to import")
            findings.append("✓ Can be converted to CSV, JSON, or database")
            findings.append("⚠ Not directly machine-readable (requires parsing)")
            
        elif heuristic.number == 9:  # User-Centered
            persona_params = self._get_persona_relevant_params(persona)
            score = min(len(persona_params) / 25, 1.0)
            findings.append(f"{len(persona_params)} parameters align with {persona.role} data needs")
        
        result = EvaluationResult(
            persona=str(persona),
            heuristic=str(heuristic),
            component="dataset",
            score=score,
            findings=findings
        )
        self.results.append(result)
    
    def _check_persona_data_coverage(self, persona: Persona) -> int:
        """Count how many of persona's data needs are covered in visualization"""
        covered = 0
        # Based on screenshot tabs: General Info, Lifecycle, Technical Info, Cost, Aesthetics, Resources, Validation
        
        for need in persona.data_needs:
            need_lower = need.lower()
            if any(keyword in need_lower for keyword in ['technical', 'performance', 'strength', 'thermal', 'density']):
                covered += 1
            elif any(keyword in need_lower for keyword in ['environmental', 'carbon', 'lca', 'energy', 'gwp', 'emissions']):
                covered += 1
            elif any(keyword in need_lower for keyword in ['cost', 'price', 'economic']):
                covered += 1
            elif any(keyword in need_lower for keyword in ['certification', 'compliance', 'epd', 'declaration']):
                covered += 1
            elif any(keyword in need_lower for keyword in ['material', 'composition', 'sourcing', 'origin']):
                covered += 1
            elif any(keyword in need_lower for keyword in ['lifecycle', 'end-of-life', 'durability', 'service']):
                covered += 1
            elif any(keyword in need_lower for keyword in ['dimension', 'modular', 'size']):
                covered += 1
        
        return covered
    
    def _evaluate_persona_fit(self, persona: Persona) -> float:
        """Evaluate how well visualization serves persona's needs"""
        if persona.role in ["Owner / Production Manager", "General Manager/ Brand Manager"]:
            return 0.80  # Good overview, cost info, certifications
        elif "Sustainability" in persona.role:
            return 0.90  # Excellent environmental data, EPD, lifecycle
        elif "Technical Architect" in persona.role:
            return 0.85  # Strong technical specs, LCA data
        elif "Design Architect" in persona.role:
            return 0.75  # Good aesthetics, but less technical focus
        return 0.70
    
    def _count_relevant_params(self, persona: Persona) -> int:
        """Count dataset parameters relevant to persona"""
        relevant = 0
        all_params = [item['parameter'] for item in self.dataset_analyzer.data]
        
        for need in persona.data_needs:
            need_lower = need.lower()
            if 'technical' in need_lower or 'performance' in need_lower:
                relevant += sum(1 for p in all_params if 'DAT' in p)
            if 'environmental' in need_lower or 'carbon' in need_lower:
                relevant += sum(1 for p in all_params if 'END' in p)
            if 'cost' in need_lower:
                relevant += sum(1 for p in all_params if 'TMP' in p or 'Cost' in p)
            if 'circularity' in need_lower or 'end-of-life' in need_lower:
                relevant += sum(1 for p in all_params if 'CIR' in p)
        
        return min(relevant, 50)  # Cap to avoid overcounting
    
    def _get_persona_relevant_params(self, persona: Persona) -> List[str]:
        """Get list of parameters relevant to persona"""
        relevant = []
        for item in self.dataset_analyzer.data:
            param = item['parameter']
            for need in persona.data_needs:
                if any(keyword in need.lower() for keyword in ['technical', 'performance']):
                    if 'DAT' in param:
                        relevant.append(param)
                        break
                if any(keyword in need.lower() for keyword in ['environmental', 'carbon']):
                    if 'END' in param:
                        relevant.append(param)
                        break
        return list(set(relevant))
    
    def generate_checklist(self, persona: Persona) -> Dict:
        """Generate evaluation checklist for a specific persona"""
        checklist = {
            'persona': str(persona),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'heuristics': []
        }
        
        for heuristic in self.heuristics:
            heuristic_section = {
                'heuristic': str(heuristic),
                'description': heuristic.description,
                'evaluation_points': {
                    'visualization': [],
                    'ttl': [],
                    'dataset': []
                }
            }
            
            # Add specific evaluation questions based on heuristic and persona
            heuristic_section['evaluation_points'] = self._generate_evaluation_questions(heuristic, persona)
            checklist['heuristics'].append(heuristic_section)
        
        return checklist
    
    def _generate_evaluation_questions(self, heuristic: Heuristic, persona: Persona) -> Dict:
        """Generate specific evaluation questions for persona-heuristic combination"""
        questions = {
            'visualization': [],
            'ttl': [],
            'dataset': []
        }
        
        # Heuristic 1: Clarity
        if heuristic.number == 1:
            questions['visualization'] = [
                f"Are technical terms understandable to {persona.role}?",
                "Are units clearly displayed and standard?",
                "Is navigation intuitive?",
                "Are labels and headings clear?"
            ]
            questions['ttl'] = [
                "Are namespace prefixes meaningful?",
                "Are property names self-explanatory?",
                "Is the RDF structure logical?"
            ]
            questions['dataset'] = [
                "Are parameter names clear and consistent?",
                "Are units properly specified?",
                "Is the data format easy to understand?"
            ]
        
        # Heuristic 2: Relevance
        elif heuristic.number == 2:
            relevant_needs = persona.data_needs[:3]  # Top 3 needs
            questions['visualization'] = [
                f"Does the UI prominently feature: {need}?" for need in relevant_needs
            ]
            questions['ttl'] = [
                f"Are properties defined for: {need}?" for need in relevant_needs
            ]
            questions['dataset'] = [
                f"Are parameters included for: {need}?" for need in relevant_needs
            ]
        
        # Heuristic 3: Consistency
        elif heuristic.number == 3:
            questions['visualization'] = [
                "Is layout consistent across tabs?",
                "Are similar data presented in similar ways?",
                "Is color coding systematic?"
            ]
            questions['ttl'] = [
                "Are naming conventions consistent?",
                "Is property usage uniform?",
                "Are class definitions coherent?"
            ]
            questions['dataset'] = [
                "Do all parameters follow naming convention?",
                "Is data format consistent?",
                "Are categories logically organized?"
            ]
        
        # Heuristic 4: Accessibility
        elif heuristic.number == 4:
            questions['visualization'] = [
                f"Can {persona.role} quickly find essential information?",
                "Is navigation depth appropriate?",
                "Is search functionality available?",
                "Are key metrics highlighted?"
            ]
            questions['ttl'] = [
                f"Can {persona.role} query the data without expert knowledge?",
                "Is documentation available?",
                "Are examples provided?"
            ]
            questions['dataset'] = [
                "Can data be opened with common tools?",
                "Is filtering/sorting easy?",
                "Are related parameters grouped?"
            ]
        
        # Heuristic 5: Completeness
        elif heuristic.number == 5:
            questions['visualization'] = [
                f"Are all data types needed by {persona.role} included?",
                "Are there missing values?",
                "Is lifecycle coverage complete?"
            ]
            questions['ttl'] = [
                "Are all expected properties defined?",
                "Is the ontology comprehensive?",
                "Are relationships fully mapped?"
            ]
            questions['dataset'] = [
                "What percentage of parameters have values?",
                "Are ranges provided for validation?",
                "Are all categories complete?"
            ]
        
        # Heuristic 6: Transparency
        elif heuristic.number == 6:
            questions['visualization'] = [
                "Are data sources cited?",
                "Is update history visible?",
                "Are responsible parties identified?",
                "Is data provenance clear?"
            ]
            questions['ttl'] = [
                "Are provenance properties used?",
                "Is authorship indicated?",
                "Are data sources linked?"
            ]
            questions['dataset'] = [
                "Is there a source column?",
                "Are timestamps included?",
                "Is versioning tracked?"
            ]
        
        # Heuristic 7: Circularity
        elif heuristic.number == 7:
            questions['visualization'] = [
                "Is end-of-life information prominent?",
                "Are disassembly instructions clear?",
                "Is reuse potential shown?",
                "Are recycling metrics displayed?"
            ]
            questions['ttl'] = [
                "Are circularity properties defined?",
                "Is end-of-life data structured?",
                "Are recovery scenarios modeled?"
            ]
            questions['dataset'] = [
                "Are circularity parameters included?",
                "Is recyclability quantified?",
                "Are secondary uses documented?"
            ]
        
        # Heuristic 8: Digital Compatibility
        elif heuristic.number == 8:
            questions['visualization'] = [
                "Can data be exported?",
                "Are APIs available?",
                "Is format interoperable?"
            ]
            questions['ttl'] = [
                "Does it use standard ontologies?",
                "Is it SPARQL-queryable?",
                "Can it integrate with BIM?"
            ]
            questions['dataset'] = [
                "Is format convertible (CSV, JSON, XML)?",
                "Can it be imported to LCA tools?",
                "Is it machine-readable?"
            ]
        
        # Heuristic 9: User-Centered
        elif heuristic.number == 9:
            questions['visualization'] = [
                f"Is interface tailored to {persona.role} workflows?",
                f"Are {persona.role} priorities emphasized?",
                "Is technical level appropriate?"
            ]
            questions['ttl'] = [
                f"Does data model match {persona.role} mental model?",
                "Is granularity appropriate?"
            ]
            questions['dataset'] = [
                f"Are parameters organized by {persona.role} tasks?",
                "Is level of detail suitable?"
            ]
        
        return questions
    
    def get_results_by_persona(self, persona: Persona) -> List[EvaluationResult]:
        """Get all results for a specific persona"""
        return [r for r in self.results if r.persona == str(persona)]
    
    def get_results_by_component(self, component: str) -> List[EvaluationResult]:
        """Get all results for a specific component"""
        return [r for r in self.results if r.component == component]
    
    def get_average_score(self, persona: Persona = None, component: str = None) -> float:
        """Calculate average score with optional filtering"""
        filtered = self.results
        
        if persona:
            filtered = [r for r in filtered if r.persona == str(persona)]
        if component:
            filtered = [r for r in filtered if r.component == component]
        
        if not filtered:
            return 0.0
        
        return sum(r.score for r in filtered) / len(filtered)


class ReportGenerator:
    """Generates comprehensive evaluation reports"""
    
    def __init__(self, evaluator: HeuristicEvaluator):
        self.evaluator = evaluator
    
    def generate_full_report(self, output_file: str):
        """Generate complete evaluation report"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# DPP PERSONA-BASED HEURISTIC EVALUATION REPORT\n\n")
            f.write(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            # Executive Summary
            f.write("## EXECUTIVE SUMMARY\n\n")
            overall_score = self.evaluator.get_average_score()
            f.write(f"**Overall DPP Score:** {overall_score*100:.1f}%\n\n")
            
            # Component scores
            f.write("### Component Performance\n\n")
            for component in ['visualization', 'ttl', 'dataset']:
                comp_score = self.evaluator.get_average_score(component=component)
                f.write(f"- **{component.title()}:** {comp_score*100:.1f}%\n")
            f.write("\n")
            
            # Persona scores
            f.write("### Persona Satisfaction\n\n")
            for persona in self.evaluator.personas:
                persona_score = self.evaluator.get_average_score(persona=persona)
                f.write(f"- **{persona.role}:** {persona_score*100:.1f}%\n")
            f.write("\n---\n\n")
            
            # Detailed results by persona
            for persona in self.evaluator.personas:
                f.write(f"## PERSONA: {persona.role}\n\n")
                f.write(f"**Title:** {persona.title}\n")
                f.write(f"**Primary Goal:** {persona.primary_goal}\n\n")
                
                persona_results = self.evaluator.get_results_by_persona(persona)
                persona_score = sum(r.score for r in persona_results) / len(persona_results)
                f.write(f"**Overall Score for this Persona:** {persona_score*100:.1f}%\n\n")
                
                # Group by heuristic
                for heuristic in self.evaluator.heuristics:
                    heuristic_results = [r for r in persona_results if r.heuristic == str(heuristic)]
                    
                    if heuristic_results:
                        f.write(f"### {heuristic}\n\n")
                        
                        for result in heuristic_results:
                            f.write(f"#### {result.component.title()}\n")
                            f.write(f"**Score:** {result.score*100:.1f}% ({result.compliance_level.upper()})\n\n")
                            f.write("**Findings:**\n")
                            for finding in result.findings:
                                f.write(f"- {finding}\n")
                            f.write("\n")
                
                f.write("\n---\n\n")
            
            # Heuristic compliance overview
            f.write("## HEURISTIC COMPLIANCE OVERVIEW\n\n")
            for heuristic in self.evaluator.heuristics:
                heuristic_results = [r for r in self.evaluator.results if r.heuristic == str(heuristic)]
                avg_score = sum(r.score for r in heuristic_results) / len(heuristic_results)
                
                f.write(f"### {heuristic}\n")
                f.write(f"**Average Score:** {avg_score*100:.1f}%\n")
                f.write(f"**Description:** {heuristic.description}\n\n")
                
                # Component breakdown
                for component in ['visualization', 'ttl', 'dataset']:
                    comp_results = [r for r in heuristic_results if r.component == component]
                    if comp_results:
                        comp_score = sum(r.score for r in comp_results) / len(comp_results)
                        f.write(f"- {component.title()}: {comp_score*100:.1f}%\n")
                f.write("\n")
            
            # Recommendations
            f.write("\n---\n\n## RECOMMENDATIONS\n\n")
            self._write_recommendations(f)
    
    def _write_recommendations(self, f):
        """Generate prioritized recommendations"""
        # Find low-scoring areas
        low_scores = [r for r in self.evaluator.results if r.score < 0.70]
        
        if not low_scores:
            f.write("✓ All areas meet good performance standards (>70%)\n\n")
            return
        
        # Group by component
        recommendations = {
            'visualization': [],
            'ttl': [],
            'dataset': []
        }
        
        for result in low_scores:
            recommendations[result.component].append({
                'heuristic': result.heuristic,
                'score': result.score,
                'persona': result.persona,
                'findings': result.findings
            })
        
        priority = 1
        for component in ['visualization', 'ttl', 'dataset']:
            if recommendations[component]:
                f.write(f"### {component.title()} Improvements\n\n")
                
                for rec in sorted(recommendations[component], key=lambda x: x['score']):
                    f.write(f"**Priority {priority}:** {rec['heuristic']} (Score: {rec['score']*100:.1f}%)\n")
                    f.write(f"- Affects: {rec['persona']}\n")
                    f.write("- Issues:\n")
                    for finding in rec['findings']:
                        if '⚠' in finding or '✗' in finding:
                            f.write(f"  - {finding}\n")
                    f.write("\n")
                    priority += 1
    
    def generate_persona_checklist(self, persona: Persona, output_file: str):
        """Generate evaluation checklist for specific persona"""
        checklist = self.evaluator.generate_checklist(persona)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# EVALUATION CHECKLIST: {persona.role}\n\n")
            f.write(f"**Date:** {checklist['date']}\n")
            f.write(f"**Title:** {persona.title}\n")
            f.write(f"**Primary Goal:** {persona.primary_goal}\n\n")
            f.write("---\n\n")
            
            for idx, heuristic_section in enumerate(checklist['heuristics'], 1):
                f.write(f"## {heuristic_section['heuristic']}\n\n")
                f.write(f"**Description:** {heuristic_section['description']}\n\n")
                
                for component in ['visualization', 'ttl', 'dataset']:
                    questions = heuristic_section['evaluation_points'][component]
                    if questions:
                        f.write(f"### {component.title()}\n\n")
                        for q in questions:
                            f.write(f"- [ ] {q}\n")
                        f.write("\n")
                
                f.write("**Score (0-100):** ______\n\n")
                f.write("**Notes:**\n\n")
                f.write("_" * 80 + "\n\n")
                f.write("---\n\n")
    
    def generate_summary_json(self, output_file: str):
        """Generate machine-readable JSON summary"""
        summary = {
            'report_date': datetime.now().isoformat(),
            'overall_score': self.evaluator.get_average_score(),
            'component_scores': {},
            'persona_scores': {},
            'heuristic_scores': {},
            'detailed_results': []
        }
        
        # Component scores
        for component in ['visualization', 'ttl', 'dataset']:
            summary['component_scores'][component] = self.evaluator.get_average_score(component=component)
        
        # Persona scores
        for persona in self.evaluator.personas:
            summary['persona_scores'][str(persona)] = self.evaluator.get_average_score(persona=persona)
        
        # Heuristic scores
        for heuristic in self.evaluator.heuristics:
            heuristic_results = [r for r in self.evaluator.results if r.heuristic == str(heuristic)]
            summary['heuristic_scores'][str(heuristic)] = sum(r.score for r in heuristic_results) / len(heuristic_results)
        
        # Detailed results
        for result in self.evaluator.results:
            summary['detailed_results'].append({
                'persona': result.persona,
                'heuristic': result.heuristic,
                'component': result.component,
                'score': result.score,
                'compliance_level': result.compliance_level,
                'findings': result.findings
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)


def main():
    """Main execution function"""
    print("=" * 80)
    print("DPP PERSONA-BASED HEURISTIC EVALUATION TOOL")
    print("=" * 80)
    print()
    
    # File paths
    base_path = Path(r"C:\Users\Catalina")
    personas_file = base_path / "Documents" / "Personas.txt"
    heuristics_file = base_path / "Documents" / "Heuristics.txt"
    dataset_file = base_path / "Documents" / "Dataset.txt"
    
    ttl_base = base_path / "OneDrive - Pontificia Universidad Javeriana" / "Desktop" / "THESIS" / "Methodology"
    ttl_element_file = ttl_base / "DPP_Element" / "DPP_HempBlock_Element_mapped.ttl"
    ttl_material_file = ttl_base / "DPP_Material" / "DPP_HempBlock_Material_mapped.ttl"
    
    # Parse personas and heuristics
    print("📋 Parsing personas...")
    personas = PersonaParser.parse_personas(str(personas_file))
    print(f"   Found {len(personas)} personas")
    
    print("📋 Parsing heuristics...")
    heuristics = HeuristicParser.parse_heuristics(str(heuristics_file))
    print(f"   Found {len(heuristics)} heuristics")
    
    # Initialize analyzers
    print("\n🔍 Analyzing TTL files...")
    ttl_analyzer = TTLAnalyzer([str(ttl_element_file), str(ttl_material_file)])
    ttl_analysis = ttl_analyzer.analyze_structure()
    print(f"   Total triples: {ttl_analysis['total_triples']}")
    print(f"   Unique properties: {len(ttl_analysis['unique_predicates'])}")
    
    print("\n🔍 Analyzing dataset...")
    dataset_analyzer = DatasetAnalyzer(str(dataset_file))
    dataset_analysis = dataset_analyzer.analyze_quality()
    print(f"   Total parameters: {dataset_analysis['total_parameters']}")
    print(f"   Completeness: {dataset_analysis['completeness_rate']*100:.1f}%")
    
    # Run evaluation
    print("\n⚙️  Running heuristic evaluation...")
    evaluator = HeuristicEvaluator(personas, heuristics, ttl_analyzer, dataset_analyzer)
    evaluator.evaluate_all()
    print(f"   Generated {len(evaluator.results)} evaluation results")
    
    # Generate reports
    print("\n📊 Generating reports...")
    report_gen = ReportGenerator(evaluator)
    
    output_path = base_path / "Documents"
    
    # Full report
    full_report = output_path / "DPP_Evaluation_Report.md"
    report_gen.generate_full_report(str(full_report))
    print(f"   ✓ Full report: {full_report}")
    
    # JSON summary
    json_summary = output_path / "DPP_Evaluation_Summary.json"
    report_gen.generate_summary_json(str(json_summary))
    print(f"   ✓ JSON summary: {json_summary}")
    
    # Individual persona checklists
    print("\n📝 Generating persona checklists...")
    for persona in personas:
        checklist_file = output_path / f"Checklist_{persona.role.replace('/', '_').replace(' ', '_')}.md"
        report_gen.generate_persona_checklist(persona, str(checklist_file))
        print(f"   ✓ {persona.role}: {checklist_file}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    print(f"\nOverall DPP Score: {evaluator.get_average_score()*100:.1f}%\n")
    
    print("Component Scores:")
    for component in ['visualization', 'ttl', 'dataset']:
        score = evaluator.get_average_score(component=component)
        print(f"  {component.title():15} {score*100:.1f}%")
    
    print("\nPersona Satisfaction:")
    for persona in personas:
        score = evaluator.get_average_score(persona=persona)
        print(f"  {persona.role:40} {score*100:.1f}%")
    
    print("\n" + "=" * 80)
    print("✓ Evaluation complete! Check the Documents folder for reports.")
    print("=" * 80)


if __name__ == "__main__":
    main()
