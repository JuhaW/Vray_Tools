import bpy
from bpy.props import BoolProperty
from . __init__ import Vray_Tools_PT_Panel #VRAYLIGHTS_PT_Panel
from . import functions as F
from bpy.app.handlers import persistent
from . import icons #VRAY_ICONS

LIGHTS = {}

LIGHT_CNT_TIMER = 0
LIGHT_DELAY_TIMER = 0.1
LIGHT_BATCH_SIZE_TIMER = 20
LIGHT_ICONS = {"DOME": "LIGHT_HEMI","SUN": "LIGHT_SUN","RECT": "LIGHT_AREA",
					"SPHERE": "LIGHT_POINT","SPOT": "LIGHT_SPOT","MESH": "MESH_MONKEY"}
PREFIX = ""


"""   	10        20        30        40        50        60        70        80        90        100	"""

#2345678901234567890123456789012345678901234567890123456789012345678901234567890
LIGHT_TYPES = ["DOME", "SUN", "RECT", "SPHERE", "SPOT"]

#============================================
#Select light object
def select(obj_name, invert=False):


	o = bpy.data.objects[obj_name]
	
	if not invert:
		bpy.ops.object.select_all(action='DESELECT')
		o.select_set(True)
	
	else:
		o.select_set(not o.select_get())

	bpy.context.view_layer.objects.active = o
	#PROPERTIES window, DATA area active for light
	F.data_area_active(bpy.context)

	

#============================================


class Vray_Lights_PT_Panel(bpy.types.Panel):
	
	bl_parent_id = "VRAYTOOLS_PT_Panel"
	bl_idname = "VRAYLIGHTS_PT_Panel"
	bl_label = "Lights"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"


	def draw(self, context):

# The above code is a Python script with comments. Comments in Python start with the `#` symbol. In
# this script, there are multiple comments denoted by `#` symbol. However, the script itself does not
# contain any executable code. It is just a series of comments.
#======
#UI LIGHT TYPE
		def light_type():
#=====
#UI Light Invisible
			def invisible(light):
				gf.scale_x = 1
				gf.prop(light, "invisible",emboss=False, text="",icon="RESTRICT_RENDER_ON" if light.invisible else "RESTRICT_RENDER_OFF")


			gf.emboss = "NORMAL"
			light_type = o.data.vray.light_type
			od = o.data.vray
			color_scalex = .1
			intensity_scalex = .3
			match light_type:
				case "DOME":
					#do not read from dome node if there are no dome.nodetree or dome node
					if dome_node := (F.node_dome_find(o.data.node_tree.nodes) if o.data.node_tree else None):
						gf.scale_x = color_scalex
						#check if Light dome node has input links on socket [Dome Color]
						#if not, use dome color for ui
						if dome_node.inputs['Dome Color'].links:
							color = dome_node.inputs['Dome Color']
							#gf.scale_x = .3
							#gf.prop(color, "multiplier",text = "")
							#gf.scale_x = .05
						
						color = dome_node.inputs['Dome Color']
						gf.prop(color, "value",text="")
							
						intensity = dome_node.inputs['Intensity']
						gf.scale_x = intensity_scalex
						gf.prop(intensity, "value", text="")
						invisible = dome_node.inputs['Invisible']
						gf.scale_x = 1
						gf.prop(invisible, "value", text="",emboss=False,icon="RESTRICT_RENDER_ON" if invisible.value else "RESTRICT_RENDER_OFF")

					else:
						gf.scale_x = color_scalex
						gf.prop(od.LightDome, "color_colortex", text="")
						gf.scale_x = intensity_scalex
						gf.prop(od.LightDome, "intensity", text="")
						invisible(od.LightDome)
				case "SUN":
					gf.scale_x = color_scalex
					gf.prop(od.SunLight, "filter_color", text="")
					gf.scale_x = intensity_scalex
					gf.prop(od.SunLight, "intensity_multiplier", text="")
					invisible(od.SunLight)
				case "RECT":
					gf.scale_x = color_scalex
					gf.prop(od.LightRectangle, "color_colortex", text="")
					#gf.template_color_picker(od.LightRectangle, "color_colortex", value_slider=False, lock=False, lock_luminosity=False, cubic=False)
					gf.scale_x = intensity_scalex
					gf.prop(od.LightRectangle, "intensity", text="")
					invisible(od.LightRectangle)
				case "SPHERE":
					gf.scale_x = color_scalex
					gf.prop(od.LightSphere, "color_colortex", text="")
					gf.scale_x = intensity_scalex
					gf.prop(od.LightSphere, "intensity", text="")
					invisible(od.LightSphere)
				case "SPOT":
					gf.scale_x = color_scalex
					gf.prop(od.LightSpot, "color_colortex", text="")
					gf.scale_x = intensity_scalex
					gf.prop(od.LightSpot, "intensity", text="")
					gf.scale_x = 1
					gf.prop(o, "tag", text="",emboss=False, icon="BLANK1")
				case "MESH":
					gf.scale_x = color_scalex
					gf.prop(od.LightMesh, "color_colortex", text="")
					gf.scale_x = intensity_scalex
					gf.prop(od.LightMesh, "intensity", text="")
					invisible(od.LightMesh)

