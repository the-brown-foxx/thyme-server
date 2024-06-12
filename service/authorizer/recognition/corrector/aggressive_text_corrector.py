from service.authorizer.recognition.corrector.text_corrector import TextCorrector


class AggressiveTextCorrector(TextCorrector):
    possible_mutations = {
        'W': ['H', 'M', 'A'],
        'M': ['W', 'H'],
        '1': ['I', 'T'],
        # 'I': ['T'],
        # '5': ['S'],
        # 'S': ['5'],
        # 'G': ['6'],
    }

    def get_possible_texts(self, original: str) -> list[str]:
        possible_texts = [original]

        for original_char, mutations in self.possible_mutations.items():
            for mutation in mutations:
                possible_texts.append(original.replace(mutation, original_char))

        return possible_texts
