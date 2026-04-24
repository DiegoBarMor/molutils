from pathlib import Path

import molutils as mu

import freyacli as fy


# //////////////////////////////////////////////////////////////////////////////
class App(fy.App):
    _APP_NAME = "molutils"
    _VERSION = mu.__version__

    # --------------------------------------------------------------------------
    def __init__(self,  argv: list[str]):
        dir_ui = Path(__file__).parent
        super().__init__(
            args = argv,
            path_fyr = dir_ui / "fy_rules.fyr",
            path_fyh = dir_ui / "fy_help.fyh",
        )
        self.subcommands = self.get_path_to_root()
        # command = self.subcommands.pop(0)


    # --------------------------------------------------------------------------
    def run(self):
        ...


# //////////////////////////////////////////////////////////////////////////////
