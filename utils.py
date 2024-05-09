from typing import Union, Any, Literal
import nltk
from nltk.corpus import wordnet
import inflect

nltk.download("wordnet")
nltk.download('averaged_perceptron_tagger')

inflect_engine = inflect.engine()


def get_synonym(word: str, pos: str) -> list[Union[str, Any]]:
    """
    Получает все синонимы для заданного слова и части речи из WordNet.

    :param word: Слово, для которого нужно найти синонимы.
    :param pos: Часть речи (POS), используемая для фильтрации результатов в WordNet.

    :return: Список синонимов для указанного слова.
    Если для заданного слова нет доступных синонимов, функция возвращает исходное слово как часть списка.
    """
    synsets = wordnet.synsets(word, pos=pos)

    synonyms = set()

    for synset in synsets:
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    synonyms.add(word)
    return list(synonyms)


def get_synonym_forms(word: str) -> list[Union[Union[str, Literal[False]], Any]]:
    """
    Возвращает все возможные синонимичные формы слова с учетом его грамматической части речи.

    :param word: Слово, для которого требуется найти синонимы и формы.

    :return: Список синонимов слова с учетом различных грамматических форм.
    """
    pos_tag = nltk.pos_tag([word])[0][1]
    pos = None

    # Определение соответствия между тегами POS и типами WordNet
    if pos_tag.startswith('NN'):
        pos = 'n'  # Noun
    elif pos_tag.startswith('VB'):
        pos = 'v'  # Verb
    elif pos_tag.startswith('JJ'):
        pos = 'a'  # Adjective
    elif pos_tag.startswith('RB'):
        pos = 'r'  # Adverb

    synonyms = get_synonym(word.lower(), pos)

    synonyms_form = []
    # Попытка вернуть слово к оригинальной форме (множественное число, время)
    for synonym in synonyms:
        if pos_tag == 'NNS' and synonym:
            synonyms_form.append(inflect_engine.plural(synonym))
        elif pos_tag == 'NN' and synonym:
            synonyms_form.append(inflect_engine.singular_noun(synonym) or synonym)
        elif pos_tag in ['VBD', 'VBN']:
            synonyms_form.append(inflect_engine.past(synonym))
        elif pos_tag == 'VBG':
            synonyms_form.append(inflect_engine.present_participle(synonym))
        else:
            synonyms_form.append(synonym)

    return synonyms_form