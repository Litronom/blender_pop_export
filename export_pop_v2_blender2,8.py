bl_info = {
    "name": "Export .OK64.POP Data",
    "author": "Robichu; Litronom",
    "version": (2, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Export > Mario Kart 64 POP (.OK64.POP)",
    "description": "Export Population Data (.OK64.POP)",
    "warning": "",
    "category": "Import-Export"}

import bpy
import os
import time
import math
import struct


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator, WindowManager


def export_pop_data(context, props, filepath):
    print("running export_pop_data...")
    file = open(filepath, 'w', encoding='utf-8')
    ob = bpy.context.object # active object
    childcurve = ob.children
    
    loopcount = 1
    
# iterate over points of the curve's first spline
    for u in childcurve:
        loopcount += 1    
    pointCount = len(ob.data.splines.active.bezier_points)
    file.write("path")
    file.write('\n')
    file.write(str(loopcount))
    file.write('\n')
    file.write(str(pointCount))
    file.write('\n')
    for p in ob.data.splines.active.bezier_points:
        file.write("[")
        file.write(str((p.co.x))+",")
        file.write(str((p.co.y))+",")
        file.write(str((p.co.z)))
        file.write("]")
        file.write('\n')
        file.write("1")
        file.write("\n")
    
    for a in childcurve:

        pointCount = len(a.data.splines.active.bezier_points)
        file.write(str(pointCount))
        file.write('\n')
        for p in a.data.splines.active.bezier_points:
            file.write("[")
            file.write(str((p.co.x))+",")
            file.write(str((p.co.y))+",")
            file.write(str((p.co.z)))
            file.write("]")
            file.write('\n')
            file.write("1")
            file.write("\n")

    file.write("item")
    file.write('\n')
    file.write("1")
    file.write('\n')
    itemCount = 0
    for a in bpy.data.objects:
        if a.name.startswith('itembox') and props.use_item:
            itemCount += 1
    file.write(str(itemCount))
    file.write('\n')
    for b in bpy.data.objects:
        if b.name.startswith('itembox') and props.use_item:
            file.write("[")
            file.write(str((b.location.x))+",")
            file.write(str((b.location.y))+",")
            file.write(str((b.location.z)))
            file.write("]")
            file.write('\n')
            file.write("1")
            file.write("\n")

		
    file.write("tree")
    file.write('\n')
    file.write("1")
    file.write('\n')
    treeCount = 0
    for a in bpy.data.objects:
        if a.name.startswith('tree') and props.use_tree:
            treeCount += 1
    file.write(str(treeCount))
    file.write('\n')
    for b in bpy.data.objects:
        if b.name.startswith('tree') and props.use_tree:
            file.write("[")
            file.write(str((b.location.x))+",")
            file.write(str((b.location.y))+",")
            file.write(str((b.location.z)))
            file.write("]")
            file.write('\n')
            file.write("1")
            file.write("\n")


		
    file.write("piranha")
    file.write('\n')
    file.write("1")
    file.write('\n')
    piranhaCount = 0
    for a in bpy.data.objects:
        if a.name.startswith('piranha') and props.use_piranha:
            piranhaCount += 1
    file.write(str(piranhaCount))
    file.write('\n')
    for b in bpy.data.objects:
        if b.name.startswith('piranha') and props.use_piranha:
            file.write("[")
            file.write(str((b.location.x))+",")
            file.write(str((b.location.y))+",")
            file.write(str((b.location.z)))
            file.write("]")
            file.write('\n')
            file.write("1")
            file.write("\n")

		
    file.write("redcoin")
    file.write('\n')
    file.write("1")
    file.write('\n')
    redcoinCount = 0
    for a in bpy.data.objects:
        if a.name.startswith('redcoin') and props.use_redcoin:
            redcoinCount += 1
    file.write(str(redcoinCount))
    file.write('\n')
    for b in bpy.data.objects:
        if b.name.startswith('redcoin') and props.use_redcoin:
            file.write("[")
            file.write(str((b.location.x))+",")
            file.write(str((b.location.y))+",")
            file.write(str((b.location.z)))
            file.write("]")
            file.write('\n')
            file.write("1")
            file.write("\n")
		
    file.close()
    ShowMessageBox("Pop data exported to file", "Finished", 'PLUS')
    return {'FINISHED'}


def export_empty(context, props, filepath):
    print("WARNING: no active curve")
    
    
    ShowMessageBox("Make sure to have a BezierCurve selected before exporting", "WARNING - BezierCurve not selected", 'ERROR')
    return {'FINISHED'}

def ShowMessageBox(message = "", title = "", icon = ''):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


class PopExport(Operator, ExportHelper):
    """Saves POP data for Mario Kart 64 custom courses"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Save OK64.POP File"
    
    filename_ext = ".OK64.POP"    # ExportHelper mixin class uses this

    filter_glob = StringProperty(
            default="*.OK64.POP",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    use_item = BoolProperty(
            name="Item Boxes",
            description="Export Item Boxes",
            default = True,
            )
               
    use_tree = BoolProperty(
            name="Trees",
            description="Export Trees",
            default=True,
            )

    use_piranha = BoolProperty(
            name="Piranhas",
            description="Export Piranha Plants",
            default=True,
            )

    use_redcoin = BoolProperty(
            name="Red Coins",
            description="Export Red Coins",
            default=True,
            )

    
    def execute(self, context):
        start_time = time.time()
        print('\n_____START_____')
        props = self.properties
        filepath = self.filepath
        filepath = bpy.path.ensure_ext(filepath, self.filename_ext)
        ob = bpy.context.object
        if ob.type in ['CURVE']:

            exported = export_pop_data(context, props, filepath)

            if exported:

                print('finished export in %s seconds' %((time.time() - start_time)))
                print(filepath)

            return {'FINISHED'}
        else:

            empty = export_empty(context, props, filepath)

                
            return {'FINISHED'}   

def menu_func_export(self, context):
    self.layout.operator(PopExport.bl_idname, text="Mario Kart 64 POP (.OK64.POP)")


def register():
    bpy.utils.register_class(PopExport)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(PopExport)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
    
