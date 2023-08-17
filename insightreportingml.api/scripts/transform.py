from . import extractkeywords


def transform(data: dict):
    eios_data_list = []

    json_results_arr = data["result"]
    total_items_fetched = len(json_results_arr)
    if total_items_fetched > 0:
        for index, item in enumerate(json_results_arr):
            ReportDate = item['pubDate']
            Title = item['title']
            ISO_Language = item['languageCode']
            psn_arr = [x for x in item['triggers'] if 'PHT' in x['key']]

            Preferred_scientific_name = ';'.join([item['key'][2:item['key'].rfind(
                '-PHT')] for item in psn_arr if item['key'].startswith('l:') and item['key'].endswith('-PHT')])

            desc = item['description'] if item['description'] else ""
            desc_tran = item['translatedDescription'] if item['translatedDescription'] else ""
            abs_sumry = item['abstractiveSummary'] if item['abstractiveSummary'] else ""
            trgrs = sorted(set([value for item in item['triggers']
                           for value in item['values']]))
            trgrs = ' '.join(trgrs)
            locations = item['locations']
            area = locations[0]['areaFullName'] if locations else ""
            area = ' '.join(area) if area else ""

            desc_to_use_for_kwds = abs_sumry if abs_sumry else desc_tran
            desc_to_use_for_kwds = desc_to_use_for_kwds if desc_to_use_for_kwds else desc
            Merged_Texts = ', '.join([desc_to_use_for_kwds, area])

            ment_org = item.get('mentionedOrganisations', None)
            ent_trgrs = [
                org["triggers"][0]["trigger"]
                for org in (ment_org if ment_org else [])
                if org.get("triggers") and len(org["triggers"]) > 0
            ]
            Entities = ', '.join(ent_trgrs)

            loc = item.get("locations")
            geo_data = loc[0].get("geoData") if loc else None
            lat, lon = (geo_data["latitude"], geo_data["longitude"]) if geo_data else (
                None, None)
            GeoRss_Point = "1" if lat and lon else "0"

            Results = item['link']
            Website = item['source']['url']
            Guid = item['rssItemId']

            src = item.get("source", {})
            source_keys = ["id", "name", "country",
                           "region", "language", "subject"]
            Source, Source_Name, Source_Country, Source_Region, Source_Language, Source_Subject = (
                ("" if value is None else value) for value in (src.get(key) for key in source_keys)
            )

            eios_data_dict = {
                "ItemUniqueID": Guid,
                "Title": Title,
                "ItemLink": Results,
                "PublishedDate": ReportDate,
                "ISOLanguageCode": ISO_Language,
                "GeoRss_Point": GeoRss_Point,
                "SourceURL": Website,
                "SourceId": Source,
                "SourceName": Source_Name,
                "SourceCountry": Source_Country,
                "SourceRegion": Source_Region,
                "SourceLanguage": Source_Language,
                "SourceSubject": Source_Subject,
                "ScientificName": Preferred_scientific_name,
                "Keywords": extractkeywords.extract_keywords(Merged_Texts)
            }

            eios_data_list.append(eios_data_dict)

    return eios_data_list
