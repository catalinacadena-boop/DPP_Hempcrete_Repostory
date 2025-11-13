# Import libraries
from pyrevit import DB, revit, script, forms
import sys
import os

# Add lib folder to path for importing modules
lib_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'lib')
if lib_path not in sys.path:
	sys.path.insert(0, lib_path)

# Prompt user to specify file path
filterXcl = 'Excel workbooks|*.xlsx'
filterRfa = 'Family Files|*.rfa'

path_xcl = forms.pick_file(files_filter=filterXcl, title="Choose excel file")

if not path_xcl:
	script.exit()

# Prompt user to specify families
path_rfas = forms.pick_file(files_filter=filterRfa, multi_file=True, title="Choose families")

if not path_rfas:
	script.exit()

# Prompt user for worksheet name
from pyrevit import forms as pyrevit_forms

worksheet_options = {
	'Standard': 'Standard',
	'Variables': 'Variables',
	'Sheet1': 'Sheet1',
	'Custom (enter name)': 'Custom'
}

selected = pyrevit_forms.CommandSwitchWindow.show(
	worksheet_options.keys(),
	message='Select the worksheet that contains the parameters:'
)

if not selected:
	script.exit()

worksheet_name = worksheet_options[selected]

# If user selected "Custom", ask for custom name
if worksheet_name == "Custom":
	worksheet_name = pyrevit_forms.ask_for_string(
		default='Sheet1',
		prompt='Enter the worksheet name:',
		title='Custom Worksheet Name'
	)
	if not worksheet_name:
		script.exit()

# Import Excel data
from guRoo_xclUtils import *

print("Using worksheet: '{}'".format(worksheet_name))

xcl = xclUtils([],path_xcl)
dat = xcl.xclUtils_import(worksheet_name, 0, 0)  # Use 0,0 to get all columns and rows
print("=" * 60)
print("EXCEL IMPORT DEBUG")
print("=" * 60)
print("Worksheet found:", dat[1])
print("Total rows imported:", len(dat[0]))
print("Total columns:", len(dat[0][0]) if len(dat[0]) > 0 else 0)

if not dat[1]:
	print("\n[ERROR] Could not find worksheet: '{}'".format(worksheet_name))
	print("Please check that the worksheet name is correct.")
	forms.alert("Worksheet '{}' not found in the Excel file.\n\n".format(worksheet_name) +
				"Make sure the name is spelled correctly and exists in the Excel file.",
				title="Worksheet Not Found")
	script.exit()

print("\nFirst row (headers):")
if len(dat[0]) > 0:
	for i, header in enumerate(dat[0][0]):
		print("  Column {}: '{}'".format(i, header))
print("\nFirst 3 data rows:")
for i, row in enumerate(dat[0][1:4]):
	print("  Row {}: {}".format(i+2, row))
print("=" * 60)


targets_params, target_bipgs, fam_inst, fam_formulae = [],[],[],[]

print("\nPROCESSING EXCEL DATA")
print("=" * 60)

for idx, row in enumerate(dat[0][1:]):
	print("\nProcessing row {}: {}".format(idx + 2, row))
	
	# Check row length
	if len(row) < 4:
		print("  WARNING: Row has only {} columns, skipping...".format(len(row)))
		continue
	
	# Column A: Shared Parameter Name
	param_name = row[0] if row[0] else ""
	targets_params.append(param_name)
	print("  Parameter Name: '{}'".format(param_name))
	
	# Column B: BIP Name (driven by lookup) - THIS IS THE GROUP!
	bipg_name = row[1] if len(row) > 1 and row[1] else ""
	target_bipgs.append(bipg_name)
	print("  BIP Group: '{}'".format(bipg_name))
	
	# Column C: Instance (Yes/No)
	is_instance = row[2] == "Yes" if len(row) > 2 else False
	fam_inst.append(is_instance)
	print("  Is Instance: {}".format(is_instance))
	
	# Column D: Formula (optional) - handle empty cells
	formula = None
	if len(row) > 3 and row[3] and str(row[3]).strip():
		formula = str(row[3])
	fam_formulae.append(formula)
	print("  Formula: '{}'".format(formula if formula else "None"))

print("\nSUMMARY:")
print("  Total parameters to add: {}".format(len(targets_params)))
print("  Parameters: {}".format(targets_params))
print("  Groups: {}".format(target_bipgs))
print("=" * 60)

# Get shared parameters
app = __revit__.Application

fam_defs  = []
fam_bipgs = []

