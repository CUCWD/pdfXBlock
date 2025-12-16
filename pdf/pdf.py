""" pdfXBlock main Python class"""

import pkg_resources
from django.conf import settings
from django.template import Context, Template

from xblock.completable import XBlockCompletionMode
from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from xblockutils.settings import XBlockWithSettingsMixin, ThemableXBlockMixin
from xblock.scorable import ScorableXBlockMixin, Score
from .utils import _, DummyTranslationService

loader = ResourceLoader(__name__)

@XBlock.wants('settings')
@XBlock.needs('i18n')
class PdfBlock(
    ScorableXBlockMixin,
    XBlock,
    XBlockWithSettingsMixin,
    ThemableXBlockMixin
):
    COMPLETION_CONDITION_VIEWING_DELAY = "viewing_delay"   # After N seconds visible
    COMPLETION_CONDITION_LAST_PAGE = "last_page"
    COMPLETION_CONDITION_SCROLL_BOTTOM = "scroll_bottom"
    
    # The pdf block is responsible for declaring when it is completed.
    completion_mode = XBlockCompletionMode.COMPLETABLE

    # User state field to track completion and avoid re-firing completion events.
    is_completed = Boolean(default=False, scope=Scope.user_state)

    # Default viewing delay for completion, in milliseconds.
    # Can be overridden by Django setting COMPLETION_BY_VIEWING_DELAY_MS
    viewing_delay_ms = getattr(settings, "COMPLETION_BY_VIEWING_DELAY_MS", 5000)

    '''
    Icon of the XBlock. Values : [other (default), video, problem]
    '''
    icon_class = "other"

    '''
    Fields
    '''
    display_name = String(
        display_name=_("Display Name"),
        default=_("PDF"),
        scope=Scope.settings,
        help=_("This name appears in the horizontal navigation at the top of the page.")
    )

    url = String(
        display_name=_("PDF URL"),
        default=_("http://tutorial.math.lamar.edu/pdf/Trig_Cheat_Sheet.pdf"),
        scope=Scope.content,
        help=_("The URL for your PDF.")
    )

    completion_condition = String(
        display_name=_("Completion Condition"),
        scope=Scope.settings,
        default=COMPLETION_CONDITION_VIEWING_DELAY,
        values=[
            COMPLETION_CONDITION_VIEWING_DELAY,
            COMPLETION_CONDITION_LAST_PAGE,
            COMPLETION_CONDITION_SCROLL_BOTTOM,
        ],
        help=_(
            "How this PDF unit is marked complete: "
            "After viewing for ${viewing_delay_seconds} delay, when last page is viewed, or when scrolled to bottom."
        ),
    )
    viewing_delay_seconds = String(
        display_name=_("Viewing Delay (seconds)"),
        default=getattr(settings, "COMPLETION_BY_VIEWING_DELAY_MS", 5000) // 1000,
        scope=Scope.settings,
        help=_("Time in seconds before the PDF is marked as viewed for completion.")
    )

    allow_download = Boolean(
        display_name=_("PDF Download Allowed"),
        default=True,
        scope=Scope.content,
        help=_("Display a download button for this PDF.")
    )

    source_text = String(
        display_name=_("Source document button text"),
        default="",
        scope=Scope.content,
        help=_(
            "Add a download link for the source file of your PDF. "
             "Use it for example to provide the PowerPoint file used to create this PDF."
        )
    )

    source_url = String(
        display_name=_("Source document URL"),
        default="",
        scope=Scope.content,
        help=_(
            "Add a download link for the source file of your PDF. "
             "Use it for example to provide the PowerPoint file used to create this PDF."
        )
    )

    '''
    Util functions
    '''
    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)
        return resource_content.decode("utf8")

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))

    '''
    Main functions
    '''
    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'completion_condition': self.completion_condition,
            'viewing_delay_seconds': self.viewing_delay_seconds,
            'allow_download': self.allow_download,
            'source_text': self.source_text,
            'source_url': self.source_url,
            '_i18n_service': self.i18n_service
        }
        html = loader.render_django_template(
            'templates/html/pdf_view.html',
            context=context,
            i18n_service=self.i18n_service,
        )

        event_type = 'edx.pdf.loaded'
        event_data = {
            'url': self.url,
            'source_url': self.source_url,
        }
        self.runtime.publish(self, event_type, event_data)
        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/pdf_view.js"))
        frag.initialize_js('pdfXBlockInitView', {
            "completionCondition": self.completion_condition,
            "completionDelayMs": self.viewing_delay_ms,
        })
        return frag

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        context = {
            'display_name': self.display_name,
            'name_help': _("This name appears in the horizontal navigation at the top of the page."),
            'url': self.url,
            'completion_condition': self.completion_condition,
            'viewing_delay_seconds': self.viewing_delay_ms // 1000,
            'allow_download': self.allow_download,
            'source_text': self.source_text,
            'source_url': self.source_url
        }
        html = loader.render_django_template(
            'templates/html/pdf_edit.html',
            context=context,
            i18n_service=self.i18n_service,
        )
        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/pdf_edit.js"))
        frag.initialize_js('pdfXBlockInitEdit', {
            "completionCondition": self.completion_condition,
            "completionDelayMs": self.viewing_delay_ms,
        })
        return frag

    @XBlock.json_handler
    def on_download(self, data, suffix=''):
        """
        The download file event handler
        """
        event_type = 'edx.pdf.downloaded'
        event_data = {
            'url': self.url,
            'source_url': self.source_url,
        }
        self.runtime.publish(self, event_type, event_data)

    @XBlock.json_handler
    def save_pdf(self, data, suffix=''):
        """
        The saving handler.
        """
        self.display_name = data['display_name']
        self.url = data['url']
        self.completion_condition = data['completion_condition']
        self.allow_download = True if data['allow_download'] == "True" else False  # Str to Bool translation
        self.source_text = data['source_text']
        self.source_url = data['source_url']

        return {
            'result': 'success',
        }

    @property
    def i18n_service(self):
        """ Obtains translation service """
        i18n_service = self.runtime.service(self, "i18n")
        if i18n_service:
            return i18n_service
        else:
            return DummyTranslationService()
        
    @XBlock.json_handler
    def mark_completed(self, data, suffix=""):
        """
        Called by the frontend when the learner has met completion criteria.
        """
        if self.is_completed:
            return {"completed": True}

        self.is_completed = True

        # Publish completion for the runtime to record in completion storage.
        # 1.0 = 100% complete.
        self.runtime.publish(self, "completion", {"completion": 1.0})

        # Log a tracking event for analytics symmetry with edx.pdf.loaded.
        event_type = 'edx.pdf.completed'
        event_data = {
            'url': self.url,
            'source_url': self.source_url,
        }
        self.runtime.publish(self, event_type, event_data)

        return {"completed": True}
