import LanguageDeck.models.Cards as cds

type_names = {"vocab a": "vocab a",
              "vocab b": "vocab b",
              "example a": "example a",
              "example b": "example b"}

type_names_to_cards = {type_names["vocab a"] : cds.LanguageAVocab,
                       type_names["vocab b"] : cds.LanguageBVocab,
                       type_names["example a"] : cds.LanguageAExample,
                       type_names["example b"] : cds.LanguageBExample}

card_example_types = {cds.LanguageAVocab : cds.LanguageAExample,
                      cds.LanguageBVocab : cds.LanguageBExample,
                      cds.LanguageAExample : cds.LanguageAVocab,
                      cds.LanguageBExample : cds.LanguageBVocab}

card_translation_types = {cds.LanguageAVocab : cds.LanguageBVocab,
                          cds.LanguageBVocab : cds.LanguageAVocab,
                          cds.LanguageAExample : cds.LanguageBExample,
                          cds.LanguageBExample : cds.LanguageAExample}

card_example_fields = {cds.LanguageAVocab : "examples",
                      cds.LanguageBVocab : "examples",
                      cds.LanguageAExample : "words",
                      cds.LanguageBExample : "words"}