print("\nSHARED PARAMETERS VALIDATION")
print("=" * 60)

# Get all definitions and names
spFile   = app.OpenSharedParameterFile()

# Check if shared parameters file exists
if spFile is None:
	print("WARNING: No shared parameters file configured in Revit.")
	print("Attempting to create/configure shared parameters file...")
	
	# Try to create a shared parameters file in the Documents folder
	import os
	sp_file_path = os.path.join(os.path.expanduser("~"), "Documents", "SharedParameters.txt")
	
	# Check if file already exists
	if not os.path.exists(sp_file_path):
		print("Creating new SharedParameters.txt at: {}".format(sp_file_path))
		# Create basic structure
		with open(sp_file_path, 'w') as f:
			f.write("# This is a Revit shared parameter file.\n")
			f.write("# Do not edit manually.\n")
			f.write("*META\tVERSION\tMINVERSION\n")
			f.write("META\t2\t1\n")
			f.write("*GROUP\tID\tNAME\n")
			f.write("GROUP\t1\tPG_TEXT\n")
			f.write("*PARAM\tGUID\tNAME\tDATATYPE\tDATACATEGORY\tGROUP\tVISIBLE\tDESCRIPTION\tUSERMODIFIABLE\tHIDEWHENNOVALUE\n")
	else:
		print("SharedParameters.txt already exists at: {}".format(sp_file_path))
	
	# Set the shared parameters file in Revit
	app.SharedParametersFilename = sp_file_path
	spFile = app.OpenSharedParameterFile()
	
	if spFile is None:
		forms.alert("Could not create or open shared parameters file.\n\n" + 
					"Please configure it manually in:\n" +
					"Manage -> Shared Parameters -> Browse -> Select SharedParameters.txt", 
					title="Script cancelled")
		script.exit()
	else:
		print("Successfully configured shared parameters file")

spGroups = spFile.Groups
print("Shared parameters file groups: {}".format(spGroups.Size))

sp_defs, sp_nams = [],[]

for g in spGroups:
	for d in g.Definitions:
		sp_defs.append(d)
		sp_nams.append(d.Name)

print("Total shared parameters available: {}".format(len(sp_nams)))
print("Available parameters: {}".format(sp_nams[:10] if len(sp_nams) > 10 else sp_nams))

# Get target parameter definitions
print("\nMatching parameters from Excel to Shared Parameters:")
for t in targets_params:
	if t in sp_nams:
		ind = sp_nams.index(t)
		fam_defs.append(sp_defs[ind])
		print("  [OK] Found: '{}'".format(t))
	else:
		print("  [ERROR] NOT FOUND: '{}'".format(t))

print("\nMatched {}/{} parameters".format(len(fam_defs), len(targets_params)))
print("=" * 60)

# Catch if we don't have all parameters
if len(fam_defs) != len(targets_params):
	print("\nWARNING: Some parameters not found in shared parameters file")
	print("Missing parameters:")
	missing_params = []
	for t in targets_params:
		if t not in sp_nams:
			print("  - {}".format(t))
			missing_params.append(t)
	
	# Ask user if they want to create missing parameters
	create_params = forms.alert(
		"The following parameters were not found in the shared parameters file:\n\n" +
		"\n".join(missing_params) + "\n\n" +
		"Do you want to create them automatically?",
		title="Missing Parameters",
		yes=True,
		no=True
	)
	
	if create_params:
		print("\nCreating missing parameters...")
		import uuid
		
		# Get or create PG_TEXT group
		pg_text_group = None
		for g in spGroups:
			if g.Name == "PG_TEXT":
				pg_text_group = g
				break
		
		if pg_text_group is None:
			print("Creating PG_TEXT group...")
			pg_text_group = spGroups.Create("PG_TEXT")
		
		# Create missing parameters
		for param_name in missing_params:
			try:
				# Create external definition options
				ext_def_options = DB.ExternalDefinitionCreationOptions(param_name, DB.ParameterType.Text)
				ext_def_options.GUID = System.Guid.NewGuid()
				
				# Create the parameter
				new_def = pg_text_group.Definitions.Create(ext_def_options)
				sp_defs.append(new_def)
				sp_nams.append(new_def.Name)
				print("  Created parameter: {}".format(param_name))
			except Exception as e:
				print("  Failed to create parameter {}: {}".format(param_name, str(e)))
		
		# Refresh the definitions list
		fam_defs = []
		for t in targets_params:
			if t in sp_nams:
				ind = sp_nams.index(t)
				fam_defs.append(sp_defs[ind])
		
		print("Successfully created {} parameters".format(len(missing_params)))
	else:
		print("User cancelled - parameters not created")
		script.exit()