#=====
# UI GLOBAL 
		layout = self.layout
		row = layout.row(align=False)
		row.operator("lights.refresh", icon_value=icons.CUSTOM_ICONS["REFRESH_LIGHTS"].icon_id)#"FILE_REFRESH")
		
		#GI 
		row.prop(context.scene.vray.SettingsGI, "on",text="",icon_value=icons.CUSTOM_ICONS["GI"].icon_id )#icon="MOD_SOFT")
		#lock
		if context.scene.addon.lights_global_lock:
			row.alert = True
		row.operator("global.lights_unlock", text="Unlock", icon="VIEW_UNLOCKED")
		row = layout.row(align=True)
		#row.scale_x = 1
		#row.separator(factor=1,type='AUTO')
		#row = layout.row(align=True)
		row = layout.box()
		row.label(text="Global settings for lights:")
		#row = layout.box()
		
		#light object DATA area auto activate
		split = row.split(factor=.5,align=True)
		
		#split.label(text="",icon_value=icons.CUSTOM_ICONS["DATA"].icon_id)
		split.prop(context.scene.addon,"lights_activate_data_area",text="Show light options")
		#row = layout.row(align=True)
		
		#Button visibility
		split.operator("global.lights_visibility", text="", icon="HIDE_ON" if context.scene.addon.lights_global_visibility else "HIDE_OFF")
		#split.operator("global.lights_visibility", text="", icon="HIDE_ON" if context.scene.addon.lights_global_visibility else "HIDE_OFF")
		#row.template_icon(icon_value=icons.CUSTOM_ICONS["SOLO"].icon_id , scale=1.5)
		#row.template_icon(icon_value=icons.CUSTOM_ICONS["GI"].icon_id , scale=1.5)
		#img = bpy.data.textures[1]
		#row.template_preview(img)
		#row.label(text="GI", icon_value=icons.CUSTOM_ICONS["DOME"].icon_id)
		row = layout.row(align=True)
		
#=====
#UI WORLD ENVIRONMENT		
		row = layout.box()
		row = row.row(align=True)
		row.separator(factor=1)
		row.label(text="",icon_value=icons.VRAY_ICONS['SUN_SKY'].icon_id)
		if context.scene.world:

			if context.scene.world.get("lock", None):
				row.alert = True

			row.active = not context.scene.world["hide_viewport"] or context.scene.world["solo"]
			if context.scene.world["solo"]:
				row.operator("environment.hide", text="", icon_value=icons.CUSTOM_ICONS["SOLO"].icon_id)
			else:
				row.operator("environment.hide", text="", icon="HIDE_ON" if context.scene.world["hide_viewport"] else "HIDE_OFF")
			row.alert = False
			row.label(text="Environment (Sun and Sky)")
		else:
			row.label(text="No environment")
		#row.operator("add.lights", icon="ADD")

