# GDAL Installation Guide for Ortho4XPDark

## Overview

GDAL (Geospatial Data Abstraction Library) is essential for advanced orthoscenery processing but notoriously difficult to install via pip. This guide provides reliable installation methods for each platform.

## ⚡ Quick Assessment

**Do you need GDAL immediately?**
- **Basic dark theme + XRoads**: No, use standard requirements.txt
- **DEM processing + advanced features**: Yes, follow this guide
- **Ireland/UK specialisation**: Recommended but not essential

## 🖥️ Platform-Specific Installation

### Windows (Recommended: OSGeo4W)

#### Method 1: OSGeo4W Installer (Most Reliable)
```batch
# Download OSGeo4W installer from https://trac.osgeo.org/osgeo4w/
# Install with Express Install option
# This installs GDAL + Python bindings automatically

# Then install Ortho4XPDark
pip install -r requirements.txt
```

#### Method 2: Conda (Alternative)
```batch
# Install Miniconda or Anaconda first
conda install -c conda-forge gdal
pip install -r requirements.txt
```

#### Method 3: Wheel (If available)
```batch
# Check for prebuilt wheels
pip install --find-links https://girder.github.io/large_image_wheels GDAL
pip install -r requirements.txt
```

### macOS (Recommended: Homebrew)

#### Method 1: Homebrew (Most Reliable)
```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install GDAL
brew install gdal

# Set environment variables
export GDAL_LIBRARY_PATH="$(brew --prefix)/lib/libgdal.dylib"
export GEOS_LIBRARY_PATH="$(brew --prefix)/lib/libgeos_c.dylib"

# Install Python bindings
pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I$(brew --prefix)/include" --global-option="-L$(brew --prefix)/lib"

# Then install Ortho4XPDark
pip install -r requirements.txt
```

#### Method 2: Conda (Alternative)
```bash
conda install -c conda-forge gdal
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)

#### Method 1: System Packages + pip (Most Reliable)
```bash
# Install system GDAL libraries
sudo apt update
sudo apt install gdal-bin libgdal-dev

# Set environment variables
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal

# Install Python bindings
pip install GDAL==$(gdal-config --version)

# Then install Ortho4XPDark  
pip install -r requirements.txt
```

#### Method 2: Conda (Alternative)
```bash
conda install -c conda-forge gdal
pip install -r requirements.txt
```

## 🔧 Verification

Test GDAL installation:
```python
# Test script
python -c "from osgeo import gdal; print(f'GDAL version: {gdal.__version__}')"
```

If successful, proceed with Ortho4XPDark:
```bash
python enhanced_launcher.py
python system_verification.py  # Should report GDAL as available
```

## 🚨 Troubleshooting

### Common Error: "Failed building wheel for GDAL"
**Cause**: Missing system GDAL development libraries

**Windows**: Use OSGeo4W installer instead of pip
**macOS**: Install via Homebrew first
**Linux**: Install `libgdal-dev` package first

### Common Error: "GDAL library not found"
**Cause**: GDAL installed but Python can't find it

**Solution**: Set environment variables:
```bash
# Linux/macOS
export GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
export GDAL_DATA=/usr/share/gdal

# Windows (OSGeo4W)
set GDAL_DATA=C:\OSGeo4W64\share\gdal
```

### Common Error: Version mismatch
**Cause**: System GDAL version doesn't match pip version

**Solution**: Install matching version:
```bash
# Check system version
gdal-config --version

# Install matching Python bindings
pip install GDAL==$(gdal-config --version)
```

## 📋 Without GDAL

**Ortho4XPDark works without GDAL** for basic functionality:
- Dark theme interface ✅
- XRoads transparent roads ✅  
- Basic scenery generation ✅
- Forest management ✅
- System verification ✅

**GDAL enables advanced features**:
- Advanced DEM processing
- Enhanced coordinate transformations
- Professional GIS operations
- Batch processing workflows

## 🎯 Installation Priority

### For Most Users:
1. Install Ortho4XPDark without GDAL first
2. Verify basic functionality works
3. Add GDAL later if needed for advanced features

### For Power Users:
1. Install GDAL first using platform-specific method
2. Verify GDAL installation  
3. Install Ortho4XPDark with full capabilities

## ⚠️ Important Notes

- **GDAL installation varies significantly by platform**
- **Pip installation of GDAL often fails** - use system packages when possible
- **Version matching is critical** - system GDAL must match Python bindings
- **Environment variables matter** - set GDAL_DATA and library paths
- **Conda environments help** - isolate GDAL installation from system

## 🔗 Resources

- **OSGeo4W**: https://trac.osgeo.org/osgeo4w/
- **GDAL Documentation**: https://gdal.org/
- **Homebrew GDAL**: https://formulae.brew.sh/formula/gdal
- **Ubuntu GDAL**: https://packages.ubuntu.com/search?keywords=gdal

---

**Bottom Line**: GDAL is powerful but complex. Start simple, add complexity as needed.
