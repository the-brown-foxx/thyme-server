from service.authorizer.recognition.corrector.text_corrector import TextCorrector


class NoTextCorrector(TextCorrector):
    def get_possible_texts(self, original: str) -> list[str]:
        return [original]
