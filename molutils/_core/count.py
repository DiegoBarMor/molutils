from pathlib import Path

import freyacli as fy
import molutils as mu

# //////////////////////////////////////////////////////////////////////////////
class Count(mu.AppSubcommand):
    # -------------------------------------------------------------------------- UI SECTION
    def run(self):
        command = self.main.subcommands.pop(0)

        if command == "models": return self.app_count_models()

        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def app_count_models(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        print(mu.Count.models(path_in))


    # -------------------------------------------------------------------------- LOGIC SECTION
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
