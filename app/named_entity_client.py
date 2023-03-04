class NamedEntityClient:
    LABEL_MAP = {
        "PERSON": "Person",
        "NORP": "Group",
        "NOUN": "Noun",
        "LOC": "Location",
        "LANGUAGE": "Language",
        "GPE": "GeoPoliticalIdentity",
    }

    def __init__(self, model):
        self.model = model

    def get_entities(self, sentence):
        doc = self.model(sentence)
        return {"ents": [{"text": ent["text"], "label": self.map_label(ent["label_"])} for ent in doc["ents"]], "html": doc["html"]}

    def map_label(self, label):
        if label in self.LABEL_MAP:
            return self.LABEL_MAP[label]
        return "Unknown"
