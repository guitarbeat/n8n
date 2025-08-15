#!/usr/bin/env python3
"""
n8n Workflow Fixer

This script automatically fixes common validation issues in n8n workflow JSON files.
It adds missing required fields and fixes common structural problems.

Usage:
    python fix_n8n_workflows.py [workflow_directory]
    
Default workflow directory is './workflow'
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
import argparse
import shutil
from datetime import datetime


class N8nWorkflowFixer:
    """Automatically fixes common n8n workflow validation issues."""
    
    def __init__(self):
        self.backup_dir = Path("workflow_backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self, file_path: Path) -> Path:
        """Create a backup of the original file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}.json"
        backup_path = self.backup_dir / backup_name
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def fix_workflow_file(self, file_path: Path) -> List[str]:
        """Fix a single n8n workflow file."""
        fixes = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
        except json.JSONDecodeError as e:
            fixes.append(f"Invalid JSON: {e}")
            return fixes
        
        # Create backup before making changes
        backup_path = self.create_backup(file_path)
        fixes.append(f"Backup created: {backup_path}")
        
        # Fix missing pinData field
        if 'pinData' not in workflow_data or workflow_data['pinData'] is None:
            workflow_data['pinData'] = {}
            fixes.append("Added missing pinData field")
        
        # Fix missing settings field
        if 'settings' not in workflow_data or workflow_data['settings'] is None:
            workflow_data['settings'] = {}
            fixes.append("Added missing settings field")
        
        # Fix missing meta field
        if 'meta' not in workflow_data or workflow_data['meta'] is None:
            workflow_data['meta'] = {}
            fixes.append("Added missing meta field")
        
        # Fix missing staticData field
        if 'staticData' not in workflow_data:
            workflow_data['staticData'] = None
            fixes.append("Added missing staticData field")
        
        # Fix missing tags field
        if 'tags' not in workflow_data:
            workflow_data['tags'] = []
            fixes.append("Added missing tags field")
        elif isinstance(workflow_data['tags'], list):
            # Fix tags that are objects instead of strings
            fixed_tags = []
            for tag in workflow_data['tags']:
                if isinstance(tag, dict) and 'name' in tag:
                    fixed_tags.append(tag['name'])
                elif isinstance(tag, str):
                    fixed_tags.append(tag)
                else:
                    # Skip invalid tags
                    continue
            if fixed_tags != workflow_data['tags']:
                workflow_data['tags'] = fixed_tags
                fixes.append("Fixed tags field - converted objects to strings")
        
        # Fix missing triggerCount field
        if 'triggerCount' not in workflow_data:
            workflow_data['triggerCount'] = 0
            fixes.append("Added missing triggerCount field")
        
        # Fix missing versionId field
        if 'versionId' not in workflow_data:
            workflow_data['versionId'] = f"fixed-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            fixes.append("Added missing versionId field")
        
        # Fix missing createdAt field
        if 'createdAt' not in workflow_data:
            workflow_data['createdAt'] = datetime.now().isoformat() + "Z"
            fixes.append("Added missing createdAt field")
        
        # Fix missing updatedAt field
        if 'updatedAt' not in workflow_data:
            workflow_data['updatedAt'] = datetime.now().isoformat() + "Z"
            fixes.append("Added missing updatedAt field")
        
        # Fix missing active field
        if 'active' not in workflow_data:
            workflow_data['active'] = False
            fixes.append("Added missing active field")
        
        # Fix missing isArchived field
        if 'isArchived' not in workflow_data:
            workflow_data['isArchived'] = False
            fixes.append("Added missing isArchived field")
        
        # Ensure nodes array exists and is valid
        if 'nodes' not in workflow_data or not isinstance(workflow_data['nodes'], list):
            workflow_data['nodes'] = []
            fixes.append("Fixed invalid nodes field")
        
        # Ensure connections object exists and is valid
        if 'connections' not in workflow_data or not isinstance(workflow_data['connections'], dict):
            workflow_data['connections'] = {}
            fixes.append("Fixed invalid connections field")
        
        # Fix null values in connections arrays
        connections = workflow_data.get('connections', {})
        for node_name, node_connections in connections.items():
            for connection_type, connection_list in node_connections.items():
                if isinstance(connection_list, list):
                    # Remove null values from connection arrays
                    original_length = len(connection_list)
                    connection_list[:] = [conn for conn in connection_list if conn is not None]
                    if len(connection_list) != original_length:
                        fixes.append(f"Removed null values from {node_name}.{connection_type} connections")
        
        # Write the fixed workflow back to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(workflow_data, f, indent=2, ensure_ascii=False)
            fixes.append("Workflow file updated successfully")
        except Exception as e:
            fixes.append(f"Error writing fixed file: {e}")
        
        return fixes
    
    def fix_workflow_directory(self, directory: Path) -> Dict[str, List[str]]:
        """Fix all n8n workflow files in a directory."""
        results = {}
        
        if not directory.exists():
            results["error"] = [f"Directory {directory} does not exist"]
            return results
        
        json_files = list(directory.glob("*.json"))
        
        if not json_files:
            results["warning"] = ["No JSON files found in directory"]
            return results
        
        for json_file in json_files:
            print(f"Fixing {json_file.name}...")
            fixes = self.fix_workflow_file(json_file)
            if fixes:
                results[json_file.name] = fixes
                print(f"✓ {json_file.name} fixed with {len(fixes)} changes")
            else:
                print(f"✓ {json_file.name} no fixes needed")
        
        return results


def main():
    """Main function to run the fixer."""
    parser = argparse.ArgumentParser(description="Fix common n8n workflow validation issues")
    parser.add_argument(
        "workflow_dir", 
        nargs="?", 
        default="./workflow",
        help="Directory containing n8n workflow files (default: ./workflow)"
    )
    
    args = parser.parse_args()
    workflow_dir = Path(args.workflow_dir)
    
    fixer = N8nWorkflowFixer()
    results = fixer.fix_workflow_directory(workflow_dir)
    
    # Print results
    if "error" in results:
        print(f"\n❌ Error: {results['error'][0]}")
        sys.exit(1)
    
    if "warning" in results:
        print(f"\n⚠️  Warning: {results['warning'][0]}")
    
    if any(key != "warning" for key in results.keys()):
        print("\n🔧 Fixes applied:")
        for filename, fixes in results.items():
            if filename != "warning":
                print(f"\n{filename}:")
                for fix in fixes:
                    print(f"  - {fix}")
    
    print(f"\n✅ Workflow fixing completed!")
    print(f"📁 Backups saved in: {fixer.backup_dir}")
    print("\n💡 Next steps:")
    print("1. Run validation: python validate_n8n_workflows.py workflow/")
    print("2. Review the fixes applied")
    print("3. Test your workflows in n8n")
    sys.exit(0)


if __name__ == "__main__":
    main()