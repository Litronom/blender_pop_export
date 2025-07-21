# blender_pop_export

## Blender addon for .pop files needed for Tarmac (Mario Kart 64 custom course population data)

Necessary for Mario Kart 64 custom course creation via Blender.
The addon will parse Bezier Curves for the course's main and alternative paths and it looks for uniquely named objects in order to compile everything into files for Tarmac.

## Installation:

Install it like any other addon via user preferences and enable the addon.
File-->Export-->Mario Kart 64 POP3 (.OK64.POP3) will bring up the save dialog.

For blender versions below 2.8 use ***__blender.py_**

For blender versions 2.8 to 2.92 use ***__blender2,8.py_**

For blender versions 2.93 and above use ***__blender2,93.py_**

![Addon](https://i.imgur.com/wb9fKMQ.png)

## Usage:

**For version 3 of the plugin**:
In your scene, create an object labeled **"Course Population"**.
Parent a Bezier Curve to it which will act as your main path for the track. Bezier Curves for alternative paths need to be parented to the main Bezier Curve (up to 3)
Item boxes, trees, piranha plants, red coins and all other custom objects also need to be parented to **"Course Population"**.
Name these objects whatever you want, they will be collected in a file as long as the main part of the name is the same for them. For example: **"Mario_Tree1"** and **"Mario_Tree1.001"** will be in the same output file. Blender's standard naming convention for duplication is taken into account.
Exporting via the save dialog will create a single .PackPOP3 file and multiple separate files, one for each set of uniquely named objects.
Each of those files can then be imported via Tarmac in order to populate your custom course.



**For version 1 and 2 of the plugin:**
Please refer to this tutorial video to get an idea how to set up your data and export it properly for Tarmac:

[![Tutorial](https://i.imgur.com/BQhocIO.png)](https://www.youtube.com/watch?v=2u1L_epK7mg "(Tutorial) MK64 Custom Course Creation - Blender 2.79 [Stream]")
