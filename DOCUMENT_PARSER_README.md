# Document Parser Module

This module provides comprehensive document parsing capabilities for the RAG system, supporting multiple file formats including PDF, Word documents, and Excel spreadsheets. **All additions are non-breaking and do not modify any existing RAG functions.**

## Overview

The document parser module consists of three main components:

1. **`document_parser.py`** - Core parsing logic for different file formats
2. **`document_processing.py`** - Utility functions for document management
3. **`examples_usage.py`** - Example code showing how to use the parsers

## Supported File Formats

| Format | Extension | Status | Library |
|--------|-----------|--------|---------|
| PDF | `.pdf` | ✓ Supported | `pypdf` |
| Word Document | `.docx` | ✓ Supported | `python-docx` |
| Word Document (Legacy) | `.doc` | ✓ Supported* | `python-docx` |
| Excel Spreadsheet | `.xlsx` | ✓ Supported | `openpyxl` |

*Note: Legacy `.doc` files are handled by treating them as DOCX format.

## Installation

The required dependencies are already added to:
- `requirements.txt` (demo folder)
- `requirements.txt` (root folder)
- `pyproject.toml`

To install manually:
```bash
pip install pypdf python-docx openpyxl
```

## Quick Start

### Basic Usage

```python
from document_parser import DocumentParser

# Parse any supported document
text, success = DocumentParser.parse_document("myfile.pdf")
if success:
    print(f"Extracted text: {text}")

# Or use specific parsers
text, success = DocumentParser.parse_pdf("document.pdf")
text, success = DocumentParser.parse_docx("report.docx")
text, success = DocumentParser.parse_xlsx("data.xlsx")
```

### Utility Functions

```python
from document_processing import DocumentProcessingUtil, DocumentIndexingHelper

# Check if file is supported
if DocumentProcessingUtil.is_supported_document("file.pdf"):
    print(f"File type: {DocumentProcessingUtil.get_file_type('file.pdf')}")

# Extract text from document
text, success = DocumentProcessingUtil.extract_text_from_document("file.docx")

# Get document preview
summary = DocumentProcessingUtil.get_document_summary("file.xlsx", max_length=500)

# Prepare metadata
metadata = DocumentIndexingHelper.prepare_document_metadata("file.pdf")

# Get parsing statistics
stats = DocumentIndexingHelper.get_parsing_stats()
```

## API Reference

### DocumentParser Class

Core parsing functionality for different document types.

#### Methods

**`parse_pdf(file_path: str) -> Tuple[str, bool]`**
- Parses PDF files and extracts text from all pages
- Returns: (extracted_text, success)
- Requires: `pypdf` library

**`parse_docx(file_path: str) -> Tuple[str, bool]`**
- Parses DOCX files and extracts text from paragraphs and tables
- Returns: (extracted_text, success)
- Requires: `python-docx` library

**`parse_xlsx(file_path: str) -> Tuple[str, bool]`**
- Parses XLSX files and extracts text from all sheets
- Returns: (extracted_text, success)
- Requires: `openpyxl` library

**`parse_document(file_path: str) -> Tuple[str, bool]`**
- Universal parser that auto-detects file type based on extension
- Returns: (extracted_text, success)
- Automatically routes to appropriate parser

**`get_supported_formats() -> List[str]`**
- Returns list of supported file extensions
- Example: `['.pdf', '.docx', '.xlsx']`

**`is_format_supported(file_extension: str) -> bool`**
- Checks if a specific format is supported
- Example: `is_format_supported('.pdf')` returns `True`

### DocumentParserFactory Class

Factory pattern implementation for parser management.

#### Methods

**`get_parser(file_extension: str)`**
- Gets the parser function for a specific file extension
- Returns: Parser function or None

**`register_parser(file_extension: str, parser_func)`**
- Registers a custom parser for a new file extension
- Allows extending support for additional formats

### DocumentProcessingUtil Class

Utility functions for document management and processing.

#### Methods

**`get_file_type(file_path: str) -> Optional[str]`**
- Returns human-readable file type description
- Example: `"PDF Document"`, `"Word Document"`, `"Excel Spreadsheet"`

**`is_supported_document(file_path: str) -> bool`**
- Checks if file is a supported document format

**`extract_text_from_document(file_path: str) -> Tuple[str, bool]`**
- Extracts text from any supported document
- Returns: (extracted_text, success)

**`batch_extract_text(directory: str) -> Dict[str, Tuple[str, bool]]`**
- Processes all supported documents in a directory
- Returns: Dictionary mapping file paths to (text, success) tuples

**`get_document_summary(file_path: str, max_length: int = 500) -> str`**
- Gets a preview/summary of document content
- Returns: Text preview (truncated to max_length)

### DocumentIndexingHelper Class

Helper functions for document indexing preparation.

#### Methods