# Final check
if len(fam_defs) != len(targets_params):
	forms.alert("Some parameters are still missing. Script cannot continue.", title="Script cancelled")
	script.exit()

# Import enum
import System
from System import Enum

print("\nPARAMETER GROUP VALIDATION")
print("=" * 60)

# Get all bipgs for checking - use reflection to access BuiltInParameterGroup
try:
	# Get BuiltInParameterGroup type from Autodesk.Revit.DB namespace
	import clr
	clr.AddReference('RevitAPI')
	from Autodesk.Revit.DB import BuiltInParameterGroup
	bipgs = [a for a in System.Enum.GetValues(BuiltInParameterGroup)]
	print("Successfully loaded BuiltInParameterGroup enum")
except Exception as e:
	print("Failed to load BuiltInParameterGroup: {}".format(str(e)))
	# Fallback: create a dictionary of common parameter groups
	bipgs = []
	# Common BuiltInParameterGroup names that can be used
	common_groups = [
		'PG_IDENTITY_DATA',
		'PG_GEOMETRY', 
		'PG_MECHANICAL',
		'PG_ELECTRICAL_CIRCUITING',
		'PG_ELECTRICAL_LOADS',
		'PG_ELECTRICAL_POWER',
		'PG_ELECTRICAL_LIGHTING',
		'PG_FIRE_PROTECTION',
		'PG_PLUMBING',
		'PG_MATERIALS',
		'PG_MATERIALS_AND_FINISHES',
		'PG_PHASING',
		'PG_STRUCTURAL',
		'PG_CONSTRUCTION',
		'PG_CUSTOM',
		'PG_STRUCTURAL_ANALYSIS',
		'PG_TEXT',
		'PG_DATA',
		'PG_IFC',
		'PG_DIMENSIONS',
		'PG_GREEN_BUILDING',
		'PG_GREEN_PROPERTIES',
		'PG_LIFE_SAFETY',
		'PG_VISUALIZATION',
		'PG_ANALYSIS_RESULTS',
		'PG_REBAR_SYSTEM_LAYERS',
		'PG_SLAB_SHAPE_EDIT',
		'PG_FLEXIBLE',
		'PG_ENERGY_ANALYSIS',
		'PG_CONCEPTUAL_ENERGY_DATA',
		'PG_ENERGY_ANALYSIS_DETAILED_MODEL',
		'PG_ENERGY_ANALYSIS_BUILDING_DATA',
		'PG_STRUCTURAL_SECTION_GEOMETRY',
		'PG_DIVISION_GEOMETRY',
		'PG_SEGMENTS_FITTINGS',
		'PG_CONTINUOUSRAIL_BEGIN_END_BASE',
		'PG_CONTINUOUSRAIL_SUPPORTS',
		'PG_STAIRS_CALCULATOR_RULES',
		'PG_SUPPORT',
	]
	print("Using fallback common groups")
	
bipg_names = []
if bipgs:
	bipg_names = [str(a) for a in bipgs]
else:
	# Use fallback common groups
	bipg_names = common_groups

print("Total parameter groups available: {}".format(len(bipg_names)))
print("Sample groups: {}".format(bipg_names[:10] if len(bipg_names) > 10 else bipg_names))

print("\nMatching groups from Excel:")
for t in target_bipgs:
	if t in bipg_names:
		if bipgs:
			ind = bipg_names.index(t)
			fam_bipgs.append(bipgs[ind])
		else:
			# For fallback, we'll use the string directly
			fam_bipgs.append(t)
		print("  [OK] Found: '{}'".format(t))
	else:
		print("  [ERROR] NOT FOUND: '{}'".format(t))

print("\nMatched {}/{} groups".format(len(fam_bipgs), len(target_bipgs)))
print("=" * 60)

# Catch if we don't have all BIPG's
if len(fam_bipgs) != len(target_bipgs):
	forms.alert("Some groups not found, refer to report for details.", title="Script cancelled")
	# Show what was missing...
	print("\nNOT A VALID PARAMETER GROUP NAME:")
	print("---")
	for t in target_bipgs:
		if t not in bipg_names:
			print(t)
	script.exit()

