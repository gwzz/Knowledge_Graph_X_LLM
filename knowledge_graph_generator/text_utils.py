"""
Text processing utilities for the knowledge graph generator.
"""
## This module provides functions to process text, including chunking text into manageable pieces with overlap.

def chunk_text_by_lenth(text, chunk_size=500, overlap=50):
    """
    Split a text into chunks of words with overlap.
    
    Args:
        text: The input text to chunk
        chunk_size: The size of each chunk in words
        overlap: The number of words to overlap between chunks
        
    Returns:
        List of text chunks
    """
    # Split text into words
    words = text.split()
    
    # If text is smaller than chunk size, return it as a single chunk
    if len(words) <= chunk_size:
        return [text]
    
    # Create chunks with overlap
    chunks = []
    start = 0
    
    while start < len(words):
        # Calculate end position for this chunk
        end = min(start + chunk_size, len(words))
        
        # Join words for this chunk
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        
        # Move start position for next chunk, accounting for overlap
        start = end - overlap
        
        # If we're near the end and the last chunk would be too small, just exit
        if start < len(words) and start + chunk_size - overlap >= len(words):
            # Add remaining words as the final chunk
            final_chunk = ' '.join(words[start:])
            chunks.append(final_chunk)
            break
    
    return chunks 

def chunk_text_by_sentences(text, chunk_size=5, overlap=1, language='en'):
    """
    Split a text into chunks of sentences with overlap.
    
    Args:
        text: The input text to chunk
        chunk_size: The number of sentences in each chunk
        overlap: The number of sentences to overlap between chunks
        
    Returns:
        List of text chunks
    """
    # Split text into sentences
    if language == 'en':
        # Simple split by period for English
        sentences = text.split('. ')
    elif language == 'ch':
        # For Chinese, we can use a simple split by punctuation
        # Note: This is a naive approach; consider using a library like jieba for better segmentation
        sentences = text.split('。')
    else:
        # For other languages, you might want to use a more sophisticated method
        # Here we just use the same method as English for simplicity
        # In practice, consider using a library like nltk or spacy for better sentence tokenization
        sentences = text.split('. ')
    
    # If text is smaller than chunk size, return it as a single chunk
    if len(sentences) <= chunk_size:
        return [text]
    
    # Create chunks with overlap
    chunks = []
    start = 0
    
    while start < len(sentences):
        # Calculate end position for this chunk
        end = min(start + chunk_size, len(sentences))
        
        # Join sentences for this chunk
        chunk = '. '.join(sentences[start:end]) + ('.' if end < len(sentences) else '')
        chunks.append(chunk)
        
        # Move start position for next chunk, accounting for overlap
        start = end - overlap
        
        # If we're near the end and the last chunk would be too small, just exit
        if start < len(sentences) and start + chunk_size - overlap >= len(sentences):
            # Add remaining sentences as the final chunk
            final_chunk = '. '.join(sentences[start:]) + ('.' if start < len(sentences) else '')
            chunks.append(final_chunk)
            break
    
    return chunks

def chunk_text_by_paragraphs(text, chunk_size=1, overlap=0):
    """
    Split a text into chunks of paragraphs with overlap.
    
    Args:
        text: The input text to chunk
        chunk_size: The number of paragraphs in each chunk
        overlap: The number of paragraphs to overlap between chunks
        
    Returns:
        List of text chunks
    """
    # Split text into paragraphs
    paragraphs = text.split('\n\n')
    
    # If text is smaller than chunk size, return it as a single chunk
    if len(paragraphs) <= chunk_size:
        return [text]
    
    # Create chunks with overlap
    chunks = []
    start = 0
    
    while start < len(paragraphs):
        # Calculate end position for this chunk
        end = min(start + chunk_size, len(paragraphs))
        
        # Join paragraphs for this chunk
        chunk = '\n\n'.join(paragraphs[start:end])
        chunks.append(chunk)
        
        # Move start position for next chunk, accounting for overlap
        start = end - overlap
        
        # If we're near the end and the last chunk would be too small, just exit
        if start < len(paragraphs) and start + chunk_size - overlap >= len(paragraphs):
            # Add remaining paragraphs as the final chunk
            final_chunk = '\n\n'.join(paragraphs[start:])
            chunks.append(final_chunk)
            break
    
    return chunks