# n8n Workflow Validation System

This system ensures that all your n8n workflow JSON files are structurally valid and follow the expected data structure before they can be committed or pushed to your repository.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
make install
# or
pip install -r requirements.txt
```

### 2. Validate All Workflows
```bash
make validate
# or
python validate_n8n_workflows.py workflow/
```

### 3. Setup Pre-commit Hooks (Recommended)
```bash
make setup
```

## 📋 What Gets Validated

The validation system checks:

### Required Fields
- `id` - Unique workflow identifier
- `name` - Workflow name
- `nodes` - Array of workflow nodes (minimum 1)
- `connections` - Node connection definitions

### Node Structure
- Each node must have: `id`, `name`, `type`, `position`
- Node IDs must be unique UUIDs
- Node names must be unique within the workflow
- Position must be a 2-element array of numbers

### Connection Integrity
- All referenced nodes must exist
- Connection structure must be valid
- No orphaned connections

### Data Types
- Proper JSON schema validation
- Correct data types for all fields
- Valid date-time formats for timestamps

## 🛠️ Usage Options

### Command Line Interface
```bash
# Validate all workflows in default directory (./workflow)
python validate_n8n_workflows.py

# Validate workflows in specific directory
python validate_n8n_workflows.py /path/to/workflows

# Validate single file
python validate_n8n_workflows.py workflow/my-workflow.json
```

### Makefile Commands
```bash
make help           # Show all available commands
make validate       # Validate all workflows
make test FILE=workflow/filename.json  # Test specific file
make clean         # Clean Python cache files
make setup         # Install pre-commit hooks
```

## 🔧 Pre-commit Hooks

The pre-commit hooks automatically validate your n8n workflows before each commit:

1. **Automatic Validation**: Runs on every commit
2. **File Filtering**: Only validates JSON files in the `workflow/` directory
3. **Prevents Invalid Commits**: Blocks commits with validation errors
4. **JSON Syntax Check**: Also validates basic JSON syntax

### Installation
```bash
make setup
```

### Manual Pre-commit Run
```bash
pre-commit run --all-files
```

## 🚀 GitHub Actions CI/CD

The system includes a GitHub Actions workflow that automatically validates workflows on:

- **Push** to main/master/develop branches
- **Pull Requests** to main/master/develop branches
- **Path Changes** in workflow files or validation scripts

### CI Workflow Features
- Runs on Ubuntu latest
- Python 3.9+ environment
- Automatic dependency installation
- Clear error reporting
- Prevents merging invalid workflows

## 📁 File Structure

```
.
├── validate_n8n_workflows.py    # Main validation script
├── requirements.txt              # Python dependencies
├── .pre-commit-config.yaml      # Pre-commit hook configuration
├── .github/workflows/           # GitHub Actions workflows
│   └── validate-n8n-workflows.yml
├── Makefile                     # Convenience commands
├── workflow/                    # Your n8n workflow files
│   ├── *.json
│   └── ...
└── README-VALIDATION.md         # This file
```

## 🔍 Validation Examples

### Valid Workflow Structure
```json
{
  "id": "A1n1MGwsnXA3N62i",
  "name": "My Workflow",
  "active": false,
  "nodes": [
    {
      "id": "57ccb060-2d83-419c-baec-fc4c4625e1ac",
      "name": "Trigger Node",
      "type": "n8n-nodes-base.trigger",
      "position": [0, 0]
    }
  ],
  "connections": {
    "Trigger Node": {
      "main": [[{"node": "Next Node", "type": "main", "index": 0}]]
    }
  }
}
```

### Common Validation Errors
- **Missing required fields**: Missing `id`, `name`, `nodes`, or `connections`
- **Invalid node structure**: Node without required properties
- **Connection errors**: References to non-existent nodes
- **Duplicate IDs**: Multiple nodes with the same ID
- **Invalid JSON**: Malformed JSON syntax

## 🐛 Troubleshooting

### Common Issues

1. **Import Error for jsonschema**
   ```bash
   pip install jsonschema
   ```

2. **Pre-commit Hook Not Working**
   ```bash
   pre-commit install
   pre-commit run --all-files
   ```

3. **Validation Fails on Valid Workflows**
   - Check if the workflow follows the n8n structure
   - Ensure all required fields are present
   - Verify node connections reference existing nodes

### Debug Mode
For detailed validation output, you can modify the script to add verbose logging or run with additional debugging information.

## 📚 n8n Data Structure Reference

This validation system is based on the official n8n data structure documentation:
- [n8n Data Structure Documentation](https://docs.n8n.io/data/data-structure/)
- [Workflow Format Specification](https://docs.n8n.io/workflows/workflows/)

## 🤝 Contributing

To extend the validation system:

1. **Add New Validation Rules**: Modify the `_validate_workflow_integrity` method
2. **Extend Schema**: Update the `schema` property in the `N8nWorkflowValidator` class
3. **Add Node Types**: Update the `node_types` list for additional node validation

## 📄 License

This validation system is provided as-is for ensuring n8n workflow integrity. Feel free to modify and adapt to your specific needs.