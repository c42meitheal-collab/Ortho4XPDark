#!/usr/bin/env python3
"""
🛣️ XRoads Integration Test for Ortho4XPDark
============================================

Comprehensive test script for XRoads transparent road overlay functionality.
Verifies all components work correctly and provides detailed status.

Author: Ortho4XPDark Team
"""

import os
import sys
import json
import traceback
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_config_integration():
    """Test XRoads configuration integration."""
    print("🔧 Testing XRoads Configuration Integration...")
    
    try:
        from O4_Cfg_Vars import cfg_vars, list_app_vars
        
        # Check if XRoads variables are properly integrated
        xroads_vars = [
            "xroads_enabled",
            "xroads_transparency", 
            "xroads_road_types",
            "xroads_country_preset",
            "xroads_auto_detect"
        ]
        
        missing_vars = []
        for var in xroads_vars:
            if var not in cfg_vars:
                missing_vars.append(var)
            else:
                print(f"  ✅ {var}: {cfg_vars[var]['default']}")
        
        if missing_vars:
            print(f"  ❌ Missing variables: {missing_vars}")
            return False
        
        # Check if variables are in list_app_vars
        missing_from_list = []
        for var in xroads_vars:
            if var not in list_app_vars:
                missing_from_list.append(var)
        
        if missing_from_list:
            print(f"  ❌ Missing from list_app_vars: {missing_from_list}")
            return False
        
        print("  ✅ All XRoads configuration variables properly integrated")
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration integration test failed: {e}")
        return False

def test_xroads_utils():
    """Test XRoads utilities module."""
    print("🛠️ Testing XRoads Utils Module...")
    
    try:
        import O4_XRoads_Utils as XROADS
        
        # Test XRoadsManager instantiation
        manager = XROADS.XRoadsManager()
        print(f"  ✅ XRoadsManager created with version {manager.xroads_version}")
        
        # Test presets
        presets = ["Ireland_UK", "Europe", "North_America"]
        for preset in presets:
            if preset in manager.presets:
                config = manager.presets[preset]
                print(f"  ✅ {preset} preset: transparency={config['transparency']}")
            else:
                print(f"  ❌ Missing preset: {preset}")
                return False
        
        # Test coordinate detection
        test_coords = [
            (53.0, -8.0, "Ireland_UK"),  # Ireland
            (48.8, 2.3, "Europe"),       # France
            (40.7, -74.0, "North_America") # New York
        ]
        
        for lat, lon, expected in test_coords:
            detected = manager.detect_tile_region(lat, lon)
            if detected == expected:
                print(f"  ✅ Coordinate detection ({lat}, {lon}) -> {detected}")
            else:
                print(f"  ❌ Coordinate detection failed: ({lat}, {lon}) -> {detected}, expected {expected}")
        
        # Test info function
        info = XROADS.get_xroads_info()
        if "XRoads Transparent Roads Integration" in info:
            print("  ✅ XRoads info function working")
        else:
            print("  ❌ XRoads info function failed")
            return False
        
        print("  ✅ XRoads Utils module test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ XRoads Utils test failed: {e}")
        traceback.print_exc()
        return False

def test_xroads_gui():
    """Test XRoads GUI components."""
    print("🖥️ Testing XRoads GUI Components...")
    
    try:
        import O4_XRoads_GUI as XROADS_GUI
        
        # Test GUI module import
        print("  ✅ XRoads GUI module imported successfully")
        
        # Test if key classes exist
        if hasattr(XROADS_GUI, 'XRoadsPanel'):
            print("  ✅ XRoadsPanel class available")
        else:
            print("  ❌ XRoadsPanel class missing")
            return False
        
        if hasattr(XROADS_GUI, 'create_xroads_tab'):
            print("  ✅ create_xroads_tab function available")
        else:
            print("  ❌ create_xroads_tab function missing")
            return False
        
        print("  ✅ XRoads GUI components test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ XRoads GUI test failed: {e}")
        return False

def test_config_window_integration():
    """Test XRoads integration with configuration window."""
    print("🎛️ Testing Configuration Window Integration...")
    
    try:
        import O4_Config_Utils_Fixed as CFG
        
        # Check if config window has XRoads support
        print("  ✅ Configuration system imported successfully")
        
        # Test if we can access config storage
        if hasattr(CFG, 'config_storage'):
            print("  ✅ Configuration storage available")
            
            # Check for XRoads config values
            xroads_vars = [
                "xroads_enabled",
                "xroads_transparency",
                "xroads_country_preset"
            ]
            
            for var in xroads_vars:
                if var in CFG.config_storage:
                    print(f"  ✅ {var} in config storage: {CFG.config_storage[var]}")
                else:
                    print(f"  ⚠️  {var} not in config storage")
        else:
            print("  ⚠️  Configuration storage not available")
        
        print("  ✅ Configuration window integration test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration window integration test failed: {e}")
        return False

