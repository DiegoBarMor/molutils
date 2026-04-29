from pathlib import Path

import molutils as mu

import freyacli as fy


# //////////////////////////////////////////////////////////////////////////////
class AppMain(fy.App):
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


    # --------------------------------------------------------------------------
    def run(self):
        command = self.subcommands.pop(0)
        if command == "list"   : return mu.List(self).run()
        if command == "count"  : return mu.Count(self).run()
        if command == "extract": return mu.Extract(self).run()
        if command == "select" : return self._run_select()
        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def _run_select(self):
        query = self.get_arg_str("query")
        path_in = self.get_arg_path("path_in")
        path_out = self.get_arg_path("path_out")
        self.assert_file_in(path_in)

        import MDAnalysis as mda
        mda.Universe(path_in).select_atoms(query).write(path_out)


# //////////////////////////////////////////////////////////////////////////////
