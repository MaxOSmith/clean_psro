"""Strategy objects defining containers of policies and a distribution over them."""
from typing import Any, List, Optional, Sequence, Tuple

import dm_env
import numpy as np

from clean_psro import _types

_Policy = Any


class Strategy:
    """A collection of player policies and a distribution over their episodic play."""

    def __init__(self, policies: Sequence[_Policy], mixture: Sequence[float], seed: Optional[int] = None):
        """Initializes a new strategy.

        Args:
            policies: Collection of all of the player's policies.
            mixture: Distribution used to sample `policies` at the start of the episode.
            seed: Random seed.
        """
        self._policies = policies
        self._mixture = np.asarray(mixture)
        self._rng = np.random.RandomState(seed)
        self._policy = None

        if len(self._policies) != len(self._mixture):
            raise ValueError("Each policy must have exactly one mixture coefficient.")
        if len(self._mixture) and (np.any(self._mixture < 0) or not np.allclose(np.sum(self._mixture), 1.0)):
            raise ValueError("Mixture must be a valid probability distribution.")

    def step(
        self, timestep: dm_env.TimeStep, state: Optional[_types.Tree] = None, **kwargs
    ) -> Tuple[_types.Action, _types.State]:
        """Selects an action to take given the current timestep.

        Args:
            timestep: Current episode timestep.
            state: Recurrent state of the current policy.

        Returns:
            Tuple containg the selected action and updated recurrent state.
        """
        if not self.policy:
            raise ValueError("Episode reset must be called before step.")
        return self.policy.step(timestep=timestep, state=state, **kwargs)

    def episode_reset(self, timestep: dm_env.TimeStep, **kwargs) -> _types.State:
        """Reset the state of the agent at the start of an episode.

        Args:
            timestep: First timestep of a new episode.

        Returns:
            Initial recurrent state for the selected policy.
        """
        policy_index = self._rng.choice(len(self._policies), p=self._mixture)
        self.set_policy(policy_index)
        return self.policy.episode_reset(timestep=timestep, **kwargs)

    def set_policy(self, policy_id: int):
        """Set the policy for the current episode.

        Args:
            policy_id: Index of the policy to play.
        """
        self._policy = self._policies[policy_id]

    def add_policy(self, policy: _Policy):
        """Adds a new policy with zero support."""
        self._policies.append(policy)
        self._mixture = np.append(self._mixture, 0.0)

    @property
    def mixture(self) -> List[float]:
        """Getter for `mixture`."""
        return self._mixture

    @mixture.setter
    def mixture(self, value: Sequence[float]):
        """Setter for `mixture`."""
        self._mixture = value

    @property
    def policy(self):
        """Gett for `policy`."""
        return self._policy

    def __len__(self):
        """Length as the number of policies."""
        return len(self._policies)
