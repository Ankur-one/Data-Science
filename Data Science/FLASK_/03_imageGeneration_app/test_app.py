import importlib.util
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


def load_app_module():
    app_path = Path(__file__).resolve().parent / "app.py"
    spec = importlib.util.spec_from_file_location("image_app", app_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ImageGenerationAppTests(unittest.TestCase):
    def test_generate_image_reports_missing_api_key(self):
        module = load_app_module()

        with patch.object(module, "get_openai_api_key", return_value=None):
            image_path, error = module.generate_image("a blue sky with clouds")

        self.assertIsNone(image_path)
        self.assertIn("OpenAI API key", error)

    def test_generate_image_downloads_from_url_response(self):
        module = load_app_module()
        image_item = Mock()
        image_item.b64_json = None
        image_item.url = "https://example.com/image.png"
        response = Mock(data=[image_item])

        with patch.object(module, "get_openai_api_key", return_value="fake-key"), \
             patch.object(module, "OpenAI") as openai_client_cls, \
             patch.object(module, "urlopen") as mock_urlopen:
            openai_client_cls.return_value.images.generate.return_value = response
            mock_urlopen.return_value.__enter__.return_value.read.return_value = b"fake-image"

            image_path, error = module.generate_image("a blue sky with clouds")

        self.assertIsNone(error)
        self.assertEqual(image_path, "static/generated_image.png")
        self.assertTrue(Path(image_path).exists())
        self.assertEqual(Path(image_path).read_bytes(), b"fake-image")


if __name__ == "__main__":
    unittest.main()
