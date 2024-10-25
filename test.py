import bpy

def light_collections():

	prefix = "V"
	C = bpy.context
	coll = {i.name: i for i in C.scene.collection.children_recursive if i.name.startswith(prefix)}

	print(f'Collections starting with "{prefix}":')
	for name, collection in coll.items():
		print("Collection:",name)
		for obj in collection.objects:
			if obj.type == "LIGHT":
				print("   ", obj.name)
			else:
				print("    Not light:", obj.name)


