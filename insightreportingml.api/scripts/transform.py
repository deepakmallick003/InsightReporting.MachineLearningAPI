from . import extractkeywords
from . import predictor
import re
from .translation_utils import translate_to_english

list_type_seperator = ';'

def get_Preferred_scientific_name(psn_arr, space=False):
    if space == True:
        return list_type_seperator.join(
            re.sub(r'([a-z])([A-Z])', lambda m: m.group(1) + ' ' +
                   m.group(2), item['key'][2:item['key'].rfind('-PHT')])
            for item in psn_arr if item['key'].startswith('l:') and item['key'].endswith('-PHT')
        )
    else:
        return list_type_seperator.join([item['key'][2:item['key'].rfind(
            '-PHT')] for item in psn_arr if item['key'].startswith('l:') and item['key'].endswith('-PHT')])


def transform(data: dict, rfc_model_version: int, lr_model_version: int):
    eios_data_list = []

    if 'result' in data:
        json_results_arr = data["result"]
        if len(json_results_arr) > 0:
            for index, item in enumerate(json_results_arr):
                ReportDate = item['pubDate'] if 'pubDate' in item else ''
                Title = item['title']
                ISO_Language = item['languageCode']
                Language_Name = item['language']
                psn_arr = [x for x in item['triggers'] if 'PHT' in x['key']]

                desc = item['description'] if item['description'] else ""
                desc_tran = item['translatedDescription'] if item['translatedDescription'] else ""
                abs_sumry = item['abstractiveSummary'] if item['abstractiveSummary'] else ""

                locations = item['locations']
                area = locations[0]['areaFullName'] if locations else ""
                area = ' '.join(area) if area else ""

                desc_to_use_for_kwds = abs_sumry if abs_sumry else desc_tran
                desc_to_use_for_kwds = desc_to_use_for_kwds if desc_to_use_for_kwds else desc
                Merged_Texts = ', '.join([desc_to_use_for_kwds, area])

                loc = item.get("locations")
                geo_data = loc[0].get("geoData") if loc else None
                lat, lon = (geo_data["latitude"], geo_data["longitude"]) if geo_data else (
                    None, None)
                GeoRss_Point = "1" if lat and lon else "0"

                Results = item['link']
                Website = item['source']['url']
                RssItemId = item['rssItemId']
                EIOSItemId = item['id']

                src = item.get("source", {})
                source_keys = ["id", "name", "country",
                               "region", "language", "subject", "type"]

                Source, Source_Name, Source_Country, Source_Region, Source_Language, Source_Subject, Source_Type = (
                    ("" if value is None else value) for value in (src.get(key) for key in source_keys)
                )

                Categories = list_type_seperator.join(
                    tag["label"] for tag in item.get("tags", []) if tag.get("folders"))
                
                MentionedCountries = list_type_seperator.join(
                    country["label"] for country in item.get("affectedCountries", []))

                trgr_seen = set()
                trgrs = list_type_seperator.join([value.lower() for trigger in item['triggers'] for value in trigger['values'] if value.lower(
                ) not in (trgr_seen := trgr_seen or set()) and not trgr_seen.add(value.lower())])
                keywords = extractkeywords.extract_keywords(Merged_Texts)
                Merged_Keywords_Triggers = list_type_seperator.join(
                    filter(None, [trgrs, keywords]))
                Score = 0
                # Score = predictor.predictor.predict([Title, ISO_Language, get_Preferred_scientific_name(psn_arr, False), GeoRss_Point,
                #                                      Source_Name, Source_Country, Source_Region, Source_Subject],
                #                                   Merged_Keywords_Triggers, rfc_model_version, lr_model_version)
                eios_data_dict = {
                    "ItemUniqueID": RssItemId,
                    "EIOSItemID": EIOSItemId,
                    "Title": Title,
                    "ItemLink": Results,
                    "PublishedDate": ReportDate,
                    "ISOLanguageCode": ISO_Language,
                    "Language_Name": Language_Name,
                    "GeoRss_Point": GeoRss_Point,
                    "SourceURL": Website,
                    "SourceId": Source,
                    "SourceName": Source_Name,
                    "SourceCountry": Source_Country,
                    "SourceRegion": Source_Region,
                    "SourceLanguage": Source_Language,
                    "SourceSubject": Source_Subject,
                    "SourceType": Source_Type,
                    "ScientificName": get_Preferred_scientific_name(psn_arr, True),
                    "Categories": Categories,
                    "MentionedCountries": MentionedCountries,
                    "Keywords": Merged_Keywords_Triggers,
                    "Accuracy": Score,
                    "RFCModelVersionID": rfc_model_version,
                    "LRModelVersionID": lr_model_version,
                }

                eios_data_list.append(eios_data_dict)

    return eios_data_list
