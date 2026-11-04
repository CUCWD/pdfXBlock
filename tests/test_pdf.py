"""Exercise PDF rendering, editing, and completion against Ulmo's XBlock."""
import json
import os
import unittest
from unittest.mock import Mock, call

import django
from webob import Request
from xblock.field_data import DictFieldData
from xblock.fields import ScopeIds
from xblock.runtime import NullI18nService

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
django.setup()

from pdf.pdf import PdfBlock  # noqa: E402


class PdfBlockTests(unittest.TestCase):
    """Use real templates and XBlock fields with a minimal runtime double."""

    def setUp(self):
        self.runtime = Mock()
        self.runtime.service.side_effect = lambda _block, name: NullI18nService() if name == 'i18n' else None
        self.block = PdfBlock(
            self.runtime,
            DictFieldData({
                'display_name': 'Example PDF',
                'url': 'https://example.org/lesson.pdf',
                'source_url': 'https://example.org/source.pptx',
                'source_text': 'Slides',
            }),
            ScopeIds('learner', 'pdf', 'definition', 'usage'),
        )

    @staticmethod
    def post(data):
        """Create the JSON request accepted by XBlock handlers."""
        return Request.blank('/', method='POST', content_type='application/json', body=json.dumps(data).encode())

    def test_student_view_uses_bundled_templates_and_javascript(self):
        fragment = self.block.student_view()
        self.assertIn('https://example.org/lesson.pdf', fragment.content)
        self.assertIn('Slides', fragment.content)
        self.assertEqual(fragment.js_init_fn, 'pdfXBlockInitView')
        self.assertEqual(fragment.json_init_args['completionDelayMs'], 5000)
        self.assertTrue(any('pdfXBlockInitView' in resource.data for resource in fragment.resources))
        self.runtime.publish.assert_called_once_with(self.block, 'edx.pdf.loaded', {
            'url': self.block.url,
            'source_url': self.block.source_url,
        })

    def test_download_controls_follow_block_fields(self):
        self.block.allow_download = False
        self.block.source_url = ''
        fragment = self.block.student_view()
        self.assertNotIn('pdf-download-button', fragment.content)
        self.assertIn('application/pdf', fragment.content)

    def test_studio_view_uses_bundled_template_and_javascript(self):
        fragment = self.block.studio_view()
        self.assertIn('pdf_edit_display_name', fragment.content)
        self.assertIn('Example PDF', fragment.content)
        self.assertEqual(fragment.js_init_fn, 'pdfXBlockInitEdit')
        self.assertTrue(any('pdfXBlockInitEdit' in resource.data for resource in fragment.resources))

    def test_save_pdf_updates_fields(self):
        data = {
            'display_name': 'Updated PDF',
            'url': 'https://example.org/updated.pdf',
            'completion_condition': 'last_page',
            'allow_download': 'False',
            'source_text': 'Updated source',
            'source_url': 'https://example.org/updated.pptx',
        }
        response = self.block.save_pdf(self.post(data))
        self.assertEqual(response.json, {'result': 'success'})
        self.assertFalse(self.block.allow_download)
        for name in ('display_name', 'url', 'completion_condition', 'source_text', 'source_url'):
            self.assertEqual(getattr(self.block, name), data[name])

    def test_completion_is_published_only_once(self):
        first = self.block.mark_completed(self.post({}))
        second = self.block.mark_completed(self.post({}))
        self.assertEqual(first.json, {'completed': True})
        self.assertEqual(second.json, {'completed': True})
        self.assertTrue(self.block.is_completed)
        self.assertEqual(self.runtime.publish.call_args_list, [
            call(self.block, 'completion', {'completion': 1.0}),
            call(self.block, 'edx.pdf.completed', {
                'url': self.block.url,
                'source_url': self.block.source_url,
            }),
        ])

    def test_download_tracking(self):
        self.block.on_download(self.post({}))
        self.runtime.publish.assert_called_once_with(self.block, 'edx.pdf.downloaded', {
            'url': self.block.url,
            'source_url': self.block.source_url,
        })
