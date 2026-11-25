"""Core heading-aware and code-fence-safe markdown chunker."""
import re
from typing import Any, Dict, List


class SemanticChunkAligner:
    """Chunks markdown documents along structural boundaries without splitting code blocks."""

    HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")

    def __init__(self, max_chars: int = 800):
        self.max_chars = max_chars

    def _tokenize_blocks(self, text: str) -> List[Dict[str, str]]:
        blocks: List[Dict[str, str]] = []
        lines = text.splitlines()
        i = 0
        trail: List[str] = []

        while i < len(lines):
            line = lines[i]
            hm = self.HEADING_RE.match(line)
            if hm:
                lvl = len(hm.group(1))
                title = hm.group(2).strip()
                trail = trail[:lvl - 1] + [title]
                i += 1
                continue

            if line.strip().startswith("```"):
                buf = [line]
                i += 1
                while i < len(lines):
                    buf.append(lines[i])
                    if lines[i].strip().startswith("```"):
                        i += 1
                        break
                    i += 1
                blocks.append({"breadcrumb": " > ".join(trail) or "Root", "content": "\n".join(buf)})
                continue

            if not line.strip():
                i += 1
                continue

            para = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("```") and not self.HEADING_RE.match(lines[i]):
                para.append(lines[i])
                i += 1
            blocks.append({"breadcrumb": " > ".join(trail) or "Root", "content": "\n".join(para)})

        return blocks

    def chunk(self, text: str) -> List[Dict[str, Any]]:
        blocks = self._tokenize_blocks(text)
        chunks: List[Dict[str, Any]] = []
        cur_bc = None
        cur_parts: List[str] = []
        cur_len = 0

        for blk in blocks:
            bc = blk["breadcrumb"]
            content = blk["content"]
            if cur_parts and (bc != cur_bc or cur_len + len(content) + 2 > self.max_chars):
                chunks.append({"index": len(chunks), "breadcrumb": cur_bc, "text": "\n\n".join(cur_parts)})
                cur_parts = []
                cur_len = 0
            cur_bc = bc
            cur_parts.append(content)
            cur_len += len(content) + 2

        if cur_parts:
            chunks.append({"index": len(chunks), "breadcrumb": cur_bc, "text": "\n\n".join(cur_parts)})
        return chunks
