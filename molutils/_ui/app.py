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
        if command == "list"   : return self._run_list()
        if command == "count"  : return self._run_count()
        if command == "extract": return self._run_extract()
        if command == "select" : return self._run_select()
        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def _run_list(self):
        def list_chains():
            path_in = self.get_arg_path("path_in")
            first_only = self.get_arg_bool("first_only")
            self.assert_file_in(path_in)
            print(*mu.List.chains(path_in, first_only))

        command = self.subcommands.pop(0)

        if command == "chains": return list_chains()

        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def _run_count(self):
        def count_models():
            path_in = self.get_arg_path("path_in")
            self.assert_file_in(path_in)
            print(mu.Count.models(path_in))


        command = self.subcommands.pop(0)

        if command == "models": return count_models()

        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def _run_extract(self):
        def extract_models():
            path_in = self.get_arg_path("path_in")
            self.assert_file_in(path_in)

            folder_out = self.get_arg_path("folder_out", default = path_in.parent)
            self.assert_dir_out(folder_out)

            data_pdb = path_in.read_text()

            if self.get_arg_bool("first_only"):
                _, model = mu.Extract.next_model(data_pdb)
                path_out = folder_out / f"{path_in.stem}.m0.pdb"
                path_out.write_text(model)
                return

            for i, model in enumerate(mu.Extract.iter_models(data_pdb)):
                path_out = folder_out / f"{path_in.stem}.m{i:03}.pdb"
                path_out.write_text(model)

        def extract_chains():
            path_in = self.get_arg_path("path_in")
            self.assert_file_in(path_in)

            folder_out = self.get_arg_path("folder_out", default = path_in.parent)
            self.assert_dir_out(folder_out)

            data_pdb = path_in.read_text()

            chains = mu.Extract.split_chains(data_pdb)

            chain_ids = mu.List.chains(path_in, first_only = True) \
                if self.get_arg_bool("first_only") else chains.keys()

            for chain_id in chain_ids:
                path_out = folder_out / f"{path_in.stem}.{chain_id}.pdb"
                path_out.write_text(chains[chain_id])


        command = self.subcommands.pop(0)

        if command == "models": return extract_models()
        if command == "chains": return extract_chains()

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
