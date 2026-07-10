from pathlib import Path

import molsimple as ms
import freyacli as fy
import molutils as mu

# //////////////////////////////////////////////////////////////////////////////
class List(mu.AppSubcommand):
    # -------------------------------------------------------------------------- UI SECTION
    def run(self):
        command = self.main.subcommands.pop(0)

        if command == "chains": return self.app_list_chains()
        if command == "residues": return self.app_list_residues()

        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def app_list_chains(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        print(*mu.List.chains(ms.System.read_pdb(path_in), do_sort = True))


    # --------------------------------------------------------------------------
    def app_list_residues(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        print(*mu.List.residues(ms.System.read_pdb(path_in), do_sort = True))


    # -------------------------------------------------------------------------- LOGIC SECTION
    @classmethod
    def chains(cls, system: ms.System, do_sort: bool = True) -> list[str]:
        unique_chains = set(system.particles.get_chainids())
        if do_sort: return sorted(unique_chains)
        return list(unique_chains)


    # --------------------------------------------------------------------------
    @classmethod
    def residues(cls, system: ms.System, do_sort: bool = True) -> list[str]:
        """Returns a list of unique residue identifiers in the format "chainid.resid"."""
        unique_residues = set(part.get_chain_resid().get_dotstr() for part in system)
        if do_sort: return sorted(unique_residues)
        return list(unique_residues)


# //////////////////////////////////////////////////////////////////////////////
