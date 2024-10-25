import bpy
from . __init__ import Vray_Tools_PT_Panel #VRAYLIGHTS_PT_Panel
from . import functions as F
from bpy.app.handlers import persistent
LIGHTS = {}

LIGHT_CNT_TIMER = 0
LIGHT_DELAY_TIMER = 0.1
LIGHT_BATCH_SIZE_TIMER = 20


#			10        20        30        40        50        60        70        80        90        100	
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
LIGHT_TYPES = ["DOME", "SUN", "RECT", "SPHERE", "SPOT"]

def draw_panel(self, context, light_type):
	
	def splitter(factor_, split_):

		split = split_.split(factor=factor_)
		col = split.column(align=True)
		return split,col
	
	def invisible(light, col):
		col.prop(light, "invisible",emboss=False, text="",icon="RESTRICT_RENDER_ON" if light.invisible else "RESTRICT_RENDER_OFF")
	
	layout = self.layout
	
	for o in LIGHTS[light_type]["objects"]:
		row = layout.row(align=True)
		row.alignment = 'LEFT'	
		split = row.split(factor=0.1)
		col1 = split.column(align=True)
		
		#1
		#check if light object has "visibility lock", if so, make row as red color
		obj = bpy.data.objects.get(o, None)
		if obj and obj.get("visibility_lock", False):
			col1.alert = True
		else:
			col1.alert = False

		col1.operator("lights.hide",text="", icon="HIDE_ON" if bpy.data.objects[o].hide_viewport else "HIDE_OFF").obj = o 
		
		#2
		split, col = splitter(0.4, split)
		#split = split.split(factor=0.4)
		#col2 = split.column(align=True)
		
		#if context.view_layer.objects.active == context.view_layer.objects[o]:
		if context.view_layer.objects[o].select_get():
			col.emboss = 'NORMAL'
		else:
			col.emboss = 'PULLDOWN_MENU'
		
		col.operator("object.select_object", text=o).obj = o
		
		od = bpy.data.objects[o].data.vray
		
		if light_type == "DOME":
			#4
			split,col = splitter(0.9, split)
			obj = bpy.data.objects[o]
			if obj.data.node_tree:
				intensity = obj.data.node_tree.nodes[obj["dome_nodename"]].inputs['Intensity']
				col.prop(intensity, "value", text="")
			
				#5
				split,col = splitter(1, split)
				col.alignment = 'RIGHT'
				invisible = obj.data.node_tree.nodes[obj["dome_nodename"]].inputs['Invisible']
				col.prop(invisible, "value", text="",emboss=False,icon="RESTRICT_RENDER_ON" if invisible.value else "RESTRICT_RENDER_OFF")

		elif light_type == "SUN":

			#3
			split,col = splitter(0.3, split)
			col.prop(od.SunLight, "filter_color", text="")
			#4
			split,col = splitter(0.9, split)
			col.prop(od.SunLight, "intensity_multiplier", text="")
			#5
			split,col = splitter(1, split)
			col.alignment = 'RIGHT'
			col.scale_x = .1
			invisible(od.SunLight, col)

		elif light_type =="RECT":

			split,col = splitter(0.3, split)
			col.prop(od.LightRectangle, "color_colortex", text="")

			split,col = splitter(0.9, split)
			col.prop(od.LightRectangle, "intensity", text="", expand=True)

			split,col = splitter(1, split)
			col.alignment = 'RIGHT'
			invisible(od.LightRectangle, col)
			

		elif light_type =="SPHERE":
			
			split,col = splitter(0.3, split)
			col.prop(od.LightSphere, "color_colortex", text="")
			
			split,col = splitter(0.9, split)
			col.prop(od.LightSphere, "intensity", text="")

			split,col = splitter(1, split)
			col.alignment = 'RIGHT'
			invisible(od.LightSphere, col)

		elif light_type =="SPOT":
			
			split,col = splitter(0.3, split)
			col.prop(od.LightSpot, "color_colortex", text="")
			
			split,col = splitter(0.9, split)
			col.prop(od.LightSpot, "intensity", text="")

			split,col = splitter(1, split)
			col.alignment = 'RIGHT'
			#invisible(od.LightSpot, col)
			col.label(text="")

		else:
			pass
		
		#bpy.data.lights["VRayRectLight"].vray.LightRectangle.color_colortex
		#row.label(text=o.name)
