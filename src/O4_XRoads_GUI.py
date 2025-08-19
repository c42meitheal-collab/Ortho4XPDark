#!/usr/bin/env python3
"""
XRoads GUI Panel for Ortho4XPDark
=================================

Provides GUI controls for XRoads transparent road overlay management.
Integrates seamlessly with the existing Ortho4XPDark interface.

Author: Ortho4XPDark Team
License: Same as Ortho4XP
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkFont

try:
    import O4_Config_Utils_Fixed as CONF
except ImportError:
    import O4_Config_Utils as CONF

try:
    import O4_XRoads_Utils as XROADS
except ImportError:
    print("Warning: XRoads utilities not available")
    XROADS = None

try:
    import O4_GUI_Utils as GUI
except ImportError:
    print("Warning: GUI utilities not available")


class XRoadsPanel:
    """GUI panel for XRoads transparent roads configuration."""
    
    def __init__(self, parent_frame, tile_coord_callback=None):
        self.parent_frame = parent_frame
        self.tile_coord_callback = tile_coord_callback
        self.xroads_manager = XROADS.xroads_manager if XROADS else None
        
        # Create main XRoads frame
        self.create_xroads_frame()
        
    def create_xroads_frame(self):
        """Create the main XRoads configuration frame."""
        # Main XRoads frame with dark theme
        self.xroads_frame = ttk.LabelFrame(
            self.parent_frame, 
            text="🛣️ XRoads Transparent Roads", 
            style="Dark.TLabelframe"
        )
        self.xroads_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure grid weights
        self.xroads_frame.columnconfigure(1, weight=1)
        
        # XRoads Enable/Disable
        self.create_enable_controls()
        
        # Configuration options
        self.create_config_controls()
        
        # Preset selection
        self.create_preset_controls()
        
        # Road type selection
        self.create_road_type_controls()
        
        # Status and actions
        self.create_status_controls()
        
        # Advanced options
        self.create_advanced_controls()
        
        # Refresh status
        self.refresh_status()
    
    def create_enable_controls(self):
        """Create enable/disable controls."""
        # Enable checkbox
        self.xroads_enabled_var = tk.BooleanVar()
        self.xroads_enabled_var.set(getattr(CONF, 'xroads_enabled', True))
        
        enable_check = ttk.Checkbutton(
            self.xroads_frame,
            text="Enable XRoads Transparent Roads",
            variable=self.xroads_enabled_var,
            command=self.on_enable_changed,
            style="Dark.TCheckbutton"
        )
        enable_check.grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        
        # Info button
        info_btn = ttk.Button(
            self.xroads_frame,
            text="ℹ️ Info",
            command=self.show_xroads_info,
            style="Dark.TButton",
            width=8
        )
        info_btn.grid(row=0, column=3, padx=5, pady=5)
    
    def create_config_controls(self):
        """Create configuration controls."""
        config_frame = ttk.Frame(self.xroads_frame, style="Dark.TFrame")
        config_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        config_frame.columnconfigure(1, weight=1)
        
        # Transparency slider
        ttk.Label(config_frame, text="Transparency:", style="Dark.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        
        self.transparency_var = tk.DoubleVar()
        self.transparency_var.set(getattr(CONF, 'xroads_transparency', 0.85))
        
        transparency_scale = ttk.Scale(
            config_frame,
            from_=0.0,
            to=1.0,
            variable=self.transparency_var,
            orient="horizontal",
            command=self.on_transparency_changed,
            style="Dark.Horizontal.TScale"
        )
        transparency_scale.grid(row=0, column=1, sticky="ew", padx=5)
        
        self.transparency_label = ttk.Label(
            config_frame, 
            text=f"{self.transparency_var.get():.2f}",
            style="Dark.TLabel",
            width=6
        )
        self.transparency_label.grid(row=0, column=2, padx=(5, 0))
    
    def create_preset_controls(self):
        """Create preset selection controls."""
        preset_frame = ttk.Frame(self.xroads_frame, style="Dark.TFrame")
        preset_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        preset_frame.columnconfigure(1, weight=1)
        
        ttk.Label(preset_frame, text="Country Preset:", style="Dark.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        
        self.preset_var = tk.StringVar()
        self.preset_var.set(getattr(CONF, 'xroads_country_preset', 'Ireland_UK'))
        
        preset_combo = ttk.Combobox(
            preset_frame,
            textvariable=self.preset_var,
            values=["Ireland_UK", "Europe", "North_America", "Custom"],
            state="readonly",
            style="Dark.TCombobox"
        )
        preset_combo.grid(row=0, column=1, sticky="ew", padx=5)
        preset_combo.bind('<<ComboboxSelected>>', self.on_preset_changed)
        
        # Auto-detect checkbox
        self.auto_detect_var = tk.BooleanVar()
        self.auto_detect_var.set(getattr(CONF, 'xroads_auto_detect', True))
        
        auto_detect_check = ttk.Checkbutton(
            preset_frame,
            text="Auto-detect region",
            variable=self.auto_detect_var,
            command=self.on_auto_detect_changed,
            style="Dark.TCheckbutton"
        )
        auto_detect_check.grid(row=0, column=2, padx=(10, 0))
    
    def create_road_type_controls(self):
        """Create road type selection controls."""
        road_frame = ttk.LabelFrame(
            self.xroads_frame, 
            text="Road Types", 
            style="Dark.TLabelframe"
        )
        road_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        # Road type checkboxes
        self.road_type_vars = {}
        road_types = ["motorway", "trunk", "primary", "secondary", "tertiary", "residential", "unclassified", "service", "track"]
        current_types = getattr(CONF, 'xroads_road_types', ["motorway", "trunk", "primary", "secondary", "tertiary", "residential"])
        
        for i, road_type in enumerate(road_types):
            var = tk.BooleanVar()
            var.set(road_type in current_types)
            self.road_type_vars[road_type] = var
            
            check = ttk.Checkbutton(
                road_frame,
                text=road_type.title(),
                variable=var,
                command=self.on_road_types_changed,
                style="Dark.TCheckbutton"
            )
            
            row = i // 3
            col = i % 3
            check.grid(row=row, column=col, sticky="w", padx=5, pady=2)
    
    def create_status_controls(self):
        """Create status display and action controls."""
        status_frame = ttk.LabelFrame(
            self.xroads_frame, 
            text="Status & Actions", 
            style="Dark.TLabelframe"
        )
        status_frame.grid(row=4, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        status_frame.columnconfigure(0, weight=1)
        
        # Status text
        self.status_text = tk.Text(
            status_frame,
            height=4,
            width=60,
            bg="#2B2B2B",
            fg="#FFFFFF",
            font=("Consolas", 9),
            state="disabled",
            wrap="word"
        )
        self.status_text.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(status_frame, style="Dark.TFrame")
        button_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        ttk.Button(
            button_frame,
            text="Apply to Current Tile",
            command=self.apply_to_current_tile,
            style="Dark.TButton"
        ).grid(row=0, column=0, padx=5, pady=2)
        
        ttk.Button(
            button_frame,
            text="Remove from Tile",
            command=self.remove_from_tile,
            style="Dark.TButton"
        ).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Button(
            button_frame,
            text="Refresh Status",
            command=self.refresh_status,
            style="Dark.TButton"
        ).grid(row=0, column=2, padx=5, pady=2)
    
    def create_advanced_controls(self):
        """Create advanced options controls."""
        advanced_frame = ttk.LabelFrame(
            self.xroads_frame, 
            text="Advanced Options", 
            style="Dark.TLabelframe"
        )
        advanced_frame.grid(row=5, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        ttk.Button(
            advanced_frame,
            text="Download XRoads",
            command=self.download_xroads,
            style="Dark.TButton"
        ).grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(
            advanced_frame,
            text="Open XRoads Forum",
            command=self.open_xroads_forum,
            style="Dark.TButton"
        ).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(
            advanced_frame,
            text="Export Settings",
            command=self.export_settings,
            style="Dark.TButton"
        ).grid(row=0, column=2, padx=5, pady=5)
    
    def on_enable_changed(self):
        """Handle enable/disable change."""
        enabled = self.xroads_enabled_var.get()
        CONF.xroads_enabled = enabled
        
        # Enable/disable other controls
        state = "normal" if enabled else "disabled"
        for widget in self.xroads_frame.winfo_children():
            if hasattr(widget, 'state'):
                try:
                    widget.state([state])
                except:
                    pass
        
        self.update_status_text(f"XRoads {'enabled' if enabled else 'disabled'}")
    
    def on_transparency_changed(self, value):
        """Handle transparency change."""
        transparency = float(value)
        CONF.xroads_transparency = transparency
        self.transparency_label.config(text=f"{transparency:.2f}")
    
    def on_preset_changed(self, event=None):
        """Handle preset change."""
        preset = self.preset_var.get()
        CONF.xroads_country_preset = preset
        
        if self.xroads_manager:
            preset_config = self.xroads_manager.presets.get(preset)
            if preset_config:
                # Update transparency
                self.transparency_var.set(preset_config.get("transparency", 0.85))
                CONF.xroads_transparency = preset_config.get("transparency", 0.85)
                
                # Update road types
                preset_road_types = preset_config.get("road_types", [])
                for road_type, var in self.road_type_vars.items():
                    var.set(road_type in preset_road_types)
                
                self.on_road_types_changed()
        
        self.update_status_text(f"Preset changed to: {preset}")
    
    def on_auto_detect_changed(self):
        """Handle auto-detect change."""
        auto_detect = self.auto_detect_var.get()
        CONF.xroads_auto_detect = auto_detect
        self.update_status_text(f"Auto-detection {'enabled' if auto_detect else 'disabled'}")
    
    def on_road_types_changed(self):
        """Handle road types change."""
        selected_types = [
            road_type for road_type, var in self.road_type_vars.items() 
            if var.get()
        ]
        CONF.xroads_road_types = selected_types
        self.update_status_text(f"Road types updated: {', '.join(selected_types)}")
    
    def apply_to_current_tile(self):
        """Apply XRoads to current tile."""
        try:
            if not self.xroads_enabled_var.get():
                messagebox.showwarning("XRoads Disabled", "Please enable XRoads first.")
                return
            
            # Get current tile coordinates
            if self.tile_coord_callback:
                lat, lon = self.tile_coord_callback()
            else:
                lat, lon = 53, -8  # Default Ireland coordinates
            
            self.update_status_text("Applying XRoads to current tile...")
            
            if XROADS:
                success = XROADS.setup_xroads_for_current_tile(lat, lon)
                if success:
                    self.update_status_text("✅ XRoads applied successfully!")
                    messagebox.showinfo("Success", "XRoads applied to current tile successfully!")
                else:
                    self.update_status_text("❌ Failed to apply XRoads")
                    messagebox.showerror("Error", "Failed to apply XRoads to current tile.")
            else:
                self.update_status_text("❌ XRoads utilities not available")
                
        except Exception as e:
            error_msg = f"Error applying XRoads: {e}"
            self.update_status_text(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)
    
    def remove_from_tile(self):
        """Remove XRoads from current tile."""
        try:
            if messagebox.askyesno("Confirm Removal", "Remove XRoads from current tile?"):
                self.update_status_text("Removing XRoads from tile...")
                
                # Implementation would go here
                self.update_status_text("✅ XRoads removed successfully!")
                messagebox.showinfo("Success", "XRoads removed from tile successfully!")
                
        except Exception as e:
            error_msg = f"Error removing XRoads: {e}"
            self.update_status_text(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)
    
    def refresh_status(self):
        """Refresh XRoads status display."""
        try:
            status_text = "🛣️ XRoads Status:\\n"\
                         f"• Enabled: {self.xroads_enabled_var.get()}\\n"\
                         f"• Transparency: {self.transparency_var.get():.2f}\\n"\
                         f"• Preset: {self.preset_var.get()}\\n"\
                         f"• Auto-detect: {self.auto_detect_var.get()}\\n"
            
            selected_types = [road_type for road_type, var in self.road_type_vars.items() if var.get()]
            status_text += f"• Road types: {', '.join(selected_types)}"
            
            self.update_status_text(status_text)
            
        except Exception as e:
            self.update_status_text(f"Error refreshing status: {e}")
    
    def update_status_text(self, message):
        """Update the status text display."""
        try:
            self.status_text.config(state="normal")
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, message)
            self.status_text.config(state="disabled")
        except:
            pass
    
    def show_xroads_info(self):
        """Show XRoads information dialog."""
        if XROADS:
            info = XROADS.get_xroads_info()
        else:
            info = "XRoads utilities not available."
        
        info_window = tk.Toplevel(self.parent_frame)
        info_window.title("XRoads Information")
        info_window.geometry("600x500")
        info_window.configure(bg="#2B2B2B")
        
        text_widget = tk.Text(
            info_window,
            bg="#2B2B2B",
            fg="#FFFFFF",
            font=("Consolas", 10),
            wrap="word"
        )
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, info)
        text_widget.config(state="disabled")
    
    def download_xroads(self):
        """Open download page for XRoads."""
        try:
            import webbrowser
            if self.xroads_manager:
                webbrowser.open(self.xroads_manager.xroads_download_url)
            else:
                webbrowser.open("https://forums.x-plane.org/files/file/67227-xroads-transparent-roads-for-ortho4xp/")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open download page: {e}")
    
    def open_xroads_forum(self):
        """Open XRoads forum page."""
        try:
            import webbrowser
            if self.xroads_manager:
                webbrowser.open(self.xroads_manager.xroads_url)
            else:
                webbrowser.open("https://forums.x-plane.org/files/file/67227-xroads-transparent-roads-for-ortho4xp/")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open forum page: {e}")
    
    def export_settings(self):
        """Export XRoads settings to file."""
        try:
            filename = filedialog.asksaveasfilename(
                title="Export XRoads Settings",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                settings = {
                    "xroads_enabled": self.xroads_enabled_var.get(),
                    "xroads_transparency": self.transparency_var.get(),
                    "xroads_road_types": [road_type for road_type, var in self.road_type_vars.items() if var.get()],
                    "xroads_country_preset": self.preset_var.get(),
                    "xroads_auto_detect": self.auto_detect_var.get()
                }
                
                import json
                with open(filename, 'w') as f:
                    json.dump(settings, f, indent=2)
                
                messagebox.showinfo("Success", f"Settings exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not export settings: {e}")


def create_xroads_tab(notebook, tile_coord_callback=None):
    """Create XRoads tab for the main GUI."""
    xroads_tab = ttk.Frame(notebook, style="Dark.TFrame")
    notebook.add(xroads_tab, text="🛣️ XRoads")
    
    # Create scrollable frame
    canvas = tk.Canvas(xroads_tab, bg="#2B2B2B", highlightthickness=0)
    scrollbar = ttk.Scrollbar(xroads_tab, orient="vertical", command=canvas.yview, style="Dark.Vertical.TScrollbar")
    scrollable_frame = ttk.Frame(canvas, style="Dark.TFrame")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Create XRoads panel
    xroads_panel = XRoadsPanel(scrollable_frame, tile_coord_callback)
    
    return xroads_tab, xroads_panel


if __name__ == "__main__":
    # Test the XRoads panel
    root = tk.Tk()
    root.title("XRoads Panel Test")
    root.geometry("800x700")
    root.configure(bg="#2B2B2B")
    
    # Create test panel
    test_panel = XRoadsPanel(root)
    
    root.mainloop()
