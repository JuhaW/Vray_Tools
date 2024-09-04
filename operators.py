import bpy

from bpy.props import BoolProperty
from . import functions as F
from . import show_image_textures as ImgTex
from bpy.types import Operator
from bl_operators.presets import AddPresetBase
import sys
import inspect


#===================================
#
#===================================


#===================================
#NODE TREE CHANGE
#===================================
class Nodetree_OT_type_change(bpy.types.Operator):
	
	bl_idname = "nodetree.change"
	bl_label = "node"
	bl_description = "nodetree change"
	bl_options = {'REGISTER', 'UNDO'}

	def next_nodetree_type(self, current_type):
		items = ["SHADER", "OBJECT", "WORLD"]
		next_item = items[(items.index(current_type) + 1) % len(items)]
		print("The next item is:", next_item)
		return next_item

	def execute(self, context):

		context.area.ui_type = 'VRayNodeTreeEditor'

		o = context.active_object
		print("active object:",o.name)	
		# object has node tree ?
		#nt = hasattr(o.data, "node_tree")		
		
		#nt_type = o.data.node_tree.type
		# set Node Editor node tree type
		wm = context.window_manager
		wm.vrayTreeType = self.next_nodetree_type(wm.vrayTreeType) # "SHADER", "WORLD", "OBJECT"
		# update node editor
		context.area.tag_redraw()
		context.area.ui_type = 'VRayNodeTreeEditor'
		return {'FINISHED'}


#===================================
#IMAGE TEXTURE
#===================================
class Vray_Mat_Show_Texture(bpy.types.Operator):
	'''Show objects uv mapped image textures on viewport'''
	bl_idname = "object.vray_show_textures"
	bl_label = "Show image textures"

	def execute(self, context):

		context.space_data.shading.type = 'SOLID'
		context.space_data.shading.color_type = 'TEXTURE'

		
		if context.scene.addon.show_texture_all_objects:
			sel_objs = [i for i in bpy.context.view_layer.objects if i.type == 'MESH']
		else:
			sel_objs = [i for i in bpy.context.view_layer.objects.selected if i.type == 'MESH']

		for o in sel_objs:
			F.remove_blender_nodes(o)
			#context.view_layer.objects.active = o
			ImgTex.find_material_image(o)
		
		return {'FINISHED'}	


class Vray_Delete_Blender_OT_Nodes(bpy.types.Operator):
	
	bl_idname = "vray.delete_blender_nodes"
	bl_label = "Delete Blendernodes"
	bl_description = "Delete Blender nodes"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		F.remove_blender_nodes(context.object)
		return {'FINISHED'}

#===================================
#SHADOW CATCHER
#===================================
class Vray_Shadow_Catcher_On(bpy.types.Operator):
	"""Set selected objects shadow catcher"""
	bl_idname = "vray.shadow_catcher_on"
	bl_label = "Enable Shadow Catcher"
	#bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	
	on : BoolProperty( default = True)

	@classmethod
	def poll(cls, context):
		cls.poll_message_set("Please select an object")
		
		if context.view_layer.objects.active and context.view_layer.objects.active.select_get():
			return F.v_ray_is_shadow_catcher_object_type(context.object) and not F.v_ray_is_shadow_catcher_object(context.object)
		return False			
		

	def execute(self, context):
				
		F.vray_shadow_catcher(self.on)
		
		return {'FINISHED'}


class Vray_Shadow_Catcher_Off(bpy.types.Operator):
	"""Disable selected objects shadow catcher"""
	bl_idname = "vray.shadow_catcher_off"
	bl_label = "Disable Shadow Catcher"
	#bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	
	on : bpy.props.BoolProperty( default = False)
	
	@classmethod
	def poll(cls, context):
		#cls.poll_message_set("Please select an object")
		return context.view_layer.objects.active and context.view_layer.objects.active.select_get() and F.v_ray_is_shadow_catcher_object(context.object)
		

	def execute(self, context):
				
		F.vray_shadow_catcher(self.on)
		
		return {'FINISHED'}


class Vray_Select_Object(bpy.types.Operator):
	
	bl_idname = "object.vray_select_object"
	bl_label = "Select object"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	
	idx : bpy.props.IntProperty(default = 0)

	def execute(self, context):

		cnt = len(context.scene.addon.shadow_catcher_objects)
		#make sure there are no deleted shadow catcher objects
		F.vray_shadow_catcher_objects_get()
		if cnt == len(context.scene.addon.shadow_catcher_objects) and context.scene.addon.shadow_catcher_objects:
			F.vray_select_object(self.idx)
		
		return {'FINISHED'}