#============================================
#COLLECTIONS
		#show if collection is visible or hidden
		#row = layout.row(align=True)
		colls = get_collections_which_have_light_objects()
		for coll in colls:
			cf = layout.box()
			#cf = layout.grid_flow(columns=4, align=True)
			cf = cf.grid_flow(columns=4, align=True)
			#custom panel open/closed
			#row = row.column(align=True)
			#emboss False makes arrow not hightlighted
			cf.prop(coll,'["panel_open"]',text="", emboss = True, icon = "TRIA_DOWN" if coll["panel_open"] else "TRIA_RIGHT")
			#collection lock indicator
			if coll.get("lock",False):
				cf.alert = True
			#p = cf.operator("collection.hide_show", text="", icon_value=icons.CUSTOM_ICONS["SOLO"].icon_id)
			p = cf.operator("collection.hide_show", text="", icon="HIDE_ON" if coll["hide"] else "HIDE_OFF")
			p.coll_name = coll.name
			p.invert_hide = False
			cf.alert = False
			#select lights
			p = cf.operator("collection.select_lights", text="", icon="RESTRICT_SELECT_OFF")
			p.coll_name = coll.name
			#collection name
			if coll['panel_open']:
				cf.emboss = "NORMAL"
			else:
				cf.emboss = "PULLDOWN_MENU"
			cf.label(text = coll.name)
			
			#row = layout.row(align=True)	
			
#============================================
#LIGHTS
			#panel is open
			#use grid flow
			if coll["panel_open"]:
				light_objs = get_collection_light_objects(coll)
				cf = layout.box()
				for o in light_objs:
					#gf = layout.grid_flow(columns=5, align=True)
					
					row = cf.row()
					gf = row.grid_flow(columns=8, align=True)
					gf.separator(factor=1)
					#light type icon
					l_type = o.data.vray.light_type
					gf.scale_x = 1 #!1.5
					
					if l_type in ["SUN", "DOME", "RECT", "SPHERE","SPOT", "MESH" ]:
						gf.label(text="", icon_value=icons.VRAY_ICONS[l_type].icon_id)
					else:
						gf.label(text="", icon=LIGHT_ICONS[l_type])
					
					#gf = row.grid_flow(columns=5, align=True)
					#gf = layout.column_flow(columns=5,align = False)
					#split = row.column(align=True)
					#check if any light of this collection is locked, set object lock
					#set also collection lock indicator locked = red 
					if o.get("lock", False):
						gf.alert = True
					gf.scale_x = 1 #!1.2
					#if Collection_OT_Hide.solo_ui:
					if o.hide_viewport:
						gf.active = False
					if o.get("solo", False):
						gf.active = True
						r = gf.operator("lights.hide",text="", icon_value=icons.CUSTOM_ICONS["SOLO"].icon_id)
					else:
						r = gf.operator("lights.hide",text="", icon="HIDE_ON" if o.hide_viewport else "HIDE_OFF")
					r.obj_name = o.name
					r.coll_name = coll.name #store collection

					#light object selection
					#no red colors here anymore
					gf.alert = False
					gf.scale_x = .6
					if o.select_get():

						gf.emboss = 'NORMAL'
					else:

						gf.emboss = 'NONE'
					gf.operator("object.select_object", text=o.name).obj_name = o.name
					
					gf.alignment = "EXPAND"
					#Light color
					light_type()
					#row = layout.row(align=True)
					#gf.label(text="",icon="OBJECT_DATA")
					#gf.label(text="",icon="OBJECT_DATA")


#============================================
#
#============================================					

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
		pass
		#draw_panel(self, context, self.bl_label)
		
	def draw_header(self, context):
		layout = self.layout

		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.label(text="", icon=self.icon)
		#row = layout.split(factor=0.3)


		"""
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
		"""


class Select_OT_Object(bpy.types.Operator):
	
	bl_idname = "object.select_object"
	bl_label = "Select object"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	bl_description = 	("Select light and unselect all other objects.\n"
						"Shift+Click to select and add to selection")
	obj_name : bpy.props.StringProperty()
	deselect_all = True

	def execute(self, context):

		print(self.obj_name)
		select(self.obj_name)
		
		return {'FINISHED'}

	def invoke(self, context, event):

		if event.shift and event.type =='LEFTMOUSE':  #invert light object selection
			select(self.obj_name, invert=True)
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
			

