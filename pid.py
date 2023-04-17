from typing import Optional, Tuple, Callable


class PID:
    """Simple PID controller for simulations with system model."""

    def __init__(
        self,
        ref: float,
        sampling: float,
        sys_func: Callable[[float], float],
        params: Optional[Tuple[float, float, float]] = None,
    ) -> None:
        """Simple PID controller.

        Args:
            ref (float): Reference value.
            sampling (float): Sampling time (sec).
            sys_func (Callable[[float], float]): Mathematical representation of the system.
            params (Optional[Tuple[float, float, float]], optional): PID parameters seperately. If not given, `[1, 0, 0]` will be assigned.

        Example:
        ```py
        from pid import PID
        import matplotlib.pyplot as plt
        import numpy as np

        pid = PID(
            ref=100,
            sampling=0.2,
            sys_func=lambda x: 0.01 * (x**2),
            params=(0.5, 0.01, 0.001)
        )
        iteration = 150 # 150 * 0.2 = 30 sec
        output = [0]
        for i in range(iteration-1):
            fb = output[-1]
            output.append(
                pid.step(fb) + fb
            )
        plt.axhline(100, color='r', label='r')
        plt.plot(np.arange(0, 30, 0.2), output, 'b-', label='y')
        plt.show()
        ```
        """
        self.ref = ref
        self.sampling = sampling
        self.sys_func = sys_func
        self.params = params or (1.0, 0.0, 0.0)
        self.clear()

    def clear(self) -> None:
        """Clears *last error* and *integration sum* memory.

        Call this if you want to repeat your simulations sequentially.
        """
        self._A = 0.0
        self._last_err = 0.0

    def step(self, feedback: float) -> float:
        """Calculates system output for one loop.

        Args:
            feedback (float): Initial feedback.

        Returns:
            float: System output.
        """
        err = self.ref - feedback
        self._A += self.sampling * (err + self._last_err) / 2.0
        p, i, d = self.params
        u = p * err + i * self._A + d * (err - self._last_err)
        self._last_err = err
        return self.sys_func(u)
