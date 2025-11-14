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

xcl = xclUtils([],path_xcl)
dat = xcl.xclUtils_import(worksheet_name, 0, 0)

if not dat[1]:
	forms.alert("Worksheet '{}' not found in the Excel file.\n\nMake sure the name is correct.".format(worksheet_name),
				title="Worksheet Not Found")
	script.exit()

print("Reading worksheet: '{}' ({} rows, {} columns)".format(
	worksheet_name, len(dat[0]), len(dat[0][0]) if len(dat[0]) > 0 else 0))


targets_params, target_bipgs, fam_inst, fam_formulae = [],[],[],[]

for idx, row in enumerate(dat[0][1:]):
	# Skip rows with insufficient columns
	if len(row) < 4:
		continue
	
	# Column A: Parameter Name - skip if empty
	param_name = row[0] if row[0] else ""
	if not param_name or str(param_name).strip() == "":
		continue
	
	targets_params.append(param_name)
	
	# Column B: Group Name
	bipg_name = row[1] if len(row) > 1 and row[1] else ""
	target_bipgs.append(bipg_name)
	
	# Column C: Instance (Yes/No)
	is_instance = row[2] == "Yes" if len(row) > 2 else False
	fam_inst.append(is_instance)
	
	# Column D: Formula (optional)
	formula = None
	if len(row) > 3 and row[3] is not None and str(row[3]).strip():
		# Try to convert to number first (preserves decimals)
		try:
			num_val = float(row[3])
			if num_val == int(num_val):
				formula = str(int(num_val))  # Whole number
			else:
				formula = '{:.10f}'.format(num_val).rstrip('0').rstrip('.')  # Decimal
		except (ValueError, TypeError):
			# Not a number - treat as text/formula
			formula = str(row[3]).strip()
			# Add spaces around operators for Revit
			import re
			formula = re.sub(r'([^\s\d])\*([^\s])', r'\1 * \2', formula)
			formula = re.sub(r'([^\s])/([^\s])', r'\1 / \2', formula)
			formula = re.sub(r'([^\s])\+([^\s])', r'\1 + \2', formula)
			formula = re.sub(r'([^\s])-([^\s])', r'\1 - \2', formula)
	fam_formulae.append(formula)

print("Processed {} parameters from Excel".format(len(targets_params)))

# Get shared parameters
app = __revit__.Application
fam_defs  = []
fam_bipgs = []

spFile = app.OpenSharedParameterFile()

# Create shared parameters file if it doesn't exist
if spFile is None:
	import os
	sp_file_path = os.path.join(os.path.expanduser("~"), "Documents", "SharedParameters.txt")
	
	if not os.path.exists(sp_file_path):
		with open(sp_file_path, 'w') as f:
			f.write("# This is a Revit shared parameter file.\n")
			f.write("# Do not edit manually.\n")
			f.write("*META\tVERSION\tMINVERSION\n")
			f.write("META\t2\t1\n")
			f.write("*GROUP\tID\tNAME\n")
			f.write("GROUP\t1\tPG_TEXT\n")
			f.write("*PARAM\tGUID\tNAME\tDATATYPE\tDATACATEGORY\tGROUP\tVISIBLE\tDESCRIPTION\tUSERMODIFIABLE\tHIDEWHENNOVALUE\n")
	
	app.SharedParametersFilename = sp_file_path
	spFile = app.OpenSharedParameterFile()
	
	if spFile is None:
		forms.alert("Could not create shared parameters file.\n\nPlease configure manually in:\nManage -> Shared Parameters", 
					title="Script Cancelled")
		script.exit()

spGroups = spFile.Groups
sp_defs, sp_nams = [],[]

for g in spGroups:
	for d in g.Definitions:
		sp_defs.append(d)
		sp_nams.append(d.Name)

# Match parameters
for t in targets_params:
	if t in sp_nams:
		ind = sp_nams.index(t)
		fam_defs.append(sp_defs[ind])

# Check for missing parameters
if len(fam_defs) != len(targets_params):
	missing_params = [t for t in targets_params if t not in sp_nams]
	
	create_params = forms.alert(
		"Missing parameters:\n\n{}\n\nCreate them automatically?".format("\n".join(missing_params)),
		title="Missing Parameters", yes=True, no=True)
	
	if create_params:
		# Get or create PG_TEXT group
		pg_text_group = None
		for g in spGroups:
			if g.Name == "PG_TEXT":
				pg_text_group = g
				break
		if pg_text_group is None:
			pg_text_group = spGroups.Create("PG_TEXT")
		
		# Create missing parameters
		for param_name in missing_params:
			try:
				ext_def_options = DB.ExternalDefinitionCreationOptions(param_name, DB.ParameterType.Text)
				ext_def_options.GUID = System.Guid.NewGuid()
				new_def = pg_text_group.Definitions.Create(ext_def_options)
				sp_defs.append(new_def)
				sp_nams.append(new_def.Name)
			except Exception as e:
				print("Failed to create {}: {}".format(param_name, str(e)))
		
		# Refresh definitions
		fam_defs = []
		for t in targets_params:
			if t in sp_nams:
				ind = sp_nams.index(t)
				fam_defs.append(sp_defs[ind])
		
		print("Created {} missing parameters".format(len(missing_params)))
	else:
		script.exit()

if len(fam_defs) != len(targets_params):
	forms.alert("Some parameters are still missing. Cannot continue.", title="Script Cancelled")
	script.exit()

# Validate parameter groups
import System
from System import Enum

try:
	import clr
	clr.AddReference('RevitAPI')
	from Autodesk.Revit.DB import BuiltInParameterGroup
	bipgs = [a for a in System.Enum.GetValues(BuiltInParameterGroup)]
