bl_info = {
    "name": "Export .OK64.POP3 Data",
    "author": "Litronom",
    "version": (3, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Export > Mario Kart 64 POP (.OK64.POP3)",
    "description": "Export Population Data (.OK64.POP3)",
    "warning": "",
    "category": "Import-Export"
}

import bpy
import os
import re
import time
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, CollectionProperty
from bpy.types import Operator, PropertyGroup


def export_pop_data(context, self, filepath, course_pop, main_curve, bezier_curves, child_curves):
    print("running export_pop_data...")

    collection = filepath
    with open(collection, 'w', encoding='utf-8') as file:
        for name_prop in self.export_names:
            if name_prop.export:
                section_name = name_prop.name
                file.write("{}\n".format(section_name))


    extension = ".OK64.POP3"
    directory, filename_with_extension = os.path.split(filepath)
    filename_without_extension = re.sub(r'\.OK64|\.POP3|\.PackPOP3', '', filename_with_extension)

    filecount = 0

    for name_prop in self.export_names:
        section_name = name_prop.name

        if name_prop.export:
            section_filepath = os.path.join(directory, "{}_{}{}".format(filename_without_extension, section_name, extension))

            with open(section_filepath, 'w', encoding='utf-8') as file:
                if section_name == "path":
                    loopcount = len(child_curves) + 1
                    
                    file.write("{}\n".format(section_name))
                    file.write("{}\n".format(loopcount))

                    pointCount = len(main_curve.data.splines.active.bezier_points)
                    file.write("{}\n".format(pointCount))

                    for p in main_curve.data.splines.active.bezier_points:
                        file.write("[{:.6f},{:.6f},{:.6f}]\n1\n".format(p.co.x, p.co.y, p.co.z))

                    for a in child_curves:
                        pointCount = len(a.data.splines.active.bezier_points)
                        file.write("{}\n".format(pointCount))
                        for p in a.data.splines.active.bezier_points:
                            file.write("[{:.6f},{:.6f},{:.6f}]\n1\n".format(p.co.x, p.co.y, p.co.z))

                    filecount += 1
                    print("exported to ", section_filepath)

                else:
                    names = {}
                    for obj in course_pop.children:
                        if obj.type != 'CURVE' and not obj.name.endswith("."):
                            obj_name = obj.name.split('.')[0]
                            location = obj.location
                            if obj_name == section_name:
                                if section_name not in names:
                                    names[section_name] = {'count': 0, 'locations': []}
                                names[section_name]['count'] += 1
                                names[section_name]['locations'].append(location)
                    
                    count = names[section_name]['count']
                    locations = names[section_name]['locations']
                    file.write("{}\n{}\n{}\n".format(section_name, 1, count))
                    for location in locations:
                        file.write("[{:.6f},{:.6f},{:.6f}]\n1\n".format(location.x, location.y, location.z))
                
                    filecount += 1
                    print("exported to ", section_filepath)

    if filecount:
        show_message_box("POP3: {} files exported".format(filecount), "Finished", 'PLUS')
    else:
        show_message_box("POP3: No Files exported", "Finished", 'CANCEL')

    return {'FINISHED'}


def show_message_box(message="", title="", icon=''):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


class NamePropertyGroup(PropertyGroup):
    name = StringProperty()
    description = StringProperty()
    export = BoolProperty(default=True)


class PopExport(Operator, ExportHelper):
    """Exports .POP3 data for MK64. Requires object named 'Course Population'"""
    bl_idname = "export_test.some_data"
    bl_label = "Save OK64.POP3 File"
    
    filename_ext = ".PackPOP3"
    filter_glob = StringProperty(
        default="*.PackPOP3",
        options={'HIDDEN'},
        maxlen=255,
    )

    export_names = CollectionProperty(type=NamePropertyGroup)

    @classmethod
    def poll(cls, context):
        return bpy.data.objects.get("Course Population") is not None

    def invoke(self, context, event):
        course_pop = bpy.data.objects.get("Course Population")
        if not course_pop:
            show_message_box("No object named 'Course Population' found", "ERROR", 'ERROR')
            return {'CANCELLED'}
        
        if not course_pop.children:
            show_message_box("'Course Population' object has no children", "ERROR", 'ERROR')
            return {'CANCELLED'}

        bezier_curves = [obj for obj in course_pop.children if obj.type == 'CURVE' and obj.data.splines.active.type == 'BEZIER']
        if not bezier_curves:
            show_message_box("No Bezier curve found among the children of 'Course Population'", "ERROR", 'ERROR')
            return {'CANCELLED'}
        
        if len(bezier_curves) > 1:
            show_message_box("More than 1 main Bezier curve found among the children of 'Course Population'", "ERROR", 'ERROR')
            return {'CANCELLED'}

        main_curve = bezier_curves[0]
        child_curves = [obj for obj in main_curve.children if obj.type == 'CURVE' and obj.data.splines.active.type == 'BEZIER']

        if len(child_curves) > 3:
            show_message_box("More than 3 alternative Bezier curves found among the children of the main Bezier curve", "ERROR", 'ERROR')
            return {'CANCELLED'}

        self.export_names.clear()
        name_set = set()

        name_set.add("path")
        name_prop = self.export_names.add()
        name_prop.name = "path"
        name_prop.description = "Export path"

        for obj in course_pop.children:
            if obj.type != 'CURVE' and not obj.name.endswith("."):
                name = obj.name.split('.')[0]
                if name not in name_set:
                    name_set.add(name)
                    name_prop = self.export_names.add()
                    name_prop.name = name
                    name_prop.description = "Export {}".format(name)

        return ExportHelper.invoke(self, context, event)

    def execute(self, context):
        start_time = time.time()
        print('\n_____START_____')
        props = self.export_names
        filepath = self.filepath
        filepath = bpy.path.ensure_ext(filepath, self.filename_ext)

        course_pop = bpy.data.objects.get("Course Population")
        bezier_curves = [obj for obj in course_pop.children if obj.type == 'CURVE' and obj.data.splines.active.type == 'BEZIER']
        main_curve = bezier_curves[0]
        child_curves = [obj for obj in main_curve.children if obj.type == 'CURVE' and obj.data.splines.active.type == 'BEZIER']

        exported = export_pop_data(context, self, filepath, course_pop, main_curve, bezier_curves, child_curves)
        if exported:
            print('finished export in %s seconds' % (time.time() - start_time))
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        for name_prop in self.export_names:
            row = layout.row()
            row.prop(name_prop, "export", text=name_prop.name)
            row.label(text=name_prop.description)


def menu_func_export(self, context):
    if "Course Population" in bpy.data.objects:
        label = "Mario Kart 64 POP (.OK64.POP3)"
    else:
        label = "Mario Kart 64 POP (.OK64.POP3) / missing object: 'Course Population'"
    self.layout.operator(PopExport.bl_idname, text=label)


def register():
    bpy.utils.register_class(NamePropertyGroup)
    bpy.utils.register_class(PopExport)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(NamePropertyGroup)
    bpy.utils.unregister_class(PopExport)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
