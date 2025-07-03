import click
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import MODULES_ENABLED, DEFAULT_LANG, SUPPORTED_LANGS, APP_VERSION
from core.localization import get_translator
from core.utils import get_logger
from core.module_manager import module_manager

logger = get_logger(__name__)

@click.group()
def cli():
    """VoxUnity AI+ Command Line Interface."""
    pass

@cli.command()
@click.option('--lang', type=click.Choice(SUPPORTED_LANGS), default=DEFAULT_LANG, help="Set display language.")
def version(lang):
    """Show the application version."""
    _ = get_translator(lang)
    click.echo(f"{_('VoxUnity AI+ Version')}: {APP_VERSION}")

# --- Módulos CLI ---

if MODULES_ENABLED.get("mod-voice"):
    @cli.group()
    def voice():
        """Voice modulation commands."""
        pass

    @voice.command()
    @click.option('--preset', default="standard", help="Preset name for voice modulation.")
    @click.pass_context
    def start(ctx, preset):
        """Start voice modulation."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-voice")
        if module:
            module.start(preset=preset)
            logger.info(_("Voice module started with preset: %s"), preset)
        else:
            logger.error(_("Voice module is not available or enabled."))

    @voice.command()
    @click.pass_context
    def stop(ctx):
        """Stop voice modulation."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-voice")
        if module:
            module.stop()
            logger.info(_("Voice module stopped."))
        else:
            logger.error(_("Voice module is not available or enabled."))

if MODULES_ENABLED.get("mod-streaming"):
    @cli.group()
    def streaming():
        """Streaming commands."""
        pass

    @streaming.command()
    @click.option('--overlay', default="default", help="Overlay name.")
    @click.pass_context
    def start(ctx, overlay):
        """Start streaming overlays."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-streaming")
        if module:
            module.start(overlay_name=overlay)
            logger.info(_("Streaming module started with overlay: %s"), overlay)
        else:
            logger.error(_("Streaming module is not available or enabled."))

    @streaming.command()
    @click.pass_context
    def stop(ctx):
        """Stop streaming overlays."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-streaming")
        if module:
            module.stop()
            logger.info(_("Streaming module stopped."))
        else:
            logger.error(_("Streaming module is not available or enabled."))

if MODULES_ENABLED.get("mod-ally"):
    @cli.group()
    def ally():
        """Ally commands."""
        pass

    @ally.command()
    @click.option('--course', default="introduction", help="Course name.")
    @click.pass_context
    def start(ctx, course):
        """Start ally module."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-ally")
        if module:
            module.start(course_name=course)
            logger.info(_("Ally module started with course: %s"), course)
        else:
            logger.error(_("Ally module is not available or enabled."))

    @ally.command()
    @click.pass_context
    def stop(ctx):
        """Stop ally module."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-ally")
        if module:
            module.stop()
            logger.info(_("Ally module stopped."))
        else:
            logger.error(_("Ally module is not available or enabled."))

if MODULES_ENABLED.get("mod-therapy"):
    @cli.group()
    def therapy():
        """Therapy commands."""
        pass

    @therapy.command()
    @click.option('--entry', help="Journal entry to add.")
    @click.pass_context
    def add_entry(ctx, entry):
        """Add a journal entry."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-therapy")
        if module:
            # Asumiendo un user_id para la CLI, en un sistema real vendría de la autenticación
            module.add_journal_entry(user_id=1, content=entry)
            logger.info(_("Therapy journal entry added."))
        else:
            logger.error(_("Therapy module is not available or enabled."))

    @therapy.command()
    @click.pass_context
    def start(ctx):
        """Start therapy module (e.g., for real-time analysis)."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-therapy")
        if module:
            module.start()
            logger.info(_("Therapy module started."))
        else:
            logger.error(_("Therapy module is not available or enabled."))

    @therapy.command()
    @click.pass_context
    def stop(ctx):
        """Stop therapy module."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-therapy")
        if module:
            module.stop()
            logger.info(_("Therapy module stopped."))
        else:
            logger.error(_("Therapy module is not available or enabled."))

if MODULES_ENABLED.get("mod-vtuber"):
    @cli.group()
    def vtuber():
        """VTuber commands."""
        pass

    @vtuber.command()
    @click.option('--model', default="default_live2d.json", help="VTuber model name.")
    @click.pass_context
    def start(ctx, model):
        """Start VTuber module."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-vtuber")
        if module:
            module.start(model_name=model)
            logger.info(_("VTuber module started with model: %s"), model)
        else:
            logger.error(_("VTuber module is not available or enabled."))

    @vtuber.command()
    @click.pass_context
    def stop(ctx):
        """Stop VTuber module."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-vtuber")
        if module:
            module.stop()
            logger.info(_("VTuber module stopped."))
        else:
            logger.error(_("VTuber module is not available or enabled."))

if MODULES_ENABLED.get("mod-activism"):
    @cli.group()
    def activism():
        """Activism commands."""
        pass

    @activism.command()
    @click.option('--file', help="File path to anonymize.")
    @click.pass_context
    def anonymize(ctx, file):
        """Anonymize a file."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-activism")
        if module:
            module.anonymize_file(file)
            logger.info(_("Activism module anonymized file: %s"), file)
        else:
            logger.error(_("Activism module is not available or enabled."))

    @activism.command()
    @click.pass_context
    def start(ctx):
        """Start activism module (e.g., Tor/Matrix setup)."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-activism")
        if module:
            module.start()
            logger.info(_("Activism module started."))
        else:
            logger.error(_("Activism module is not available or enabled."))

    @activism.command()
    @click.pass_context
    def stop(ctx):
        """Stop activism module."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-activism")
        if module:
            module.stop()
            logger.info(_("Activism module stopped."))
        else:
            logger.error(_("Activism module is not available or enabled."))

