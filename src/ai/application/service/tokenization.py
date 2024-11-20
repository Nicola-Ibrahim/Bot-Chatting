class TokenizationService:
    def __init__(self, model, tokenizer) -> None:
        self.tokenizer = tokenizer

    def tokenize(self, text: str, token_limit: int = 500):
        tokenized_text = self.tokenizer.tokenize(text)
        return tokenized_text
