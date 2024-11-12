from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING

import markdown
import markdown.postprocessors
import markdown.treeprocessors


if TYPE_CHECKING:
    from collections.abc import Sequence
    from xml.etree import ElementTree as ET


logger = logging.getLogger(__name__)


class ExtractTitleTreeprocessor(markdown.treeprocessors.Treeprocessor):
    """Extract title from markdown content."""

    def __init__(self, md: markdown.Markdown | None = None) -> None:
        super().__init__(md)
        self.title: str | None = None
        self.postprocessors: Sequence[markdown.postprocessors.Postprocessor] = ()

    def run(self, root: ET.Element) -> ET.Element:
        """Extract title from the first h1 element."""
        try:
            el = next(el for el in root if el.tag == "h1")
            # Fix for deprecation warning: use explicit length check
            if len(el) > 0 and el[-1].tag == "a" and not (el[-1].tail or "").strip():
                el = copy.copy(el)
                del el[-1]
            # Join all text content, including nested elements
            title = "".join(el.itertext())
            # Apply postprocessors
            for pp in self.postprocessors:
                title = pp.run(title)
            self.title = title.strip()

        except StopIteration:
            pass

        return root

    def _register(self, md: markdown.Markdown) -> None:
        self.postprocessors = list(md.postprocessors)
        md.treeprocessors.register(
            self,
            "mklib_extract_title",
            priority=-1,  # After the end.
        )
