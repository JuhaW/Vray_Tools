
bl_info = {
	"name" : "V-Ray Tools",
	"description" : "V-Ray Tools to help",
	"author" : "JuhaW",
	"version" : (1, 0, 0),
	"blender" : (4, 1, 1),
	"location" : "Node",
	"warning" : "",
	"support" : "COMMUNITY",
	"doc_url" : "",
	"category" : "3D View"
}

import bpy
from bpy.utils import register_classes_factory
from bpy.props import BoolProperty, PointerProperty, CollectionProperty, StringProperty
import sys
import inspect
from . import functions as F
#from . import delete_blender_nodes as dbn
from . import show_image_textures as ImgTex
from . import operators as Op
from . import panels as P
from . import clouds as SunClouds
from . import caustics
from . import lights 

import importlib.util
#        10        20        30        40        50        60        70        80        90        100
#234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
addon_keymaps=[]

def keymap(mode = "init"):
	global menu_keymap

	match mode:
		case "init":
			wm = bpy.context.window_manager
			kc = wm.keyconfigs.addon
			if kc:
				km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
				kmi = km.keymap_items.new(Op.Nodetree_OT_type_change.bl_idname, 'E','PRESS')
				addon_keymaps.append((km, kmi))
			
		case "remove":
			for km, kmi in addon_keymaps:
				km.keymap_items.remove(kmi)
			addon_keymaps.clear()

	
def update_lights(self, context):
	
	print("Lights changed", self.on, self.light_type)	
	
	#prevents error if light type is not set
	if not self.light_type:
		return
	
	for i in lights.LIGHTS[self.light_type]["objects"]:
		o = bpy.data.objects[i] 
		o.hide_set(not self.on)
		o.hide_viewport = not self.on
		o.hide_render = not self.on
		


class Shadow_Catch(bpy.types.PropertyGroup):
	obj: PointerProperty(type=bpy.types.Object)

class Lights_on(bpy.types.PropertyGroup):
	on 			: BoolProperty(default = True, update=update_lights,description="If ON, set lights on. If OFF, set lights off")
	light_type	: StringProperty()

class Addon_variables(bpy.types.PropertyGroup):

	shadow_catcher_objects 		: CollectionProperty(type=Shadow_Catch)
	show_texture_all_objects 	: BoolProperty(default = True, description="If ON, set image textures to all objects. If OFF, set only selected objects image textures")
	lights 		: CollectionProperty(type=Lights_on)

class Vray_Tools_PT_Panel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "VRay Tools Panel"
	bl_idname = "VRAYTOOLS_PT_Panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "V-Ray Tools"

	#bl_context = "object"


	def draw(self, context):
		layout = self.layout
		
		#row = layout.row()
		#row.label(text="V-Ray Tools Panel")
		#row = layout.row();row.operator("vray.delete_blender_nodes", icon="REMOVE")
		#row = layout.row()


class Vray_IMAGE_TEXTURE_PT_Panel(bpy.types.Panel):
	
	bl_parent_id = "VRAYTOOLS_PT_Panel"
	bl_idname = "VRAYIMAGETEXTURE_PT_Panel"
	bl_label = "Show image textures"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"

	def draw(self, context):
		layout = self.layout
		
		row = layout.row()
		row.prop(context.scene.addon, "show_texture_all_objects", text="All objects")#, icon="RESTRICT_SELECT_OFF")
		row = layout.row()
		row.operator("object.vray_show_textures", icon="TEXTURE_DATA")


class Vray_Shadow_Catcher_PT_Panel(bpy.types.Panel):
	
	bl_parent_id = "VRAYTOOLS_PT_Panel"
	bl_idname = "VRAYSHADOWCATCHER_PT_Panel"
	bl_label = "Shadow Catcher"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"

	def draw(self, context):
		layout = self.layout
		
		row = layout.row()
		row.operator(Op.Vray_Shadow_Catcher_On.bl_idname, text="Enable",icon="ADD")
		row.operator(Op.Vray_Shadow_Catcher_Off.bl_idname, text="Disable", icon="REMOVE")
		row = layout.row()
		
		#row.label(text="Shadow Catcher objects:")
		#row = layout.row()
		for idx, i in enumerate(context.scene.addon.shadow_catcher_objects):
			a =  i.obj.name
			row.operator(Op.Vray_Select_Object.bl_idname, text="", icon="RESTRICT_SELECT_OFF").idx = idx
			row.label(text=a)
			row = layout.row()


# Get all Blender classes defined in the current module, checking "bl_rna"
#classes = [(name, cls) for name, cls in inspect.getmembers(__import__(__name__), inspect.isclass) if "bl_rna" in dir(cls)]
#mod_name = __import__(__name__)

# Module information
#module_name = "delete_blender_nodes"
#module_file = "C:/Blender addons/addons/Vray_Tools/delete_blender_nodes.py"


def register():
	
	

	F.register_classes(ImgTex)
	F.register_classes(Op)
	F.register_classes(P)
	F.register_classes(SunClouds)
	F.register_classes(caustics)
	
	
	# Sun clouds presets
	bpy.types.VRAY_PT_context_lamp.append(SunClouds.panel_func)
	SunClouds.Vray_Clouds_attr_get()

	F.register_classes(__package__) #this __init__.py file
	bpy.types.Scene.addon = bpy.props.PointerProperty(type=Addon_variables)
	
	F.register_classes(lights)

	keymap(mode="init")


def unregister():

	F.unregister_classes(lights)
	F.unregister_classes(caustics)
	F.unregister_classes(Op)
	F.unregister_classes(ImgTex)
	F.unregister_classes(P)
	F.unregister_classes(SunClouds)
	F.unregister_classes(__package__)

	print("Removing Sun Clouds Presets")
	print(bpy.types.VRAY_PT_context_lamp)
	#Sun clouds presets
	bpy.types.VRAY_PT_context_lamp.remove(SunClouds.panel_func)
	del bpy.types.Scene.addon
	
	keymap(mode="remove")
	
		
if __name__ == '__main__':
	register()


"""

Nodes:




#V-Ray light types
[i.data.vray.light_type for i in C.selected_objects]
['MESH', 'IES', 'SPOT', 'OMNI', 'DIRECT', 'AMBIENT', 'SUN']

#change negative scales to positive for V-Ray
import bpy

for i in bpy.context.view_layer.objects:
	chk = False
	if i.scale.x < 0:
		i.scale.x = - i.scale.x
		chk = True
	if i.scale.y < 0:
		i.scale.y = - i.scale.y
		chk = True
	if i.scale.z < 0:
		i.scale.z = - i.scale.z
		chk = True
	if chk:
		print ("Scale was negative:", i.name)

"""



"""
import bpy


C = bpy.context

def VRay():
	# set Node Editor node tree type
	C.window_manager.vrayTreeType = "SHADER" #"WORLD", "OBJECT"



	# update V-Ray Node Editor
	C.window.screen.areas[7].tag_redraw()
	

def VRay_find_node_editor(C):	
	#find V-Ray Node Editor window

	for area in C.screen.areas:
		if area.type == 'NODE_EDITOR':
			print("found node editor")
			ret = area
			break
	else:
		print("for else")
		ret = None
			
	return ret

#V-Ray node editor
C.screen.areas[7].ui_type = 'VRayNodeTreeEditor'



				
n_editor = VRay_find_node_editor(C)
if n_editor:
	print (n_editor.type)


# object has node tree ?
#hasattr(o.data, "node_tree")

#yes, get node tree type
#o.data.node_tree.type
"""