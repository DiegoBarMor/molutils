# //////////////////////////////////////////////////////////////////////////////
class Extract:
    # --------------------------------------------------------------------------
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


# //////////////////////////////////////////////////////////////////////////////
