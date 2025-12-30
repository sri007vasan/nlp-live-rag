"""
Example usage of the document parser modules.

This file demonstrates how to use the DocumentParser and DocumentProcessingUtil
to extract text from PDF, DOCX, and XLSX files without affecting existing RAG functions.
"""

from document_parser import DocumentParser, DocumentParserFactory
from document_processing import DocumentProcessingUtil, DocumentIndexingHelper
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# EXAMPLE 1: Parse Individual Documents
# ============================================================================

def example_parse_individual_documents():
    """Example: Parse individual documents of different types."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Parse Individual Documents")
    print("="*70)
    
    # Example PDF parsing
    pdf_path = "sample.pdf"
    text, success = DocumentParser.parse_pdf(pdf_path)
    if success:
        print(f"✓ Successfully parsed PDF. Extracted {len(text)} characters.")
        print(f"Preview: {text[:200]}...")
    else:
        print(f"✗ Failed to parse PDF: {pdf_path}")
    
    # Example DOCX parsing
    docx_path = "sample.docx"
    text, success = DocumentParser.parse_docx(docx_path)
    if success:
        print(f"✓ Successfully parsed DOCX. Extracted {len(text)} characters.")
        print(f"Preview: {text[:200]}...")
    else:
        print(f"✗ Failed to parse DOCX: {docx_path}")
    
    # Example XLSX parsing
    xlsx_path = "sample.xlsx"
    text, success = DocumentParser.parse_xlsx(xlsx_path)
    if success:
        print(f"✓ Successfully parsed XLSX. Extracted {len(text)} characters.")
        print(f"Preview: {text[:200]}...")
    else:
        print(f"✗ Failed to parse XLSX: {xlsx_path}")


# ============================================================================
# EXAMPLE 2: Universal Parse Using DocumentParser.parse_document()
# ============================================================================

def example_universal_parsing():
    """Example: Use universal parser that auto-detects file type."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Universal Document Parsing")
    print("="*70)
    
    files = ["document.pdf", "report.docx", "data.xlsx"]
    
    for file_path in files:
        text, success = DocumentParser.parse_document(file_path)
        if success:
            print(f"✓ {file_path}: {len(text)} characters extracted")
        else:
            print(f"✗ {file_path}: Failed to parse")


# ============================================================================
# EXAMPLE 3: Use DocumentParserFactory for Custom Extensions
# ============================================================================

def example_factory_pattern():
    """Example: Use factory pattern to get parsers."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Factory Pattern for Parsers")
    print("="*70)
    
    # Get parser for a specific extension
    pdf_parser = DocumentParserFactory.get_parser(".pdf")
    docx_parser = DocumentParserFactory.get_parser(".docx")
    xlsx_parser = DocumentParserFactory.get_parser(".xlsx")
    
    if pdf_parser:
        print("✓ PDF parser available")
    if docx_parser:
        print("✓ DOCX parser available")
    if xlsx_parser:
        print("✓ XLSX parser available")
    
    # Example: Register custom parser
    def custom_txt_parser(file_path):
        """Custom parser for .txt files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read(), True
        except Exception as e:
            return "", False
    
    # Register the custom parser
    DocumentParserFactory.register_parser(".txt", custom_txt_parser)
    print("✓ Custom .txt parser registered")


# ============================================================================
# EXAMPLE 4: Utility Functions for Document Processing
# ============================================================================

def example_document_processing_util():
    """Example: Use DocumentProcessingUtil for document management."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Document Processing Utilities")
    print("="*70)
    
    # Check if file is supported
    files = ["document.pdf", "report.docx", "data.xlsx", "image.jpg"]
    
    for file_path in files:
        if DocumentProcessingUtil.is_supported_document(file_path):
            file_type = DocumentProcessingUtil.get_file_type(file_path)
            print(f"✓ {file_path}: Supported ({file_type})")
        else:
            print(f"✗ {file_path}: Not supported")
    
    # Get document summary/preview
    print("\nDocument Preview:")
    text, success = DocumentProcessingUtil.extract_text_from_document("document.pdf")
    if success:
        summary = DocumentProcessingUtil.get_document_summary("document.pdf", max_length=100)
        print(f"Summary: {summary}")


# ============================================================================
# EXAMPLE 5: Batch Processing Documents
# ============================================================================

def example_batch_processing():
    """Example: Process multiple documents in a directory."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Batch Document Processing")
    print("="*70)
    
    directory = "./documents"
    results = DocumentProcessingUtil.batch_extract_text(directory)
    
    print(f"Processed {len(results)} documents:")
    for file_path, (text, success) in results.items():
        status = "✓" if success else "✗"
        chars = len(text) if success else 0
        print(f"{status} {file_path}: {chars} characters")


