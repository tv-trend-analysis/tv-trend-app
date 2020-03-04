from googletrans import Translator

def trans(untranslated_tweet):
    translator = Translator()
    return translator.translate(untranslated_tweet).text
