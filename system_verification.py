#!/usr/bin/env python3
"""
Ortho4XPDark System Check
========================

Simple system check for the dark theme mod and enhancements.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

def test_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"  ✅ {description}")
        return True
    else:
        print(f"  ❌ {description} - missing")
        return False

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Check what's working"""
    clear_screen()
    
    print("ORTHO4XPDARK SYSTEM CHECK")
    print("=" * 40)
    print("Checking what's installed and working...")
    print()
    
    # Check core files
    print("Core Files:")
    core_files = 0
    
    if test_file_exists("Ortho4XPDark.py", "Dark theme mod"):
        core_files += 1
    if test_file_exists("enhanced_launcher.py", "Main launcher"):
        core_files += 1
    if test_file_exists("treelines_manager.py", "Forest manager"):
        core_files += 1
    if test_file_exists("test_xroads.py", "XRoads testing"):
        core_files += 1
    
    # Check documentation
    print("\nDocumentation:")
    docs = 0
    
    if test_file_exists("README.md", "Main documentation"):
        docs += 1
    if test_file_exists("GDAL_INSTALLATION.md", "GDAL setup guide"):
        docs += 1
    
    # Check for Python dependencies
    print("\nPython Dependencies:")
    deps_ok = 0
    
    try:
        import tkinter
        print("  ✅ tkinter (for dark theme)")
        deps_ok += 1
    except ImportError:
        print("  ❌ tkinter - dark theme won't work")
    
    try:
        import shapely
        print("  ✅ shapely (for XRoads)")
        deps_ok += 1
    except ImportError:
        print("  ❌ shapely - XRoads won't work (run: pip install -r requirements.txt)")
    
    try:
        import requests
        print("  ✅ requests (for downloads)")
        deps_ok += 1
    except ImportError:
        print("  ❌ requests - some features won't work")
    
    # Check for treelines libraries
    print("\nTreelines Libraries:")
    libs = 0
    
    filesystem_base = Path("C:\\Users\\matt2\\Desktop\\Claude FileSystem")
    lib1_path = filesystem_base / "zzz_Treelines_Farms_Europe_v3"
    lib2_path = filesystem_base / "zzz_Treelines_Europe_v3_NoFarms"
    
    if lib1_path.exists():
        libs += 1
        print(f"  ✅ Main treelines library found")
    else:
        print(f"  ❌ Main treelines library not found at {lib1_path}")
    
    if lib2_path.exists():
        libs += 1
        print(f"  ✅ Alternative treelines library found") 
    else:
        print(f"  ❌ Alternative treelines library not found")
    
    # Summary
    print(f"\nSUMMARY")
    print("=" * 20)
    print(f"Core files: {core_files}/4")
    print(f"Documentation: {docs}/2") 
    print(f"Python dependencies: {deps_ok}/3")
    print(f"Treelines libraries: {libs}/2")
    
    total_score = core_files + docs + deps_ok + libs
    max_score = 11
    percentage = (total_score / max_score) * 100
    
    print(f"\nOverall: {total_score}/{max_score} ({percentage:.0f}%)")
    
    if percentage >= 80:
        print("✅ Most things working")
    elif percentage >= 60:
        print("⚠️  Some things need fixing")
    else:
        print("❌ Needs setup work")
    
    # What works and what doesn't
    print(f"\nWHAT SHOULD WORK:")
    if core_files >= 3:
        print("- Dark theme mod (if tkinter available)")
        print("- Main launcher and tools")
    
    if deps_ok >= 2:
        print("- Basic functionality")
    
    print(f"\nWHAT NEEDS FIXING:")
    if deps_ok < 3:
        print("- Run: pip install -r requirements.txt")
    
    if libs == 0:
        print("- No treelines libraries found (forest features won't work)")
    
    # Simple recommendations
    print(f"\nNEXT STEPS:")
    print("1. Try dark theme: python Ortho4XPDark.py")
    
    if deps_ok < 3:
        print("2. Install dependencies: pip install -r requirements.txt")
    
    if libs == 0:
        print("3. Get treelines libraries for forest features")
    
    # Save simple report
    report = {
        'timestamp': datetime.now().isoformat(),
        'core_files': core_files,
        'docs': docs, 
        'dependencies': deps_ok,
        'libraries': libs,
        'percentage': percentage
    }
    
    try:
        with open('system_check_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved: system_check_report.json")
    except Exception as e:
        print(f"Could not save report: {e}")
    
    print(f"\nThis is a hobbyist dark theme modification for Ortho4XP.")
    print("It works best with all dependencies installed.")

if __name__ == "__main__":
    try:
        main()
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        input("Press Enter to exit...")
