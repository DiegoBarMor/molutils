from pathlib import Path
from collections import defaultdict

import molsimple as ms
import freyacli as fy
import molutils as mu

# //////////////////////////////////////////////////////////////////////////////
class Extract(mu.AppSubcommand):
    # -------------------------------------------------------------------------- UI SECTION
    def run(self):
        command = self.main.subcommands.pop(0)

        if command == "models" : return self.app_extract_models()
        if command == "chains" : return self.app_extract_chains()
        if command == "residue": return self.app_extract_residue()
        if command == "frames" : return self.app_extract_frames()

        raise ValueError(f"Unknown command: {command}")

    # --------------------------------------------------------------------------
    def app_extract_models(self):
        path_in, folder_out = self._io_filein_dirout()

        first_only = self.main.get_arg_bool("first_only")
        for i, model in enumerate(ms.System(path_in).models):
            path_out = folder_out / f"{path_in.stem}.m{i:03}.pdb"
            model.save(path_out)
            if first_only: break


    # --------------------------------------------------------------------------
    def app_extract_chains(self):
        path_in, folder_out = self._io_filein_dirout()
        data_pdb = path_in.read_text()

        chains = mu.Extract.split_chains(data_pdb)

        chain_ids = mu.List.chains(path_in, first_only = True) \
            if self.main.get_arg_bool("first_only") else chains.keys()

        for chain_id in chain_ids:
            path_out = folder_out / f"{path_in.stem}.{chain_id}.pdb"
            path_out.write_text(chains[chain_id])


    # --------------------------------------------------------------------------
    def app_extract_residue(self):
        path_in, folder_out = self._io_filein_dirout()
        residue_dotstr = self.main.get_arg_str("residue")

        pdb = ms.System(path_in)
        chres = ms.ChainResid.from_dotstr(residue_dotstr)
        extracted = pdb.particles.select_chain_resid(chres)
        extracted.save(folder_out / f"{path_in.stem}.{residue_dotstr}.pdb")


    # --------------------------------------------------------------------------
    def app_extract_frames(self):
        path_struct, folder_out = self._io_filein_dirout(key_in = "path_struct")
        path_traj = self.main.get_arg_path("path_traj",
            assertion = fy.PathAssertion.FILE_IN, allow_none = True
        )
        frames = self.main.get_arg_int("frames", is_list = True)
        unpack = self.main.get_arg_bool("unpack")
        mu.Extract.frames(path_struct, path_traj, folder_out, frames, unpack)


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


    # --------------------------------------------------------------------------
    @classmethod
    def frames(cls,
        path_struct: Path, path_traj: Path | None, folder_out: Path,
        frames: list[int] = None, unpack: bool = False
    ) -> None:
        """Note: This method directly saves the specified frames instead of returning them."""
        import MDAnalysis as mda

        args_traj = [str(path_traj)] if path_traj is not None else []
        u = mda.Universe(str(path_struct), *args_traj)

        if frames is not None and len(frames) == 1:
            unpack = True

        if unpack:
            if frames is None: frames = range(u.trajectory.n_frames)
            for frame in frames:
                u.trajectory[frame]
                path_pdb_out = folder_out / f"{path_struct.stem}.{frame:04}.pdb"
                u.atoms.write(str(path_pdb_out))
            return

        if path_traj is None:
            ### save a struct file separately, useful when the input file
            ### had both the struct and traj data inside (e.g. XYZ)
            path_pdb_out = folder_out / f"{path_struct.stem}.sliced.pdb"
            u.atoms.write(str(path_pdb_out))

        path_xtc_out = folder_out / f"{path_struct.stem}.sliced.xtc"
        u.atoms.write(str(path_xtc_out), frames = "all" if frames is None else frames)
        return


    # --------------------------------------------------------------------------
    def _io_filein_dirout(self, key_in = "path_in") -> tuple[Path, Path]:
        path_in = self.main.get_arg_path(key_in, assertion = fy.PathAssertion.FILE_IN)
        folder_out = self.main.get_arg_path("folder_out",
            default = path_in.parent, assertion = fy.PathAssertion.DIR_OUT
        )
        return path_in, folder_out


# //////////////////////////////////////////////////////////////////////////////