# Function to convert string to BuiltInParameterGroup enum or ForgeTypeId
def str_to_bipg(bipg_str):
	"""Convert a string parameter group name to BuiltInParameterGroup enum or ForgeTypeId"""
	try:
		# Try ForgeTypeId approach first (newer Revit versions)
		from Autodesk.Revit.DB import GroupTypeId
		
		# Map common group names to GroupTypeId properties
		# Only use properties that actually exist
		group_map = {
			'PG_TEXT': 'Text',
			'PG_IDENTITY_DATA': 'IdentityData',
			'PG_GEOMETRY': 'Geometry',
			'PG_MECHANICAL': 'Mechanical',
			'PG_ELECTRICAL': 'Electrical',
			'PG_DATA': 'Data',
			'PG_IFC': 'Ifc',
			'PG_STRUCTURAL': 'Structural',
			'PG_CONSTRUCTION': 'Construction',
			'PG_PLUMBING': 'Plumbing',
			'PG_FIRE_PROTECTION': 'FireProtection',
			'PG_PHASING': 'Phasing',
			'PG_CUSTOM': 'Custom',
			'PG_MATERIALS': 'Materials',
			'PG_MATERIALS_AND_FINISHES': 'MaterialsAndFinishes',
			'PG_DIMENSIONS': 'Dimensions',
			'PG_GREEN_BUILDING': 'GreenBuilding',
			'PG_GREEN_PROPERTIES': 'GreenBuilding',  # Alias
			'PG_LIFE_SAFETY': 'LifeSafety',
			'PG_VISUALIZATION': 'Graphics',  # Visualization maps to Graphics
			'PG_ANALYSIS_RESULTS': 'AnalysisResults',
			'PG_ENERGY_ANALYSIS': 'EnergyAnalysis',
		}
		
		# First, check what's actually available
		available_attrs = [attr for attr in dir(GroupTypeId) if not attr.startswith('_') and not attr.startswith('Get') and not attr.startswith('To')]
		
		if bipg_str in group_map:
			attr_name = group_map[bipg_str]
			if hasattr(GroupTypeId, attr_name):
				result = getattr(GroupTypeId, attr_name)
				print("    Successfully mapped '{}' to GroupTypeId.{}".format(bipg_str, attr_name))
				return result
			else:
				print("    GroupTypeId.{} not found".format(attr_name))
				# Try to find similar names
				similar = [a for a in available_attrs if attr_name.lower() in a.lower() or a.lower() in attr_name.lower()]
				if similar:
					print("    Similar properties found: {}".format(similar))
					# Try the first similar one
					result = getattr(GroupTypeId, similar[0])
					print("    Using GroupTypeId.{} instead".format(similar[0]))
					return result
		
		# Try to get it dynamically by removing PG_ prefix
		clean_name = bipg_str.replace('PG_', '').replace('_', '')
		if hasattr(GroupTypeId, clean_name):
			result = getattr(GroupTypeId, clean_name)
			print("    Successfully mapped to GroupTypeId.{}".format(clean_name))
			return result
		
		# If nothing worked, show what's available and raise
		print("    Could not find mapping for '{}'".format(bipg_str))
		print("    Available GroupTypeId properties (first 20): {}".format(available_attrs[:20]))
		raise Exception("No matching GroupTypeId found for: {}".format(bipg_str))
		
	except Exception as e1:
		print("    ForgeTypeId approach failed: {}".format(str(e1)))
		try:
			# Fallback to old BuiltInParameterGroup enum
			import System
			from Autodesk.Revit.DB import BuiltInParameterGroup as BIPG
			result = System.Enum.Parse(BIPG, bipg_str)
			print("    Successfully used BuiltInParameterGroup enum for '{}'".format(bipg_str))
			return result
		except Exception as e2:
			print("    BuiltInParameterGroup enum approach also failed: {}".format(str(e2)))
			raise Exception("All conversion methods failed for: {}".format(bipg_str))

# Function to open family document
def famDoc_open(filePath, app):
	try:
		famDoc = app.OpenDocumentFile(filePath)
		return famDoc
	except:
		return None

# Function to close and save family document
def famDoc_close(famDoc, saveOpt=True):
	try:
		famDoc.Close(saveOpt)
		return 1
	except:
		return 0

