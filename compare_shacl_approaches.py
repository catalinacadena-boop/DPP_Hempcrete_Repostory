"""
Comparison of SHACL validation approaches: Single vs Multi-Ontology
"""

print("=" * 80)
print("SHACL VALIDATION APPROACH COMPARISON")
print("=" * 80)

print("\n📋 ORIGINAL APPROACH (SHACL1.0.ttl)")
print("-" * 80)
print("""
CONSTRAINT:
    sh:property [
        sh:path dpp:hasHeight ;
        sh:datatype xsd:decimal ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ]

DATA EXAMPLES:
    ✅ inst:element_84 dpp:hasHeight 200.0 .
    ❌ inst:element_84 qudt:hasHeight 200.0 .      # FAILS - wrong namespace!
    ❌ inst:element_84 schema:height 200.0 .       # FAILS - wrong namespace!
    
PROBLEM: Only accepts ONE specific ontology namespace (dpp:)
""")

print("\n📋 NEW APPROACH (SHACL_MultiOntology.ttl)")
print("-" * 80)
print("""
CONSTRAINT:
    sh:property [
        sh:path [ sh:alternativePath (qudt:hasHeight schema:height dpp:hasHeight) ] ;
        sh:or (
            [ sh:datatype xsd:double ]
            [ sh:datatype xsd:decimal ]
        ) ;
        sh:minCount 1 ;
    ]

DATA EXAMPLES:
    ✅ inst:element_84 dpp:hasHeight 200.0 .       # PASSES
    ✅ inst:element_84 qudt:hasHeight 200.0 .      # PASSES
    ✅ inst:element_84 schema:height 200.0 .       # PASSES
    ✅ inst:element_84 qudt:hasHeight 200.0 ;      # PASSES - multi-mapping!
                      schema:height 200.0 ;
                      dpp:hasHeight 200.0 .
    
BENEFIT: Accepts ANY mapped ontology namespace!
""")

print("\n📊 PROPERTY MAPPING COVERAGE")
print("-" * 80)

mappings = {
    "Dimensions": {
        "Height": ["qudt:hasHeight", "schema:height", "dpp:hasHeight"],
        "Width": ["qudt:hasWidth", "schema:width", "dpp:hasWidth"],
        "Length": ["qudt:hasLength", "schema:depth", "dpp:hasLength"],
        "Area": ["qudt:hasArea", "dpp:hasArea"],
        "Volume": ["qudt:hasVolume", "dpp:hasVolume"],
    },
    "Identity": {
        "GUID": ["bot:hasGuid", "dpp:hasGuid", "dcterms:identifier"],
        "ID": ["dpp:hasId", "dcterms:identifier", "schema:identifier"],
        "Category": ["schema:category", "dpp:hasCategory"],
        "Family": ["bpo:hasProductType", "schema:productID", "dpp:hasFamily"],
    },
    "Material": {
        "Material": ["dpp:hasMaterial", "schema:material", "bpo:consistsOf"],
        "MaterialType": ["dpp:hasMaterialType", "schema:additionalType"],
        "Color": ["schema:color", "dpp:hasColor"],
    },
    "Environmental": {
        "GWP": ["dpp:hasGlobalWarmingPotential", "schema:emissionsCO2"],
        "EPD": ["dpp:hasEPD", "schema:hasCredential"],
        "Weight": ["dpp:hasWeight", "schema:weight"],
    },
    "Temporal": {
        "ServiceLife": ["dpp:hasServiceLife", "schema:duration"],
        "Warranty": ["dpp:hasWarranty", "schema:warranty"],
        "Origin": ["dpp:hasOrigin", "schema:manufacturer", "prov:wasAttributedTo"],
        "Phase": ["dpp:hasPhase", "prov:wasGeneratedBy"],
    },
    "Spatial": {
        "Level": ["bot:hasStorey", "dpp:hasLevel"],
        "Host": ["bot:hasHost", "dpp:hasHost"],
    },
    "Cost": {
        "ReplacementCost": ["dpp:hasReplacementCost", "schema:price"],
        "UnitCost": ["dpp:hasUnitCost", "schema:price"],
    },
    "Compliance": {
        "Compliance": ["dpp:hasCompliance", "schema:isAccessibleForFree"],
    }
}

for category, props in mappings.items():
    print(f"\n{category}:")
    for prop_name, ontologies in props.items():
        print(f"  • {prop_name:20s} → {', '.join(ontologies)}")

print("\n" + "=" * 80)
print(f"TOTAL PROPERTIES WITH MULTI-ONTOLOGY SUPPORT: {sum(len(props) for props in mappings.values())}")
print("=" * 80)

print("\n✨ KEY ADVANTAGES")
print("-" * 80)
print("""
1. ✅ Ontology Agnostic - Works with any namespace
2. ✅ Interoperability - Different systems use different ontologies
3. ✅ Future-Proof - Easy to add new ontology mappings
4. ✅ Backward Compatible - Still validates single-ontology data
5. ✅ Standards Compliant - Uses SHACL sh:alternativePath feature
6. ✅ Redundancy Tolerant - Accepts multiple assertions of same property
7. ✅ Query Flexibility - Data queryable from any ontology perspective
""")

print("\n🎯 USE CASES")
print("-" * 80)
print("""
1. Digital Product Passports - Cross-industry data exchange
2. Building Information Modeling - Multi-tool interoperability
3. Semantic Web Applications - Schema.org compatibility
4. Linked Data Publishing - Standards-based vocabularies
5. Research Projects - Multiple ontology frameworks
6. API Integrations - Different consumers prefer different ontologies
""")

print("\n📝 MIGRATION PATH")
print("-" * 80)
print("""
OLD WORKFLOW:
  1. IFC → TTL (props: namespace)
  2. Map to single ontology (dpp: only)
  3. Validate with SHACL1.0.ttl (strict single-path)
  4. ❌ Fails if any alternative namespace used

NEW WORKFLOW:
  1. IFC → TTL (props: namespace)
  2. Map to MULTIPLE ontologies (dpp:, schema:, qudt:, bpo:, bot:, etc.)
  3. Validate with SHACL_MultiOntology.ttl (flexible multi-path)
  4. ✅ Passes regardless of ontology namespace(s) used
""")

print("\n" + "=" * 80)
print("For detailed documentation, see: SHACL_MultiOntology_README.md")
print("=" * 80)
