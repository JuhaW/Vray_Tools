import bpy
from bpy.utils import previews


VRAY_ICONS = previews.new()
CUSTOM_ICONS = previews.new()


def load_VRay_icons():
	global VRAY_ICONS
	path = bpy.utils.script_path_user()
	path += r"/addons/vray_blender/resources/icons/"

	icon_names={"SUN":"VRayLightSun", "DOME":"VRayLightDome", "RECT":"VRayLightRectangle",
					"SPHERE":"VRayLightSphere", "SPOT":"VRayLightSpot",
					"MESH":"VRayLightMesh", "SUN_SKY":"VRaySunSky"}

	for i in icon_names.keys():
		VRAY_ICONS.load(name=i, path=path+icon_names[i]+".png", path_type='IMAGE')
	print("Vray icons loaded")

def unload_VRay_icons():
	previews.remove(VRAY_ICONS)
	print("Vray icons unloaded")

def load_Custom_icons():
	import pathlib
	global CUSTOM_ICONS
	#get current file path
	#pathlib.Path(__file__).parent
	
	path = str(pathlib.Path(__file__).parent) + r"/icons/"
	icon_names={"SOLO":"Solo"}

	for i in icon_names.keys():
		CUSTOM_ICONS.load(name=i, path=path+icon_names[i]+".png", path_type='IMAGE')
	print("Custom icons loaded from:", path)


def unload_Custom_icons():
	previews.remove(CUSTOM_ICONS)
	print("Custom icons unloaded")