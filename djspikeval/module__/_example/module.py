##---IMPORTS

from .gnode_spike.apps.module._example.models import ResultExample

from spikeval.module import BaseModule, MRScalar, ModuleExecutionError

##---MODULE

class Module(BaseModule):
    """example module"""

    RESULT_TYPES = [MRScalar]

    ## implement check methods if necessary

    ## implement apply

    def _apply(self):
        self.result.append(666)

    ## save django model results

    def save(self, mod, ev):
        """save django result entities"""

        # check for finalised module
        if self._stage != 3:
            raise ModuleExecutionError('save initiated when module was not finalised!')

        # result saving
        rval = ResultExample(evaluation=ev, module=mod)
        rval.value = self.result[0].value
        rval.save()

##---MAIN

if __name__ == '__main__':
    pass
