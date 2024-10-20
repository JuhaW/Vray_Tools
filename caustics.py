import bpy
from . import operators as Op

class Vray_Caustics_PT_Panel(bpy.types.Panel):
	
	#bl_parent_id = "VRAYTOOLS_PT_Panel"
	#bl_parent_id = "NODE_PT_active_node_generic"
	bl_idname = "VRAYCAUSTICS_PT_Panel"
	bl_label = "V-Ray Caustics"
	bl_space_type = "NODE_EDITOR"
	bl_region_type = "UI"
	bl_category = "Node"
	
	@classmethod
	def poll(self, context):
		return context.active_node and context.active_node.select and hasattr(context.active_node,"vray_plugin") and context.active_node.vray_plugin == 'BRDFVRayMtl'
	
	def draw(self, context):
		layout = self.layout
		
		row = layout.row(align=True)
		row.operator(Op.Vray_Caustics_OT_Nodes.bl_idname, text="Set Caustics",icon="STICKY_UVS_DISABLE")
		caust_icon = "HIDE_OFF" if context.scene.vray.SettingsCaustics.on else "HIDE_ON"
		row.prop(context.scene.vray.SettingsCaustics, "on", text="", toggle=True, icon = caust_icon)

		row = layout.row(align=True)
		row.prop(context.active_node.inputs['Fog Color'] , "value")
		
		row = layout.row(align=True)
		row.label(text="Depth (cm):")
		row.prop(context.active_node.inputs['Depth (cm)'] , "value", text="")
		
		row = layout.row(align=True)
		row.label(text=context.active_node.inputs['Refraction IOR'].identifier)
		row.prop(context.active_node.inputs['Refraction IOR'] , "value", text="")
		
		

		
		