**`prepare_document_metadata(file_path: str) -> Dict`**
- Prepares metadata for a document
- Returns dictionary with:
  - `file_name`: Name of the file
  - `file_path`: Full path to the file
  - `file_type`: Human-readable file type
  - `file_size`: Size in bytes
  - `extension`: File extension
  - `created_time`: Creation timestamp (if available)
  - `modified_time`: Modification timestamp (if available)

**`get_parsing_stats() -> Dict[str, bool]`**
- Returns parsing capabilities
- Example return:
  ```python
  {
      'pdf_available': True,
      'docx_available': True,
      'xlsx_available': True,
      'supported_formats': ['.pdf', '.docx', '.xlsx']
  }
  ```

## Integration with Existing RAG System

The document parsers are designed to work **alongside** the existing RAG system without any modifications. Here are integration examples:

### 1. Local Document Validation

```python
from document_processing import DocumentProcessingUtil

def validate_local_document(file_path):
    """Validate if document can be parsed before uploading to Pathway."""
    if DocumentProcessingUtil.is_supported_document(file_path):
        text, success = DocumentProcessingUtil.extract_text_from_document(file_path)
        if success:
            return True, f"Document type: {DocumentProcessingUtil.get_file_type(file_path)}"
    return False, "Unsupported or unreadable document"
```

### 2. Enhanced Document Metadata

```python
from document_processing import DocumentIndexingHelper

def add_metadata_to_documents(docs_list):
    """Add metadata to retrieved documents."""
    enhanced_docs = []
    for doc in docs_list:
        metadata = DocumentIndexingHelper.prepare_document_metadata(doc['path'])
        doc['metadata'] = metadata
        enhanced_docs.append(doc)
    return enhanced_docs
```

### 3. Document Type Display

```python
from document_processing import DocumentProcessingUtil

def get_documents_with_types(file_paths):
    """Get file paths with their types."""
    result = []
    for path in file_paths:
        if DocumentProcessingUtil.is_supported_document(path):
            file_type = DocumentProcessingUtil.get_file_type(path)
            result.append({
                'path': path,
                'type': file_type,
                'name': path.split('/')[-1]
            })
    return result
```

### 4. Batch Processing

```python
from document_processing import DocumentProcessingUtil

def process_document_directory(directory):
    """Process all documents in a directory."""
    results = DocumentProcessingUtil.batch_extract_text(directory)
    return {
        'total_documents': len(results),
        'processed': sum(1 for _, (_, success) in results.items() if success),
        'documents': results
    }
```

## Examples

See `examples_usage.py` for comprehensive examples including:

1. Individual document parsing
2. Universal document parsing
3. Factory pattern usage
4. Document processing utilities
5. Batch document processing
6. Document metadata preparation
7. Supported format checking
8. RAG system integration patterns

Run the examples:
```bash
python examples_usage.py
```

## Error Handling

All parser functions return a tuple `(text, success)`:
- `success = True` if parsing succeeded, `False` otherwise
- `text` contains extracted content on success, empty string on failure
- Errors are logged using Python's `logging` module

Example:
```python
from document_parser import DocumentParser

text, success = DocumentParser.parse_pdf("document.pdf")
if not success:
    # Handle parsing failure
    print("Failed to parse PDF")
```

## Performance Considerations

- **PDF files**: Processing speed depends on number of pages and complexity
- **DOCX files**: Generally fast; includes table extraction
- **XLSX files**: Extracts all sheets; large files may use more memory
- **Batch processing**: Consider memory usage for large directories

## Extending with Custom Parsers

To add support for additional file formats:

```python
from document_parser import DocumentParserFactory

def parse_custom_format(file_path):
    """Custom parser for .custom files."""
    try:
        # Your parsing logic here
        with open(file_path, 'r') as f:
            text = f.read()
        return text, True
    except Exception as e:
        return "", False

# Register the parser
DocumentParserFactory.register_parser(".custom", parse_custom_format)

# Now you can use it
from document_parser import DocumentParser
text, success = DocumentParser.parse_document("file.custom")
```

## Troubleshooting

### Library Import Errors

If you get import errors for `pypdf`, `python-docx`, or `openpyxl`:

```bash
# Install missing libraries
pip install pypdf python-docx openpyxl

# Or reinstall from requirements
pip install -r requirements.txt
```

### Parsing Failures

Check the logs for detailed error messages:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Unsupported File Formats

Check which formats are available:
```python
from document_parser import DocumentParser
print(DocumentParser.get_supported_formats())
```

## Future Enhancements

Potential additions for future versions:
- Support for `.doc` files (legacy Word format) with conversion
- Support for `.pptx` (PowerPoint) files
- Support for `.csv` files
- Optical Character Recognition (OCR) for image-based PDFs
- Streaming parser for very large files
- Caching mechanisms for parsed documents

## License

These document parsing utilities are part of the NLP Live RAG project.

## Support

For issues, questions, or feature requests, please refer to the main project repository.