# Functions to add parameters
def famDoc_addSharedParams(famDoc, famDefs, famBipgs, famInst, famForm = None):
	print("\n--- Processing family: {} ---".format(famDoc.Title))
	# Make sure document is a family document
	if famDoc.IsFamilyDocument:
		print("  [OK] Document is a family document")
		# Get family manager and parameter names
		famMan   = famDoc.FamilyManager
		parNames = [p.Definition.Name for p in famMan.Parameters]
		print("  Existing parameters in family: {}".format(len(parNames)))
		print("  Existing parameters: {}".format(parNames[:5] if len(parNames) > 5 else parNames))
		
		# Check if family has types, if not create one
		print("  Checking family types...")
		print("  Current family types: {}".format(famMan.Types.Size))
		if famMan.Types.Size == 0:
			print("  [WARNING] No family types exist, creating default type...")
		
		# Make a transaction
		t = DB.Transaction(famDoc, 'Add parameters')
		t.Start()
		print("  Transaction started")
		
		# Ensure we have at least one family type
		if famMan.Types.Size == 0:
			try:
				newType = famMan.NewType("Type 1")
				print("  [OK] Created new family type: '{}'".format(newType.Name))
			except Exception as e:
				print("  [ERROR] Failed to create family type: {}".format(str(e)))
		
		# Set current type to work with
		if famMan.Types.Size > 0:
			# Get first type by iterating
			for ftype in famMan.Types:
				famMan.CurrentType = ftype
				print("  Working with family type: '{}'".format(famMan.CurrentType.Name))
				break
		
		# Add parameters to document
		params = []
		for idx, (d, b, i, f) in enumerate(zip(famDefs, famBipgs, famInst, famForm)):
			print("\n  Processing parameter {}/{}: '{}'".format(idx+1, len(famDefs), d.Name))
			print("    Group: {}".format(b))
			print("    Is Instance: {}".format(i))
			print("    Formula: {}".format(f if f else "None"))
			
			# Convert string BIPG to enum if needed
			if isinstance(b, str):
				print("    Converting string '{}' to BIPG enum...".format(b))
				b = str_to_bipg(b)
				print("    Converted to: {}".format(b))
			
			if d.Name not in parNames:
				try:
					p = famMan.AddParameter(d, b, i)
					params.append(p)
					print("    [OK] Parameter added successfully")
					
					# Optional, set formulae - only if f is not None and not empty
					if f and str(f).strip():
						try:
							famMan.SetFormula(p, str(f))
							print("    [OK] Formula set: '{}'".format(f))
						except Exception as e:
							print("    [ERROR] Failed to set formula: {}".format(str(e)))
				except Exception as e:
					print("    [ERROR] Failed to add parameter: {}".format(str(e)))
			else:
				print("    [SKIP] Parameter already exists, skipping")
		
		# Commit transaction
		t.Commit()
		print("\n  Transaction committed")
		print("  Total parameters added: {}/{}".format(len(params), len(famDefs)))
		
		# Return parameters
		return params
	# If not a family document, return None
	else:
		print("  [ERROR] Document is NOT a family document")
		return None

# Finally undertake the process
print("\n" + "=" * 60)
print("STARTING FAMILY PROCESSING")
print("=" * 60)
print("Total families to process: {}".format(len(path_rfas)))
print("Parameters to add: {}".format(len(fam_defs)))

with forms.ProgressBar(step=1, title="Updating families", cancellable=True) as pb:
	# Create progress bar
	pbCount = 1
	pbTotal = len(path_rfas)
	passCount = 0
	# Run the process
	for filePath in path_rfas:
		print("\n" + "=" * 60)
		print("Processing family {}/{}".format(pbCount, pbTotal))
		print("File: {}".format(filePath))
		
		# Make sure not cancelled
		if pb.cancelled:
			print("CANCELLED by user")
			break
		else:
			famDoc = famDoc_open(filePath, app)
			if famDoc != None:
				print("[OK] Family opened successfully")
				pars = famDoc_addSharedParams(famDoc, fam_defs, fam_bipgs, fam_inst, fam_formulae)
				if pars is not None:
					print("Parameters returned: {}".format(len(pars)))
				else:
					print("No parameters returned (not a family document?)")
				
				if pb.cancelled or len(pars) == 0:
					print("Not saving (cancelled or no parameters added)")
					famDoc_close(famDoc, False)
				else:
					print("[OK] Saving and closing family")
					famDoc_close(famDoc)
					passCount += 1
			else:
				print("[ERROR] Failed to open family")
			# Update progress bar
			pb.update_progress(pbCount, pbTotal)
			pbCount += 1

print("\n" + "=" * 60)
print("PROCESSING COMPLETE")
print("Successfully updated: {}/{}".format(passCount, pbTotal))
print("=" * 60)

# Final message to user
form_message = str(passCount) + "/" + str(pbTotal) + " families updated."
forms.alert(form_message, title= "Script completed", warn_icon=False)