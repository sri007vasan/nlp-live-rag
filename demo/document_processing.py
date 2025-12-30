"""
Document processing utilities for integration with RAG system.
Provides helper functions to process documents before indexing.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from document_parser import DocumentParser, DocumentParserFactory


logger = logging.getLogger(__name__)


class DocumentProcessingUtil:
    """Utility class for document processing and text extraction."""
    
    SUPPORTED_EXTENSIONS = {
        '.pdf': 'PDF Document',
        '.docx': 'Word Document',
        '.doc': 'Word Document',
        '.xlsx': 'Excel Spreadsheet',
    }
    
    @staticmethod
    def get_file_type(file_path: str) -> Optional[str]:
        """
        Get human-readable file type.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type description or None if unsupported
        """
        ext = Path(file_path).suffix.lower()
        return DocumentProcessingUtil.SUPPORTED_EXTENSIONS.get(ext)
    
    @staticmethod
    def is_supported_document(file_path: str) -> bool:
        """
        Check if file is a supported document format.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is supported
        """
        ext = Path(file_path).suffix.lower()
        return ext in DocumentProcessingUtil.SUPPORTED_EXTENSIONS
    
    @staticmethod
    def extract_text_from_document(file_path: str) -> Tuple[str, bool]:
        """
        Extract text from any supported document format.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Tuple of (extracted_text, success)
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return "", False
        
        ext = Path(file_path).suffix.lower()
        parser = DocumentParserFactory.get_parser(ext)
        
        if parser is None:
            logger.warning(f"No parser found for extension: {ext}")
            return "", False
        
        logger.info(f"Extracting text from {file_path} ({DocumentProcessingUtil.get_file_type(file_path)})")
        return parser(file_path)
    
    @staticmethod
    def batch_extract_text(directory: str) -> Dict[str, Tuple[str, bool]]:
        """
        Extract text from all supported documents in a directory.
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            Dictionary mapping file paths to (text, success) tuples
        """
        results = {}
        
        if not os.path.isdir(directory):
            logger.error(f"Directory not found: {directory}")
            return results
        
        for file_path in Path(directory).glob('**/*'):
            if file_path.is_file() and DocumentProcessingUtil.is_supported_document(str(file_path)):
                results[str(file_path)] = DocumentProcessingUtil.extract_text_from_document(str(file_path))
        
        return results
    
    @staticmethod
    def get_document_summary(file_path: str, max_length: int = 500) -> str:
        """
        Get a summary/preview of document content.
        
        Args:
            file_path: Path to the document
            max_length: Maximum length of preview text
            
        Returns:
            Preview text from the document
        """
        text, success = DocumentProcessingUtil.extract_text_from_document(file_path)
        if success:
            return text[:max_length] + ("..." if len(text) > max_length else "")
        return "Failed to extract text"


class DocumentIndexingHelper:
    """Helper class for preparing documents for indexing in the RAG system."""
    
    @staticmethod
    def prepare_document_metadata(file_path: str) -> Dict:
        """
        Prepare metadata for a document.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Metadata dictionary
        """
        path_obj = Path(file_path)
        
        metadata = {
            'file_name': path_obj.name,
            'file_path': str(file_path),
            'file_type': DocumentProcessingUtil.get_file_type(file_path),
            'file_size': os.path.getsize(file_path),
            'extension': path_obj.suffix.lower(),
        }
        
        # Add file timestamps if available
        try:
            metadata['created_time'] = os.path.getctime(file_path)
            metadata['modified_time'] = os.path.getmtime(file_path)
        except OSError:
            pass
        
        return metadata
    
    @staticmethod
    def get_parsing_stats() -> Dict[str, bool]:
        """
        Get statistics on which document types are available for parsing.
        
        Returns:
            Dictionary indicating availability of each parser
        """
        return {
            'pdf_available': DocumentParser.is_format_supported('.pdf'),
            'docx_available': DocumentParser.is_format_supported('.docx'),
            'xlsx_available': DocumentParser.is_format_supported('.xlsx'),
            'supported_formats': DocumentParser.get_supported_formats(),
        }
