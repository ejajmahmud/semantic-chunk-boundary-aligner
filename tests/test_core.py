"""Tests for Semantic Chunk Boundary Aligner."""
import unittest
from semantic_chunk_boundary_aligner.core import SemanticChunkAligner


class TestSemanticChunkAligner(unittest.TestCase):
    def test_preserves_breadcrumbs_and_code_fences(self):
        doc = "# Docs\n## Install\nInstall steps.\n```bash\necho hello world\n```\n## Run\nRun it."
        chunks = SemanticChunkAligner(max_chars=120).chunk(doc)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0]["breadcrumb"], "Docs > Install")
        fence_chunk = [c for c in chunks if "```bash" in c["text"]][0]
        self.assertTrue(fence_chunk["text"].endswith("```"))

    def test_empty_document(self):
        self.assertEqual(SemanticChunkAligner().chunk("   "), [])