# ============================================================================
# EXAMPLE 6: Document Metadata and Indexing
# ============================================================================

def example_document_metadata():
    """Example: Prepare document metadata for indexing."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Document Metadata Preparation")
    print("="*70)
    
    file_path = "document.pdf"
    metadata = DocumentIndexingHelper.prepare_document_metadata(file_path)
    
    print(f"Metadata for {file_path}:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    
    # Get parsing statistics
    stats = DocumentIndexingHelper.get_parsing_stats()
    print(f"\nParsing Capabilities:")
    print(f"  PDF: {'Available' if stats['pdf_available'] else 'Not available'}")
    print(f"  DOCX: {'Available' if stats['docx_available'] else 'Not available'}")
    print(f"  XLSX: {'Available' if stats['xlsx_available'] else 'Not available'}")
    print(f"  Supported formats: {', '.join(stats['supported_formats'])}")


# ============================================================================
# EXAMPLE 7: Check Supported Formats
# ============================================================================

def example_check_supported_formats():
    """Example: Check which formats are supported."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Supported File Formats")
    print("="*70)
    
    formats = DocumentParser.get_supported_formats()
    print(f"Supported formats: {', '.join(formats)}")
    
    test_extensions = [".pdf", ".docx", ".doc", ".xlsx", ".txt", ".json"]
    for ext in test_extensions:
        is_supported = DocumentParser.is_format_supported(ext)
        status = "✓" if is_supported else "✗"
        print(f"{status} {ext}")


# ============================================================================
# EXAMPLE 8: Integration with RAG System (How to use in app.py)
# ============================================================================

def example_rag_integration():
    """
    Example: How to integrate document parsing with the existing RAG system.
    
    This shows how you can use the parsers WITHOUT changing existing functions.
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: Integration with Existing RAG System")
    print("="*70)
    
    print("""
    INTEGRATION POINTS (No changes needed to existing RAG functions):
    
    1. Pre-processing documents before uploading to Pathway:
       -------------------------------------------------------
       from document_processing import DocumentProcessingUtil
       
       # Extract and validate documents locally
       text, success = DocumentProcessingUtil.extract_text_from_document("file.pdf")
       if success:
           # Validate or preprocess
           store_in_vector_db(text)
    
    
    2. Post-processing retrieved documents:
       -----------------------------------
       from document_parser import DocumentParser
       
       # In endpoint_utils.py or app.py, after retrieving files:
       for doc in docs_list:
           text, success = DocumentParser.parse_document(doc['path'])
           if success:
               # Enhance with parsed content
               doc['extracted_text'] = text
    
    
    3. Add a document info endpoint:
       ----------------------------
       from document_processing import DocumentIndexingHelper
       
       # Get metadata about ingested documents
       metadata = DocumentIndexingHelper.prepare_document_metadata(file_path)
       stats = DocumentIndexingHelper.get_parsing_stats()
    
    
    4. File upload validation:
       -----------------------
       from document_processing import DocumentProcessingUtil
       
       # Check if uploaded file is supported
       if DocumentProcessingUtil.is_supported_document(file_path):
           file_type = DocumentProcessingUtil.get_file_type(file_path)
           # Process file...
    """)


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Document Parser - Usage Examples")
    print("="*70)
    print("\nThese examples show how to use the new document parsing capabilities")
    print("without changing any existing RAG functions.")
    
    # Note: Uncomment the examples you want to run
    # Make sure you have sample files in the correct paths
    
    # example_parse_individual_documents()
    # example_universal_parsing()
    # example_factory_pattern()
    # example_document_processing_util()
    # example_batch_processing()
    # example_document_metadata()
    example_check_supported_formats()
    example_rag_integration()
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70 + "\n")