if MODULES_ENABLED.get("mod-educator"):
    @cli.group()
    def educator():
        """Educator commands."""
        pass

    @educator.command()
    @click.option('--text', help="Text to narrate.")
    @click.pass_context
    def narrate(ctx, text):
        """Generate AI narration from text."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-educator")
        if module:
            module.generate_narration(text)
            logger.info(_("Educator module generated narration."))
        else:
            logger.error(_("Educator module is not available or enabled."))

    @educator.command()
    @click.pass_context
    def start(ctx):
        """Start educator module (e.g., resource management)."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-educator")
        if module:
            module.start()
            logger.info(_("Educator module started."))
        else:
            logger.error(_("Educator module is not available or enabled."))

    @educator.command()
    @click.pass_context
    def stop(ctx):
        """Stop educator module."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-educator")
        if module:
            module.stop()
            logger.info(_("Educator module stopped."))
        else:
            logger.error(_("Educator module is not available or enabled."))

if MODULES_ENABLED.get("mod-mobile"):
    @cli.group()
    def mobile():
        """Mobile commands."""
        pass

    @mobile.command()
    @click.option('--device', help="Mobile device ID or name.")
    @click.pass_context
    def connect(ctx, device):
        """Connect to a mobile device."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-mobile")
        if module:
            module.connect_device(device)
            logger.info(_("Mobile module connected to device: %s"), device)
        else:
            logger.error(_("Mobile module is not available or enabled."))

    @mobile.command()
    @click.pass_context
    def start(ctx):
        """Start mobile module (e.g., TUI)."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-mobile")
        if module:
            module.start()
            logger.info(_("Mobile module started."))
        else:
            logger.error(_("Mobile module is not available or enabled."))

    @mobile.command()
    @click.pass_context
    def stop(ctx):
        """Stop mobile module."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-mobile")
        if module:
            module.stop()
            logger.info(_("Mobile module stopped."))
        else:
            logger.error(_("Mobile module is not available or enabled."))

if MODULES_ENABLED.get("mod-devtools"):
    @cli.group()
    def devtools():
        """Devtools commands."""
        pass

    @devtools.command()
    @click.option('--module', help="Module to run tests for.")
    @click.pass_context
    def run_tests(ctx, module):
        """Run tests for a specific module or all modules."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module_instance = module_manager.get_module("mod-devtools")
        if module_instance:
            module_instance.run_tests(module)
            logger.info(_("Devtools module ran tests for: %s"), module if module else "all modules")
        else:
            logger.error(_("Devtools module is not available or enabled."))

    @devtools.command()
    @click.pass_context
    def start(ctx):
        """Start devtools module (e.g., activate hooks)."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-devtools")
        if module:
            module.start()
            logger.info(_("Devtools module started."))
        else:
            logger.error(_("Devtools module is not available or enabled."))

    @devtools.command()
    @click.pass_context
    def stop(ctx):
        """Stop devtools module."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-devtools")
        if module:
            module.stop()
            logger.info(_("Devtools module stopped."))
        else:
            logger.error(_("Devtools module is not available or enabled."))

if MODULES_ENABLED.get("mod-accessibility"):
    @cli.group()
    def accessibility():
        """Accessibility commands."""
        pass

    @accessibility.command()
    @click.option('--theme', default="light", help="Theme name to apply.")
    @click.pass_context
    def apply_theme(ctx, theme):
        """Apply a visual theme."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-accessibility")
        if module:
            module.apply_theme(theme)
            logger.info(_("Accessibility module applied theme: %s"), theme)
        else:
            logger.error(_("Accessibility module is not available or enabled."))

    @accessibility.command()
    @click.pass_context
    def start(ctx):
        """Start accessibility module (e.g., activate screen reader)."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-accessibility")
        if module:
            module.start()
            logger.info(_("Accessibility module started."))
        else:
            logger.error(_("Accessibility module is not available or enabled."))

    @accessibility.command()
    @click.pass_context
    def stop(ctx):
        """Stop accessibility module."""
        _ = get_translator(ctx.parent.params.get('lang', DEFAULT_LANG))
        module = module_manager.get_module("mod-accessibility")
        if module:
            module.stop()
            logger.info(_("Accessibility module stopped."))
        else:
            logger.error(_("Accessibility module is not available or enabled."))

def main():
    cli()

if __name__ == "__main__":
    main()