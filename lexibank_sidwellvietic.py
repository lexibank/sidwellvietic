import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language
from pylexibank import FormSpec


@attr.s
class CustomLanguage(Language):
    Sources = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "sidwellvietic"
    language_class = CustomLanguage
    form_spec = FormSpec(
            separators="~;,/", missing_data=["∅", "#", "NA", 'XX', '*#'], first_form_only=True,
            replacements=[
                (x, y) for x, y in zip(
                    '1234567890',
                    '¹²³⁴⁵⁶⁷⁸⁹⁰',
                    )
                ]+[
                    ('-', ''),
                    ("(diː | tiː)", "diː"),
                    ("(guːs | kuːs)", "guːs"),
                    ("(ɟiːŋ | ciɲ)", "ɟiːŋ"),
                    ("(k-riɛs / k-rɛs | res)", "k-riɛs"),
                    #("'", 'ʰ'),
                    (' "mountain"', ''),
                    (' "hill"', ''),
                    (' [<Lao]', ''),
                    ('[', ''),
                    (']', ''),
                    (' < Lao', ''),
                    (' ', '_'),
                    ("ʔək__̄", "ʔək"),
                    ("anaŋ__᷅ ", "anaŋ"),
                    ("_'abdomen'", ""),
                    ("dŋ.³³", "dəŋ³³"),
                    ("_᷄ "[:-2], ""),
                    ("m̀", "m"),
                    ("ŋ᷄ "[:-1], "ŋ"),
                    ("\u1dc4", ""),
                    ("\u1dc5", ""),

                    ])

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for concept in self.concepts:
            idx = concept["NUMBER"]+"_"+slug(concept["ENGLISH"])
            concepts[concept["ENGLISH"]] = idx
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["ENGLISH"],
                    Concepticon_ID=concept["CONCEPTICON_ID"],
                    Concepticon_Gloss=concept["CONCEPTICON_GLOSS"],
                    )
        args.log.info("added concepts")
        # add language
        languages = args.writer.add_languages()
        sources = {
                language["ID"]: language["Sources"].strip().replace(" ", "")
                for language in self.languages}
        args.log.info("added languages")

        # read in data
        data = self.raw_dir.read_csv(
            "data.tsv", delimiter="\t", 
        )
        header = data[0]
        header[0] = "Gloss"
        cognates = {}
        cogidx = 1
        for i in range(2, len(data), 2):
            words = dict(zip(header, data[i]))
            cognates = dict(zip(header, data[i+1]))
            concept = data[i][0]
            for language in languages:
                entry = words.get(language).strip()
                cog = cognates.get(language).strip()
                if entry.replace('#', '').strip():
                    if concept+'-'+cog not in cognates:
                        cognates[concept+'-'+cog] = cogidx
                        cogidx += 1
                    cogid = cognates[concept+'-'+cog]
                    for lex in args.writer.add_forms_from_value(
                            Language_ID=language,
                            Parameter_ID=concepts[concept],
                            Value=entry,
                            Source=sources[language],
                            Cognacy=cogid
                            ):
                        args.writer.add_cognate(
                                lexeme=lex,
                                Cognateset_ID=cogid,
                                Source="Sidwell2021"
                                )

