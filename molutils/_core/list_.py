from pathlib import Path

# //////////////////////////////////////////////////////////////////////////////
class List:
    LENGTH_RECORD = 80
    IDX_CHAIN_ID = 21

    # --------------------------------------------------------------------------
    @classmethod
    def chains(cls, path_pdb: Path, first_only: bool = False) -> list[str]:
        data = '\n' + path_pdb.read_text()
        gen_chain_ids = (cls._get_chainid(line) for line in cls._iter_atoms(data))
        if first_only: return next(gen_chain_ids)
        return sorted(set(gen_chain_ids))


    # --------------------------------------------------------------------------
    @classmethod
    def _iter_atoms(cls, data: str):
        """Guarantees that at least one line is yielded, otherwise raises an error."""
        idx = 0
        yielded = False
        while True:
            idx = 1 + data.find("\nATOM", idx)
            if not idx: break
            yield data[idx:idx+cls.LENGTH_RECORD]
            yielded = True
            idx += cls.LENGTH_RECORD

        if not yielded:
            raise ValueError(f"No ATOM records found in PDB file")


    # --------------------------------------------------------------------------
    @classmethod
    def _get_chainid(cls, line: str) -> str:
        try: return line[cls.IDX_CHAIN_ID]
        except IndexError: raise ValueError(f"Unexpected format of ATOM records in PDB file")


# //////////////////////////////////////////////////////////////////////////////
