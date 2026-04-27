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


# //////////////////////////////////////////////////////////////////////////////
