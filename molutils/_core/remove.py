from pathlib import Path

import molsimple as ms
import freyacli as fy
import molutils as mu

# //////////////////////////////////////////////////////////////////////////////
class Remove(mu.AppSubcommand):
    # -------------------------------------------------------------------------- UI SECTION
    def run(self):
        command = self.main.subcommands.pop(0)

        if command == "altlocs" : return self.app_remove_altlocs()

        raise ValueError(f"Unknown command: {command}")


    # --------------------------------------------------------------------------
    def app_remove_altlocs(self):
        path_in  = self.main.get_arg_path("path_in",  assertion = fy.PathAssertion.FILE_IN)
        path_out = self.main.get_arg_path("path_out", assertion = fy.PathAssertion.FILE_OUT)
        mu.Remove.altlocs(path_in).save(path_out)


    # --------------------------------------------------------------------------
    @classmethod
    def altlocs(cls, path_pdb: Path) -> ms.ParticleGroup:
        pdb = ms.System(path_pdb)

        out: list[ms.Particle] = []
        seen_altlocs = set()
        for particle in pdb.particles:
            if particle.altloc == "":
                out.append(particle)
                continue

            chres = particle.get_chain_resid().get_dotstr()
            name  = particle.name

            key = (chres, name)
            if key in seen_altlocs: continue

            seen_altlocs.add(key)
            particle.altloc = ""
            out.append(particle)

        return ms.ParticleGroup(out)


# //////////////////////////////////////////////////////////////////////////////