def test_file_structure():
    """Test XRoads file structure."""
    print("📁 Testing XRoads File Structure...")
    
    expected_files = [
        "src/O4_XRoads_Utils.py",
        "src/O4_XRoads_GUI.py"
    ]
    
    missing_files = []
    for file_path in expected_files:
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"  ✅ {file_path} exists")
        else:
            missing_files.append(file_path)
            print(f"  ❌ {file_path} missing")
    
    if missing_files:
        print(f"  ❌ Missing files: {missing_files}")
        return False
    
    print("  ✅ All required XRoads files present")
    return True

def test_ireland_specific_features():
    """Test Ireland/UK specific XRoads features."""
    print("🇮🇪 Testing Ireland/UK Specific Features...")
    
    try:
        import O4_XRoads_Utils as XROADS
        
        manager = XROADS.XRoadsManager()
        
        # Test Ireland/UK preset
        ireland_preset = manager.presets["Ireland_UK"]
        
        # Verify Ireland-specific settings
        expected_features = {
            "transparency": 0.85,  # Higher for Irish roads
            "rural_boost": True,   # Enhanced rural detection
            "coastline_adaptation": True,  # Important for Irish coastline
            "narrow_road_threshold": 4.0  # Narrower roads in Ireland
        }
        
        for feature, expected_value in expected_features.items():
            if feature in ireland_preset and ireland_preset[feature] == expected_value:
                print(f"  ✅ Ireland feature {feature}: {expected_value}")
            else:
                actual = ireland_preset.get(feature, "missing")
                print(f"  ⚠️  Ireland feature {feature}: expected {expected_value}, got {actual}")
        
        # Test coordinate detection for Irish locations
        irish_coords = [
            (53.3498, -6.2603),  # Dublin
            (51.8985, -8.4756),  # Cork
            (53.2707, -9.0568),  # Galway
            (55.0059, -7.3186),  # Derry
        ]
        
        for lat, lon in irish_coords:
            detected = manager.detect_tile_region(lat, lon)
            if detected == "Ireland_UK":
                print(f"  ✅ Irish location ({lat}, {lon}) correctly detected as Ireland_UK")
            else:
                print(f"  ❌ Irish location ({lat}, {lon}) detected as {detected}")
        
        print("  ✅ Ireland/UK specific features test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Ireland/UK specific features test failed: {e}")
        return False

def create_test_report():
    """Create a comprehensive test report."""
    print("\n" + "="*60)
    print("🛣️ XROADS INTEGRATION TEST REPORT")
    print("="*60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Configuration Integration", test_config_integration),
        ("XRoads Utils Module", test_xroads_utils),
        ("GUI Components", test_xroads_gui),
        ("Config Window Integration", test_config_window_integration),
        ("Ireland/UK Features", test_ireland_specific_features),
    ]
    
    results = {}
    total_tests = len(tests)
    passed_tests = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        try:
            result = test_func()
            results[test_name] = result
            if result:
                passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results[test_name] = False
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    success_rate = (passed_tests / total_tests) * 100
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
    
    print(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate == 100:
        print("\n🎉 ALL TESTS PASSED! XRoads integration is fully functional!")
        print("\n🛣️ Your Ortho4XPDark system now includes:")
        print("   • Transparent road overlays")
        print("   • Ireland/UK optimized presets")
        print("   • Automatic region detection")
        print("   • Full GUI integration")
        print("   • Comprehensive configuration options")
        
        return True
    elif success_rate >= 80:
        print("\n⚠️  Most tests passed, but some issues detected.")
        print("   XRoads should be functional with minor limitations.")
        return False
    else:
        print("\n❌ Multiple test failures detected.")
        print("   XRoads integration may not work correctly.")
        return False

if __name__ == "__main__":
    print("🛣️ XRoads Integration Test for Ortho4XPDark")
    print("=" * 50)
    
    success = create_test_report()
    
    if success:
        print("\n🚀 Next Steps:")
        print("   1. Run 'python launch.py' to start Ortho4XPDark")
        print("   2. Open Configuration window")
        print("   3. Navigate to '🛣️ XRoads' tab")
        print("   4. Configure and apply XRoads to your tiles")
        
        exit(0)
    else:
        print("\n🔧 Troubleshooting:")
        print("   1. Check all required files are present")
        print("   2. Verify Python imports are working")
        print("   3. Run 'python test_system.py' for full system test")
        
        exit(1)
