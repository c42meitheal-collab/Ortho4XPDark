# 🛣️ XRoads - Transparent Roads for Ortho4XPDark

## 🎆 Revolutionary Road Technology by melbo

**Creator**: [melbo](https://forums.x-plane.org/profile/895828-melbo/) - X-Plane.org Forums  
**Integration**: Ortho4XPDark Team  
**Purpose**: Show satellite imagery through roads instead of artificial X-Plane road textures  

---

## 🎯 What XRoads Does

XRoads is a revolutionary X-Plane library that dramatically improves the realism of Ortho4XP orthoscenery by making road polygons transparent. This allows the beautiful satellite imagery detail to show through roads instead of covering it with artificial road textures.

### 🌟 Key Benefits:
- **🖼️ Satellite Road Detail**: See actual road surfaces from aerial photography
- **🌿 Natural Integration**: Roads blend seamlessly with surrounding terrain
- **🇮🇪 Perfect for Ireland/UK**: Preserves stone walls, hedgerows, and rural character
- **⚡ Performance Boost**: Slightly increased FPS from reduced polygon rendering
- **🎨 Selective Application**: Only affects tiles with orthoscenery

### 🛣️ What Remains Visible:
- **Bridges**: Maintained for proper elevation representation
- **Highways & Autobahn**: Preserved for major infrastructure
- **Railroad Tracks**: Train infrastructure remains visible
- **Airport Areas**: Aviation infrastructure unaffected

To allow better control where to enable or disable these autogen roads, a library.txt file gets generated, which contains the coordinates of all available Ortho4XP tiles. These tiles will then be using the "transparent roads". Locations for which we do not have a Ortho tile, the autogen roads are still being shown.

---

## 🌑 Ortho4XPDark Integration

### 🎯 Seamless GUI Control
XRoads is now fully integrated into Ortho4XPDark with a dedicated GUI control panel:

- **⚙️ Configuration Tab**: Dedicated 🛣️ XRoads tab in the config window
- **🌍 Auto-Detection**: Automatic regional settings based on tile coordinates
- **🎮 One-Click Control**: Enable/disable with simple checkboxes
- **🇮🇪 Ireland/UK Optimized**: Pre-configured settings for Irish/UK scenery
- **🎯 Transparency Control**: Adjust how much satellite detail shows through

### 🎱 How to Use in Ortho4XPDark:
1. **Launch Ortho4XPDark**: `python launch.py`
2. **Open Config**: Click the ⚙️ Config button
3. **Navigate to XRoads**: Click the 🛣️ XRoads tab
4. **Configure Settings**:
   - ✅ Enable XRoads (default: enabled for Ireland/UK)
   - 🎯 Set transparency level (default: 0.85 for Ireland/UK)
   - 🗺️ Choose road types (motorway, trunk, primary, etc.)
   - 🌍 Select country preset or enable auto-detection
5. **Apply to Tiles**: Click "Apply to Current Tile" or build tiles normally

### 🇮🇪 Ireland/UK Optimization:
- **Higher Transparency (0.85)**: More satellite detail visible
- **Rural Road Focus**: Perfect for narrow Irish country lanes
- **Coastal Enhancement**: Accurate shoreline road representation
- **Stone Wall Preservation**: Maintains traditional Irish landscape features

---

## 🚗 AI Traffic Enhancement

During the creation of the new roads.net files, the "speed" of the AI cars is being reduced to 70%. This makes the cars travel with a more realistic speed. The 70% is the default but the command line option "-v" (stands for Velocity) can be used to select any other percentage between 50 and 100%.

After installation you simply run the binary again if Ortho tiles have been added or deleted. The program will then just update the existing library.txt accordingly.

"xroads" looks for folders and shortcuts starting with "zOrtho..." to get the tile coordinates. It is also scanning the "Earth nav data" folder inside sceneries folders (or symlinks) whos name start with "zPhoto...", "zVstates.." and "z_..." . The difference is, that it still works on Ortho4XP tiles as before, but it also works on "Ortho bundles", which cover multiple tiles, like the "US Orthophotos" provided by @Forkboy2. To hide the roads network on them, just rename your scenery folder to start with "zOrtho", "zPhoto" ,"zVstates" or "z_" and run the program. That's it.

Some examples:

    zOrtho4XP_+48+011
    zOrtho_some_cool_ortho
    zOrtho_Forkboy2_California_v5
    zPhoto_Italy_Milano
    z_ortho_1234
    z_ParisTexas



Xroads "help" and command line options (macos example):



   % ./xroads
   Xroads - 0.46 - melbo @x-plane.org

     usage: ./xroads [-v velocity] [-l] [-r] [-s] [-d] [-h]

       -v  set percentage of default car velocity
       -l  left hand driving support
       -r  hide rail tracks
       -s  hide street lights
       -d  print debug information
       -h  this help



# 💾 Installation

## 🌑 Option 1: Integrated with Ortho4XPDark (Recommended)

**XRoads is already integrated into your Ortho4XPDark system!**

🚀 **Quick Start:**
```bash
# Test XRoads integration
python test_xroads.py

# Launch Ortho4XPDark with XRoads
python launch.py
```

🎱 **Using the GUI:**
1. Open Ortho4XPDark configuration window
2. Navigate to the 🛣️ XRoads tab
3. Configure settings for your region
4. Apply to tiles automatically during building

✨ **Benefits of Integration:**
- 🎮 **GUI Control**: No command line needed
- 🌍 **Auto-Detection**: Settings chosen automatically for Ireland/UK
- 📋 **Per-Tile Configuration**: Different settings for different regions
- 🔄 **Seamless Workflow**: Applied during normal tile building

## 💻 Option 2: Standalone Installation (Manual)

**For advanced users who want direct XRoads control:**

Download the ZIP file and copy the correct binary (xroads.exe for Windows, xroads.app for macOS) to your X-Plane base directory and execute it. The program creates a folder "Xroads" in your "Custom Scenery" folder. Then it copies the "roads.net" and "roads-EU.net" files from the "default scenery" to it and modifies them on the fly. 

It also creates a "library.txt" file inside the "Custom Scenery/Xroads" folder. The library.txt contains the coordinates of the tiles which should use "transparent roads". The coordinates are taken from the "Earth nav data" folders from sceneries whos name start with "zOrtho", "zPhoto", "zVstates" or "z_".

The content of an optional xroads.pre in the same folder is being inserted BEFORE the region definition.
The content of an optional xroads.add in the same folder is being inserted AFTER the tile coordinates. This allows to set non-Ortho tiles to use "transparent roads" as well.
The content of an optional xroads.opt is being APPENDED to the and of the library.txt, which allows manual additions.


# Uninstall

Simply delete the "Xroads" folder in your "Custom Scenery" folder and restart X-Plane. No other file has been changed. 


# scenery_packs.ini

Make sure the Xroads folder stay on the top of your scenery_packs.ini.


# Build

Windows:

    requires "dirent.h"  ( i.e. from https://github.com/tronkko/dirent/blob/master/include/dirent.h )

	cl xroads.c /D "NODEBUG" /O2 /link Ole32.lib


macOS or Linux:

	make xroads



# Left-Hand-Driving Support

Based on @troopie's idea, Xroads is now able to integrate LHD into the transparent roads too. However there is some manual work to do.

First create a "xroads.add" file inside the X-Plane main folder. Its content will be included in the generated library.txt. You can simply use the one included in the ZIP file and add/remove the tile coordinates you want to use LHD. You will have to put the tiles coordinates under the Xroads_UK or Xroads_LH definition. The difference is which NET file is being used ( roads.net or roads_EU.net). The format is the same as in the existing library.txt. Actually you can just copy/paste tile coordinates from the library.txt to the xroads.add file.

Next step is to run xroads ( exe or app ) with the command line option "-l" (stands for LHD). You can use the included "xroads.bat" file which you can edit with NOTEPAD or any other text-editor. Note: Starting a line with REM turns the whole line into a comment, so commands in that line are not executed. It allows you to prepare the command with parameters but you only need click on the BAT and let it pass the options automatically to the binary.

---

## 🎆 Credits & Attribution

### 🌟 **Original Creator**
**🛣️ melbo** - [X-Plane.org Profile](https://forums.x-plane.org/profile/895828-melbo/)
- 🎨 **Visionary**: Conceived and created the XRoads transparent roads system
- 🔧 **Developer**: Built the entire XRoads architecture and implementation
- 🌎 **Community Leader**: Shared this revolutionary technology with the X-Plane community
- 🏆 **Innovation**: Pioneered transparent road technology for flight simulation

### 🌑 **Ortho4XPDark Integration**
**Ortho4XPDark Development Team**
- 🎮 **GUI Integration**: Created seamless configuration interface
- 🇮🇪 **Ireland/UK Optimization**: Specialized presets for regional excellence
- 🌍 **Auto-Detection**: Intelligent regional setting selection
- 🔄 **Workflow Integration**: Embedded into Ortho4XP tile building process

### 🌎 **Community Contributors**
- **🇮🇪 Irish Pilots**: Regional expertise and testing feedback
- **🇨🇾 @troopie**: Left-hand driving integration concept
- **🇨🇾 @Forkboy2**: Ortho bundle compatibility insights
- **🌎 X-Plane Community**: Continuous feedback and improvement suggestions

### 📚 **Technical Foundation**
- **🚀 Laminar Research**: X-Plane flight simulator platform
- **🎯 Sonny**: Original Ortho4XP creator and visionary
- **✈️ Oscar Pilote**: Ortho4XP development and community leadership
- **🔧 shred86**: Modern Ortho4XP enhancements and maintenance

---

## 🎆 Thank You melbo!

**The entire Ortho4XPDark community extends our heartfelt gratitude to melbo for:**

🎯 **Revolutionary Vision**: Creating a technology that transforms orthoscenery realism  
💫 **Technical Excellence**: Building a robust, efficient, and reliable system  
🌎 **Community Spirit**: Sharing this incredible tool freely with the flight simulation community  
🇮🇪 **Perfect for Ireland/UK**: A system that makes Irish and UK scenery absolutely stunning  
🚀 **Ongoing Innovation**: Continuing to improve and expand XRoads capabilities  

**XRoads + Ortho4XPDark = The ultimate combination for photorealistic Ireland/UK orthoscenery!**

---

*"Where Intelligence Meets Darkness - Enhanced with Revolutionary Road Technology"*

**Built with respect for melbo's incredible innovation and the entire X-Plane community.**
