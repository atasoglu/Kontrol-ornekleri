import skfuzzy.control as ctrl
from typing import Callable


class FuzzyControl(ctrl.ControlSystemSimulation):
    """Simple Fuzzy controller for simulations with system model."""
    def __init__(
        self,
        ref: float,
        err: ctrl.Antecedent,
        derivative_err: ctrl.Antecedent,
        u: ctrl.Consequent,
        sys_func: Callable[[float], float],
        control_system: ctrl.ControlSystem,
        clip_to_bounds: bool = True,
        cache: bool = True,
        flush_after_run: bool = 1000
    ) -> None:
        """Simple Fuzzy controller.

        Args:
            ref (float): Reference value.
            err (ctrl.Antecedent): Error input.
            derivative_err (ctrl.Antecedent): Derivative of error input.
            u (ctrl.Consequent): Output.
            sys_func (Callable[[float], float]): Mathematical representation of the system.
            control_system (ctrl.ControlSystem): Control system object with defined rules.
            clip_to_bounds (bool, optional): Defaults to True.
            cache (bool, optional): Defaults to True.
            flush_after_run (bool, optional): Defaults to 1000.
        """
        super().__init__(control_system, clip_to_bounds, cache, flush_after_run)
        self.ref = ref
        self.err = err
        self.derr = derivative_err
        self.u = u
        self.sys_func = sys_func
        self.control_sys = control_system
        self.clear()

    def clear(self) -> None:
        """Clears *last error* memory.

        Call this if you want to repeat your simulations sequentially.
        """
        self._last_err = 0

    def step(self, feedback: float) -> float:
        """Calculates system output for one loop.

        Args:
            feedback (float): Initial feedback.

        Returns:
            float: System output.
        """
        err = self.ref - feedback
        derr = err - self._last_err
        self._last_err = err
        self.input[self.err.label] = err
        self.input[self.derr.label] = derr
        self.compute()
        u = self.output[self.u.label]
        return self.sys_func(u)