except:
	bipgs = []

# Common groups as fallback
common_groups = ['PG_IDENTITY_DATA', 'PG_GEOMETRY', 'PG_MECHANICAL', 'PG_FIRE_PROTECTION', 
				 'PG_PLUMBING', 'PG_MATERIALS', 'PG_STRUCTURAL', 'PG_CONSTRUCTION', 'PG_TEXT', 
				 'PG_DATA', 'PG_GREEN_BUILDING', 'PG_GREEN_PROPERTIES', 'PG_LIFE_SAFETY', 'PG_VISUALIZATION']

bipg_names = [str(a) for a in bipgs] if bipgs else common_groups

# Match groups
for t in target_bipgs:
	if t in bipg_names:
		if bipgs:
			ind = bipg_names.index(t)
			fam_bipgs.append(bipgs[ind])
		else:
			fam_bipgs.append(t)

# Validate all groups found
if len(fam_bipgs) != len(target_bipgs):
	missing = [t for t in target_bipgs if t not in bipg_names]
	forms.alert("Invalid parameter groups:\n\n{}".format("\n".join(missing)), title="Script Cancelled")
	script.exit()

def str_to_bipg(bipg_str):
	"""Convert string group name to GroupTypeId or BuiltInParameterGroup"""
	try:
		from Autodesk.Revit.DB import GroupTypeId
		
		group_map = {
			'PG_TEXT': 'Text', 'PG_IDENTITY_DATA': 'IdentityData', 'PG_GEOMETRY': 'Geometry',
			'PG_MECHANICAL': 'Mechanical', 'PG_ELECTRICAL': 'Electrical', 'PG_DATA': 'Data',
			'PG_STRUCTURAL': 'Structural', 'PG_CONSTRUCTION': 'Construction', 'PG_PLUMBING': 'Plumbing',
			'PG_FIRE_PROTECTION': 'FireProtection', 'PG_MATERIALS': 'Materials',
			'PG_GREEN_BUILDING': 'GreenBuilding', 'PG_GREEN_PROPERTIES': 'GreenBuilding',
			'PG_LIFE_SAFETY': 'LifeSafety', 'PG_VISUALIZATION': 'Graphics',
		}
		
		if bipg_str in group_map:
			attr_name = group_map[bipg_str]
			if hasattr(GroupTypeId, attr_name):
				return getattr(GroupTypeId, attr_name)
		
		# Try dynamic mapping
		clean_name = bipg_str.replace('PG_', '').replace('_', '')
		if hasattr(GroupTypeId, clean_name):
			return getattr(GroupTypeId, clean_name)
		
		raise Exception("No GroupTypeId found for: {}".format(bipg_str))
	except:
		# Fallback to BuiltInParameterGroup enum
		import System
		from Autodesk.Revit.DB import BuiltInParameterGroup as BIPG
		return System.Enum.Parse(BIPG, bipg_str)

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

def famDoc_addSharedParams(famDoc, famDefs, famBipgs, famInst, famForm = None):
	"""Add shared parameters to family document"""
	if not famDoc.IsFamilyDocument:
		return None
	
	famMan = famDoc.FamilyManager
	parNames = [p.Definition.Name for p in famMan.Parameters]
	
	t = DB.Transaction(famDoc, 'Add parameters')
	t.Start()
	
	# Ensure at least one family type exists
	if famMan.Types.Size == 0:
		famMan.NewType("Type 1")
	
	# PASS 1: Add parameters without formulas
	params = []
	params_with_formulas = []
	
	for d, b, i, f in zip(famDefs, famBipgs, famInst, famForm):
		# Convert string group to GroupTypeId/enum
		if isinstance(b, str):
			b = str_to_bipg(b)
		
		if d.Name not in parNames:
			try:
				p = famMan.AddParameter(d, b, i)
				params.append(p)
				if f and str(f).strip():
					params_with_formulas.append((p, str(f)))
			except Exception as e:
				print("Failed to add {}: {}".format(d.Name, str(e)))
		else:
			# Get existing parameter for formula setting
			for existing_p in famMan.Parameters:
				if existing_p.Definition.Name == d.Name:
					if f and str(f).strip():
						params_with_formulas.append((existing_p, str(f)))
					break
	
	# PASS 2: Set formulas
	formula_success = 0
	for p, formula in params_with_formulas:
		try:
			famMan.SetFormula(p, formula)
			formula_success += 1
		except Exception as e:
			print("Formula failed for {}: {}".format(p.Definition.Name, str(e)))
	
	t.Commit()
	
	print("Added {}/{} parameters, set {}/{} formulas".format(
		len(params), len(famDefs), formula_success, len(params_with_formulas)))
	
	return params

# Process families
print("\nProcessing {} families with {} parameters...".format(len(path_rfas), len(fam_defs)))

with forms.ProgressBar(step=1, title="Updating families", cancellable=True) as pb:
	passCount = 0
	for idx, filePath in enumerate(path_rfas, 1):
		if pb.cancelled:
			break
		
		famDoc = famDoc_open(filePath, app)
		if famDoc:
			pars = famDoc_addSharedParams(famDoc, fam_defs, fam_bipgs, fam_inst, fam_formulae)
			if pars and len(pars) > 0 and not pb.cancelled:
				famDoc_close(famDoc)
				passCount += 1
			else:
				famDoc_close(famDoc, False)
		
		pb.update_progress(idx, len(path_rfas))

print("\nCompleted: {}/{} families updated".format(passCount, len(path_rfas)))
forms.alert("{}/{} families updated successfully".format(passCount, len(path_rfas)), 
			title="Script Completed", warn_icon=False)