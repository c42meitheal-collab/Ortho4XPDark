"""
🛣️ Ortho4XPDark XRoads Integration System

Provides seamless integration with XRoads transparent roads system
for enhanced realism in orthophoto scenery.

Features:
- Toggle transparent roads on/off
- Support for LHD regions (UK/Ireland)
- Automatic Ortho4XP tile detection
- Custom road type filtering
- GUI integration with Ortho4XPDark
"""

import os
import sys
import subprocess
import threading
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Tuple

try:
    import O4_UI_Utils as UI
    import O4_File_Names as FNAMES
    from O4_Cfg_Vars import cfg_vars
    ORTHO4XP_AVAILABLE = True
except ImportError:
    ORTHO4XP_AVAILABLE = False

class XRoadsManager:
    """Manages XRoads transparent roads integration with Ortho4XPDark"""
    
    def __init__(self, xplane_path: str = "", custom_scenery_path: str = ""):
        self.xplane_path = xplane_path
        self.custom_scenery_path = custom_scenery_path or os.path.join(xplane_path, "Custom Scenery")
        self.xroads_path = os.path.join(self.custom_scenery_path, "Xroads")
        
        # XRoads configuration
        self.transparent_roads_enabled = False
        self.lhd_mode = False  # Left-hand drive for UK/Ireland
        self.preserve_highways = True
        self.preserve_bridges = True
        self.preserve_railroads = True
        self.reduce_car_speed = True
        
        # Detected Ortho4XP tiles
        self.ortho_tiles = []
        self.ortho_folders = []
        
    def detect_xplane_installation(self) -> Optional[str]:
        """Auto-detect X-Plane installation path"""
        common_paths = [
            "C:\\X-Plane 12",
            "C:\\X-Plane 11", 
            "C:\\Games\\X-Plane 12",
            "C:\\Games\\X-Plane 11",
            "D:\\X-Plane 12",
            "D:\\X-Plane 11"
        ]
        
        for path in common_paths:
            if os.path.exists(os.path.join(path, "X-Plane.exe")):
                self.xplane_path = path
                self.custom_scenery_path = os.path.join(path, "Custom Scenery")
                self.xroads_path = os.path.join(self.custom_scenery_path, "Xroads")
                return path
                
        return None
    
    def scan_ortho_tiles(self) -> List[Dict]:
        """Scan for Ortho4XP tiles in Custom Scenery"""
        self.ortho_tiles = []
        self.ortho_folders = []
        
        if not os.path.exists(self.custom_scenery_path):
            if ORTHO4XP_AVAILABLE:
                UI.vprint(0, f"Custom Scenery path not found: {self.custom_scenery_path}")
            return []
        
        try:
            for item in os.listdir(self.custom_scenery_path):
                item_path = os.path.join(self.custom_scenery_path, item)
                
                # Look for Ortho4XP scenery folders
                if os.path.isdir(item_path) and (
                    item.startswith("zOrtho4XP_") or
                    item.startswith("z_ortho") or
                    item.startswith("zPhoto") or
                    item.startswith("zVStates")
                ):
                    self.ortho_folders.append(item_path)
                    tiles = self._extract_tile_coordinates(item_path)
                    self.ortho_tiles.extend(tiles)
                    
                    if ORTHO4XP_AVAILABLE:
                        UI.vprint(2, f"Found Ortho4XP scenery: {item} with {len(tiles)} tiles")
            
            if ORTHO4XP_AVAILABLE:
                UI.vprint(1, f"XRoads: Detected {len(self.ortho_tiles)} Ortho4XP tiles in {len(self.ortho_folders)} folders")
                
        except Exception as e:
            if ORTHO4XP_AVAILABLE:
                UI.vprint(0, f"Error scanning Ortho4XP tiles: {e}")
                
        return self.ortho_tiles
    
    def _extract_tile_coordinates(self, scenery_path: str) -> List[Dict]:
        """Extract tile coordinates from Ortho4XP scenery folder"""
        tiles = []
        earth_nav_path = os.path.join(scenery_path, "Earth nav data")
        
        if not os.path.exists(earth_nav_path):
            return tiles
            
        try:
            for region_folder in os.listdir(earth_nav_path):
                region_path = os.path.join(earth_nav_path, region_folder)
                if os.path.isdir(region_path):
                    for dsf_file in os.listdir(region_path):
                        if dsf_file.endswith(".dsf"):
                            # Extract coordinates from filename like "+53-006.dsf"
                            try:
                                coords = dsf_file.replace(".dsf", "")
                                if coords.startswith("+") or coords.startswith("-"):
                                    lat_str = coords[:3]
                                    lon_str = coords[3:]
                                    lat = int(lat_str)
                                    lon = int(lon_str)
                                    
                                    tiles.append({
                                        'lat': lat,
                                        'lon': lon,
                                        'coord_string': coords,
                                        'scenery_path': scenery_path,
                                        'scenery_name': os.path.basename(scenery_path)
                                    })
                            except (ValueError, IndexError):
                                continue
        except Exception as e:
            if ORTHO4XP_AVAILABLE:
                UI.vprint(2, f"Error extracting coordinates from {scenery_path}: {e}")
                
        return tiles
    
    def generate_xroads_library(self) -> bool:
        """Generate XRoads library.txt file"""
        if not self.ortho_tiles:
            self.scan_ortho_tiles()
            
        if not self.ortho_tiles:
            if ORTHO4XP_AVAILABLE:
                UI.vprint(0, "No Ortho4XP tiles found for XRoads generation")
            return False
            
        try:
            # Create Xroads directory
            os.makedirs(self.xroads_path, exist_ok=True)
            
            library_path = os.path.join(self.xroads_path, "library.txt")
            
            with open(library_path, "w") as f:
                # Write header
                f.write("I\n")
                f.write("1200\n")
                f.write("LIBRARY\n\n")
                
                # Write exports for transparent roads
                f.write("# XRoads - Transparent Roads for Ortho4XP\n")
                f.write("# Generated by Ortho4XPDark\n\n")
                
                # Configure for LHD if enabled (UK/Ireland)
                if self.lhd_mode:
                    f.write("EXPORT_BACKUP lib/autos/road_nets/roads_EU.net lib/autos/road_nets/roads.net\n")
                    f.write("EXPORT_BACKUP lib/autos/road_nets/roads.net lib/autos/road_nets/roads_EU.net\n\n")
                
                # Write region definitions
                region_name = "Xroads_LH" if self.lhd_mode else "Xroads"
                f.write(f"REGION_DEFINE {region_name}\n")
                
                # Add tile coordinates
                for tile in sorted(self.ortho_tiles, key=lambda x: (x['lat'], x['lon'])):
                    coord_str = tile['coord_string']
                    f.write(f"REGION_POINT {coord_str}\n")
                
                f.write("REGION_POINT_END\n\n")
                
                # Apply transparent roads to region
                if self.preserve_highways:
                    f.write(f"REGION_RECT {region_name}\n")
                    f.write("EXPORT_EXCLUDE lib/autos/road_nets/roads.net lib/autos/road_nets/roads_transparent.net\n")
                else:
                    f.write(f"REGION_RECT {region_name}\n") 
                    f.write("EXPORT_EXCLUDE lib/autos/road_nets/roads.net lib/autos/road_nets/roads_transparent_all.net\n")
                
                f.write("REGION_RECT_END\n\n")
                
                # Add custom options if available
                self._add_custom_xroads_options(f)
                
            if ORTHO4XP_AVAILABLE:
                UI.vprint(1, f"XRoads library.txt generated with {len(self.ortho_tiles)} tiles")
                UI.vprint(1, f"LHD mode: {'Enabled' if self.lhd_mode else 'Disabled'}")
                
            return True
            
        except Exception as e:
            if ORTHO4XP_AVAILABLE:
                UI.vprint(0, f"Error generating XRoads library: {e}")
            return False
    
    def _add_custom_xroads_options(self, f):
        """Add custom XRoads options to library.txt"""
        # Read custom options files if they exist
        xroads_files = {
            "xroads.pre": "# Custom pre-region content\n",
            "xroads.add": "# Custom additional coordinates\n", 
            "xroads.opt": "# Custom options\n"
        }
        
        for filename, header in xroads_files.items():
            filepath = os.path.join(self.xplane_path, filename)
            if os.path.exists(filepath):
                f.write(f"\n{header}")
                try:
                    with open(filepath, "r") as custom_file:
                        f.write(custom_file.read())
                    f.write("\n")
                except Exception as e:
                    if ORTHO4XP_AVAILABLE:
                        UI.vprint(2, f"Warning: Could not read {filename}: {e}")
    
    def create_transparent_road_nets(self) -> bool:
        """Create transparent road network files"""
        try:
            # Paths to original road nets
            xplane_resources = os.path.join(self.xplane_path, "Resources", "default scenery", "default apt dat", "lib", "autos", "road_nets")
            roads_net = os.path.join(xplane_resources, "roads.net")
            roads_eu_net = os.path.join(xplane_resources, "roads_EU.net")
            
            # Destination paths
            xroads_lib = os.path.join(self.xroads_path, "lib", "autos", "road_nets")
            os.makedirs(xroads_lib, exist_ok=True)
            
            # Copy and modify road nets for transparency
            for source_file, dest_name in [(roads_net, "roads_transparent.net"), (roads_eu_net, "roads_transparent_EU.net")]:
                if os.path.exists(source_file):
                    dest_file = os.path.join(xroads_lib, dest_name)
                    self._create_transparent_net_file(source_file, dest_file)
                    
            if ORTHO4XP_AVAILABLE:
                UI.vprint(1, "XRoads transparent road networks created")
                
            return True
            
        except Exception as e:
            if ORTHO4XP_AVAILABLE:
                UI.vprint(0, f"Error creating transparent road nets: {e}")
            return False
    
    def _create_transparent_net_file(self, source: str, dest: str):
        """Create transparent version of road network file"""
        try:
            with open(source, "r") as src, open(dest, "w") as dst:
                for line in src:
                    # Make roads transparent but preserve certain types
                    if line.strip().startswith("ROAD_DRAPED"):
                        # Make draped roads transparent
                        if not (self.preserve_highways and "highway" in line.lower()):
                            if not (self.preserve_bridges and "bridge" in line.lower()):
                                # Add transparency
                                line = line.replace("ROAD_DRAPED", "ROAD_DRAPED TRANSPARENT")
                    
                    # Reduce car speed if enabled
                    if self.reduce_car_speed and "CAR_SPEED" in line:
                        try:
                            parts = line.split()
                            if len(parts) >= 2:
                                speed = float(parts[1])
                                new_speed = speed * 0.7  # Reduce to 70%
                                line = f"CAR_SPEED {new_speed:.1f}\n"
                        except (ValueError, IndexError):
                            pass
                    
                    dst.write(line)
                    
        except Exception as e:
            if ORTHO4XP_AVAILABLE:
                UI.vprint(0, f"Error creating transparent net file {dest}: {e}")
    
    def enable_transparent_roads(self) -> bool:
        """Enable XRoads transparent roads"""
        if not self.xplane_path:
            if not self.detect_xplane_installation():
                if ORTHO4XP_AVAILABLE:
                    UI.vprint(0, "X-Plane installation not found")
                return False
        
        try:
            # Scan for Ortho4XP tiles
            self.scan_ortho_tiles()
            
            if not self.ortho_tiles:
                if ORTHO4XP_AVAILABLE:
                    UI.vprint(0, "No Ortho4XP tiles found - transparent roads not needed")
                return False
            
            # Create transparent road networks
            if not self.create_transparent_road_nets():
                return False
                
            # Generate library.txt
            if not self.generate_xroads_library():
                return False
            
            self.transparent_roads_enabled = True
            
            if ORTHO4XP_AVAILABLE:
                UI.vprint(1, f"✅ XRoads transparent roads enabled for {len(self.ortho_tiles)} tiles")
                if self.lhd_mode:
                    UI.vprint(1, "🇬🇧 Left-hand drive mode enabled for UK/Ireland")
                    
            return True
            
        except Exception as e:
            if ORTHO4XP_AVAILABLE:
                UI.vprint(0, f"Error enabling transparent roads: {e}")
            return False
    
    def disable_transparent_roads(self) -> bool:
        """Disable XRoads transparent roads"""
        try:
            if os.path.exists(self.xroads_path):
                shutil.rmtree(self.xroads_path)
                
            self.transparent_roads_enabled = False
            
            if ORTHO4XP_AVAILABLE:
                UI.vprint(1, "XRoads transparent roads disabled")
                
            return True
            
        except Exception as e:
            if ORTHO4XP_AVAILABLE:
                UI.vprint(0, f"Error disabling transparent roads: {e}")
            return False
    
    def get_status(self) -> Dict[str, any]:
        """Get XRoads status information"""
        return {
            'enabled': self.transparent_roads_enabled,
            'xplane_path': self.xplane_path,
            'custom_scenery_path': self.custom_scenery_path,
            'xroads_path': self.xroads_path,
            'lhd_mode': self.lhd_mode,
            'ortho_tiles_count': len(self.ortho_tiles),
            'ortho_folders_count': len(self.ortho_folders),
            'preserve_highways': self.preserve_highways,
            'preserve_bridges': self.preserve_bridges,
            'preserve_railroads': self.preserve_railroads,
            'library_exists': os.path.exists(os.path.join(self.xroads_path, "library.txt"))
        }

