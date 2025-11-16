import queue

from transformers import TextStreamer

from .typedefs import Tokenizer


class ChunkedTextStreamer(TextStreamer):
    def __init__(self, tokenizer: Tokenizer, skip_prompt: bool = False, **decode_kwargs):
        super().__init__(tokenizer=tokenizer, skip_prompt=skip_prompt, **decode_kwargs)
        self.reached_end = False
        self.queue = queue.Queue()

    def on_finalized_text(self, text: str, stream_end: bool = False):
        """Prints the new text to stdout. If the stream is ending, also prints a newline."""
        text = text.replace("<|begin_of_text|>", "")
        text = text.replace("<|end_of_text|>", "")
        self.queue.put(text)
        self.reached_end = stream_end

    def mark_complete(self):
        """Explicit completion marker for error cases"""
        self.reached_end = True
