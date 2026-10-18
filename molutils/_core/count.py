from pathlib import Path

import molsimple as ms
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
        if command == "altlocs" : return self.app_count_altlocs()

        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def app_count_models(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        print(mu.Count.models(ms.System.read_pdb(path_in)))


    # --------------------------------------------------------------------------
    def app_count_chains(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        print(mu.Count.chains(ms.System.read_pdb(path_in)))


    # --------------------------------------------------------------------------
    def app_count_residues(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        print(mu.Count.residues(ms.System.read_pdb(path_in)))


    # --------------------------------------------------------------------------
    def app_count_frames(self):
        path_struct = self.main.get_arg_path("path_struct", assertion = fy.PathAssertion.FILE_IN)
        path_traj = self.main.get_arg_path("path_traj",
            assertion = fy.PathAssertion.FILE_IN, allow_none = True
        )

        import MDAnalysis as mda
        args_traj = [str(path_traj)] if path_traj is not None else []
        u = mda.Universe(str(path_struct), *args_traj)

        nframes_valid, _ = mu.Count.frames(u)
        print(f"{nframes_valid}")



    # --------------------------------------------------------------------------
    def app_count_altlocs(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        print(mu.Count.altlocs(ms.System.read_pdb(path_in)))


    # -------------------------------------------------------------------------- LOGIC SECTION
    @classmethod
    def models(cls, system: ms.System) -> int:
        return len(system.models)


    # --------------------------------------------------------------------------
    @classmethod
    def chains(cls, system: ms.System) -> int:
        return len(mu.List.chains(system, do_sort = False))


    # --------------------------------------------------------------------------
    @classmethod
    def residues(cls, system: ms.System) -> int:
        return len(mu.List.residues(system, do_sort = False))


    # --------------------------------------------------------------------------
    @classmethod
    def frames(cls, universe) -> tuple[int, int]:
        """
        Requires MDAnalysis (`universe` should be an instance of `MDAnalysis.Universe`).
        Returns a tuple of `(nframes_valid, nframes_expected)`, where:
        - `nframes_valid`: The number of frames that could be successfully read from the trajectory.
        - `nframes_expected`: The total number of frames expected based on the trajectory metadata.
        """
        nframes_expected = universe.trajectory.n_frames
        nframes_valid = sum(1 for _ in universe.trajectory)
        return nframes_valid, nframes_expected


    # --------------------------------------------------------------------------
    @classmethod
    def altlocs(cls, system: ms.System) -> int:
        parts_with_altloc: set[tuple[str, str]] = set()

        for particle in system.particles:
            if not particle.altloc: continue

            key = (particle.get_chain_resid().get_dotstr(), particle.name)
            if key in parts_with_altloc: continue

            parts_with_altloc.add(key)

        return len(parts_with_altloc)


# //////////////////////////////////////////////////////////////////////////////