# Global XRoads manager instance
_xroads_manager: Optional[XRoadsManager] = None

def get_xroads_manager() -> XRoadsManager:
    """Get or create global XRoads manager"""
    global _xroads_manager
    
    if _xroads_manager is None:
        _xroads_manager = XRoadsManager()
        
    return _xroads_manager

def enable_transparent_roads(lhd_mode: bool = False) -> bool:
    """Enable transparent roads with optional LHD mode for UK/Ireland"""
    manager = get_xroads_manager()
    manager.lhd_mode = lhd_mode
    return manager.enable_transparent_roads()

def disable_transparent_roads() -> bool:
    """Disable transparent roads"""
    manager = get_xroads_manager()
    return manager.disable_transparent_roads()

def configure_xroads(xplane_path: str = "", lhd_mode: bool = False, 
                    preserve_highways: bool = True, preserve_bridges: bool = True) -> bool:
    """Configure XRoads settings"""
    manager = get_xroads_manager()
    
    if xplane_path:
        manager.xplane_path = xplane_path
        manager.custom_scenery_path = os.path.join(xplane_path, "Custom Scenery")
        manager.xroads_path = os.path.join(manager.custom_scenery_path, "Xroads")
    
    manager.lhd_mode = lhd_mode
    manager.preserve_highways = preserve_highways
    manager.preserve_bridges = preserve_bridges
    
    return True

def get_xroads_status() -> Dict[str, any]:
    """Get XRoads status"""
    manager = get_xroads_manager()
    return manager.get_status()

# Test function
if __name__ == "__main__":
    print("🛣️ Testing XRoads Integration...")
    
    manager = XRoadsManager()
    
    # Test X-Plane detection
    xplane_path = manager.detect_xplane_installation()
    if xplane_path:
        print(f"✅ X-Plane found: {xplane_path}")
        
        # Test Ortho4XP tile scanning
        tiles = manager.scan_ortho_tiles()
        print(f"✅ Found {len(tiles)} Ortho4XP tiles")
        
        # Test library generation
        if tiles:
            manager.lhd_mode = True  # Test LHD for UK/Ireland
            success = manager.generate_xroads_library()
            print(f"✅ Library generation: {'Success' if success else 'Failed'}")
            
        status = manager.get_status()
        print(f"📊 Status: {status}")
        
    else:
        print("❌ X-Plane installation not found")