def Lights_refresh():

	print("Lights_refresh")
	colls = get_collections_which_have_light_objects()
	
	for coll in colls:
		#set hide/show
		if not coll.get("hide", False):
			coll["hide"] = False
		#set panel open/closed
		if not coll.get("panel_open", False):
			coll["panel_open"] = False
		if not coll.get("lock", False):
			#set object view locked/unlocked
			coll["lock"] = False
	
	light_objs = get_all_light_objects(bpy.context)	
	for o in light_objs:
		if not o.get("visibility_lock", False):
			o["visibility_lock"] = False
		if not o.get("lock", False):
			o["lock"] = False
		if not o.get("solo", False):
			o["solo"] = False
		if not o.get("solo_stored_visibility", False):
			o["solo_stored_visibility"] = False

	
	#world, environment visibility
	if bpy.context.scene.world:
		w = bpy.context.scene.world
		if not w.get("hide_viewport", False):
			w["hide_viewport"] = False
		if not w.get("solo", False):
			w["solo"] = False
		if not w.get("solo_stored_visibility", False):
			w["solo_stored_visibility"] = False
		
	bpy.context.scene.addon.light_solo_cnt = 0
	
	print("solo_cnt", bpy.context.scene.addon.light_solo_cnt)

	return None
	#!todo is World 
	#!todo is Environment node
	#!todo is Environment connected to output
	
	#context = bpy.context
	
	"""
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
	"""

class Lights_OT_Refresh(bpy.types.Operator):
	
	bl_idname = "lights.refresh"
	bl_label = "Refresh lights"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.

	def execute(self, context):

		Lights_refresh()

		return {'FINISHED'}
	
class Collection_OT_Select_Lights(bpy.types.Operator):

	bl_idname = "collection.select_lights"
	bl_label = "Select all lights of this collection"
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	
	coll_name	: bpy.props.StringProperty()

	def execute(self, context):
		
		bpy.ops.object.select_all(action='DESELECT')
		coll = get_collection_by_name(context, self.coll_name)
		light_objs = get_collection_light_objects(coll)
		for o in light_objs:
			o.select_set(True)
			bpy.context.view_layer.objects.active = o

		return {'FINISHED'}

	def invoke(self, context, event):
		if event.type == 'LEFTMOUSE' and event.shift:
			coll = get_collection_by_name(context, self.coll_name)
			light_objs = get_collection_light_objects(coll)
			for o in light_objs:
				o.select_set(not o.select_get())
				bpy.context.view_layer.objects.active = o

			return {'FINISHED'}

		return self.execute(context)

#=======
#OP Environment hide
class Environment_OT_Hide_Show(bpy.types.Operator):
	bl_idname = "environment.hide"
	bl_label = ""
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	bl_description = 	("Hide/show on viewport and render.\n"
							"Ctrl+Click to lock")
		
	def execute(self, context):

		context.scene.world["hide_viewport"] ^= True
		if context.scene.world["hide_viewport"]:
			sky(unlink_env_and_output=True)
			print("Unlink")
		else:
			sky(link_env_and_output=True)
			print("Link")
		return {'FINISHED'}

	def invoke(self, context, event):

		if context.scene.addon.light_solo_cnt == 0 and event.ctrl and event.type =='LEFTMOUSE': 
			
			world = context.scene.world
			if not world.get("lock", False):
				world["lock"] = True
			else:
				world["lock"] ^= True #invert

			return {'FINISHED'}
		if event.type == 'LEFTMOUSE' and event.alt:
			print("Leftclick+ alt")
			
			self.solo(context)	

			return {'FINISHED'}
		elif context.scene.addon.light_solo_cnt > 0:
			return {'FINISHED'}
		
		return self.execute(context)

	def solo(self,context):
		#if solo_cnt == 0, no lights and env are not in solo mode
		world = context.scene.world
		world["solo"] ^= True
		addon = context.scene.addon
		if world["solo"]:
			if addon.light_solo_cnt == 0:
				lights_store_visibility(context)
				sky(link_env_and_output=True)
				
			addon.light_solo_cnt += 1
			print("env, light solo cnt:", addon.light_solo_cnt)
		else:
			addon.light_solo_cnt -= 1
			print("env, light solo cnt:", addon.light_solo_cnt)
			if addon.light_solo_cnt == 0:
				lights_restore_visibility(context)
			else:
				#world['hide_viewport'] = True
				sky(unlink_env_and_output=True)
	

