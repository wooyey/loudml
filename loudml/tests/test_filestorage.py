import datetime
import logging
import tempfile
import unittest

logging.getLogger('tensorflow').disabled = True

from loudml import (
    errors,
)

from loudml.timeseries import TimeSeriesModel
from loudml.filestorage import FileStorage

FEATURES = [
    {
        'name': 'avg_foo',
        'metric': 'avg',
        'field': 'foo',
        'default': 0,
    },
]

class TestFileStorage(unittest.TestCase):
    def test_create_and_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            storage = FileStorage(tmp)

            # Create
            model = TimeSeriesModel(dict(
                name='test-1',
                offset=30,
                span=300,
                bucket_interval=3,
                interval=60,
                features=FEATURES,
                threshold=30,
            ))
            self.assertEqual(model.type, 'timeseries')
            storage.create_model(model)
            self.assertTrue(storage.model_exists(model.name))

            # Create
            model = TimeSeriesModel(dict(
                name='test-2',
                offset=56,
                span=200,
                bucket_interval=20,
                interval=120,
                features=FEATURES,
                threshold=30,
            ))
            storage.create_model(model)

            # List
            self.assertEqual(storage.list_models(), ["test-1", "test-2"])

            # Delete
            storage.delete_model("test-1")
            self.assertFalse(storage.model_exists("test-1"))
            self.assertEqual(storage.list_models(), ["test-2"])

            with self.assertRaises(errors.ModelNotFound):
                storage.get_model_data("test-1")

            # Rebuild
            model = storage.load_model("test-2")
            self.assertEqual(model.type, 'timeseries')
            self.assertEqual(model.name, 'test-2')
            self.assertEqual(model.offset, 56)
