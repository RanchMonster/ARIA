import nltk
nltk.download('punkt')

punctuation_marks = ['.', '?', '!', ';', ':']

def format(trigger, string):
    sentences = nltk.sent_tokenize(string)
    for index, sentence in enumerate(sentences):
        def check_end(content = sentence.split()[-1]):
            if any(content.endswith(mark) for mark in punctuation_marks):
                if content[:-1] == trigger: return True
                else: check_end(content[:-1])
        if check_end(): break
        example_indicator = ': '
        if example_indicator in sentence:
            trigger_index = sentence.find(trigger)
            example_indicator_index = sentence.find(example_indicator)
            if trigger_index == example_indicator_index + len(example_indicator): break
            if trigger_index == example_indicator_index - len(trigger): break
        if not sentence.startswith(trigger) or sentence.endswith(trigger): sentences[index] = ''
    return ' '.join([item for item in sentences if item])