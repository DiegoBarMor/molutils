from pathlib import Path

import freyacli as fy
import molutils as mu

# //////////////////////////////////////////////////////////////////////////////
class Count(mu.AppSubcommand):
    # -------------------------------------------------------------------------- UI SECTION
    def run(self):
        command = self.main.subcommands.pop(0)

        if command == "models"  : return self.app_count_models()
        if command == "chains"  : return self.app_count_chains()
        if command == "residues": return self.app_count_residues()
        if command == "frames"  : return self.app_count_frames()

        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def app_count_models(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        print(mu.Count.models(path_in))


    # --------------------------------------------------------------------------
    def app_count_chains(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        print(len(mu.List.chains(path_in, do_sort = False)))


    # --------------------------------------------------------------------------
    def app_count_residues(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        print(len(mu.List.residues(path_in, do_sort = False)))


    # --------------------------------------------------------------------------
    def app_count_frames(self):
        path_struct = self.main.get_arg_path("path_struct", assertion = fy.PathAssertion.FILE_IN)
        path_traj = self.main.get_arg_path("path_traj",
            assertion = fy.PathAssertion.FILE_IN, allow_none = True
        )
        nframes_valid, nframes_expected = mu.Count.frames(path_struct, path_traj)
        print(f"{nframes_valid}/{nframes_expected}")


    # -------------------------------------------------------------------------- LOGIC SECTION
    @classmethod
    def models(cls, path_pdb: Path) -> int:
        data = path_pdb.read_text()
        return max(1, cls._count_substring('\n'+data, "\nMODEL"))


    # --------------------------------------------------------------------------
    @classmethod
    def frames(cls, path_struct: Path, path_traj: Path | None) -> tuple[int, int]:
        import MDAnalysis as mda
        args_traj = [str(path_traj)] if path_traj is not None else []
        u = mda.Universe(str(path_struct), *args_traj)

        nframes_expected = u.trajectory.n_frames
        nframes_valid = sum(1 for _ in u.trajectory)
        return nframes_valid, nframes_expected


    # --------------------------------------------------------------------------
    @staticmethod
    def _count_substring(string: str, substring: str) -> int:
        """Counts the number of occurrences of `substring` in `string`."""
        replaced = string.replace(substring, "")
        return (len(string) - len(replaced)) // len(substring)


# //////////////////////////////////////////////////////////////////////////////
