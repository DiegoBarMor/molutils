from pathlib import Path

import freyacli as fy
import molutils as mu

# //////////////////////////////////////////////////////////////////////////////
class Traj(mu.AppSubcommand):
    # -------------------------------------------------------------------------- UI SECTION
    def run(self):
        command = self.main.subcommands.pop(0)

        if command == "align": return self.app_traj_align()
        if command == "rmsd" : return self.app_traj_rmsd()

        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def app_traj_align(self):
        path_struct = self.main.arg_path("path_struct", assertion = fy.PathAssertion.FILE_IN)
        path_traj = self.main.arg_path("path_traj", assertion = fy.PathAssertion.FILE_IN)
        path_ref = self.main.arg_path("path_ref",
            default = path_struct, assertion = fy.PathAssertion.FILE_IN
        )
        path_out = self.main.arg_path("path_out",
            default = path_struct.with_suffix(".align.xtc"), assertion = fy.PathAssertion.FILE_OUT
        )
        selection = self.main.arg_str("selection")

        mu.Traj.align(path_struct, path_traj, path_ref, path_out, selection)


    # --------------------------------------------------------------------------
    def app_traj_rmsd(self):
        path_struct = self.main.arg_path("path_struct", assertion = fy.PathAssertion.FILE_IN)
        path_traj = self.main.arg_path("path_traj", assertion = fy.PathAssertion.FILE_IN)
        path_ref = self.main.arg_path("path_ref",
            default = path_struct, assertion = fy.PathAssertion.FILE_IN
        )
        selection = self.main.arg_str("selection")

        print(*mu.Traj.rmsd(path_struct, path_traj, path_ref, selection))


    # -------------------------------------------------------------------------- LOGIC SECTION
    @classmethod
    def align(cls,
        path_struct: Path, path_traj: Path | None,
        path_ref: Path, path_out: Path,
        selection: str
    ) -> None:
        """Note: This method directly saves the aligned trajectory instead of returning it."""
        u_to_align = mu.MDAUtils.create_universe_quiet(path_struct, path_traj)
        u_ref      = mu.MDAUtils.create_universe_quiet(path_ref)

        from MDAnalysis.analysis import align
        align.AlignTraj(
            u_to_align, u_ref, select = selection,
            filename = str(path_out), match_atoms = False,
        ).run()


    # --------------------------------------------------------------------------
    @classmethod
    def rmsd(cls,
        path_struct: Path, path_traj: Path | None,
        path_ref: Path, selection: str
    ) -> list[float]:
        u_for_rmsd = mu.MDAUtils.create_universe_quiet(path_struct, path_traj)
        u_ref      = mu.MDAUtils.create_universe_quiet(path_ref)

        from MDAnalysis.analysis import rms
        rmsd = rms.RMSD(u_for_rmsd, u_ref, select = selection).run() # shape (n_frames, 3)
        idxs_frame, timesteps, arr_rmsd = rmsd.results.rmsd.T # shape (3, n_frames)
        return [float(r) for r in arr_rmsd] # ensure it's a "normal" float e.g. json serializable


# //////////////////////////////////////////////////////////////////////////////
