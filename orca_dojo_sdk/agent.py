from abc import ABC, abstractmethod
from typing import Optional
from orca_dojo_sdk.types import AgentConfig, Task, TaskResult
from orca_dojo_sdk.wallet import DojoWallet


class BaseAgent(ABC):
    """Abstract base class for all 0rca Dojo agents."""

    def __init__(self, config: AgentConfig, wallet: Optional[DojoWallet] = None):
        """
        Initializes the agent with configuration and optional wallet.
        
        Args:
            config: The agent's unique configuration.
            wallet: The agent's Algorand wallet for transaction signing.
        """
        self.config = config
        self.wallet = wallet or DojoWallet.create_random()
        self.is_active = False

    def get_llm_params(self) -> dict:
        """Returns the LLM parameters resolved from the tier in sealed config."""
        params = self.config.llm_params
        if not params:
            raise RuntimeError(
                "llm_params not found in agent config. "
                "Ensure ConfigLoader resolved the LLM tier correctly."
            )
        return params

    def activate(self):
        """Starts the agent's listener/execution cycle."""
        self.is_active = True
        self.on_activated()

    def deactivate(self):
        """Stops the agent's lifecycle."""
        self.is_active = False
        self.on_deactivated()

    @abstractmethod
    async def process_task(self, task: Task) -> TaskResult:
        """
        Core task execution logic to be implemented by concrete agents.
        
        Args:
            task: The assigned task payload.
        
        Returns:
            TaskResult containing the execution outcome and metadata.
        """
        pass

    def on_activated(self):
        """Hook called when the agent starts."""
        pass

    def on_deactivated(self):
        """Hook called when the agent stops."""
        pass

    def on_task_received(self, task: Task):
        """Hook called when a new task is detected."""
        pass

    def on_task_completed(self, result: TaskResult):
        """Hook called after task processing is finished."""
        pass
