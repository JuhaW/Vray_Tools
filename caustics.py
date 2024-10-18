import bpy
from . import operators as Op

class Vray_Caustics_PT_Panel(bpy.types.Panel):
	
	#bl_parent_id = "VRAYTOOLS_PT_Panel"
	bl_idname = "VRAYCAUSTICS_PT_Panel"
	bl_label = "V-Ray Caustics"
	bl_space_type = "NODE_EDITOR"
	bl_region_type = "UI"
	bl_category = "Node"
	
	@classmethod
	def poll(self, context):
		return context.active_node and context.active_node.vray_plugin == 'BRDFVRayMtl'
	
	def draw(self, context):
		layout = self.layout
		
		row = layout.row()
		row.operator(Op.Vray_Caustics_OT_Nodes.bl_idname, text="Set Caustics",icon="STICKY_UVS_DISABLE")
		row = layout.row()
		row.prop(context.active_node.inputs['Fog Color'] , "value")
		row = layout.row()
		row.label(text="Depth (cm):")
		row.prop(context.active_node.inputs['Depth (cm)'] , "value", text ="")
		
		
		
		