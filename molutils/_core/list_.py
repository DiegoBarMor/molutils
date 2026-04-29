from pathlib import Path

import molutils as mu

# //////////////////////////////////////////////////////////////////////////////
class List:
    # --------------------------------------------------------------------------
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
