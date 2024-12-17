import markdown


class AnsiColors:
    """
    Class to define ANSI color codes for terminal output.
    These codes can be used to add colored output in terminal-based applications.
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class HtmlColorTags:
    """
    Class to define HTML color tags for web output.
    These can be used to add color to words or phrases in HTML-formatted text.
    """

    OKGREEN = '<span style="color:green">'
    WARNING = '<span style="color:yellow">'
    FAIL = '<span style="color:red">'
    ENDC = "</span>"


def highlight_words(text: str, words_to_highlight: list, paths: list = None) -> str:
    """
    Highlights specific words in a text by wrapping them in HTML color tags.

    Args:
        text (str): The input text where words will be highlighted.
        words_to_highlight (list): A list of words to highlight in the text.

    Returns:
        str: The text with the specified words wrapped in HTML green color tags.

    Example:
        text = "This is a sample text."
        words_to_highlight = ["sample", "text"]
        result = highlight_words_in_html(text, words_to_highlight)
        # Output: 'This is a <span class="green">sample</span> <span class="green">text</span>.'
    """

    if words_to_highlight is None or len(words_to_highlight) == 0:
        return text

    highlighted_text = text
    for i in range(len(words_to_highlight)):
        if paths is None:
            highlighted_text = highlighted_text.replace(
                words_to_highlight[i], f"{HtmlColorTags.OKGREEN}{words_to_highlight[i]}{HtmlColorTags.ENDC}"
            )
        else:
            highlighted_text = highlighted_text.replace(
                words_to_highlight[i],
                f'<span class="highlighted-sentence" style="color:green" data-content="{paths[i]}">{words_to_highlight[i]}{HtmlColorTags.ENDC}',
            )

    return highlighted_text


def replacer(text: str) -> str:
    return text.replace("&quot;", '"').replace("&#x27;", "'")


def format_text_for_html(text: str) -> str:
    """
    Formats a given text for HTML display by replacing newlines with <br> tags.

    Args:
        text (str): The input text to be formatted for HTML.

    Returns:
        str: The text with newlines replaced by <br> tags.

    Example:
        text = "This is a line.\nThis is another line."
        result = format_text_for_html(text)
        # Output: 'This is a line.<br>This is another line.'
    """
    output = markdown.markdown(text, extensions=["fenced_code"])
    output = replacer(output)
    return output


# format output
def format_llm_output(llm_output: str) -> str:
    """
    Formats the LLM output into a user-friendly HTML format.

    Args:
        llm_output (str): The raw output from the LLM.

    Returns:
        str: The formatted output for display.
    """
    # Example formatting logic: Check for bullet points or numbered lists
    formatted_output = ""

    # Split the output into lines
    lines = llm_output.strip().split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("- "):  # Bullet point
            formatted_output += f"<li>{line[2:]}</li>\n"
        elif line.startswith("1. "):  # Numbered list
            formatted_output += f"<li>{line[3:]}</li>\n"
        else:
            formatted_output += f"<p>{line}</p>\n"  # Regular paragraph

    # Wrap in an unordered list if bullet points are present
    if "<li>" in formatted_output:
        formatted_output = f"<ul>\n{formatted_output}</ul>"

    # Finally, convert any Markdown syntax in the output
    formatted_output = format_text_for_html(formatted_output)

    return formatted_output
