"""
SDK verification tests — validates core imports and type construction.
"""
import sys
import os

# Add current directory to sys.path if not installed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orca_dojo_sdk import DojoWallet, AgentConfig, Task, LaneType
from orca_dojo_sdk.lanes import ResearchLane


def test_wallet():
    print("Testing DojoWallet...")
    wallet = DojoWallet.create_random()
    addr = wallet.get_public_address()
    print(f"Address: {addr}")
    assert len(addr) == 58, f"Expected 58-char address, got {len(addr)}"
    print("✅ Wallet OK.")


def test_types():
    print("Testing Pydantic Types...")
    config = AgentConfig(
        agent_address="test-agent-001",
        lane=LaneType.RESEARCH,
        llmTier="Standard",
        biddingStrategy="Volume",
        openai_api_key="gsk_test_key_for_validation_purposes_only_1234567890"
    )
    print(f"Config: {config.model_dump()}")
    assert config.lane == LaneType.RESEARCH

    task = Task(
        task_id="task-123",
        lane=LaneType.RESEARCH,
        payload={"query": "Who is 0rca?"},
        reward_micro_usdc=1000000
    )
    print(f"Task: {task.model_dump()}")
    assert task.task_id == "task-123"
    print("✅ Types OK.")


def test_lane_type():
    print("Testing LaneType enum...")
    assert LaneType.RESEARCH.value == "research"
    assert LaneType.CODE.value == "code"
    assert LaneType.DATA.value == "data"
    assert LaneType.OUTREACH.value == "outreach"
    print("✅ LaneType OK.")


if __name__ == "__main__":
    try:
        test_wallet()
        test_types()
        test_lane_type()
        print("\n✅ All SDK verifications PASSED.")
    except Exception as e:
        print(f"\n❌ Verification FAILED: {e}")
        sys.exit(1)
