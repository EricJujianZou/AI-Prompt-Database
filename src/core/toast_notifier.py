"""Windows Toast Notification Handler - Provides non-intrusive toast notifications for prompt generation feedback."""
import logging

logger = logging.getLogger(__name__)

try:
    from winotify import Notification
    TOAST_AVAILABLE = True
except ImportError:
    logger.warning("winotify not available. Toast notifications will be disabled.")
    TOAST_AVAILABLE = False

class PromptToastNotifier:
    """Handles Windows toast notifications for prompt generation."""
    
    def __init__(self):
        self.current_toast = None
        
    def show_generating_toast(self):
        if not TOAST_AVAILABLE:
            return
        try:
            toast = Notification(app_id="PromptAssist", title="PromptAssist", msg=" Generating prompt...", duration="short")
            toast.show()
            logger.debug("Showed generating toast")
        except Exception as e:
            logger.error(f"Error showing generating toast: {e}")
    
    def show_success_toast(self, message=" Prompt ready! Press Ctrl+V to paste."):
        if not TOAST_AVAILABLE:
            return
        try:
            toast = Notification(app_id="PromptAssist", title="PromptAssist", msg=message, duration="short")
            toast.show()
            logger.debug(f"Showed success toast")
        except Exception as e:
            logger.error(f"Error showing success toast: {e}")
    
    def show_error_toast(self, message=" Prompt generation failed. Contact support."):
        if not TOAST_AVAILABLE:
            return
        try:
            toast = Notification(app_id="PromptAssist", title="PromptAssist Error", msg=message, duration="long")
            toast.show()
            logger.debug(f"Showed error toast")
        except Exception as e:
            logger.error(f"Error showing error toast: {e}")
    
    def cleanup(self):
        self.current_toast = None