class Lights_OT_Hide_Show(bpy.types.Operator):

	bl_idname = "lights.hide"
	bl_label = ""
	bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
	bl_description = 	("Hide/show on viewport and render.\n"
							"Ctrl+Click to lock")

	#which light to select
	obj_name 			: bpy.props.StringProperty()
	coll_name	: bpy.props.StringProperty()

	def execute(self, context):
		
		print("Light:", self.obj_name)
		o = bpy.data.objects[self.obj_name]
		F.object_hide_viewport_and_render(o, o.hide_viewport)
		return {'FINISHED'}


	def invoke(self, context, event):
		print ("Invoke")

		o = bpy.data.objects[self.obj_name]
		#if solo mode is on of this object, ignore click except solo mode click (Alt)
		#solo_mode =  o.get("solo", False)
		light_solo_cnt = context.scene.addon.light_solo_cnt
		
		if light_solo_cnt == 0 and event.ctrl and event.type =='LEFTMOUSE': 
			print ("Leftclick+ ctrl")
			
			if not o.get("lock", False):
				o["lock"] = True
			else:
				o["lock"] ^= True #invert
			#now we need to loop every lights in this collection to set collection view locked/unlocked
			#if one of the lights has lock on, collection will show view lock = red
			#coll = bpy.data.collections[self.coll_name]
			coll = get_collection_by_name(context, self.coll_name)
			for o in coll.objects:
				if o.get("lock", False):
					coll["lock"] = True
					#set global lock also for UI
					#context.scene.addon.lights_global_lock = True
					break
			else:
				coll["lock"] = False
			#check if all collections are unlocked, if so, set global lock to false
			colls = get_collections_which_have_light_objects()
			for coll in colls:
				if coll.get("lock", False):
					context.scene.addon.lights_global_lock = True
					break
			else:
				context.scene.addon.lights_global_lock = False

		elif event.type == 'LEFTMOUSE' and event.alt:
			print("Leftclick+ alt")
			self.solo(context)

			#Solo_OT_Mode.execute(self, context)
		elif light_solo_cnt==0:
			return self.execute(context)
		
		return {'FINISHED'}
	
	def solo(self, context):
		
		# Toggle current light object solo mode, #.["solo"]
		# Check if any light object is in solo mode, except the current one
		#If no objects are in solo mode
			#Check current light object solo mode
			#Yes, current light is in solo mode
				#Store all other light objects visibility, #.["solo_stored_visibility"]
				#Hide all light objects except the current one
			#No, current light is not in solo mode
				#Restore light objects visibility, #.["solo_stored_visibility"]

		o = bpy.data.objects[self.obj_name]
		o["solo"] ^= True
		addon = context.scene.addon
		print ("light solo cnt:", addon.light_solo_cnt)
		#light_objs = get_all_light_objects(context)
		
		#objs = [ obj for obj in light_objs if obj.get("solo", False) and obj != o] 
		if o["solo"]:
			print("Yes, in solo mode")
			object_hide_viewport_and_render(o, False)
			if addon.light_solo_cnt == 0:
			
				lights_store_visibility(context)
					
			object_hide_viewport_and_render(o, False)
			addon.light_solo_cnt += 1
			print ("light solo cnt:", addon.light_solo_cnt)
			#ENV
			context.scene.world["hide_viewport"] = True
		else:
			addon.light_solo_cnt -= 1
			print("This light object not in solo mode")
			if addon.light_solo_cnt == 0:
				lights_restore_visibility(context)

			else:
				object_hide_viewport_and_render(o, True)

