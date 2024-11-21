class ResponseGenerationService:
    def __init__(self, model, tokenizer) -> None:
        self.model = model
        self.tokenizer = tokenizer

    def generate_response(self, text: str) -> str:

        # Check the length of text if exceed the available tokens in generator
        if not self.tokenizer.check_tokenization(text=text):
            raise InValidOperationException("The text its too long, consider to make it shorter")

        # call LLM to generate response for the model
        response = self.model.generate(text=text)

        return response
