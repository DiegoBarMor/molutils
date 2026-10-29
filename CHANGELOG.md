# Changelog

## [0.7.0] - 2026-10-29
- Started `traj` subcommands.
    - Added `traj align` operation.
    - Added `traj rmsd` operation.


## [0.6.1] - 2026-10-22
- Added `count particles` operation.
- Updated `freyacli` dependency.


## [0.6.0] - 2026-10-18
- `molutils` now uses the `molsimple` package to parse PDB files.
- Added tests.
- Some bugfixes.


## [0.5.0] - 2026-05-16
- Added `count chains`, `count residues` and `count altlocs` subcommands.
- Added `remove` subcommand, with `remove altlocs` subcommand.
- Started adding operations for trajectories.
    - Added `count frames` subcommand.
    - Added `extract frames` subcommand.


## [0.4.0] - 2026-05-02
- Renamed `list resids` to `list residues`.
    - Operations over "residues" aren't based on residue identifiers alone (which was hinted by using the word *resids*). Instead, they follow a **chain_id.resid** format to avoid ambiguity between different residues along chains.
- Added `extract residue` subcommand.
- Added `merge` subcommand.
- Fixed typo in `Extract.run()`.


## [0.3.0] - 2026-04-29
- Added list subcommand `resids`.


## [0.2.0] - 2026-04-27
- Added `select` subcommand.
    - selects atoms with a custom `MDAnalysis` query.
- Added `list` subcommand, with `list chains` child.
- Added subcommand for saving splitted chains.


## [0.1.0] - 2026-04-25
- Initial upload to PyPI
