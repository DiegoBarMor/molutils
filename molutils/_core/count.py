from pathlib import Path

# //////////////////////////////////////////////////////////////////////////////
class Count:
    # --------------------------------------------------------------------------
    @classmethod
    def models(cls, path_pdb: Path) -> int:
        data = path_pdb.read_text()
        return max(1, cls._count_substring('\n'+data, "\nMODEL"))


    # --------------------------------------------------------------------------
    @staticmethod
    def _count_substring(string: str, substring: str) -> int:
        """Counts the number of occurrences of `substring` in `string`."""
        replaced = string.replace(substring, "")
        return (len(string) - len(replaced)) // len(substring)


# //////////////////////////////////////////////////////////////////////////////
