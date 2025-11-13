"""
Script to map IFC-extracted TTL properties to multiple standard ontology vocabularies
This makes the data readable by any ontology system through multiple mappings and OWL equivalence
"""

from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD, OWL
from rdflib.namespace import DCTERMS
import sys

# Define namespaces
BOT = Namespace("https://w3id.org/bot#")
PROPS = Namespace("https://w3id.org/props#")
DPP = Namespace("http://www.semanticweb.org/janneke.bosma/DPP#")
BPO = Namespace("https://w3id.org/bpo#")
BMP = Namespace("https://w3id.org/bmp#")
SCHEMA = Namespace("http://schema.org/")
QUDT = Namespace("http://qudt.org/schema/qudt/")
UNIT = Namespace("http://qudt.org/vocab/unit/")
PROV = Namespace("http://www.w3.org/ns/prov#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

def map_properties_to_ontology(input_file, output_file):
    """
    Map custom props: properties to multiple standard ontology vocabularies
    Creates redundant mappings for maximum interoperability
    """
    # Load the input TTL file
    g = Graph()
    g.parse(input_file, format="turtle")
    
    # Create output graph
    output_g = Graph()
    
    # Bind namespaces for output
    output_g.bind("bot", BOT)
    output_g.bind("dpp", DPP)
    output_g.bind("bpo", BPO)
    output_g.bind("bmp", BMP)
    output_g.bind("schema", SCHEMA)
    output_g.bind("rdf", RDF)
    output_g.bind("rdfs", RDFS)
    output_g.bind("xsd", XSD)
    output_g.bind("owl", OWL)
    output_g.bind("qudt", QUDT)
    output_g.bind("unit", UNIT)
    output_g.bind("dcterms", DCTERMS)
    output_g.bind("prov", PROV)
    output_g.bind("foaf", FOAF)
    
    # Property mapping dictionary - now supports MULTIPLE mappings per property
    # Format: "property_name": [("namespace", "predicate"), ("namespace2", "predicate2"), ...]
    property_mapping = {
        # Identity & Classification
        "hasCompressedGuid": [("dpp", "hasGuid"), ("dcterms", "identifier")],
        "Category": [("schema", "category"), ("dpp", "hasCategory")],
        "FamilyName": [("bpo", "hasProductType"), ("schema", "productID")],
        "Family": [("bpo", "hasProductType"), ("dpp", "hasFamily")],
        "Type": [("rdf", "type"), ("dpp", "hasType")],
        "TypeName": [("schema", "name"), ("dpp", "hasTypeName")],
        
        # Material properties
        "Dpp_Mat_Material": [("dpp", "hasMaterial"), ("schema", "material"), ("bpo", "consistsOf")],
        "Dpp_Aut_Materialtype": [("dpp", "hasMaterialType"), ("schema", "additionalType")],
        
        # Dimensions (use QUDT for units)
        "Dpp_Dim_Height_Mm": [("qudt", "hasHeight"), ("schema", "height"), ("dpp", "hasHeight")],
        "Dpp_Dim_Length_Mm": [("qudt", "hasLength"), ("schema", "depth"), ("dpp", "hasLength")],
        "Dpp_Dim_Width_Mm": [("qudt", "hasWidth"), ("schema", "width"), ("dpp", "hasWidth")],
        "Area": [("qudt", "hasArea"), ("dpp", "hasArea")],
        "Volume": [("qudt", "hasVolume"), ("dpp", "hasVolume")],
        
        # Circularity Properties
        "Dpp_Cir_Recyclingpotential": [("dpp", "hasRecyclingPotential")],
        "Dpp_Cir_Reusabilitypotential": [("dpp", "hasReusabilityPotential")],
        "Dpp_Cir_Disassemblypotential": [("dpp", "hasDisassemblyPotential")],
        "Dpp_Cir_Circularityindex": [("dpp", "hasCircularityIndex")],
        "Dpp_Cir_Prefabrication": [("dpp", "hasPrefabrication")],
        "Dpp_Cir_Prefabricationfactor": [("dpp", "hasPrefabricationFactor")],
        "Dpp_Cir_Reusability": [("dpp", "hasReusability")],
        "Dpp_Cir_Deconstructabilityscore": [("dpp", "hasDeconstructabilityScore")],
        "Dpp_Cir_Recoveryscore": [("dpp", "hasRecoveryScore")],
        
        # Environmental Data
        "Dpp_End_Gwp_Kgco₂Eq": [("dpp", "hasGlobalWarmingPotential"), ("schema", "emissionsCO2")],
        "Dpp_End_Embodiedcarbon_Kgco₂Eq": [("dpp", "hasEmbodiedCarbon")],
        "Dpp_End_Biogeniccarbon_Kgco₂Eq": [("dpp", "hasBiogenicCarbon")],
        "Dpp_End_Endoflifeemissions_Kgco₂Eq": [("dpp", "hasEndOfLifeEmissions")],
        "Dpp_End_Environmentalscore": [("dpp", "hasEnvironmentalScore")],
        "Dpp_End_Epd": [("dpp", "hasEPD"), ("schema", "hasCredential")],
        "Dpp_End_Penrt_Mjkg": [("dpp", "hasPrimaryEnergyNonRenewable")],
        "Dpp_End_Pert_Mjkg": [("dpp", "hasPrimaryEnergyRenewable")],
        "Dpp_End_Ap_Kgso₂Eq": [("dpp", "hasAcidificationPotential")],
        "Dpp_End_Ei": [("dpp", "hasEnvironmentalImpact")],
        "Dpp_End_W": [("dpp", "hasWeight"), ("schema", "weight")],
        
        # Safety & Compliance
        "Dpp_Sad_Fire_Class": [("dpp", "hasFireClass")],
        "Dpp_Sad_Fire_Dsubclass": [("dpp", "hasFireDSubclass")],
        "Dpp_Sad_Fire_Ssubclass": [("dpp", "hasFireSSubclass")],
        "Dpp_Sad_Fireresistance": [("dpp", "hasFireResistance")],
        "Dpp_Sad_Compliance": [("dpp", "hasCompliance"), ("schema", "isAccessibleForFree")],
        "Dpp_Sad_Toxicity": [("dpp", "hasToxicity")],
        "Dpp_Sad_Coatings": [("dpp", "hasCoatings")],
        "Dpp_Sad_Coatingtype": [("dpp", "hasCoatingType")],
        "Dpp_Sad_Pm_Ctuh": [("dpp", "hasParticulateMatter")],
        "Dpp_Sad_Sqp": [("dpp", "hasSoundQualityPerformance")],
        
        # Aesthetic & Sensory
        "Dpp_Asd_Aesthetic": [("dpp", "hasAestheticScore")],
        "Dpp_Asd_Aging": [("dpp", "hasAgingScore")],
        "Dpp_Asd_Architectural": [("dpp", "hasArchitecturalScore")],
        "Dpp_Asd_Color": [("schema", "color"), ("dpp", "hasColor")],
        "Dpp_Asd_Odor": [("dpp", "hasOdor")],
        "Dpp_Asd_Temp": [("dpp", "hasThermalFeeling")],
        "Dpp_Asd_Texture": [("dpp", "hasTexture")],
        "Dpp_Asd_Agriculturalvalue": [("dpp", "hasAgriculturalValue")],
        "Dpp_Asd_Climatesuitability": [("dpp", "hasClimateSuitability")],
        "Dpp_Asd_Resourseavailability": [("dpp", "hasResourceAvailability")],
        
        # Technical Data
        "Dpp_Dat_Standarcompliance": [("dpp", "hasStandardCompliance")],
        "Dpp_Dat_Compressivestrenght_Mpa": [("dpp", "hasCompressiveStrength")],
        "Dpp_Dat_Shearstrenght_Mpa": [("dpp", "hasShearStrength")],
        "Dpp_Dat_Vaporabsorption": [("dpp", "hasVaporAbsorption")],
        "Dpp_Dat_Vapordiffμ_Dry": [("dpp", "hasVaporDiffusionDry")],
        "Dpp_Dat_Vapordiffμ_Wet": [("dpp", "hasVaporDiffusionWet")],
        
        # Cost Data
        "Dpp_Cod_Replacement_Eur": [("dpp", "hasReplacementCost"), ("schema", "price")],
        "Dpp_Cod_Unitcost_Eur": [("dpp", "hasUnitCost"), ("schema", "price")],
        "Dpp_Cod_Circularbenefit_Eur": [("dpp", "hasCircularBenefit")],
        
        # Temporal & Origin
        "Dpp_Tmp_Servicelife_Years": [("dpp", "hasServiceLife"), ("schema", "duration")],
        "Dpp_Tmp_Soursing_Km": [("dpp", "hasSourcingDistance")],
        "Dpp_Tmp_Warranty": [("dpp", "hasWarranty"), ("schema", "warranty")],
        "Dpp_Aut_Origin": [("dpp", "hasOrigin"), ("schema", "manufacturer"), ("prov", "wasAttributedTo")],
        "Dpp_Aut_Id": [("dpp", "hasId"), ("dcterms", "identifier"), ("schema", "identifier")],
        
        # General
        "Reference": [("dcterms", "identifier"), ("dpp", "hasReference")],
        "PhaseCreated": [("dpp", "hasPhase"), ("prov", "wasGeneratedBy")],
        "Level": [("bot", "hasStorey"), ("dpp", "hasLevel")],
        "Host": [("bot", "hasHost"), ("dpp", "hasHost")],
    }
    
    # Namespace mapping
    ns_mapping = {
        "dpp": DPP,
        "bpo": BPO,
        "bmp": BMP,
        "schema": SCHEMA,
        "qudt": QUDT,
        "unit": UNIT,
        "bot": BOT,
        "rdf": RDF,
        "rdfs": RDFS,
        "dcterms": DCTERMS,
        "prov": PROV,
        "foaf": FOAF,
        "owl": OWL,
    }
    
    # Process all subjects
    for subject in g.subjects(predicate=RDF.type, object=BOT.Element):
        # Add the subject with multiple types
        output_g.add((subject, RDF.type, BOT.Element))
        output_g.add((subject, RDF.type, DPP.product))
        output_g.add((subject, RDF.type, BPO.Product))
        
        # Copy label and bot:hasGuid
        for label in g.objects(subject, RDFS.label):
            output_g.add((subject, RDFS.label, label))
        
        for guid in g.objects(subject, BOT.hasGuid):
            output_g.add((subject, BOT.hasGuid, guid))
        
        # Create circularity property set
        circ_node = URIRef(str(subject).replace("element_", "circularity_"))
        output_g.add((subject, DPP.hasCircularityPropertySet, circ_node))
        output_g.add((circ_node, RDF.type, DPP.circularityPropertySet))
        
        # Process all properties
        for pred, obj in g.predicate_objects(subject):
            # Skip already processed predicates
            if pred in [RDF.type, RDFS.label, BOT.hasGuid]:
                continue
            
            # Extract property name
            prop_name = str(pred).split("#")[-1].split("/")[-1]
            
            # Check if we have a mapping for this property
            if prop_name in property_mapping:
                # Get list of all mappings for this property
                mappings = property_mapping[prop_name]
                
                # Create triples for EACH ontology mapping
                for ns_prefix, new_prop in mappings:
                    if ns_prefix in ns_mapping:
                        ns = ns_mapping[ns_prefix]
                        new_predicate = ns[new_prop]
                        
                        # Add to circularity set if it's a circularity property
                        if prop_name.startswith("Dpp_Cir_"):
                            output_g.add((circ_node, new_predicate, obj))
                        else:
                            output_g.add((subject, new_predicate, obj))
            else:
                # Keep unmapped properties with props: namespace for reference
                output_g.add((subject, pred, obj))
    
    # Copy other non-element entities (buildings, storeys, etc.)
    for s, p, o in g:
        subject_is_element = (s, RDF.type, BOT.Element) in g
        if not subject_is_element:
            output_g.add((s, p, o))
    
    # Generate OWL equivalence statements for mapped properties
    generate_owl_equivalences(output_g, property_mapping, ns_mapping)
    
    # Write output
    output_g.serialize(destination=output_file, format="turtle")
    print(f"✓ Successfully mapped properties to ontology vocabularies")
    print(f"✓ Input file: {input_file}")
    print(f"✓ Output file: {output_file}")
    print(f"✓ Total triples in output: {len(output_g)}")

def generate_owl_equivalences(graph, property_mapping, ns_mapping):
    """
    Generate OWL equivalentProperty statements for all mapped properties.
    This declares that properties from different ontologies are semantically equivalent.
    """
    # Track property URIs that need equivalence declarations
    property_uris = {}
    
    # Build a map of property names to their URIs in different ontologies
    for prop_name, mappings in property_mapping.items():
        uris = []
        for ns_prefix, pred_name in mappings:
            if ns_prefix in ns_mapping:
                ns = ns_mapping[ns_prefix]
                uri = ns[pred_name]
                uris.append(uri)
        
        if len(uris) > 1:  # Only create equivalences if multiple mappings exist
            property_uris[prop_name] = uris
    
    # Create owl:equivalentProperty statements
    # For each set of equivalent properties, declare pairwise equivalence
    for prop_name, uris in property_uris.items():
        # Take first URI as the "canonical" one
        canonical = uris[0]
        
        # Declare all others as equivalent to the canonical
        for uri in uris[1:]:
            graph.add((canonical, OWL.equivalentProperty, uri))
            # Also add the reverse for symmetry (optional but explicit)
            graph.add((uri, OWL.equivalentProperty, canonical))
    
    print(f"✓ Generated OWL equivalence statements for {len(property_uris)} properties")

if __name__ == "__main__":
    # Default input/output files
    input_file = "Project1.ttl"
    output_file = "Project1_mapped.ttl"
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    try:
        map_properties_to_ontology(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
