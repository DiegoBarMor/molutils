from collections import defaultdict

import molutils as mu

# //////////////////////////////////////////////////////////////////////////////
class Extract:
    # --------------------------------------------------------------------------
    @classmethod
    def next_model(cls, data: str, start: int = 0) -> tuple[int, str]:
        idx_0 = data.find("\nMODEL", start)
        if idx_0 == -1: return -1, data

        idx_1 = data.find("\nENDMDL", idx_0)
        if idx_1 == -1: return -1, data[idx_0:]

        idx_1 += len("\nENDMDL")
        return idx_1, data[idx_0:idx_1] + "\nEND"


    # --------------------------------------------------------------------------
    @classmethod
    def iter_models(cls, data: str):
        while data:
            idx, model = cls.next_model(data)
            yield model
            if idx == -1: break
            data = data[idx:]


    # --------------------------------------------------------------------------
    @classmethod
    def split_chains(cls, data: str) -> dict[str, str]:
        pdb = mu.ParserPDB(data)
        chains = defaultdict(list)
        for line in pdb.iter_atoms():
            chain_id = mu.ParserPDB.get_chainid(line)
            chains[chain_id].append(line)
        return {
            chain_id: mu.ParserPDB.join_lines(lines)
            for chain_id, lines in chains.items()
        }


# //////////////////////////////////////////////////////////////////////////////
