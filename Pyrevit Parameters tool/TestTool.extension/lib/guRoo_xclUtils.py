# -*- coding: UTF-8 -*-

# import Excel dependent libraries
import clr
import System
from System import Array,Type, Activator
from System.Collections.Generic import *
from System.Runtime.InteropServices import Marshal

clr.AddReference('System.Drawing')
import System.Drawing
from System.Drawing import *

# Try and get specific interop, if not just the general one
try:
    clr.AddReference('Microsoft.Office.Interop.Excel')
except:
    clr.AddReferenceToFileAndPath(r'C:\Windows\assembly\GAC_MSIL\Microsoft.Office.Interop.Excel\15.0.0.0__71e9bce111e9429c\Microsoft.Office.Interop.Excel.dll')


from Microsoft.Office.Interop import Excel

# Force int or string
def xclUtils_strFix(s):
	try:
		fix = str(int(s))
	except:
		fix = str(s)
	return fix

# Excel utility class
# Thanks Cyril Poupin for most of this code with some tweaks...
class xclUtils():
	
	def __init__(self, lstData, filepath):
		self.lstData = lstData
		self.filepath = filepath

	# Define import function
	def xclUtils_import(self,wsName,col=0,row=0):
		ex = None
		workbook = None
		dataOut = []
		wsFound = False
		
		try:
			# Create Excel Application using COM with proper reflection
			excelType = Type.GetTypeFromProgID("Excel.Application")
			ex = Activator.CreateInstance(excelType)
			
			# Use reflection to set properties for COM object
			import System.Reflection
			
			# Set Visible property
			excelType.InvokeMember("Visible", 
				System.Reflection.BindingFlags.SetProperty, 
				None, ex, Array[object]([False]))
			
			# Set DisplayAlerts property
			excelType.InvokeMember("DisplayAlerts", 
				System.Reflection.BindingFlags.SetProperty, 
				None, ex, Array[object]([False]))
			
			# Open workbook
			workbooksObj = excelType.InvokeMember("Workbooks",
				System.Reflection.BindingFlags.GetProperty,
				None, ex, None)
			
			workbookType = workbooksObj.GetType()
			workbook = workbookType.InvokeMember("Open",
				System.Reflection.BindingFlags.InvokeMethod,
				None, workbooksObj, Array[object]([self.filepath]))
			
			# Debug: Print all available worksheet names
			print("DEBUG: Available worksheets in Excel file:")
			
			workbookType = workbook.GetType()
			worksheetsObj = workbookType.InvokeMember("Worksheets",
				System.Reflection.BindingFlags.GetProperty,
				None, workbook, None)
			
			worksheetsType = worksheetsObj.GetType()
			worksheetCount = int(worksheetsType.InvokeMember("Count",
				System.Reflection.BindingFlags.GetProperty,
				None, worksheetsObj, None))
			
			for i in range(1, worksheetCount + 1):
				ws_temp = worksheetsType.InvokeMember("Item",
					System.Reflection.BindingFlags.GetProperty,
					None, worksheetsObj, Array[object]([i]))
				ws_name = ws_temp.GetType().InvokeMember("Name",
					System.Reflection.BindingFlags.GetProperty,
					None, ws_temp, None)
				print("  Sheet {}: '{}'".format(i, ws_name))
			
			# Try to get the worksheet, if not pass
			try:
				# Try by name first
				ws = worksheetsType.InvokeMember("Item",
					System.Reflection.BindingFlags.GetProperty,
					None, worksheetsObj, Array[object]([wsName]))
				wsFound = True
				print("DEBUG: Found worksheet by name: '{}'".format(wsName))
			except Exception as e1:
				print("DEBUG: Failed to find by name '{}': {}".format(wsName, str(e1)))
				# Try by index if it's the first sheet
				try:
					ws = worksheetsType.InvokeMember("Item",
						System.Reflection.BindingFlags.GetProperty,
						None, worksheetsObj, Array[object]([1]))
					ws_name = ws.GetType().InvokeMember("Name",
						System.Reflection.BindingFlags.GetProperty,
						None, ws, None)
					if ws_name == wsName:
						wsFound = True
						print("DEBUG: Found worksheet by index 1")
					else:
						print("DEBUG: First sheet name '{}' doesn't match '{}'".format(ws_name, wsName))
						wsFound = False
				except Exception as e3:
					print("DEBUG: Failed to get by index: {}".format(str(e3)))
					wsFound = False
			
			# If worksheet is found
			if wsFound:
				print("DEBUG: Reading data from worksheet...")
				wsType = ws.GetType()
				
				# Get UsedRange
				usedRange = wsType.InvokeMember("UsedRange",
					System.Reflection.BindingFlags.GetProperty,
					None, ws, None)
				urType = usedRange.GetType()
				
				# Get Columns and Rows
				columnsObj = urType.InvokeMember("Columns",
					System.Reflection.BindingFlags.GetProperty,
					None, usedRange, None)
				rowsObj = urType.InvokeMember("Rows",
					System.Reflection.BindingFlags.GetProperty,
					None, usedRange, None)
				
				# Have row and column been specified
				if col == 0:
					colCountF = int(columnsObj.GetType().InvokeMember("Count",
						System.Reflection.BindingFlags.GetProperty,
						None, columnsObj, None))
				else:
					colCountF = col
				if row == 0:
					rowCountF = int(rowsObj.GetType().InvokeMember("Count",
						System.Reflection.BindingFlags.GetProperty,
						None, rowsObj, None))
				else:
					rowCountF = row
				
				print("DEBUG: Rows: {}, Columns: {}".format(rowCountF, colCountF))
				
				# Read all data cell by cell using Cells property
				dataOut = []
				print("DEBUG: Reading data row by row...")
				
				for i in range(1, rowCountF + 1):
					row_data = []
					for j in range(1, colCountF + 1):
						try:
							# Get each cell using Cells property
							cell = wsType.InvokeMember("Cells",
								System.Reflection.BindingFlags.GetProperty,
								None, ws, Array[object]([i, j]))
							
							# Get cell value
							cell_value = cell.GetType().InvokeMember("Value2",
								System.Reflection.BindingFlags.GetProperty,
								None, cell, None)
							
							row_data.append(xclUtils_strFix(cell_value) if cell_value is not None else "")
						except Exception as e:
							print("DEBUG: Error reading cell ({}, {}): {}".format(i, j, str(e)))
							row_data.append("")
					
					dataOut.append(row_data)
					if i <= 3:  # Print first 3 rows for debugging
						print("DEBUG: Row {}: {}".format(i, row_data))
				
				print("DEBUG: Successfully read {} rows".format(len(dataOut)))
			
			# If worksheet is not found
			else:
				print("DEBUG: Worksheet '{}' was not found".format(wsName))
				dataOut = []
		
		except Exception as e:
			print("DEBUG: Exception in xclUtils_import: {}".format(str(e)))
			import traceback
			print("DEBUG: Traceback:")
			print(traceback.format_exc())
			dataOut = []
			wsFound = False
		
		finally:
			# Close and cleanup
			try:
				if workbook is not None:
					workbookType = workbook.GetType()
					workbookType.InvokeMember("Close",
						System.Reflection.BindingFlags.InvokeMethod,
						None, workbook, Array[object]([False]))
			except:
				pass
			
			try:
				if ex is not None:
					excelType.InvokeMember("Quit",
						System.Reflection.BindingFlags.InvokeMethod,
						None, ex, None)
			except:
				pass
			
			# Release COM objects
			try:
				if workbook is not None:
					Marshal.ReleaseComObject(workbook)
				if ex is not None:
					Marshal.ReleaseComObject(ex)
			except:
				pass
			
			# Clean up
			workbook = None
			ex = None
		
		return [dataOut, wsFound]