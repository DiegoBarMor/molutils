from pathlib import Path

import molutils as mu

# //////////////////////////////////////////////////////////////////////////////
class List(mu.AppSubcommand):
    # -------------------------------------------------------------------------- UI SECTION
    def run(self):
        command = self.main.subcommands.pop(0)

        if command == "chains": return self.app_list_chains()
        if command == "resids": return self.app_list_resids()

        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def app_list_chains(self):
        path_in = self.main.get_arg_path("path_in")
        first_only = self.main.get_arg_bool("first_only")
        self.main.assert_file_in(path_in)
        print(*mu.List.chains(path_in, first_only))


    # --------------------------------------------------------------------------
    def app_list_resids(self):
        path_in = self.main.get_arg_path("path_in")
        self.main.assert_file_in(path_in)
        print(*mu.List.resids(path_in))


    # -------------------------------------------------------------------------- LOGIC SECTION
    @classmethod
    def chains(cls, path_pdb: Path, first_only: bool = False) -> list[str]:
        pdb = mu.ParserPDB.from_file(path_pdb)
        gen_chain_ids = (mu.ParserPDB.get_chainid(line) for line in pdb.iter_atoms())
        if first_only: return mu.ParserPDB.safe_next(gen_chain_ids)
        return sorted(set(gen_chain_ids))


    # --------------------------------------------------------------------------
    @classmethod
    def resids(cls, path_pdb: Path) -> list[str]:
        """Returns list of unique residue identifiers in the format "chainid.resid"."""
        pdb = mu.ParserPDB.from_file(path_pdb)
        gen_resids = (
            f"{mu.ParserPDB.get_chainid(line)}.{mu.ParserPDB.get_resid(line)}"
            for line in pdb.iter_atoms()
        )
        return sorted(set(gen_resids))


# //////////////////////////////////////////////////////////////////////////////
