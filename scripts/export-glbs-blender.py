import bpy
import os
import sys

# --- Parse blend file path from command line args after '--' ---
argv = sys.argv
if "--" in argv:
    idx = argv.index("--")
    custom_args = argv[idx + 1:]
else:
    custom_args = []

if not custom_args:
    print("❌ Please provide the blend file path after '--'")
    sys.exit(1)

blend_file = custom_args[0]
export_path = os.path.dirname(blend_file)

# --- Open the specified .blend file ---
bpy.ops.wm.open_mainfile(filepath=blend_file)

# --- Clear location (Alt+G) for all objects ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.location_clear(clear_delta=False)
bpy.ops.object.select_all(action='DESELECT')

# --- Export each visible mesh object by collection ---
visible_objects = [obj for obj in bpy.context.scene.objects if obj.visible_get()]
exported_count = 0

for obj in visible_objects:
    if obj.type != 'MESH':
        continue

    # Try to get first non-hidden collection the mesh belongs to
    collection_name = None
    for coll in obj.users_collection:
        if not coll.hide_viewport:
            collection_name = coll.name
            break
    if not collection_name:
        collection_name = "Uncategorized"

    # Prepare directory and file path
    folder_path = os.path.join(export_path, collection_name)
    os.makedirs(folder_path, exist_ok=True)

    filename = obj.name + ".glb"
    filepath = os.path.join(folder_path, filename)

    # Export this mesh only
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=True
    )

    # Delete after export
    bpy.ops.object.delete()
    exported_count += 1

print(f"✅ Exported {exported_count} mesh(es) into collection-named folders under {export_path}")
