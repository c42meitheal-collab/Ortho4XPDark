#!/usr/bin/env python3
"""
Ortho4XPDark Installation Helper
===============================

Assists with dependency installation and system setup.
Handles common installation issues and provides guidance.
"""

import sys
import subprocess
import os
import platform
from pathlib import Path

def print_header():
    print("🌑 Ortho4XPDark Installation Helper")
    print("=" * 40)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        print("   Please upgrade Python and try again")
        return False
    else:
        print("✅ Python version compatible")
        return True

def detect_system():
    """Detect system information."""
    system = platform.system()
    machine = platform.machine()
    print(f"💻 System: {system} {machine}")
    print(f"🏠 Platform: {platform.platform()}")
    return system

def check_pip():
    """Check if pip is available and working."""
    try:
        import pip
        pip_version = pip.__version__
        print(f"📦 pip version: {pip_version}")
        return True
    except ImportError:
        print("❌ pip not found")
        print("   Please install pip and try again")
        return False

def install_requirements(requirements_file):
    """Install requirements from specified file."""
    print(f"\n🔧 Installing dependencies from {requirements_file}...")
    print("   This may take 5-15 minutes...")
    print()
    
    try:
        cmd = [sys.executable, "-m", "pip", "install", "-r", requirements_file]
        
        # Add upgrade flag to ensure latest versions
        cmd.extend(["--upgrade", "--no-cache-dir"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print("❌ Installation failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def provide_troubleshooting():
    """Provide troubleshooting guidance."""
    print("\n🔧 Troubleshooting Guide:")
    print("=" * 25)
    print()
    
    system = platform.system()
    
    if system == "Windows":
        print("Windows-specific solutions:")
        print("• Install Microsoft Visual C++ Build Tools")
        print("• Try: pip install --only-binary=all -r requirements.txt")
        print("• For GDAL issues: Install OSGeo4W first")
        
    elif system == "Darwin":  # macOS
        print("macOS-specific solutions:")
        print("• Install Xcode command line tools: xcode-select --install")
        print("• Install Homebrew: brew install gdal")
        print("• Try: pip install --user -r requirements.txt")
        
    elif system == "Linux":
        print("Linux-specific solutions:")
        print("• Install build essentials: sudo apt install build-essential")
        print("• Install GDAL: sudo apt install gdal-bin libgdal-dev")
        print("• Install Python dev: sudo apt install python3-dev")
    
    print("\nGeneral solutions:")
    print("• Try minimal requirements: pip install -r requirements_minimal.txt")
    print("• Update pip: python -m pip install --upgrade pip")
    print("• Use virtual environment: python -m venv venv")
    print("• Check internet connection and retry")

def main():
    """Main installation workflow."""
    print_header()
    
    # System checks
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    system = detect_system()
    
    print("\n📋 Installation Options:")
    print("1. Full installation (all features) - requirements.txt")
    print("2. Minimal installation (core only) - requirements_minimal.txt")
    print("3. Show troubleshooting guide")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                if Path("requirements.txt").exists():
                    success = install_requirements("requirements.txt")
                    if success:
                        print("\n🎉 Full installation complete!")
                        print("Ready to run: python enhanced_launcher.py")
                    else:
                        print("\n⚠️ Full installation failed")
                        print("Try option 2 (minimal) or 3 (troubleshooting)")
                else:
                    print("❌ requirements.txt not found")
                break
                
            elif choice == "2":
                if Path("requirements_minimal.txt").exists():
                    success = install_requirements("requirements_minimal.txt")
                    if success:
                        print("\n🎉 Minimal installation complete!")
                        print("Ready to run: python Ortho4XPDark.py")
                        print("Note: Some advanced features may not be available")
                    else:
                        print("\n⚠️ Minimal installation failed")
                        print("See option 3 for troubleshooting")
                else:
                    print("❌ requirements_minimal.txt not found")
                break
                
            elif choice == "3":
                provide_troubleshooting()
                continue
                
            elif choice == "4":
                print("👋 Installation cancelled")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-4.")
                continue
                
        except KeyboardInterrupt:
            print("\n👋 Installation cancelled")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    
    print("\n📖 Next steps:")
    print("• Run: python enhanced_launcher.py")
    print("• Or: python test_xroads.py (test XRoads)")
    print("• Read: README.md for complete guide")

if __name__ == "__main__":
    main()
