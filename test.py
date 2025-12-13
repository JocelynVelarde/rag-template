from backend import ingest_text, get_rag_response
# rename "rag" to your actual file name

sample_text = """
VisPay is a digital payment verification system.
It verifies receipts using OCR and AI-based fraud detection.
"""

# print("Ingesting text...")
# ingest_text(sample_text)

# print("\nAsking question...")
response = get_rag_response("What is VisPay? and is there any repository i can find it on?")
print("\nAnswer:", response)
