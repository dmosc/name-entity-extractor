import pytest

from app.named_entity_client import NamedEntityClient


@pytest.fixture
def mock_spacy_model_with_response():
    class SpacyModel:
        def __init__(self):
            self.ents = [],
            self.html = ""

        def __call__(self, sentence):
            return {"ents": self.ents, "html": self.html}

        def set_return(self, ents, html):
            self.ents = ents
            self.html = html

    return SpacyModel()


def test_get_entities_dictionary_from_empty_string(mock_spacy_model_with_response):
    mock_spacy_model_with_response.set_return([], "")
    named_entity_client = NamedEntityClient(mock_spacy_model_with_response)
    get_entities_response = named_entity_client.get_entities("")

    assert isinstance(get_entities_response, dict)


def test_get_entities_dictionary_from_nonempty_string(mock_spacy_model_with_response):
    mock_spacy_model_with_response.set_return(
        [{"text": 'Madison', "label_": 'NOUN'}], "")
    named_entity_client = NamedEntityClient(mock_spacy_model_with_response)
    get_entities_response = named_entity_client.get_entities(
        "Madison is a city in Wisconsin")

    assert isinstance(get_entities_response, dict)


def test_get_entity_PERSON_serialized_as_Person(mock_spacy_model_with_response):
    mock_spacy_model_with_response.set_return(
        [{"text": "Laurent Fressinet", "label_": "PERSON"}], "")
    named_entity_client = NamedEntityClient(mock_spacy_model_with_response)
    get_entities_response = named_entity_client.get_entities(
        "Laurent Fressinet is a famous person")

    assert isinstance(get_entities_response, dict)
    assert get_entities_response["ents"] == [
        {"text": "Laurent Fressinet", "label": "Person"}]


def test_get_entity_NORP_serialized_as_Group(mock_spacy_model_with_response):
    mock_spacy_model_with_response.set_return(
        [{"text": "Latinx", "label_": "NORP"}], "")
    named_entity_client = NamedEntityClient(mock_spacy_model_with_response)
    get_entities_response = named_entity_client.get_entities(
        "Meet the Latinx community")

    assert isinstance(get_entities_response, dict)
    assert get_entities_response["ents"] == [
        {"text": "Latinx", "label": "Group"}]


def test_get_entity_LOC_serialized_as_Location(mock_spacy_model_with_response):
    mock_spacy_model_with_response.set_return(
        [{"text": "ocean", "label_": "LOC"}], "")
    named_entity_client = NamedEntityClient(mock_spacy_model_with_response)
    get_entities_response = named_entity_client.get_entities(
        "the ocean")

    assert isinstance(get_entities_response, dict)
    assert get_entities_response["ents"] == [
        {"text": "ocean", "label": "Location"}]


def test_get_entity_LANGUAGE_serialized_as_Language(mock_spacy_model_with_response):
    mock_spacy_model_with_response.set_return(
        [{"text": "ASL", "label_": "LANGUAGE"}], "")
    named_entity_client = NamedEntityClient(mock_spacy_model_with_response)
    get_entities_response = named_entity_client.get_entities(
        "the ocean")

    assert isinstance(get_entities_response, dict)
    assert get_entities_response["ents"] == [
        {"text": "ASL", "label": "Language"}]


def test_get_entity_GPE_serialized_as_GeoPoliticalIdentity(mock_spacy_model_with_response):
    mock_spacy_model_with_response.set_return(
        [{"text": "European Union", "label_": "GPE"}], "")
    named_entity_client = NamedEntityClient(mock_spacy_model_with_response)
    get_entities_response = named_entity_client.get_entities(
        "the ocean")

    assert isinstance(get_entities_response, dict)
    assert get_entities_response["ents"] == [
        {"text": "European Union", "label": "GeoPoliticalIdentity"}]


def test_get_multiple_entities(mock_spacy_model_with_response):
    mock_spacy_model_with_response.set_return(
        [{"text": "Laurent Fressinet", "label_": "PERSON"}, {"text": "European Union", "label_": "GPE"}], "")
    named_entity_client = NamedEntityClient(mock_spacy_model_with_response)
    get_entities_response = named_entity_client.get_entities(
        "Laurent Fressinet is from the European Union")

    assert isinstance(get_entities_response, dict)
    assert len(get_entities_response["ents"]) == 2
    assert get_entities_response["ents"] == [
        {"text": "Laurent Fressinet", "label": "Person"}, {"text": "European Union", "label": "GeoPoliticalIdentity"}]
