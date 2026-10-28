from pathlib import Path

# //////////////////////////////////////////////////////////////////////////////
class MDAUtils:
    # --------------------------------------------------------------------------
    @staticmethod
    def create_universe_quiet(path_struct: Path, path_traj: Path|None = None):
        import io
        import logging
        import warnings
        import MDAnalysis as mda
        from contextlib import redirect_stdout, redirect_stderr

        buf = io.StringIO()
        logger = logging.getLogger("MDAnalysis")
        old_level = logger.getEffectiveLevel()
        try:
            logger.setLevel(logging.ERROR)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with redirect_stdout(buf), redirect_stderr(buf):
                    args_traj = [str(path_traj)] if path_traj is not None else []
                    u = mda.Universe(str(path_struct), *args_traj)
        finally:
            logger.setLevel(old_level)
        return u


# //////////////////////////////////////////////////////////////////////////////
