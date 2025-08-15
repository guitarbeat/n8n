#!/usr/bin/env python3
"""
n8n Workflow Validator

This script validates n8n workflow JSON files to ensure they conform to the expected structure.
It checks for required fields, data types, and validates the overall workflow integrity.

Usage:
    python validate_n8n_workflows.py [workflow_directory]
    
Default workflow directory is './workflow'
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import jsonschema
from jsonschema import ValidationError
import argparse


class N8nWorkflowValidator:
    """Validator for n8n workflow JSON files."""
    
    def __init__(self):
        # Define the n8n workflow schema based on the official structure
        self.schema = {
            "type": "object",
            "required": ["id", "name", "nodes", "connections"],
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "active": {"type": "boolean"},
                "isArchived": {"type": "boolean"},
                "createdAt": {"type": "string", "format": "date-time"},
                "updatedAt": {"type": "string", "format": "date-time"},
                "nodes": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["id", "name", "type", "position"],
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "typeVersion": {"type": "number"},
                            "position": {
                                "type": "array",
                                "minItems": 2,
                                "maxItems": 2,
                                "items": {"type": "number"}
                            },
                            "parameters": {"type": "object"},
                            "credentials": {"type": "object"},
                            "webhookId": {"type": "string", "format": "uuid"}
                        }
                    }
                },
                "connections": {
                    "type": "object",
                    "patternProperties": {
                        "^.*$": {
                            "type": "object",
                            "patternProperties": {
                                "^.*$": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "required": ["node", "type", "index"],
                                            "properties": {
                                                "node": {"type": "string"},
                                                "type": {"type": "string"},
                                                "index": {"type": "number"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "settings": {"type": "object"},
                "staticData": {"type": ["object", "null"]},
                "meta": {"type": "object"},
                "pinData": {"type": "object"},
                "versionId": {"type": "string", "format": "uuid"},
                "triggerCount": {"type": "number"},
                "tags": {"type": "array", "items": {"type": "string"}}
            }
        }
        
        # Additional validation rules
        self.node_types = [
            "n8n-nodes-base.gmailTrigger",
            "n8n-nodes-base.if",
            "n8n-nodes-base.stickyNote",
            "@n8n/n8n-nodes-langchain.chatTrigger",
            "@n8n/n8n-nodes-langchain.agent",
            "@n8n/n8n-nodes-langchain.lmChatOpenRouter",
            "@n8n/n8n-nodes-langchain.outputParserStructured"
        ]
    
    def validate_workflow_file(self, file_path: Path) -> List[str]:
        """Validate a single n8n workflow file."""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {e}")
            return errors
        except Exception as e:
            errors.append(f"Error reading file: {e}")
            return errors
        
        # Basic schema validation
        try:
            jsonschema.validate(instance=workflow_data, schema=self.schema)
        except ValidationError as e:
            # Provide more specific error messages
            if "None is not of type 'object'" in str(e.message):
                errors.append(f"Schema validation error: Missing or null required field at path '{e.path}'")
            else:
                errors.append(f"Schema validation error: {e.message}")
        
        # Additional custom validations
        errors.extend(self._validate_workflow_integrity(workflow_data))
        
        return errors
    
    def _validate_workflow_integrity(self, workflow_data: Dict[str, Any]) -> List[str]:
        """Perform additional workflow integrity checks."""
        errors = []
        
        # Check if all nodes referenced in connections exist
        node_names = {node["name"] for node in workflow_data.get("nodes", [])}
        connections = workflow_data.get("connections", {})
        
        for source_node, connections_dict in connections.items():
            if source_node not in node_names:
                errors.append(f"Connection references non-existent node: {source_node}")
            
            for connection_type, connection_list in connections_dict.items():
                if connection_list is None:
                    continue
                for connection_group in connection_list:
                    if connection_group is None:
                        continue
                    for connection in connection_group:
                        if connection is None:
                            continue
                        target_node = connection.get("node")
                        if target_node and target_node not in node_names:
                            errors.append(f"Connection references non-existent target node: {target_node}")
        
        # Check for duplicate node IDs
        node_ids = [node["id"] for node in workflow_data.get("nodes", [])]
        if len(node_ids) != len(set(node_ids)):
            errors.append("Duplicate node IDs found")
        
        # Check for duplicate node names
        node_names_list = [node["name"] for node in workflow_data.get("nodes", [])]
        if len(node_names_list) != len(set(node_names_list)):
            errors.append("Duplicate node names found")
        
        # Validate node types
        for node in workflow_data.get("nodes", []):
            node_type = node.get("type")
            if node_type and node_type not in self.node_types:
                # Warning rather than error for unknown node types
                print(f"Warning: Unknown node type '{node_type}' in node '{node.get('name', 'Unknown')}'")
        
        return errors
    
    def validate_workflow_directory(self, directory: Path) -> Dict[str, List[str]]:
        """Validate all n8n workflow files in a directory."""
        results = {}
        
        if not directory.exists():
            results["error"] = [f"Directory {directory} does not exist"]
            return results
        
        json_files = list(directory.glob("*.json"))
        
        if not json_files:
            results["warning"] = ["No JSON files found in directory"]
            return results
        
        for json_file in json_files:
            print(f"Validating {json_file.name}...")
            errors = self.validate_workflow_file(json_file)
            if errors:
                results[json_file.name] = errors
            else:
                print(f"✓ {json_file.name} is valid")
        
        return results


def main():
    """Main function to run the validator."""
    parser = argparse.ArgumentParser(description="Validate n8n workflow JSON files")
    parser.add_argument(
        "workflow_dir", 
        nargs="?", 
        default="./workflow",
        help="Directory containing n8n workflow files (default: ./workflow)"
    )
    
    args = parser.parse_args()
    workflow_dir = Path(args.workflow_dir)
    
    validator = N8nWorkflowValidator()
    results = validator.validate_workflow_directory(workflow_dir)
    
    # Print results
    if "error" in results:
        print(f"\n❌ Error: {results['error'][0]}")
        sys.exit(1)
    
    if "warning" in results:
        print(f"\n⚠️  Warning: {results['warning'][0]}")
    
    if any(key != "warning" for key in results.keys()):
        print("\n❌ Validation errors found:")
        for filename, errors in results.items():
            if filename != "warning":
                print(f"\n{filename}:")
                for error in errors:
                    print(f"  - {error}")
        sys.exit(1)
    
    print("\n✅ All workflows are valid!")
    sys.exit(0)


if __name__ == "__main__":
    main()