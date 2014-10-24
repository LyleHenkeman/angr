from ..analysis import Analysis
from ..vfg import VFG
from ..variableseekr import VariableSeekr

class VSA(Analysis):
    #pylint:disable=attribute-defined-outside-init
    __dependencies__ = [ ('CFG', (), {'context_sensitivity': 1}) ]

    def __init__(self, context_sensitivity_level=2, interfunction_level=2):
        self.finished_functions = set()
        self._cfg = self._deps[0].cfg
        self.vfg = VFG(project=self._p, cfg=self._cfg, context_sensitivity_level=context_sensitivity_level)
        self.seeker = VariableSeekr(self._p, self._cfg, self.vfg)

        for f in self._cfg.function_manager.functions:
            if f in self.finished_functions:
                continue

            with self._resilience():
                self.vfg.construct(f, interfunction_level=interfunction_level)
                self.seeker.construct(func_start=f)

            self.finished_functions.add(f)
            self._checkpoint()