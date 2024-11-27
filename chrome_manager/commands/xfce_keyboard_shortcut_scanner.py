#!/usr/bin/env python3

import subprocess
import os
import xml.etree.ElementTree as ET
import json
from datetime import datetime

class XFCEShortcutScanner:
    def __init__(self):
        self.shortcuts = {
            'window_manager': {},
            'commands': {},
            'xfconf': {}
        }
        self.config_paths = {
            'xfce4_keyboard': os.path.expanduser('~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml'),
            'window_manager': os.path.expanduser('~/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml')
        }

    def read_xml_config(self, file_path):
        try:
            if os.path.exists(file_path):
                tree = ET.parse(file_path)
                return tree.getroot()
            return None
        except ET.ParseError as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def scan_xfconf_shortcuts(self):
        """Scan shortcuts using xfconf-query"""
        try:
            cmd = ["xfconf-query", "-c", "xfce4-keyboard-shortcuts", "-l"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.strip():
                        try:
                            value_cmd = ["xfconf-query", "-c", "xfce4-keyboard-shortcuts", "-p", line]
                            value_result = subprocess.run(value_cmd, capture_output=True, text=True)
                            if value_result.returncode == 0:
                                self.shortcuts['xfconf'][line] = value_result.stdout.strip()
                        except subprocess.SubprocessError as e:
                            print(f"Error getting value for {line}: {e}")
        except subprocess.SubprocessError as e:
            print(f"Error running xfconf-query: {e}")

    def parse_keyboard_shortcuts(self):
        """Parse keyboard shortcuts from XML config"""
        root = self.read_xml_config(self.config_paths['xfce4_keyboard'])
        if root is not None:
            for property in root.findall('.//property'):
                if 'command' in property.attrib.get('name', ''):
                    shortcut = property.get('name', '').split('/')[-1]
                    command = property.get('value', '')
                    self.shortcuts['commands'][shortcut] = command

    def parse_window_manager_shortcuts(self):
        """Parse window manager shortcuts from XML config"""
        root = self.read_xml_config(self.config_paths['window_manager'])
        if root is not None:
            for property in root.findall('.//property'):
                name = property.get('name', '')
                if 'key' in name:
                    action = name.split('/')[-1]
                    shortcut = property.get('value', '')
                    self.shortcuts['window_manager'][action] = shortcut

    def get_active_window_manager(self):
        """Get the currently active window manager"""
        try:
            cmd = ["wmctrl", "-m"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "Name:" in line:
                        return line.split("Name:")[-1].strip()
        except subprocess.SubprocessError:
            pass
        return "Unknown"

    def scan_shortcuts(self):
        """Main method to scan all shortcuts"""
        self.parse_keyboard_shortcuts()
        self.parse_window_manager_shortcuts()
        self.scan_xfconf_shortcuts()
        
        # Add system information
        self.shortcuts['system_info'] = {
            'window_manager': self.get_active_window_manager(),
            'scan_date': datetime.now().isoformat(),
            'hostname': os.uname().nodename
        }

    def save_to_file(self, output_file='xfce_shortcuts.json'):
        """Save shortcuts to a JSON file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(self.shortcuts, f, indent=2)
            print(f"Shortcuts saved to {output_file}")
        except IOError as e:
            print(f"Error saving shortcuts to file: {e}")

    def print_shortcuts(self):
        """Print shortcuts to console"""
        print("\nXFCE Keyboard Shortcuts Summary:")
        print("\nWindow Manager Shortcuts:")
        for action, shortcut in self.shortcuts['window_manager'].items():
            print(f"{action}: {shortcut}")
        
        print("\nCommand Shortcuts:")
        for shortcut, command in self.shortcuts['commands'].items():
            print(f"{shortcut}: {command}")

def main():
    scanner = XFCEShortcutScanner()
    scanner.scan_shortcuts()
    scanner.save_to_file()
    scanner.print_shortcuts()

if __name__ == "__main__":
    main()