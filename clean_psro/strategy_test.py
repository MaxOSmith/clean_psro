"""Test suite for `clean_psro.strategy`."""
import dataclasses
from typing import Any, Optional, Tuple

import dm_env
from absl.testing import absltest, parameterized

from clean_psro import _types, strategy


@dataclasses.dataclass
class _DummyAgent:
    """Dummy agent for testing."""

    action: Any
    state: Optional[Any] = None

    def step(
        self, timestep: dm_env.TimeStep, state: Optional[_types.Tree] = None
    ) -> Tuple[_types.Action, _types.State]:
        """Select an action."""
        del timestep, state
        return self.action, self.state

    def episode_reset(self, timestep: dm_env.TimeStep) -> _types.State:
        """Reset the state of the agent at the start of an episode."""
        del timestep
        return self.state


class StrategyTest(parameterized.TestCase):
    """Test suite for `Strategy`."""

    def test_pure_strategy(self):
        """Tests a pure strategy."""
        player = strategy.Strategy(
            policies=[_DummyAgent(1), _DummyAgent(2), _DummyAgent(3)],
            mixture=[1, 0, 0],
        )

        # Correctly sample first policy on reset.
        player.episode_reset(None)
        self.assertEqual(1, player.step(None, None)[0])
        self.assertEqual(1, player.step(None, None)[0])

        # Policy is correctly resampled.
        player.episode_reset(None)
        self.assertEqual(1, player.step(None, None)[0])
        self.assertEqual(1, player.step(None, None)[0])

        # Changing mixture.
        for policy_index in [1, 2]:
            mixture = [0, 0, 0]
            mixture[policy_index] = 1
            player.mixture = mixture

            player.episode_reset(None)
            self.assertEqual(policy_index + 1, player.step(None, None)[0])
            self.assertEqual(policy_index + 1, player.step(None, None)[0])
            player.episode_reset(None)
            self.assertEqual(policy_index + 1, player.step(None, None)[0])
            self.assertEqual(policy_index + 1, player.step(None, None)[0])


if __name__ == "__main__":
    absltest.main()
