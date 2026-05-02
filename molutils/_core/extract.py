from collections import defaultdict

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

        raise ValueError(f"Unknown command: {command}")

    # --------------------------------------------------------------------------
    def app_extract_models(self):
        path_in, folder_out = self._io_filein_dirout()
        data_pdb = path_in.read_text()

        if self.main.get_arg_bool("first_only"):
            _, model = mu.Extract.next_model(data_pdb)
            path_out = folder_out / f"{path_in.stem}.m0.pdb"
            path_out.write_text(model)
            return

        for i, model in enumerate(mu.Extract.iter_models(data_pdb)):
            path_out = folder_out / f"{path_in.stem}.m{i:03}.pdb"
            path_out.write_text(model)


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
        data_pdb = path_in.read_text()

        residue_dotstr = self.main.get_arg_str("residue")
        chres = mu.ChainResid.from_dotstr(residue_dotstr)
        extracted = mu.Extract.residue(data_pdb, chres.resid, chres.chain)

        path_out = folder_out / f"{path_in.stem}.{residue_dotstr}.pdb"
        path_out.write_text(extracted)


    # -------------------------------------------------------------------------- LOGIC SECTION
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


    # --------------------------------------------------------------------------
    @classmethod
    def residue(cls, data: str, resid: str, chain: str = None):
        pdb = mu.ParserPDB(data)
        gen_residue = (
            line for line in pdb.iter_atoms()
            if mu.ParserPDB.get_resid(line) == resid
        )
        if chain is not None: gen_residue = (
            line for line in gen_residue
            if mu.ParserPDB.get_chainid(line) == chain
        )
        return mu.ParserPDB.join_lines(gen_residue)


    # --------------------------------------------------------------------------
    def _io_filein_dirout(self):
        path_in = self.main.get_arg_path("path_in", assertion = fy.PathAssertion.FILE_IN)
        folder_out = self.main.get_arg_path("folder_out",
            default = path_in.parent, assertion = fy.PathAssertion.DIR_OUT
        )
        return path_in, folder_out


# //////////////////////////////////////////////////////////////////////////////