def lights_store_visibility(context):
	#store all light objects visibility
	light_objs = get_all_light_objects(context)
	for obj in light_objs:
		obj["solo_stored_visibility"] = obj.hide_viewport
		object_hide_viewport_and_render(obj,True)
	world = context.scene.world
	world["solo_stored_visibility"] = world["hide_viewport"]
	if not world["solo"]:
		sky(unlink_env_and_output=True)

def lights_restore_visibility(context):
	print("lights restore")
	#restore all light objects visibility
	light_objs = get_all_light_objects(context)
	for obj in light_objs:
		obj.hide_viewport = obj["solo_stored_visibility"]
	world = context.scene.world
	world["hide_viewport"] = world["solo_stored_visibility"] 
	if not world["hide_viewport"]:
		sky(link_env_and_output=True)

def object_hide_viewport_and_render(o, hide):
	o.hide_viewport = hide
	o.hide_render = hide

def get_collection_by_name(context, name):
	#special case when collection is scene collection
	if name == context.scene.collection.name:
		coll = context.scene.collection
	else:			
		coll = bpy.data.collections[name]
	return coll

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

class Collection_OT_Hide(bpy.types.Operator):
	bl_idname = "collection.hide_show"
	bl_label = "Mouse Click Operator"

	coll_name 		: bpy.props.StringProperty() #from panel
	invert_hide 	: bpy.props.BoolProperty() #invert ligth object selection

	solo_ui = False

	@classmethod
	def poll(cls, context):
		return  context.scene.addon.light_solo_cnt == 0 #cls.solo_ui

	def execute(self, context):

		#we dont use collection own hide_viewport etc. properties. because they are limited
		#we use collection objects hide properties
		#that way we can hide all of of collection objects at once and the same time
		#we can use collection objects hide properties

		coll = get_collection_by_name(context, self.coll_name)

		#ignore view locked objects
		objs = [o for o in coll.objects if not o.get("lock", False)]

		if not self.invert_hide:
			
			coll["hide"] ^= True
			value = coll["hide"]
			for o in objs:
				o.hide_viewport = value
				o.hide_render = value
		else:
			for o in objs:
				hide = o.hide_viewport
				o.hide_viewport = not hide
				o.hide_render = not hide

		print ("Collection hide execute")
		
		return {'FINISHED'}
	def invoke(self, context, event):
		print(event.type, event.value)
		

		if event.type == 'LEFTMOUSE':
			if event.alt and event.ctrl:
				print ("Alt+Ctrl+Click, Collection hide invoke")
				return {'FINISHED'}
			elif event.ctrl:
				print ("Ctrl+Click, Collection hide invoke")
				self.invert_hide = True
				return self.execute(context)
			elif event.shift:
				print ("Shift+Click, Collection hide invoke")
				return {'FINISHED'}
			elif event.alt:
				print ("Alt+Click, Collection hide invoke")
				return {'FINISHED'}
			
			
		return self.execute(context)


"""
class Solo_OT_Mode(bpy.types.Operator):
	bl_idname = "solo.mode"
	bl_label = "Solo Mode Operator"

	obj_name :bpy.props.StringProperty()

	def invoke(self, context, event):
		if event.ctrl and event.type == 'LEFTMOUSE':
			
			return self.execute(context)
		return {'CANCELLED'}

	def execute(self, context):

		

		return {'FINISHED'}

	def store_visibility(self):
		# Store visibility properties of all light objects in the 'Lights' collection
		for obj in bpy.data.collections['Lights'].objects:
			obj['stored_visibility'] = obj.hide_viewport

	def restore_visibility(self):
		# Restore stored visibility properties of all light objects in the 'Lights' collection
		for obj in bpy.data.collections['Lights'].objects:
			if 'stored_visibility' in obj:
					obj.hide_viewport = obj['stored_visibility']
					del obj['stored_visibility']
					if 'solo' in obj:
						del obj['solo']

"""
#======
#Global lights visibility
class Global_OT_Lights_Visibility(bpy.types.Operator):
	bl_idname = "global.lights_visibility"
	bl_label = "Global lights visibility"


	def invoke(self, context, event):
		if event.type == 'LEFTMOUSE' and event.ctrl:
			
			return {'FINISHED'}
		return self.execute(context)
		#return {'PASS_THROUGH'}

	def execute(self, context):
		print("Global lights visibility")
		objs = get_all_light_objects(context)
		context.scene.addon.lights_global_visibility ^= True 
		env_visibility = context.scene.addon.lights_global_visibility
		#for light objects and world environment
		for o in objs:
			object_hide_viewport_and_render(o, env_visibility)

		if env_visibility:
			sky(unlink_env_and_output=True)
		else:
			sky(link_env_and_output=True)
		
			
		return {'FINISHED'}


