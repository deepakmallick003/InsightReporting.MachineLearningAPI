import unittest

from scripts import predictor

class TestTransformData(unittest.TestCase):
    def test_prediction(self):
        pred = predictor.predictor

        title = 'Newly Discovered Protein in Fungus Bypasses Plant Defenses'
        iso = 'en'
        pref_sci_name = 'SclerotiniaSclerotiorum'
        geo_rss = '46.72928 -117.17326'
        keywords = 'newly discovered protein,overcome plant defenses,agricultural research service,protein in fungus,washington state university,wuhan polytechnic university,bypasses plant defenses,huazhong agricultural university,white mold stem,pgip,sclerotinia sclerotiorum fungus'
        src_name = 'Global Plant Protection'
        src_country = 'USA'
        src_region = 'North America'
        src_subject = 'Medical'

        raw_input_list = [title, iso, pref_sci_name, geo_rss,
                          src_name, src_country, src_region, src_subject]

        score = pred.predict(raw_input_list, keywords, 1, 2)

        self.assertGreater(score, 50)


if __name__ == '__main__':
    unittest.main()