#bpy.data.lights["VRaySunLight"].vray.SunLight.filter_color sun
#bpy.data.lights["VRayDomeLight.001"].node_tree.nodes["Light Dome"].inputs['Color'].value 

def select(obj_name, invert=False):


	o = bpy.data.objects[obj_name]
	if not invert:
		bpy.ops.object.select_all(action='DESELECT')
		o.select_set(True)
	else:
		o.select_set(not o.select_get())

	bpy.context.view_layer.objects.active = o

class Vray_Lights_PT_Panel(bpy.types.Panel):
	
	bl_parent_id = "VRAYTOOLS_PT_Panel"
	bl_idname = "VRAYLIGHTS_PT_Panel"
	bl_label = "Lights"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"


	def draw(self, context):
		layout = self.layout
		row = layout.row(align=False)
		row.operator("lights.refresh", icon="FILE_REFRESH")
		row.alignment='RIGHT'
		row.prop(context.scene.vray.SettingsGI, "on",text="", icon="IPO_BOUNCE")
		#draw_panel(self, context, light_type="SUN")

		#row = layout.row()
		#row.alignment = 'EXPAND'
		row = layout.row(align=True)
		row.operator("add.lights", icon="ADD")

		test = False
		if not test:
			return
		#1
		#cf = layout.column_flow(columns=6, align=True)
		cf = layout.grid_flow(columns=6, align=True)
		cf.alignment = 'LEFT'
		#split = layout.split(factor=0.08, align=True)
		#col1 = split.column(align=True)
		cf.alert = True
		cf.label(text="", icon='FILE_FOLDER')
		#2
		#split = split.split(factor=0.08)
		#col2 = split.column()
		cf.alert = False
		cf.label(text="", icon='FILE_FOLDER')
		#3
		#split = row.split(factor=0.08)
		#col3 = split.column()
		#col3.alert = True
		cf.label(text="", icon='FILE_FOLDER')
		#4
		#split = split.split(factor=0.4)
		#col4 = split.column(align=True)
		cf.operator("splitter.splatter", text="Cancel")
		#5
		#split = split.split(factor=0.8)
		#col5 = split.column(align=True)
		#col5.alignment = 'RIGHT'
		cf.operator("splitter.splatter", text="Ok")
		#6
		#split = split.split()
		#col6 = split.column()
		#col6.alignment = 'RIGHT'
		
		cf.prop(context.scene.vray.SettingsGI, "on",text="")

		"""
		row = row.row(align=True)
		row.scale_x = 0.3
		row.operator("splitter.splatter", text="My Button")
		#4
		row = row.row(align=True)
		row.scale_x = 0.7
		row.operator("splitter.splatter", text="My Button")
		#5
		row = row.row(align=True)
		#row.scale_x = 1
		row.alignment = 'RIGHT'
		row.prop(context.scene.vray.SettingsGI,"on", text="")
		"""
		#row.operator("splitter.splatter")

class Copythis_PT_Panel():
	#bl_parent_id = "VRAYLIGHTS_PT_Panel"
	#bl_parent_id = "VRAYTOOLS_PT_Panel"
	bl_idname ="Copy"
	bl_label = ""
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "V-Ray Tools"
	count = 0
	
	
	def draw(self, context):
		if LIGHTS:
			draw_panel(self, context, self.bl_label)
		
	def draw_header(self, context):
		layout = self.layout

		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.label(text="", icon=self.icon)
		#row = layout.split(factor=0.3)

		#show if light type is on or off
		#row = layout.split(factor=0.5)
		row.prop(context.scene.addon.lights[self.idx], "on", text="", icon = "HIDE_OFF" if context.scene.addon.lights[self.idx].on else "HIDE_ON")
		
		#select lights by light type
		row.operator("lights.select", text="", icon="RESTRICT_SELECT_OFF").light_type_idx = self.idx
		
		#unlock lights by light type
		for o_name in LIGHTS[self.bl_label]["objects"]:
			#o = bpy.data.objects[o_name]
			o = bpy.data.objects.get(o_name, None)
			if o and o.get("visibility_lock", False):
				row.alert = True
				break	

		#row.alert = True
		row.operator("lights.unlock", text="", icon="VIEW_UNLOCKED").light_type_idx = self.idx

		split = layout.split()
		col = split.column()
		row = col.row()
		cnt = str(LIGHTS[self.bl_label]["count"])
		row.label(text=cnt)  ##f"{1:3d}"


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
	bl_description = 	("Select light and unselect all other objects.\n"
						"Shift+Click to select and add to selection")
	obj : bpy.props.StringProperty()
	deselect_all = True

	def execute(self, context):

		print(self.obj)
		select(self.obj)
		
		return {'FINISHED'}

	def invoke(self, context, event):

		if event.shift and event.type =='LEFTMOUSE':  #invert light object selection
			select(self.obj, invert=True)
			return {'FINISHED'}
		
		return self.execute(context)

