from pathlib import Path

# //////////////////////////////////////////////////////////////////////////////
class ParserPDB:
    LENGTH_RECORD = 80
    IDX_CHAIN_ID = 21

    # --------------------------------------------------------------------------
    def __init__(self, data_pdb: str):
        self.data = data_pdb.splitlines()


    # --------------------------------------------------------------------------
    @classmethod
    def from_file(cls, path_pdb: Path):
        return cls(path_pdb.read_text())


    # --------------------------------------------------------------------------
    @classmethod
    def join_lines(cls, lines: list[str]) -> str:
        return '\n'.join(lines) + "\nEND"


    # --------------------------------------------------------------------------
    def iter_atoms(self):
        return (
            line for line in self.data
            if line.startswith("ATOM") or line.startswith("HETATM")
        )


    # --------------------------------------------------------------------------
    @classmethod
    def safe_next(cls, gen):
        try: return next(gen)
        except StopIteration: raise ValueError(f"No ATOM records found in PDB file")


    # --------------------------------------------------------------------------
    @classmethod
    def get_chainid(cls, line: str) -> str:
        try: return line[cls.IDX_CHAIN_ID]
        except IndexError: raise ValueError(f"Unexpected format of ATOM records in PDB file")


# //////////////////////////////////////////////////////////////////////////////
