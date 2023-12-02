# blender_pop_export
## Blender addon for .pop files needed for Tarmac (Mario Kart 64 custom course population data)

Necessary for Mario Kart 64 custom course creation, if you're a Blender user.
The addon will parse a bezier curve for the course's main path and looks for specifically named objects in order to compile everything into a file, which then can be used in Tarmac.



## Installation:

Install it like any other addon via user preferences and enable the addon.
File-->Export-->Mario Kart 64 POP (.OK64.POP) will bring up the save dialog.
Make sure to have your BezierCurve selected as the active object (A reminder message will appear, in case you forget to do that)

For blender versions below 2.8 use **_export_pop_v1_blender.py_**

For blender versions 2.8 to 2.92 use **_export_pop_v1_blender2,8.py_**

For blender versions 2.93 and above use **_export_pop_v1_blender2,93.py_**


![Addon](https://i.imgur.com/wb9fKMQ.png)

## Usage:

Please refer to this tutorial video to get an idea how to set up your data and export it properly for Tarmac

[![Tutorial](https://i.imgur.com/BQhocIO.png)](https://www.youtube.com/watch?v=2u1L_epK7mg "(Tutorial) MK64 Custom Course Creation - Blender 2.79 [Stream]")
