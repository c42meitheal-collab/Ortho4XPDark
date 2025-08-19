#!/usr/bin/env python3
"""
X-Plane Treelines Library Integration Tool
=========================================

Integrates the zzz_Treelines_Farms_Europe_v3 library with X-Plane 12
and ensures proper loading priority for enhanced forest rendering.

Features:
- Auto-detects X-Plane installations
- Copies treelines library to Custom Scenery
- Updates scenery_packs.ini with proper priority
- Verifies library integrity
- Creates backup before changes
- Provides integration status and troubleshooting
"""

import os
import shutil
import sys
from pathlib import Path
import configparser
from datetime import datetime
import json

class XPlaneTreelinesIntegrator:
    """Main integration class for X-Plane treelines library"""
    
    def __init__(self):
        self.xplane_paths = []
        self.treelines_source = None
        self.integration_log = []
        self.backup_created = False
        
    def find_xplane_installations(self):
        """Find all X-Plane 12 installations"""
        print("🔍 Searching for X-Plane 12 installations...")
        
        # Common X-Plane installation paths
        common_paths = [
            "C:\\X-Plane 12",
            "C:\\Program Files\\X-Plane 12", 
            "C:\\Program Files (x86)\\X-Plane 12",
            "D:\\X-Plane 12",
            "E:\\X-Plane 12",
            # Steam paths
            "C:\\Program Files (x86)\\Steam\\steamapps\\common\\X-Plane 12",
            "C:\\Program Files\\Steam\\steamapps\\common\\X-Plane 12",
        ]
        
        found_installations = []
        
        for path_str in common_paths:
            path = Path(path_str)
            if self.is_valid_xplane_installation(path):
                found_installations.append(str(path))
                print(f"  ✅ Found: {path}")
        
        self.xplane_paths = found_installations
        
        if not found_installations:
            print("  ❌ No X-Plane 12 installations found in common locations")
            print("     Please provide your X-Plane 12 installation path manually")
            
            # Ask user for manual path input
            manual_path = self.get_manual_xplane_path()
            if manual_path:
                found_installations.append(manual_path)
                self.xplane_paths = found_installations
        
        return found_installations
    
    def get_manual_xplane_path(self):
        """Ask user to manually provide X-Plane installation path"""
        print("\n📝 Please enter your X-Plane 12 installation path:")
        print("Examples:")
        print("  C:\\X-Plane 12")
        print("  D:\\Games\\X-Plane 12")
        print("  C:\\Program Files\\X-Plane 12")
        print("\nOr press Enter to cancel...")
        
        while True:
            try:
                user_input = input("\nX-Plane 12 path: ").strip()
                
                # User cancelled
                if not user_input:
                    print("❌ User cancelled path input")
                    return None
                
                # Remove quotes if user included them
                user_input = user_input.strip('"\'')
                
                # Validate the path
                path = Path(user_input)
                if self.is_valid_xplane_installation(path):
                    print(f"  ✅ Valid X-Plane installation found: {path}")
                    return str(path)
                else:
                    print(f"  ❌ Invalid X-Plane installation: {path}")
                    print("     Make sure the path contains:")
                    print("     - X-Plane.exe (or X-Plane on Mac/Linux)")
                    print("     - Custom Scenery folder")
                    print("\n     Try again or press Enter to cancel...")
                    
            except KeyboardInterrupt:
                print("\n👋 User cancelled")
                return None
            except Exception as e:
                print(f"  ⚠️ Error: {e}")
                print("     Please try again or press Enter to cancel...")
    
    def is_valid_xplane_installation(self, path):
        """Check if path contains valid X-Plane installation"""
        if not path.exists():
            return False
            
        # Check for X-Plane executable
        exe_files = ['X-Plane.exe', 'X-Plane']
        has_exe = any((path / exe).exists() for exe in exe_files)
        
        # Check for Custom Scenery folder
        custom_scenery = path / "Custom Scenery"
        
        return has_exe and custom_scenery.exists()
    
    def find_treelines_library(self):
        """Find the treelines library in current directory structure"""
        print("🌲 Searching for treelines library...")
        
        # Look for treelines library in common locations
        search_paths = [
            Path(".") / "zzz_Treelines_Farms_Europe_v3",
            Path("..") / "zzz_Treelines_Farms_Europe_v3",
            Path("C:\\Users\\matt2\\Desktop\\Claude FileSystem\\zzz_Treelines_Farms_Europe_v3"),
        ]
        
        for path in search_paths:
            if self.is_valid_treelines_library(path):
                self.treelines_source = path
                print(f"  ✅ Found treelines library: {path}")
                return str(path)
        
        print("  ❌ Treelines library not found")
        print("     Expected: zzz_Treelines_Farms_Europe_v3 folder with 1200 forests subfolder")
        return None
    
    def is_valid_treelines_library(self, path):
        """Check if path contains valid treelines library"""
        if not path.exists():
            return False
            
        # Check for key components
        forests_1200 = path / "1200 forests"
        library_txt = forests_1200 / "library.txt"
        summer_folder = forests_1200 / "sum"
        
        return forests_1200.exists() and library_txt.exists() and summer_folder.exists()
    
    def copy_treelines_library(self, xplane_path):
        """Copy treelines library to X-Plane Custom Scenery"""
        if not self.treelines_source:
            print("  ❌ No treelines library source found")
            return False
            
        custom_scenery = Path(xplane_path) / "Custom Scenery"
        destination = custom_scenery / "zzz_Treelines_Farms_Europe_v3"
        
        print(f"📋 Copying treelines library to: {destination}")
        
        try:
            # Remove existing installation if present
            if destination.exists():
                print("  🗑️ Removing existing treelines installation...")
                shutil.rmtree(destination)
            
            # Copy the library
            print("  📂 Copying files... (this may take a few minutes)")
            shutil.copytree(self.treelines_source, destination)
            
            # Verify copy
            if self.is_valid_treelines_library(destination):
                print("  ✅ Library copied successfully")
                return True
            else:
                print("  ❌ Copy verification failed")
                return False
                
        except Exception as e:
            print(f"  ❌ Copy failed: {e}")
            return False
    
    def update_scenery_packs_ini(self, xplane_path):
        """Update scenery_packs.ini to include treelines library"""
        custom_scenery = Path(xplane_path) / "Custom Scenery"
        scenery_packs_path = custom_scenery / "scenery_packs.ini"
        
        print("📝 Updating scenery_packs.ini...")
        
        # Create backup first
        if scenery_packs_path.exists():
            backup_path = scenery_packs_path.with_suffix('.ini.backup')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = scenery_packs_path.parent / f"scenery_packs.ini.backup_{timestamp}"
            
            try:
                shutil.copy2(scenery_packs_path, backup_path)
                print(f"  💾 Backup created: {backup_path.name}")
                self.backup_created = True
            except Exception as e:
                print(f"  ⚠️ Backup failed: {e}")
        
        # Read existing entries
        existing_entries = []
        if scenery_packs_path.exists():
            try:
                with open(scenery_packs_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            existing_entries.append(line)
            except Exception as e:
                print(f"  ⚠️ Error reading existing scenery_packs.ini: {e}")
        
        # Prepare new entry for treelines library
        treelines_entry = "SCENERY_PACK Custom Scenery/zzz_Treelines_Farms_Europe_v3/"
        
        # Check if already present
        if treelines_entry in existing_entries:
            print("  ℹ️ Treelines library already in scenery_packs.ini")
            return True
        
        # Create new scenery_packs.ini with proper priority order
        try:
            with open(scenery_packs_path, 'w', encoding='utf-8') as f:
                # Header comments
                f.write("# X-Plane Scenery Packages\n")
                f.write("# Generated by X-Plane Treelines Integration Tool\n")
                f.write(f"# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("#\n")
                f.write("# Loading order (top to bottom):\n")
                f.write("# 1. Treelines Library (high priority for forest replacement)\n")
                f.write("# 2. Existing scenery packages\n")
                f.write("\n")
                
                # Add treelines library FIRST (highest priority)
                f.write(f"{treelines_entry}\n")
                
                # Add existing entries
                for entry in existing_entries:
                    f.write(f"{entry}\n")
            
            print("  ✅ scenery_packs.ini updated successfully")
            print("  🌲 Treelines library set to HIGH PRIORITY (loads first)")
            return True
            
        except Exception as e:
            print(f"  ❌ Failed to update scenery_packs.ini: {e}")
            return False
    
    def verify_integration(self, xplane_path):
        """Verify the integration was successful"""
        print("🔍 Verifying integration...")
        
        verification_results = {
            'library_present': False,
            'library_valid': False,
            'scenery_packs_updated': False,
            'priority_correct': False
        }
        
        # Check if library is present
        custom_scenery = Path(xplane_path) / "Custom Scenery"
        treelines_path = custom_scenery / "zzz_Treelines_Farms_Europe_v3"
        
        if treelines_path.exists():
            verification_results['library_present'] = True
            print("  ✅ Library directory present")
            
            # Check if library is valid
            if self.is_valid_treelines_library(treelines_path):
                verification_results['library_valid'] = True
                print("  ✅ Library structure valid")
            else:
                print("  ❌ Library structure invalid")
        else:
            print("  ❌ Library directory not found")
        
        # Check scenery_packs.ini
        scenery_packs_path = custom_scenery / "scenery_packs.ini"
        if scenery_packs_path.exists():
            try:
                with open(scenery_packs_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Find treelines entry
                treelines_line = None
                for i, line in enumerate(lines):
                    if 'zzz_Treelines_Farms_Europe_v3' in line:
                        treelines_line = i
                        verification_results['scenery_packs_updated'] = True
                        break
                
                if treelines_line is not None:
                    print("  ✅ Library found in scenery_packs.ini")
                    
                    # Check if it's near the top (high priority)
                    non_comment_lines = [i for i, line in enumerate(lines) 
                                       if line.strip() and not line.strip().startswith('#')]
                    
                    if non_comment_lines and treelines_line == non_comment_lines[0]:
                        verification_results['priority_correct'] = True
                        print("  ✅ Library has highest priority (correct)")
                    else:
                        print("  ⚠️ Library priority could be higher")
                else:
                    print("  ❌ Library not found in scenery_packs.ini")
                    
            except Exception as e:
                print(f"  ⚠️ Error checking scenery_packs.ini: {e}")
        else:
            print("  ❌ scenery_packs.ini not found")
        
        return verification_results
    
    def integrate_with_xplane(self, xplane_path=None):
        """Main integration process"""
        print("🌟 X-Plane Treelines Library Integration")
        print("="*50)
        
        # Find X-Plane installations if not specified
        if not xplane_path:
            installations = self.find_xplane_installations()
            if not installations:
                return False
            xplane_path = installations[0]  # Use first found installation
            
            if len(installations) > 1:
                print(f"\n🔢 Multiple X-Plane installations found:")
                for i, path in enumerate(installations):
                    print(f"  {i+1}. {path}")
                print(f"\nUsing: {xplane_path}")
                print("(You can specify a different path manually)")
        
        print(f"\n🎯 Target X-Plane installation: {xplane_path}")
        
        # Find treelines library
        if not self.find_treelines_library():
            print("\n❌ Cannot proceed without treelines library")
            return False
        
        print(f"\n🚀 Starting integration process...")
        
        # Copy library
        if not self.copy_treelines_library(xplane_path):
            print("\n❌ Library copy failed")
            return False
        
        # Update scenery_packs.ini
        if not self.update_scenery_packs_ini(xplane_path):
            print("\n❌ scenery_packs.ini update failed")
            return False
        
        # Verify integration
        verification_results = self.verify_integration(xplane_path)
        
        # Generate report
        if all(verification_results.values()):
            print("\n🎉 INTEGRATION COMPLETED SUCCESSFULLY!")
            print("\nNext steps:")
            print("1. Launch X-Plane 12")
            print("2. Fly over European forests")
            print("3. Enjoy enhanced seasonal forest rendering!")
            return True
        else:
            print("\n⚠️ Integration completed with issues")
            print("Run verification tool for detailed troubleshooting")
            return False

def main():
    """Main entry point"""
    integrator = XPlaneTreelinesIntegrator()
    
    # Check if user provided X-Plane path as argument
    xplane_path = None
    if len(sys.argv) > 1:
        xplane_path = sys.argv[1]
        if not integrator.is_valid_xplane_installation(Path(xplane_path)):
            print(f"❌ Invalid X-Plane path: {xplane_path}")
            sys.exit(1)
    
    try:
        success = integrator.integrate_with_xplane(xplane_path)
        if success:
            print("\n✅ Integration completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Integration failed or incomplete")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Integration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

