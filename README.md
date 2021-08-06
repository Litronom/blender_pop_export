# blender_pop_export
Blender addon for .pop files needed for Tarmac (Mario Kart 64 custom course population data)

Necessary for Mario Kart 64 custom course creation, if you're a Blender user.
The addon will parse a bezier curve for the course's main path and looks for specifically named objects.


Installation: 
Install it like any other addon via user preferences and enable the addon.
File-->Export-->Mario Kart 64 POP (.OK64.POP) will bring up the save dialog.
Make sure to have your BezierCurve selected as the active object (A reminder message will appear, in case you forget to do that)

For blender versions below 2.8 use export_pop_v1_blender.py
For blender versions 2.8 to 2.92 use export_pop_v1_blender2,8.py
For blender versions 2.93 and above use export_pop_v1_blender2,93.py
