import unittest
import json  
import pytest

from scripts import transform 

class TestTransformData(unittest.TestCase):
    def test_empty_json(self):
        result = transform.transform(json.loads('{}'), 1, 2)
        self.assertEqual(result,[])
    def test_empty_item_json(self):
        with pytest.raises(Exception) as exc_info:
            result = transform.transform(json.loads('{"result":[{}]}'), 1, 2)
        assert str(exc_info.value) == "'title'"

if __name__=='__main__':
	unittest.main()