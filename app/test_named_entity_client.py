import pytest

from app.named_entity_client import NamedEntityClient


@pytest.fixture
def mock_spacy_model_with_response():
    class SpacyModel:
        def __init__(self, ents):
            self.ents = ents

        def __call__(self, sentence):
            return {"ents": self.ents}

    return SpacyModel


def test_get_entities_dictionary_from_empty_string(mock_spacy_model_with_response):
    named_entity_client = NamedEntityClient(mock_spacy_model_with_response([]))
    entities = named_entity_client.get_entities("")

    assert isinstance(entities, dict)


def test_get_entities_dictionary_from_nonempty_string(mock_spacy_model_with_response):
    named_entity_client = NamedEntityClient(
        mock_spacy_model_with_response([{"text": 'Madison', "label_": 'NOUN'}]))
    entities = named_entity_client.get_entities(
        "Madison is a city in Wisconsin")

    assert isinstance(entities, dict)
    assert "ents" in entities
    assert entities["ents"][0]["text"] == "Madison"
    assert entities["ents"][0]["label_"] == "NOUN"
