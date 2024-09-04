import bpy
from collections import OrderedDict
import ast
import inspect
import sys
from . import operators as Op

SHADOW_CATCHER_OBJECT_TYPES = ('MESH', 'CURVE','SURFACE','META','FONT')

def get_object_materials(o):
	return list(OrderedDict.fromkeys(o.data.materials))
	#return list(set(filter(None, o.data.materials)))
	
def is_VRay_node(n):
	return hasattr(n, "vray_plugin")


def materials_get(o):

	mats = list(OrderedDict.fromkeys(o.data.materials))
	return mats if mats != [None] else None


def node_if_reroute_has_connect(node):
	
	#o.active_material.node_tree.nodes.active.inputs[0].links
	if not node.inputs[0].links:
		return False	

	return True

def remove_blender_nodes(o):

	materials = materials_get(o)
	#skip if no materials on object
	if not materials:
		return
	#skip materials without node tree
	materials = [i for i in materials if i.node_tree]


	for i in materials:
	
		_nodes = i.node_tree.nodes

		#Blender render nodes
		for n in _nodes[:]:
			if not is_VRay_node(n) and not n.bl_idname.startswith(("NodeFrame","NodeReroute")):
				i.node_tree.nodes.remove(n)
		#Reroute	nodes			
		for n in _nodes[:]:
			if n.bl_idname == "NodeReroute":
				if not node_if_reroute_has_connect(n):
					i.node_tree.nodes.remove(n)					
		#Frame nodes
		# Collect all frame nodes
		frame_nodes = [node for node in _nodes if node.bl_idname == 'NodeFrame']
		# Check if frame node has content, if has continue to next frame node
		# If no content, delete frame node and start frame loop from the beginning
		content_found = False 
		frame_deleted = True #this is needed to check if during the loop there was any frame node deletion

		while frame_nodes and frame_deleted:
			frame_deleted = False
			for frame in frame_nodes[:]:
				content_found = False
				for n in _nodes[:]:
					
					#any frame content found ?
					if n.parent == frame:
						#Yes, continue
						content_found = True
						frame_deleted = False
						
						break

				if not content_found:
					frame_nodes.remove(frame)
					_nodes.remove(frame)
					frame_deleted = True

def vray_shadow_catcher(on):
	
	print("on:", on)
	matte = 'Shadow catcher '
	o = bpy.context.object
	if o.type not in SHADOW_CATCHER_OBJECT_TYPES:
		return
	if on :
		if not o.vray.VRayObjectProperties.matte_surface:
			o.vray.VRayObjectProperties.matte_surface = False
			o.vray.VRayObjectProperties.matte_surface = True
		o.vray.VRayObjectProperties.affect_alpha = True
		o.vray.VRayObjectProperties.shadows = True
		o.vray.VRayObjectProperties.alpha_contribution = -1
		o.name = matte + o.name if o.name[:len(matte)] != matte else o.name
		#o.draw_type = 'WIRE'
		vray_shadow_catcher_objects_get()

	else:

		o.vray.VRayObjectProperties.matte_surface = False
		o.name = o.name[len(matte):] if o.name[:len(matte)] == matte else o.name
		#o.draw_type = 'TEXTURED'
		vray_shadow_catcher_objects_get()

def v_ray_is_shadow_catcher_object(o):
	if o.type in SHADOW_CATCHER_OBJECT_TYPES:
		return o.vray.VRayObjectProperties.matte_surface and o.vray.VRayObjectProperties.alpha_contribution == -1.0
	return False

def v_ray_is_shadow_catcher_object_type(o):
	return o.type in SHADOW_CATCHER_OBJECT_TYPES

def vray_shadow_catcher_objects_get():
	
	objs =[o for o in bpy.context.view_layer.objects if o.type in SHADOW_CATCHER_OBJECT_TYPES]

	objects = []
	sco = bpy.context.scene.addon.shadow_catcher_objects
	sco.clear()

	for o in objs:
		if v_ray_is_shadow_catcher_object(o):
			a = sco.add()
			a.obj = o

def vray_select_object(idx):
	o = bpy.context.scene.addon.shadow_catcher_objects[idx].obj
	bpy.ops.object.select_all(action="DESELECT")
	o.select_set(True)
	bpy.context.view_layer.objects.active = o

def is_derived_from_any_bpy_type(cls):
	bpy_base_classes = (
	bpy.types.Operator,
	bpy.types.Panel,
	bpy.types.PropertyGroup,
	bpy.types.Menu,
	bpy.types.UIList,
	bpy.types.Header,
	bpy.types.ID,  # Includes most data-blocks
	bpy.types.Node,  # For nodes
	bpy.types.NodeTree,  # For node trees
	# Add other bpy.types classes as needed
	)
	return any(issubclass(cls, base_class) for base_class in bpy_base_classes)

def get_classes_in_order(module_name, module_file):
	with open(module_file, "r") as source:
		tree = ast.parse(source.read())

	classes = []
	for node in tree.body:
		if isinstance(node, ast.ClassDef):
			class_name = node.name
			# Get the class object by name
			class_obj = getattr(sys.modules[module_name], class_name, None)
			if class_obj and inspect.isclass(class_obj) and is_derived_from_any_bpy_type(class_obj):
				classes.append(class_obj)
	return classes

def register_classes(module_name:str):
	if module_name != __package__:
		module_name = module_name.__name__
	else:
		module_name = __package__

	module = sys.modules.get(module_name)
	module_file = inspect.getfile(module)

	# Get classes in order of definition
	classes = get_classes_in_order(module_name, module_file)
	print("Module:", module_name);print()
	for cls in classes:
		bpy.utils.register_class(cls)
		print("Registered:", cls.__name__)
	print("="*40)

def unregister_classes(module_name:str):
	if module_name != __package__:
		module_name = module_name.__name__
	else:
		module_name = __package__

	module = sys.modules.get(module_name)
	module_file = inspect.getfile(module)

	# Get classes in order of definition
	classes = get_classes_in_order(module_name, module_file)
	print("Module:", module_name);print()
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
		print("Unregistered:", cls.__name__)
	print("="*40)