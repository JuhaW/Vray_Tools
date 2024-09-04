import bpy

from bpy.types import Operator, Menu
from bl_operators.presets import AddPresetBase

# The line `CLOUD_PRESET_FOLDER = "vray/clouds"` is defining a variable `CLOUD_PRESET_FOLDER` with the
# value `"vray/clouds"`. This variable is used to specify the folder path where the presets related to
# V-Ray clouds are stored. It helps in organizing and accessing the presets for V-Ray clouds in a
# specific directory within the Blender environment.
CLOUD_PRESET_FOLDER = "vray/clouds"

def Vray_Clouds_attr_get():
	"""
	This Python function reads a JSON file containing Vray Cloud attributes and extracts attributes
	starting with "clouds" to add them to a preset list.
	"""
	
	import json

	path = bpy.utils.script_path_user()
	# Opening JSON file
	f = open(path+ r"/addons/vray_blender/plugins_desc/light/SunLight.json")
	data = json.load(f)

	# Iterating through the json list
	print ("Cloud attributes from:", f.name)
	attr = [i["attr"] for  i in data["Parameters"] if i["attr"].startswith("clouds")]
		
	for x, i in enumerate(attr):
		print(x,i)
		#add them to preset list
		VRAYCLOUDS_AddPresetObjectDisplay.preset_values.append( "d." + i)
	
	f.close()

# The class ADD_OT_PRESET defines an operator in Python for adding a preset with specific properties.
class ADD_OT_PRESET(Operator):
	bl_idname = "add.preset"
	bl_label = "add preset"
	bl_description = "add preset"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		print ("Add preset")
		VRAYCLOUDS_AddPresetObjectDisplay.bl_idname


# The class `VRAYCLOUDS_MT_display_presets` defines a menu for displaying presets related to sun
# clouds in a Python script.
class VRAYCLOUDS_MT_display_presets(Menu):
	bl_label = "Sun Clouds Presets"
	preset_subdir = CLOUD_PRESET_FOLDER
	preset_operator = "script.execute_preset"
	draw = Menu.draw_preset


# This class defines an operator in Blender for adding a preset object display configuration for V-Ray
# Clouds.
class VRAYCLOUDS_AddPresetObjectDisplay(AddPresetBase, Operator):
	'''Add a Object Display Preset'''
	bl_idname = "camera.object_display_preset_add"
	bl_label = "Add Object Display Preset"
	preset_menu = "VRAYCLOUDS_MT_display_presets"
	
	# where to store the preset
	preset_subdir = CLOUD_PRESET_FOLDER
	# the operator this preset is assigned to
	# variable used for all preset values
	preset_defines = ["o = bpy.context.object",
							"d = o.data.vray.SunLight"]
						
	preset_values = []
	"""
	# properties to store in the preset
	preset_values = [
		"d.clouds_cirrus_amount",
		"d.clouds_contrails_distortion",
		"d.clouds_contrails_num_planes",
		"d.clouds_contrails_offset_x",
		"d.clouds_contrails_offset_y",
		"d.clouds_contrails_on",
		"d.clouds_contrails_strength",
		"d.clouds_contrails_time",
		"d.clouds_density",
		"d.clouds_density_multiplier",
		"d.clouds_enscape_compatibility",
		"d.clouds_ground_shadows",
		"d.clouds_height",
		"d.clouds_offset_x",
		"d.clouds_offset_y",
		"d.clouds_on",
		"d.clouds_phase_x",
		"d.clouds_phase_y",
		"d.clouds_seed",
		"d.clouds_thickness",
		"d.clouds_variety",
		]
	"""

	
	print ("Add preset")

# Display into an existing panel
def panel_func(self, context):
	"""
	The function `panel_func` creates a panel layout for VRay Sun settings with options for cloud
	presets.
	
	:param context: The `context` parameter in your `panel_func` function is a reference to the context
	in which the function is being called. It provides information about the current state of the
	Blender environment, such as the active object, selected objects, scene settings, and more. In your
	code snippet, you are
	:return: If the conditions in the if statement are not met (i.e., if the context object does not
	have a VRay SunLight or if the light type is not "SUN"), then the function will return without
	executing the rest of the code.
	"""
	
	#must be VRay Sun selected
	if (not hasattr(context.object.data.vray, "SunLight") or not context.object.data.vray.light_type=="SUN"):

		return

	layout = self.layout
	row = layout.row(align=True)

	row.label(text="Cloud Presets:", icon = "OUTLINER_DATA_VOLUME")
	row.menu(VRAYCLOUDS_MT_display_presets.__name__, text=VRAYCLOUDS_MT_display_presets.bl_label)
	#row.operator(ADD_OT_PRESET.bl_idname, text="", icon='MOD_SOFT')
	row.operator(VRAYCLOUDS_AddPresetObjectDisplay.bl_idname, text="", icon='ADD')
	row.operator(VRAYCLOUDS_AddPresetObjectDisplay.bl_idname, text="", icon='REMOVE').remove_active = True

#Panel VRAY_PT_context_lamp