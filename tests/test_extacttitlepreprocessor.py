import markdown
import pytest

from mklib.processors.extracttitlepreprocessor import ExtractTitleTreeprocessor


@pytest.fixture
def md():
    return markdown.Markdown(
        extensions=["attr_list"]
    )  # Add attr_list extension for handling attributes


@pytest.fixture
def processor(md: markdown.Markdown):
    processor = ExtractTitleTreeprocessor(md)
    processor._register(md)
    return processor


def test_basic_title_extraction(
    md: markdown.Markdown, processor: ExtractTitleTreeprocessor
):
    """Test basic h1 title extraction."""
    text = "# Simple Title\nSome content"
    md.convert(text)
    assert processor.title == "Simple Title"


def test_no_title(md: markdown.Markdown, processor: ExtractTitleTreeprocessor):
    """Test behavior when no h1 title is present."""
    text = "## Secondary Title\nSome content"
    md.convert(text)
    assert processor.title is None


def test_multiple_h1_takes_first(
    md: markdown.Markdown, processor: ExtractTitleTreeprocessor
):
    """Test that only the first h1 is used as title."""
    text = "# First Title\nContent\n# Second Title"
    md.convert(text)
    assert processor.title == "First Title"


def test_complex_title(md: markdown.Markdown, processor: ExtractTitleTreeprocessor):
    """Test title with formatting."""
    text = "# Title with *italic* and **bold**\nContent"
    md.convert(text)
    assert processor.title == "Title with italic and bold"


def test_title_with_anchor(md: markdown.Markdown, processor: ExtractTitleTreeprocessor):
    """Test title with anchor link."""
    text = "# Title with anchor {: #anchor}\nContent"
    md.convert(text)
    assert processor.title == "Title with anchor"


def test_empty_title(md: markdown.Markdown, processor: ExtractTitleTreeprocessor):
    """Test empty h1 tag."""
    text = "#\nContent"
    md.convert(text)
    assert processor.title == ""


def test_title_with_multiple_lines(
    md: markdown.Markdown,
    processor: ExtractTitleTreeprocessor,
):
    """Test title in a single h1 tag."""
    text = "# Title that spans multiple lines\nContent"
    md.convert(text)
    assert processor.title == "Title that spans multiple lines"


def test_processor_registration(md: markdown.Markdown):
    """Test that processor is properly registered."""
    processor = ExtractTitleTreeprocessor(md)
    processor._register(md)
    assert "mklib_extract_title" in md.treeprocessors


def test_title_with_special_characters(
    md: markdown.Markdown, processor: ExtractTitleTreeprocessor
):
    """Test title with special characters."""
    text = "# Title with $pecial & <chars>\nContent"
    md.convert(text)
    assert processor.title == "Title with $pecial & <chars>"


def test_subsequent_conversions(
    md: markdown.Markdown, processor: ExtractTitleTreeprocessor
):
    """Test that processor works correctly for multiple conversions."""
    text1 = "# First Document\nContent"
    text2 = "# Second Document\nContent"

    md.convert(text1)
    assert processor.title == "First Document"

    md.convert(text2)
    assert processor.title == "Second Document"
