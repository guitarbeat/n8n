# N8N Workflow Collection

This directory contains a collection of n8n workflows for various automation tasks.

## Naming Convention

Workflows are named using the following pattern:
- **Format**: `category-description-tools.json`
- **Examples**:
  - `ai-email-manager-gmail.json` - AI-powered Gmail email management
  - `document-qa-voyage-embeddings-mongodb.json` - Document Q&A system using Voyage embeddings and MongoDB
  - `financial-assistant-qdrant-mistral.json` - Financial documents assistant using Qdrant and Mistral AI

## Categories

### AI & Email Management
- `ai-email-manager-gmail.json` - Gmail AI email manager
- `ai-email-manager-utexas.json` - UT Austin email manager
- `ai-inbox-manager-gpt4-gmail-slack.json` - GPT-4 powered inbox manager with Slack integration
- `gmail-auto-classify-ai-labels.json` - Automatic Gmail classification with AI labels
- `gmail-ai-auto-responder.json` - AI-powered Gmail auto-responder

### Document Processing & Q&A
- `document-qa-voyage-embeddings-mongodb.json` - Document Q&A with Voyage embeddings
- `vision-rag-cohere-embeddings.json` - Vision RAG with Cohere embeddings
- `document-breakdown-mistral-qdrant.json` - Document breakdown using Mistral AI and Qdrant
- `financial-assistant-qdrant-mistral.json` - Financial documents assistant
- `tax-assistant-qdrant-mistral-openai.json` - Tax code assistant

### Personal Automation
- `ai-personal-assistant.json` - General AI personal assistant
- `personal-assistant-gemini-gmail-calendar.json` - Gemini-powered assistant with Gmail and Calendar
- `inbox-manager-gpt-calendar-supabase.json` - Inbox manager with GPT, Calendar, and Supabase
- `look-into-later.json` - Look into later workflow

### Financial & Business
- `expense-extraction-gmail-sheets.json` - Extract expenses from emails to Google Sheets
- `work-attendance-location-triggers.json` - Automated work attendance with location

### Development & Sync
- `github-sync.json` - GitHub synchronization
- `github-workflow-sync-version-control.json` - Bidirectional GitHub workflow sync

### Media & Entertainment
- `spotify-playlist.json` - Spotify playlist management

### Demo & Development
- `demo-first-ai-agent.json` - Demo of first AI agent in n8n
- `my-workflow.json` - Personal workflow template
- `placeholder.json` - Placeholder workflow file

## Usage

Each workflow file contains the complete n8n workflow configuration. Import them into your n8n instance to use them.

## Original Names

The original filenames were quite long and descriptive. They have been shortened to improve readability while maintaining clarity about the workflow's purpose and tools used.

## File Renaming Summary

The following files were renamed for better organization:

### Before → After
- `document-q&a-system-with-voyage-context-3-embeddings-and-mongodb-atlas.json` → `document-qa-voyage-embeddings-mongodb.json`
- `vision-rag-and-image-embeddings-using-cohere-command-a-and-embed-v4.json` → `vision-rag-cohere-embeddings.json`
- `breakdown-documents-into-study-notes-using-templating-mistralai-and-qdrant.json` → `document-breakdown-mistral-qdrant.json`
- `build-a-financial-documents-assistant-using-qdrant-and-mistral.ai.json` → `financial-assistant-qdrant-mistral.json`
- `build-a-tax-code-assistant-with-qdrant,-mistral.ai-and-openai.json` → `tax-assistant-qdrant-mistral-openai.json`
- `ai-email-manager-(gmail).json` → `ai-email-manager-gmail.json`
- `ai-email-manager-(utexas).json` → `ai-email-manager-utexas.json`
- `ai-powered-email-inbox-manager-with-gpt-4,-gmail,-and-slack-integration.json` → `ai-inbox-manager-gpt4-gmail-slack.json`
- `auto-classify-gmail-emails-with-ai-and-apply-labels-for-inbox-organization.json` → `gmail-auto-classify-ai-labels.json`
- `basic-automatic-gmail-email-labelling-with-openai-and-gmail-api.json` → `gmail-auto-labeling-openai.json`
- `gmail-ai-auto-responder:-create-draft-replies-to-incoming-emails.json` → `gmail-ai-auto-responder.json`
- `build-a-personal-assistant-with-google-gemini,-gmail-and-calendar-using-mcp.json` → `personal-assistant-gemini-gmail-calendar.json`
- `!!!-inbox-manager-(gpt,-google-calendar-&-supabase).json` → `inbox-manager-gpt-calendar-supabase.json`
- `extract-expenses-from-emails-and-add-to-google-sheets.json` → `expense-extraction-gmail-sheets.json`
- `bidirectional-github-workflow-sync-&-version-control-for-n8n-workflows.json` → `github-workflow-sync-version-control.json`
- `automated-work-attendance-with-location-triggers.json` → `work-attendance-location-triggers.json`
- `demo:-my-first-ai-agent-in-n8n.json` → `demo-first-ai-agent.json`