def lights_refresh_from_timer(o):
	

	def dome():

		def node_dome_find(nodes):
			for i in nodes:
				if i.vray_plugin == "LightDome":
					return i
			return None

		if o.data.node_tree:
			print(o.name,"Dome light has node tree")
			dome_node = node_dome_find(o.data.node_tree.nodes)
			if dome_node:
				o["dome_nodename"] = dome_node.name
		else:
			print(o.name,"Dome light has no node tree")


	light_type = o.data.vray.light_type
	if light_type in LIGHT_TYPES:
	
		#is light object already in dictionary ?
		if not o.name in LIGHTS[light_type]["objects"]:
			LIGHTS[light_type]["objects"].append(o.name)
			LIGHTS[light_type]["count"] = len(LIGHTS[light_type]["objects"])

			if light_type == "DOME":
				print("dome found")
				dome()

			C = bpy.context
			area = next((area for area in C.screen.areas if area.type == 'VIEW_3D'), None)
			if not area:
				return
			region = next((region for region in area.regions if region.type == 'UI'), None)
			if not region:
				return
			#print("region.redraw")
			#region.tag_redraw()


def Lights_refresh():

	print("Lights_refresh")
	global LIGHTS
	context = bpy.context

	def node_dome_find(nodes):
		for i in nodes:
			if i.vray_plugin == "LightDome":
				return i
		return None

		

	#LIGHT_TYPES = ["DOME", "SUN", "RECT", "SPHERE", "SPOT"]
	for i in LIGHT_TYPES:
		LIGHTS[i] = {"objects":[], "count": 0}
	
	
	objs = context.scene.objects

	for o in objs:
		if o.type == 'LIGHT': 
			
			for l_type in LIGHT_TYPES:
				if l_type == o.data.vray.light_type:
					LIGHTS[l_type]["objects"].append(o.name)

					#check also Dome light, if it has node tree and image, store dome node name
					if l_type == "DOME":
						if o.data.node_tree:
							print(o.name,"Dome light has node tree")
							dome_node = node_dome_find(o.data.node_tree.nodes)
							if dome_node:
								o["dome_nodename"] = dome_node.name

						else:
							print(o.name,"Dome light has no node tree")
					break
	
	for i in LIGHT_TYPES:
		LIGHTS[i]["count"] = len(LIGHTS[i]["objects"])

	#first time set scene.addon.lights, later no need to set, there are only 6 V-Ray light types
	if not context.scene.addon.lights:
		print ("First time set addon lights")
		context.scene.addon.lights.clear()

		for i in LIGHT_TYPES:
			l = context.scene.addon.lights.add()
			l.on = True
			l.light_type = i

class Lights_OT_Refresh(bpy.types.Operator):
	
	bl_idname = "lights.refresh"
	bl_label = "Refresh lights"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.

	def execute(self, context):

		Lights_refresh()

		return {'FINISHED'}
	

class Lights_OT_Select(bpy.types.Operator):

	bl_idname = "lights.select"
	bl_label = "Select all lights of this light type"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.

	#which light type lights to select
	light_type_idx : bpy.props.IntProperty(default = 0)

	def execute(self, context):
		
		print("Light type selected", self.light_type_idx)
		bpy.ops.object.select_all(action='DESELECT')
		for o in LIGHTS[LIGHT_TYPES[self.light_type_idx]]["objects"]:
			obj = bpy.data.objects[o]
			obj.select_set(True)
			bpy.context.view_layer.objects.active = obj

		return {'FINISHED'}
	

