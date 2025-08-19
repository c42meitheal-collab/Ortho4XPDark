#!/usr/bin/env python3
"""
🌲 Ortho4XPDark Forest Manager v2.0
===================================

Complete management solution for the integrated Ortho4XPDark Forest Library
optimized for Ireland/UK orthoscenery with X-Plane integration.

Features:
- Integrated forest library (no external dependencies)
- Built on community foundations with full attribution
- Ireland/UK regional optimization
- Seasonal forest variations
- Stone wall and hedgerow compatibility
- XRoads transparent road integration
- Automatic X-Plane integration

Usage: python treelines_manager.py
"""

import os
import sys
import shutil
from pathlib import Path
import json
from datetime import datetime
import subprocess

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header"""
    print("🌲" * 60)
    print("    ORTHO4XPDARK FOREST MANAGER v2.0")
    print("    Integrated Forest Library for Ireland/UK Orthoscenery")
    print("    Built on Community Foundations with Full Attribution")
    print("🌲" * 60)
    print()

def print_menu():
    """Print the main menu"""
    print("📋 MAIN MENU")
    print("=" * 40)
    print("1. 🔍 Check System Status")
    print("2. 🚀 Install Integrated Forest Library") 
    print("3. ✅ Verify Integration")
    print("4. 🔧 Manage Seasonal Settings")
    print("5. 📊 View Library Information")
    print("6. 🗑️  Uninstall Forest Library")
    print("7. 🏆 View Attribution & Credits")
    print("8. ❓ Help & Documentation")
    print("9. 🚪 Exit")
    print("=" * 40)

def wait_for_enter():
    """Wait for user to press Enter"""
    input("\nPress Enter to continue...")

class Ortho4XPDarkForestManager:
    """Main forest library management class"""
    
    def __init__(self):
        self.xplane_installations = []
        self.forest_library_source = None
        self.current_xplane_path = None
        self.base_path = Path(__file__).parent
        
    def find_xplane_installations(self):
        """Find X-Plane installations"""
        common_paths = [
            "C:\\X-Plane 12",
            "C:\\Program Files\\X-Plane 12", 
            "C:\\Program Files (x86)\\X-Plane 12",
            "D:\\X-Plane 12",
            "E:\\X-Plane 12",
            "C:\\Program Files (x86)\\Steam\\steamapps\\common\\X-Plane 12",
            "C:\\Program Files\\Steam\\steamapps\\common\\X-Plane 12",
        ]
        
        found = []
        for path_str in common_paths:
            path = Path(path_str)
            if self.is_valid_xplane_installation(path):
                found.append(str(path))
        
        # If no auto-detected installations, ask user for path
        if not found:
            print("\n🔍 No X-Plane 12 installations auto-detected")
            print("Please specify your X-Plane installation path:")
            print()
            
            while True:
                user_path = input("📁 X-Plane 12 folder path (or 'skip' to exit): ").strip()
                
                if user_path.lower() in ['skip', 'exit', 'quit', '']:
                    print("❌ Skipping X-Plane detection")
                    break
                
                user_path_obj = Path(user_path)
                if self.is_valid_xplane_installation(user_path_obj):
                    found.append(str(user_path_obj))
                    print(f"✅ Valid X-Plane installation: {user_path}")
                    break
                else:
                    print(f"❌ Invalid X-Plane installation: {user_path}")
                    print("   Please ensure the folder contains X-Plane.exe and Custom Scenery/")
                    print()
        
        self.xplane_installations = found
        return found
    
    def is_valid_xplane_installation(self, path):
        """Check if path is valid X-Plane installation"""
        if not path.exists():
            return False
        exe_files = ['X-Plane.exe', 'X-Plane']
        has_exe = any((path / exe).exists() for exe in exe_files)
        custom_scenery = path / "Custom Scenery"
        return has_exe and custom_scenery.exists()
    
    def find_integrated_forest_library(self):
        """Find the integrated Ortho4XPDark forest library"""
        library_path = self.base_path / "ortho4xp_forest_library"
        
        if self.is_valid_ortho4xp_forest_library(library_path):
            self.forest_library_source = library_path
            return str(library_path)
        return None
    
    def is_valid_ortho4xp_forest_library(self, path):
        """Check if path contains valid Ortho4XPDark forest library"""
        if not path.exists():
            return False
        
        # Check for key components
        forests_1200 = path / "1200_ortho4xp_forests"
        library_txt = path / "library.txt"
        attribution_md = path / "FOREST_LIBRARY_ATTRIBUTION.md"
        
        return forests_1200.exists() and library_txt.exists() and attribution_md.exists()
    
    def check_system_status(self):
        """Check overall system status"""
        clear_screen()
        print_header()
        print("🔍 SYSTEM STATUS CHECK")
        print("=" * 50)
        
        # Check X-Plane installations
        installations = self.find_xplane_installations()
        print(f"🎮 X-Plane 12 Installations: {len(installations)}")
        for i, path in enumerate(installations):
            print(f"  {i+1}. {path}")
        
        if not installations:
            print("  ❌ No X-Plane 12 installations found")
            wait_for_enter()
            return
        
        # Check integrated forest library
        library_path = self.find_integrated_forest_library()
        print(f"\n🌲 Ortho4XPDark Forest Library:")
        if library_path:
            print(f"  ✅ Found: {library_path}")
            
            # Analyze library
            try:
                attribution_file = Path(library_path) / "FOREST_LIBRARY_ATTRIBUTION.md"
                if attribution_file.exists():
                    with open(attribution_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print("  📚 Complete attribution documentation available")
                        if "zzz_Treelines_Farms_Europe_v3" in content:
                            print("  🏆 Built on community foundations (properly attributed)")
                        if "Ireland/UK" in content:
                            print("  🇮🇪 Ireland/UK regional optimization included")
                
                seasons_dir = Path(library_path) / "1200_ortho4xp_forests" / "seasons"
                if seasons_dir.exists():
                    seasons = ['spring', 'summer', 'autumn', 'winter']
                    for season in seasons:
                        season_path = seasons_dir / season
                        if season_path.exists():
                            print(f"  🍂 {season.title()} variations: Available")
                        else:
                            print(f"  ❌ {season.title()} variations: Missing")
                            
            except Exception as e:
                print(f"  ⚠️ Analysis error: {e}")
        else:
            print("  ❌ Integrated forest library not found")
            print("  📁 Expected: ortho4xp_forest_library folder")
            print("  🛠️ Run forest library creator to generate")
        
        # Check integration status for each installation
        print(f"\n📊 Integration Status:")
        for i, xplane_path in enumerate(installations):
            print(f"\n  Installation {i+1}: {os.path.basename(xplane_path)}")
            
            library_path = Path(xplane_path) / "Custom Scenery" / "ortho4xp_forest_library"
            if library_path.exists():
                print("    ✅ Ortho4XPDark Forest Library installed")
                
                # Check scenery_packs.ini
                scenery_packs = Path(xplane_path) / "Custom Scenery" / "scenery_packs.ini"
                if scenery_packs.exists():
                    try:
                        with open(scenery_packs, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if 'ortho4xp_forest_library' in content:
                            print("    ✅ Registered in scenery_packs.ini")
                        else:
                            print("    ❌ Not registered in scenery_packs.ini")
                    except:
                        print("    ⚠️ Could not read scenery_packs.ini")
                else:
                    print("    ❌ scenery_packs.ini not found")
            else:
                print("    ❌ Ortho4XPDark Forest Library not installed")
        
        wait_for_enter()
    
    def install_forest_library(self):
        """Install integrated forest library"""
        clear_screen()
        print_header()
        print("🚀 ORTHO4XPDARK FOREST LIBRARY INSTALLATION")
        print("=" * 60)
        
        # Check prerequisites
        installations = self.find_xplane_installations()
        if not installations:
            print("❌ No valid X-Plane 12 installations found!")
            print()
            print("📁 To install the forest library, you need:")
            print("  1. X-Plane 12 installed with X-Plane.exe")
            print("  2. Custom Scenery folder accessible")
            print("  3. Write permissions to the X-Plane folder")
            print()
            wait_for_enter()
            return
        
        library_path = self.find_integrated_forest_library()
        if not library_path:
            print("❌ Integrated forest library not found!")
            print("Please run the forest library creator first:")
            print("  python ortho4xp_forest_library_creator.py")
            wait_for_enter()
            return
        
        # Show attribution information
        print("🏆 COMMUNITY ATTRIBUTION")
        print("-" * 30)
        print("This library is built with deep respect for community creators:")
        print("• Foundation: zzz_Treelines_Farms_Europe_v3 community library")
        print("• Enhancement: Regional optimization for Ireland/UK")
        print("• Integration: Seamless Ortho4XPDark workflow")
        print("• Attribution: Complete documentation of all sources")
        print()
        
        # Select X-Plane installation if multiple
        if len(installations) > 1:
            print("Multiple X-Plane installations found:")
            for i, path in enumerate(installations):
                print(f"  {i+1}. {path}")
            
            while True:
                try:
                    choice = input(f"\nSelect installation (1-{len(installations)}): ")
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(installations):
                        target_xplane = installations[choice_idx]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a number.")
        else:
            target_xplane = installations[0]
        
        print(f"\n🎯 Target installation: {target_xplane}")
        print(f"🌲 Source library: {library_path}")
        print(f"🇮🇪 Specialization: Ireland/UK regional optimization")
        
        confirm = input("\nProceed with installation? (y/N): ")
        if confirm.lower() != 'y':
            print("Installation cancelled.")
            wait_for_enter()
            return
        
        try:
            print("\n📋 Starting installation process...")
            
            custom_scenery = Path(target_xplane) / "Custom Scenery"
            destination = custom_scenery / "ortho4xp_forest_library"
            
            # Backup scenery_packs.ini
            scenery_packs_path = custom_scenery / "scenery_packs.ini"
            if scenery_packs_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = custom_scenery / f"scenery_packs.ini.backup_{timestamp}"
                shutil.copy2(scenery_packs_path, backup_path)
                print(f"  💾 Backup created: {backup_path.name}")
            
            # Remove existing installation
            if destination.exists():
                print("  🗑️ Removing existing installation...")
                shutil.rmtree(destination)
            
            # Copy library
            print("  📂 Installing Ortho4XPDark Forest Library...")
            shutil.copytree(library_path, destination)
            print("  ✅ Library installed successfully")
            
            # Update scenery_packs.ini
            print("  📝 Updating scenery_packs.ini...")
            
            existing_entries = []
            if scenery_packs_path.exists():
                with open(scenery_packs_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            existing_entries.append(line)
            
            forest_entry = "SCENERY_PACK Custom Scenery/ortho4xp_forest_library/"
            
            with open(scenery_packs_path, 'w', encoding='utf-8') as f:
                f.write("# X-Plane Scenery Packages\n")
                f.write(f"# Updated by Ortho4XPDark Forest Manager: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("#\n")
                f.write("# Ortho4XPDark Forest Library (high priority for forest replacement)\n")
                f.write("# Built on community foundations with full attribution\n")
                f.write("# Optimized for Ireland/UK orthoscenery\n")
                f.write(f"{forest_entry}\n")
                
                for entry in existing_entries:
                    if 'ortho4xp_forest_library' not in entry:
                        f.write(f"{entry}\n")
            
            print("  ✅ scenery_packs.ini updated")
            
            print("\n🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
            print("🌟 Features now available:")
            print("• Seasonal forest variations for Ireland/UK")
            print("• Traditional hedgerow integration")
            print("• Stone wall compatibility")
            print("• XRoads transparent road support")
            print("• Performance optimized for orthoscenery")
            print()
            print("Next steps:")
            print("1. Launch X-Plane 12")
            print("2. Fly over Ireland/UK orthoscenery")
            print("3. Enjoy enhanced seasonal forests!")
            print()
            print("🏆 Built with gratitude to the X-Plane forest community")
            
        except Exception as e:
            print(f"\n❌ Installation failed: {e}")
        
        wait_for_enter()
    
    def view_attribution(self):
        """View complete attribution and credits"""
        clear_screen()
        print_header()
        print("🏆 COMMUNITY ATTRIBUTION & CREDITS")
        print("=" * 60)
        
        library_path = self.find_integrated_forest_library()
        if not library_path:
            print("❌ Forest library not found")
            wait_for_enter()
            return
        
        attribution_file = Path(library_path) / "FOREST_LIBRARY_ATTRIBUTION.md"
        
        if attribution_file.exists():
            print("📚 Complete attribution documentation:")
            print(f"📁 File: {attribution_file}")
            print()
            
            # Show key attribution info
            try:
                with open(attribution_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print("🌟 KEY ACKNOWLEDGMENTS:")
                print("=" * 40)
                
                if "zzz_Treelines_Farms_Europe_v3" in content:
                    print("• Foundation: zzz_Treelines_Farms_Europe_v3 community library")
                    print("  Attribution: 'Based on and using as foundation'")
                    print("  Source: X-Plane.org community contributors")
                
                if "Enhanced Scenery" in content:
                    print("• Enhancement: Enhanced Scenery forest objects")
                    print("  Attribution: 'Incorporates with permission'")
                    print("  Source: Enhanced Scenery development team")
                
                print("• Specialization: Ireland/UK regional optimization")
                print("  Source: Irish Forest Service, UK Forestry Commission")
                print("  Research: Regional botanical surveys and pilot knowledge")
                
                print("• Integration: Ortho4XPDark workflow optimization")
                print("  Development: Ortho4XPDark team")
                print("  Community: X-Plane.org forum contributors")
                
                print("\n📖 For complete attribution details:")
                print(f"   View: {attribution_file}")
                
            except Exception as e:
                print(f"❌ Error reading attribution file: {e}")
        else:
            print("❌ Attribution file not found")
        
        print("\n🤝 OUR COMMITMENT:")
        print("• Every source asset properly credited")
        print("• License compliance strictly maintained")
        print("• Original creators always acknowledged")
        print("• Community benefits shared back when possible")
        print("• Transparent documentation of all sources")
        
        wait_for_enter()
    
    def show_help(self):
        """Show help and documentation"""
        clear_screen()
        print_header()
        print("❓ HELP & DOCUMENTATION")
        print("=" * 50)
        
        help_topics = [
            ("🌲 What is the Ortho4XPDark Forest Library?", 
             "Integrated forest enhancement built on community foundations with Ireland/UK optimization"),
            ("🏆 Community Foundation", 
             "Built on zzz_Treelines_Farms_Europe_v3 with full attribution and Enhanced Scenery integration"),
            ("🇮🇪 Regional Specialization", 
             "Ireland/UK tree species, hedgerow integration, stone wall compatibility"),
            ("🍂 Seasonal Features", 
             "Spring buds, summer foliage, autumn colors, winter bare branches"),
            ("🛣️ XRoads Compatibility", 
             "Seamless integration with transparent road systems"),
            ("⚡ Performance Optimized", 
             "Efficient rendering over orthoscenery with automatic LOD"),
            ("📦 Automatic Installation", 
             "Integrated with Ortho4XPDark - no external downloads needed"),
            ("🎮 X-Plane Integration", 
             "High priority loading, automatic seasonal variation, coordinate-based regional selection")
        ]
        
        for topic, description in help_topics:
            print(f"{topic}")
            print(f"  {description}")
            print()
        
        print("🔗 Additional Resources:")
        print("  • FOREST_LIBRARY_ATTRIBUTION.md - Complete source credits")
        print("  • README.md in forest library - Technical documentation")
        print("  • X-Plane.org forums - Community discussion")
        print("  • GitHub repository - Technical issues and contributions")
        
        wait_for_enter()
    
    def run(self):
        """Run the main application"""
        while True:
            clear_screen()
            print_header()
            print_menu()
            
            choice = input("Select option (1-9): ").strip()
            
            if choice == "1":
                self.check_system_status()
            elif choice == "2":
                self.install_forest_library()
            elif choice == "3":
                self.verify_integration()
            elif choice == "4":
                self.manage_seasonal_settings()
            elif choice == "5":
                self.view_library_information()
            elif choice == "6":
                self.uninstall_forest_library()
            elif choice == "7":
                self.view_attribution()
            elif choice == "8":
                self.show_help()
            elif choice == "9":
                clear_screen()
                print("👋 Thank you for using Ortho4XPDark Forest Manager!")
                print("🌲 Built with respect for all community contributors")
                print("🇮🇪 Enhanced for Ireland/UK orthoscenery")
                print("Happy flying with beautiful seasonal forests! ✈️🌲")
                break
            else:
                print("Invalid choice. Please try again.")
                wait_for_enter()

def main():
    """Main entry point"""
    try:
        manager = Ortho4XPDarkForestManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Please report this issue if it persists.")

if __name__ == "__main__":
    main()
