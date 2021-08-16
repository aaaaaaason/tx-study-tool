"""Define test case reader."""
import os
from typing import List

import yaml

from txtool import (
    database,
    step,
)


class CaseNotFoundError(Exception):
    pass


class EngineNotFoundError(Exception):
    pass


class SetupStepsNotFoundError(Exception):
    pass


class TeardownStepsNotFoundError(Exception):
    pass


class StepsNotFoundError(Exception):
    pass


class Reader:
    """Read provided case, validate it and
       provide methods for runner to call.
    """
    def __init__(self, case: str):
        if not os.path.exists(case):
            raise CaseNotFoundError(f'Test case not found in "{case}".')
        with open(case, 'r') as f:
            self.case = yaml.load(f, Loader=yaml.FullLoader)

    def get_engine(self) -> str:
        if not self.case.get('engine'):
            raise EngineNotFoundError(
                'Field "engine" not specified in given test case.')
        return self.case['engine']

    def get_steps_for_setup(self) -> List[step.Step]:
        if not self.case.get('setup'):
            raise SetupStepsNotFoundError(
                'Field "setup" not specified in given test case.')
        session_id = database.get_default_session_id()
        return [step.Step(session_id, stmt) for stmt in self.case['setup']]

    def get_steps_for_teardown(self) -> List[step.Step]:
        if not self.case.get('teardown'):
            raise TeardownStepsNotFoundError(
                'Field "teardown" not specified in given test case.')
        session_id = database.get_default_session_id()
        return [step.Step(session_id, stmt) for stmt in self.case['teardown']]

    def get_steps(self) -> List[step.Step]:
        if not self.case.get('steps'):
            raise StepsNotFoundError(
                'Field "steps" not specified in given test case.')
        return [step.Step(*each) for each in self.case['steps']]
