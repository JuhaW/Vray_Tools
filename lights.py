import bpy
from . __init__ import Vray_Tools_PT_Panel #VRAYLIGHTS_PT_Panel

LIGHTS = {}


def draw_panel(self, context, light_type):
	
	def splitter(col3):

		split = col3.split(factor=0.3, align=True)
		col3 = split.column(align=True)
		row = col3.row(align=True)
		return split,col3, row

	layout = self.layout
	for o in LIGHTS[light_type]["objects"]:
		split = layout.split(factor=0.05)

		col1 = split.column(align=True)
		col1.label(text="")
		split = split.split(factor=0.5, align=True)
		col2 = split.column(align=True)
		
		if context.view_layer.objects.active == context.view_layer.objects[o]:
			col2.emboss = 'NORMAL'
		else:
			col2.emboss = 'PULLDOWN_MENU'
		
		#col2.alignment = 'LEFT'
		col2.operator("object.select_object", text=o).obj = o
		
		col3 = split.column()
		od = bpy.data.objects[o].data.vray
		if light_type == "SUN":
			split, col3, row = splitter(col3)
			row.prop(od.SunLight, "filter_color", text="")
			row = split.column(align=True)
			row.prop(od.SunLight, "intensity_multiplier", text="")

		elif light_type =="RECT":
			#split = col3.split(factor=0.3, align=True)
			#col3 = split.column(align=True)
			#row = col3.row(align=True)
			split, col3, row = splitter(col3)
			row.prop(od.LightRectangle, "color_colortex", text="")
			row = split.column(align=True)
			row.prop(od.LightRectangle, "intensity", text="")

		elif light_type =="SPHERE":
			#split = col3.split(factor=0.3, align=True)
			#col3 = split.column(align=True)
			#row = col3.row(align=True)
			split, col3, row = splitter(col3)
			row.prop(od.LightSphere, "color_colortex", text="")
			row = split.column(align=True)
			row.prop(od.LightSphere, "intensity", text="")

		elif light_type =="SPOT":
			split, col3, row = splitter(col3)
			row.prop(od.LightSpot, "color_colortex", text="")
			row = split.column(align=True)
			row.prop(od.LightSpot, "intensity", text="")

		else:
			pass
		
		#bpy.data.lights["VRayRectLight"].vray.LightRectangle.color_colortex
		#row.label(text=o.name)
#bpy.data.lights["VRaySunLight"].vray.SunLight.filter_color sun
#bpy.data.lights["VRayDomeLight.001"].node_tree.nodes["Light Dome"].inputs['Color'].value 

def select(obj_name):

	bpy.ops.object.select_all(action='DESELECT')
	bpy.data.objects[obj_name].select_set(True)
	bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]

class Vray_Lights_PT_Panel(bpy.types.Panel):
	
	bl_parent_id = "VRAYTOOLS_PT_Panel"
	bl_idname = "VRAYLIGHTS_PT_Panel"
	bl_label = "Lights"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"


	def draw(self, context):
		layout = self.layout
		row = layout.row(align=True)
		row.operator("lights.refresh", icon="FILE_REFRESH")
		#draw_panel(self, context, light_type="SUN")


class Copythis_PT_Panel():
	bl_parent_id = "VRAYLIGHTS_PT_Panel"
	bl_idname ="Copy"
	bl_label = ""
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	count = 0
	

	
	def draw(self, context):
		if LIGHTS:
			draw_panel(self, context, self.bl_label)
		
	def draw_header(self, context):
		layout = self.layout
		row = layout.row(align=True)
		row.label(text=str(LIGHTS[self.bl_label]["count"]), icon=self.icon)
		#show if light type is on or off
		row.prop(context.scene.addon.lights[self.idx], "on", text="", icon = "HIDE_OFF" if context.scene.addon.lights[self.idx].on else "HIDE_ON")
	

class Dome_PT_Panel(Copythis_PT_Panel, bpy.types.Panel):
	bl_idname = "DOME_PT_Panel"
	bl_label = "DOME" 
	icon = "LIGHT_HEMI"
	idx = 0

class Sun_PT_Panel(Copythis_PT_Panel, bpy.types.Panel):
	bl_idname = "SUN_PT_Panel"
	bl_label = "SUN"
	icon = "LIGHT_SUN"
	idx = 1


class Rect_PT_Panel(Copythis_PT_Panel, bpy.types.Panel):
	bl_idname = "RECT_PT_Panel"
	bl_label = "RECT"
	icon = "LIGHT_AREA"
	idx = 2

class Sphere_PT_Panel(Copythis_PT_Panel, bpy.types.Panel):
	bl_idname = "SPHERE_PT_Panel"
	bl_label = "SPHERE"
	icon = "LIGHT_POINT"
	idx = 3

class Spot_PT_Panel(Copythis_PT_Panel, bpy.types.Panel):
	bl_idname = "SPOT_PT_Panel"
	bl_label = "SPOT"
	icon = "LIGHT_SPOT"
	idx = 4

class Select_OT_Object(bpy.types.Operator):
	
	bl_idname = "object.select_object"
	bl_label = "Select object"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	
	obj : bpy.props.StringProperty()

	def execute(self, context):

		print(self.obj)
		select(self.obj)
		
		return {'FINISHED'}


class Lights_OT_Refresh(bpy.types.Operator):

	bl_idname = "lights.refresh"
	bl_label = "Refresh lights"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.

	def execute(self, context):

		global LIGHTS

		light_types = ["DOME", "SUN", "RECT", "SPHERE", "SPOT"]
		for i in light_types:
			LIGHTS[i] = {"objects":[], "count": 0}
		
		
		objs = context.scene.objects

		for o in objs:
			if o.type == 'LIGHT': 
				
				for l_type in light_types:
					if l_type == o.data.vray.light_type:
						LIGHTS[l_type]["objects"].append(o.name)
						break
		
		for i in light_types:
			LIGHTS[i]["count"] = len(LIGHTS[i]["objects"])

		#first time set scene.addon.lights, later no need to set, there are only 6 V-Ray light types
		if not context.scene.addon.lights:
			print ("First time set addon lights")
			context.scene.addon.lights.clear()

			for i in light_types:
				l = context.scene.addon.lights.add()
				l.on = True
				l.light_type = i

		return {'FINISHED'}