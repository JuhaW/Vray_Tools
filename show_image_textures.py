import bpy
from bpy.props import StringProperty, IntProperty
from bpy.utils import register_classes_factory
from . import functions as F
import sys
import inspect


def Vray_material_panel(self, context):
	
	layout = self.layout
	layout.operator('object.vray_show_textures', icon = 'IMAGE_DATA')

def node_images_get(material): #return dictionary : {"active" / "nodename": image}
	
	images = {}
	for node in material.node_tree.nodes:
	
		#search image texture
		if hasattr(node, 'vray_plugin') and node.vray_plugin in ('TexBitmap','BitmapBuffer'):

			if node.texture.image:
			
				if material.node_tree.nodes.active == node and material.node_tree.nodes.active.select:
					images.update({"active" : node.texture.image})
					
				else:
					images.update({node.name : node.texture.image})
						
	return images
	#["active:", "1.jpg"]
	#["V-Ray Bitmap", "1.jpg"]
	#["V-Ray Bitmap.001", "1.jpg"]

def create_blender_render_nodes(nodetree, image):

	#node_types = ["ShaderNodeOutputMaterial","ShaderNodeBsdfDiffuse","ShaderNodeTexImage","NodeFrame"]
	node_types = ["ShaderNodeTexImage","NodeFrame"]
	nodes = []

	for node_type in node_types:
		nodes.append(nodetree.nodes.new(type=node_type))
	
	#nodes[1].location.x -= 300
	nodes[0].image = image
	nodes[0].hide = True
	nodes[0].mute = True
	nodes[0].location.x -= 600
	
	#link sockets
	#nodetree.links.new(nodes[1].outputs["BSDF"], nodes[0].inputs["Surface"])
	#nodetree.links.new(nodes[2].outputs["Color"], nodes[1].inputs["Color"])
	
	for node in nodes[:-1]:
		node.parent = nodes[1] #Frame is parent

	#frame label
	nodes[1].label = "Blender render nodes"
	nodes[1].location.y += 700

def find_material_image(o):
	
	materials = F.materials_get(o)
	if not materials:
		return
	#skip materials without node tree
	materials = [i for i in materials if i.node_tree]

	if not materials:
		return

	for mat in materials:
		
		#if material has no node tree, skip it
		if not mat.node_tree:
			print ("Material has no node tree: ", mat.name)
			continue
		images = node_images_get(mat)

		#check if image file node is selected, it overrites image which is shown at 3dview
		if images:

			if "active" in images.keys():
				image = images["active"] 
				print ("Bitmap node has image and node is active")
			else:
				image = next(iter(images.values()))
				print ("Bitmap image node is not active")

			create_blender_render_nodes(mat.node_tree, image)