class Lights_OT_Hide_Show(bpy.types.Operator):

	bl_idname = "lights.hide"
	bl_label = ""
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	bl_description = 	("Hide/show on viewport and render.\n"
							"Ctrl+Click to lock")

	#which light to select
	obj : bpy.props.StringProperty()

	def execute(self, context):
		
		print("Light:", self.obj)
		o = bpy.data.objects[self.obj]
		F.object_hide_viewport_and_render(o, o.hide_viewport)
		return {'FINISHED'}


	def invoke(self, context, event):
		print ("Invoke")
		if event.ctrl and event.type =='LEFTMOUSE':  # Cancel
			print ("Leftclick+ ctrl")
			o = bpy.data.objects[self.obj]
			if not o.get("visibility_lock"):
				o["visibility_lock"] = True
			else:
				o["visibility_lock"] ^= True #invert
		else:
			return self.execute(context)
		
		return {'FINISHED'}
		

class Lights_OT_Unlock(bpy.types.Operator):
	
	bl_idname = "lights.unlock"
	bl_label = "Unlock all this type of lights"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.

	#which light to select
	light_type_idx : bpy.props.IntProperty()

	def execute(self, context):
		
		print("UNLOCK light type index:", self.light_type_idx)
		for o in LIGHTS[LIGHT_TYPES[self.light_type_idx]]["objects"]:
			bpy.data.objects[o]["visibility_lock"] = False
		
		return {'FINISHED'}
	
class Splitter_OT_Splatter(bpy.types.Operator):
	
	bl_idname = "splitter.splatter"
	bl_label = "Split UI test"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	bl_description = 	("This is a tooltip\n"
							"with multiple lines")
	
	def execute(self, context):
		
		
		return {'FINISHED'}
	

class Add_OT_Lights(bpy.types.Operator):
	
	bl_idname = "add.lights"
	bl_label = "Testing add lights"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	bl_description = 	("This is a tooltip\n"
							"with multiple lines")

	def cursor(self,loc):

		bpy.context.scene.cursor.location = loc
		loc.x += 1

	def execute(self, context):
		from mathutils import Vector
	
		loc = Vector((0,0,3))
		for i in range(3):

			self.cursor(loc)
			bpy.ops.vray.add_object_vray_light_dome()
			self.cursor(loc)
			bpy.ops.vray.add_object_vray_light_sun()
			self.cursor(loc)
			bpy.ops.vray.add_object_vray_light_rect()
			self.cursor(loc)
			bpy.ops.vray.add_object_vray_light_sphere()
			self.cursor(loc)
			bpy.ops.vray.add_object_vray_light_spot()
			loc.x = 0
			loc.y -= 1		
		return {'FINISHED'}

@persistent
def lights_timer1():
	global LIGHT_CNT_TIMER

	def read_next_batch():
	
		global LIGHT_CNT_TIMER	
		objects = bpy.data.objects
		if LIGHT_CNT_TIMER >= len(objects):
			return None
		batch = objects[LIGHT_CNT_TIMER:LIGHT_CNT_TIMER + LIGHT_BATCH_SIZE_TIMER]
		LIGHT_CNT_TIMER += LIGHT_BATCH_SIZE_TIMER
		return batch
	
	batch = read_next_batch()
	if batch is not None:
		print(LIGHT_CNT_TIMER)
		#print("Batch of objects:", [obj.name for obj in batch])
		#print("Total objects in batch:", len(batch))
		for o in batch:
			if o.type == 'LIGHT':
				lights_refresh_from_timer(o)
		
	else:
		#print("No more objects to read")	
		LIGHT_CNT_TIMER = 0
		
	return LIGHT_DELAY_TIMER






PREFIX = "S"

#==================================================================================================
def get_collections():

	#include also the scene base collection
	colls = [bpy.context.scene.collection, *bpy.data.collections]
	return [i for i in colls if i.name.startswith(PREFIX)]

def get_collection_light_objects(coll: bpy.types.Collection):
	return [o for o in coll.objects if o.type == "LIGHT" and o.data.vray.light_type != "BLENDER"]

#==================================================================================================
#print()
#coll = get_collections()
#print("coll:",coll)

#objs = get_collection_light_objects(coll[0])
#print("Collection:",coll[0].name, "has these objects:", objs[:])