#======
#Global lights unlock
class Global_OT_Lights_Unlock(bpy.types.Operator):
	bl_idname = "global.lights_unlock"
	bl_label = "Global lights visibility"


	def invoke(self, context, event):
		if event.type == 'LEFTMOUSE' and event.ctrl:
			
			return {'FINISHED'}
		return self.execute(context)
		#return {'PASS_THROUGH'}

	def execute(self, context):
		print("Global lights unlock")
		#set collections and light objects lock to False
		colls = get_collections_which_have_light_objects()
		for coll in colls:
			coll["lock"] = False
			for o in coll.objects:
				o['lock'] = False	

		context.scene.addon.lights_global_lock = False
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


#==================================================================================================
def get_all_light_objects(context):

	return [o for o in context.view_layer.objects if o.type == "LIGHT" and o.data.vray.light_type != "BLENDER"]

def get_collections():

	#include also the scene base collection
	colls = [bpy.context.scene.collection, *bpy.data.collections]
	return [i for i in colls if i.name.startswith(PREFIX)]

def get_collections_which_have_light_objects():

	#include also the scene base collection
	colls = [bpy.context.scene.collection, *bpy.data.collections]
	return [i for i in colls if i.name.startswith(PREFIX) and any(o.type == "LIGHT" and o.data.vray.light_type != "BLENDER" for o in i.objects)]

def get_collection_light_objects(coll: bpy.types.Collection):
	return [o for o in coll.objects if o.type == "LIGHT" and o.data.vray.light_type != "BLENDER"]

#==================================================================================================

def sky(is_environment_node=False,
			is_link_environment_to_output=False,
			link_env_and_output=False,
			unlink_env_and_output=False
			):
	
	def get_env_node():
		return next((node for node in ntree.nodes if node.bl_idname == "VRayNodeEnvironment"), None)

	def get_output_node():
		return next((node for node in ntree.nodes if node.bl_idname == "VRayNodeWorldOutput"), None)
			
	def is_environment_linked_to_output():
		if env_node := get_env_node():
			return any(l.to_node.bl_idname == "VRayNodeWorldOutput" and l.from_node == env_node for l in ntree.links)
		return None

	def link_env():
		env = get_env_node()
		out = get_output_node()
		if env and out:
			ntree.links.new(out.inputs['Environment'], env.outputs['Environment'])
			world = bpy.context.scene.world
			world['hide_viewport'] = False

	def unlink_env():
		env = get_env_node()
		out = get_output_node()
		if env and out:
			#get the link
			link = next((l for l in ntree.links if l.to_node == out and l.from_node == env), None)
			if link:
				ntree.links.remove(link)
			
			world = bpy.context.scene.world
			world['hide_viewport'] = True

	if w := bpy.context.scene.world:

		ntree = w.node_tree
		
		if is_link_environment_to_output:
			return is_environment_linked_to_output()
		elif is_environment_node:
			return get_env_node()		
		elif link_env_and_output:
			link_env()
		elif unlink_env_and_output:
			unlink_env()
								
			return True				
	else:
		print("world not found")		



#Selected lamp object's properties>data
#C.screen.areas[0].spaces.active.context = "DATA"