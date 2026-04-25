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


    # --------------------------------------------------------------------------
    def run(self):
        command = self.subcommands.pop(0)
        if command == "count": return self._run_count()
        if command == "extract": return self._run_extract()
        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def _run_count(self):
        def count_models():
            path_pdb = self.get_arg_path("path_pdb")
            self.assert_file_in(path_pdb)
            print(mu.Count.models(path_pdb))


        command = self.subcommands.pop(0)

        if command == "models": return count_models()

        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def _run_extract(self):
        def extract_models():
            path_pdb = self.get_arg_path("path_pdb")
            self.assert_file_in(path_pdb)

            folder_out = self.get_arg_path("folder_out", default = path_pdb.parent)
            self.assert_dir_out(folder_out)

            data_pdb = path_pdb.read_text()

            if self.get_arg_bool("first_only"):
                _, model = mu.Extract.next_model(data_pdb)
                path_out = folder_out / f"{path_pdb.stem}.m0.pdb"
                path_out.write_text(model)
                return

            for i, model in enumerate(mu.Extract.iter_models(data_pdb)):
                path_out = folder_out / f"{path_pdb.stem}.m{i:03}.pdb"
                path_out.write_text(model)


        command = self.subcommands.pop(0)

        if command == "models": return extract_models()

        raise ValueError(f"Unknown command: {command}")


# //////////////////////////////////////////////////////////////////////////////
