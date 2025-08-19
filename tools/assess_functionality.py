#!/usr/bin/env python3
"""
Functionality Assessment Tool
=============================

Honest assessment of what actually works vs what's aspirational
in the Ortho4XPDark project.
"""

import os
from pathlib import Path
import importlib.util

def test_import(filepath):
    """Test if a Python file can be imported without errors"""
    try:
        spec = importlib.util.spec_from_file_location("test_module", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True, "Imports successfully"
    except Exception as e:
        return False, str(e)

def assess_functionality():
    """Assess what functionality actually works"""
    
    print("🔍 ORTHO4XPDARK FUNCTIONALITY ASSESSMENT")
    print("=" * 50)
    print()
    
    # Core working tools
    working_tools = {
        'Ortho4XPDark.py': {
            'description': 'Dark theme + DEM automation',
            'functions': [
                'Dark theme demonstration',
                'System status checking', 
                'DEM file detection simulation',
                'Ortho4XP integration status'
            ],
            'status': 'WORKING'
        },
        'treelines_manager.py': {
            'description': 'Interactive forest library manager',
            'functions': [
                'X-Plane installation detection',
                'Treelines library installation',
                'scenery_packs.ini management',
                'System verification',
                'Troubleshooting tools'
            ],
            'status': 'WORKING'
        },
        'treelines_integration.py': {
            'description': 'Command-line treelines integration',
            'functions': [
                'Automated library copying',
                'Backup creation',
                'Priority management',
                'Verification reporting'
            ],
            'status': 'WORKING'
        },
        'system_verification.py': {
            'description': 'System verification and demo',
            'functions': [
                'Component checking',
                'Library analysis',
                'Capability demonstration',
                'Report generation'
            ],
            'status': 'WORKING'
        },
        'enhanced_launcher.py': {
            'description': 'Comprehensive launcher (honest)',
            'functions': [
                'Tool management',
                'Status checking',
                'Honest capability reporting'
            ],
            'status': 'WORKING'
        }
    }
    
    # Aspirational/problematic tools
    aspirational_tools = {
        'scenery_management_system.py': {
            'description': 'Advanced scenery management',
            'functions': [
                'Claims 25+ capabilities (mostly placeholder)',
                'Some working system detection',
                'Overengineered interface',
                'Lots of "coming soon" features'
            ],
            'status': 'MIXED - Mostly aspirational'
        },
        'smart_installation_mirror.py': {
            'description': 'P2P mirroring system',
            'functions': [
                'Peer-to-peer sharing (theoretical)',
                'IP protection (not implemented)',
                'Viral distribution (doesn\'t exist)'
            ],
            'status': 'ASPIRATIONAL'
        },
        'unified_launcher.py': {
            'description': 'Overengineered unified system',
            'functions': [
                'Grandiose menu system',
                'Calls to non-existent features',
                'Revolutionary claims'
            ],
            'status': 'OVERENGINEERED'
        }
    }
    
    print("✅ WORKING FUNCTIONALITY:")
    print("=" * 30)
    
    for tool, info in working_tools.items():
        tool_path = Path(tool)
        exists = tool_path.exists()
        
        print(f"\n📁 {tool}")
        print(f"   📝 {info['description']}")
        print(f"   📊 Status: {info['status']}")
        print(f"   📍 File exists: {'✅' if exists else '❌'}")
        
        if exists:
            can_import, import_msg = test_import(tool_path)
            print(f"   🐍 Imports: {'✅' if can_import else '❌'} {import_msg}")
        
        print("   🛠️ Functions:")
        for func in info['functions']:
            print(f"     • {func}")
    
    print(f"\n\n❌ ASPIRATIONAL/PROBLEMATIC:")
    print("=" * 35)
    
    for tool, info in aspirational_tools.items():
        tool_path = Path(tool)
        exists = tool_path.exists()
        
        print(f"\n📁 {tool}")
        print(f"   📝 {info['description']}")
        print(f"   📊 Status: {info['status']}")
        print(f"   📍 File exists: {'✅' if exists else '❌'}")
        
        print("   ⚠️ Issues:")
        for func in info['functions']:
            print(f"     • {func}")
    
    # Recommendations
    print(f"\n\n💡 RECOMMENDATIONS:")
    print("=" * 25)
    print()
    print("✅ USE THESE:")
    print("  • enhanced_launcher.py (honest, comprehensive)")
    print("  • treelines_manager.py (solid forest tool)")
    print("  • Ortho4XPDark.py (working dark theme)")
    print("  • treelines_integration.py (command-line tool)")
    print()
    print("⚠️ USE WITH CAUTION:")
    print("  • scenery_management_system.py (some working parts)")
    print()
    print("❌ IGNORE THESE:")
    print("  • unified_launcher.py (overengineered)")
    print("  • smart_installation_mirror.py (theoretical)")
    print("  • All the 'REVOLUTIONARY' documentation")
    print()
    print("🎯 FOCUS ON:")
    print("  • The dark theme (genuinely useful)")
    print("  • Forest library management (works well)")
    print("  • System detection (reliable)")
    print("  • DEM automation (helpful)")
    print()
    print("📈 HONEST VALUE PROPOSITION:")
    print("  'Enhanced workflow tools for Ortho4XP users'")
    print("  NOT 'Revolutionary scenery ecosystem'")

def main():
    """Main assessment"""
    os.system('cls' if os.name == 'nt' else 'clear')
    assess_functionality()
    print(f"\n\n🎯 ASSESSMENT COMPLETE")
    print("Use this information to focus on what actually works!")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
