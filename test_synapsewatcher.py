"""
SynapseWatcher v1.0 - Test Suite

Tests for the SynapseWatcher real-time notification system.
"""

import sys
import json
import time
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from synapsewatcher import SynapseWatcher, MessageFilter, SynapseMessage


class TestResults:
    """Track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_true(self, condition, message):
        if condition:
            self.passed += 1
            print(f"  [OK] {message}")
        else:
            self.failed += 1
            self.errors.append(message)
            print(f"  [FAIL] {message}")
    
    def assert_equal(self, actual, expected, message):
        if actual == expected:
            self.passed += 1
            print(f"  [OK] {message}")
        else:
            self.failed += 1
            error = f"{message} (expected: {expected}, got: {actual})"
            self.errors.append(error)
            print(f"  [FAIL] {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST RESULTS: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for error in self.errors:
                print(f"  - {error}")
        print(f"{'='*60}\n")
        return self.failed == 0


def create_test_message(temp_dir: Path, msg_id: str, **kwargs) -> Path:
    """Create a test Synapse message file."""
    message = {
        "msg_id": msg_id,
        "from": kwargs.get("from_agent", "TEST_AGENT"),
        "to": kwargs.get("to", ["ALL_AGENTS"]),
        "subject": kwargs.get("subject", "Test Message"),
        "priority": kwargs.get("priority", "NORMAL"),
        "timestamp": kwargs.get("timestamp", "2026-01-18T12:00:00"),
        "body": kwargs.get("body", {"message": "Test content"})
    }
    
    filepath = temp_dir / f"{msg_id}.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(message, f, indent=2)
    
    return filepath


def test_message_loading():
    """Test loading messages from JSON files."""
    print("\n[TEST] Message Loading")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test message
        filepath = create_test_message(
            temp_path,
            "test_msg_001",
            from_agent="FORGE",
            to=["ATLAS"],
            subject="Test Subject",
            priority="HIGH"
        )
        
        # Load message
        message = SynapseMessage.from_file(filepath)
        
        # Verify
        results.assert_equal(message.msg_id, "test_msg_001", "Message ID correct")
        results.assert_equal(message.from_agent, "FORGE", "From agent correct")
        results.assert_equal(message.to, ["ATLAS"], "To agents correct")
        results.assert_equal(message.subject, "Test Subject", "Subject correct")
        results.assert_equal(message.priority, "HIGH", "Priority correct")
    
    return results.summary()


def test_message_filter():
    """Test message filtering logic."""
    print("\n[TEST] Message Filtering")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test message
        filepath = create_test_message(
            temp_path,
            "test_msg_002",
            from_agent="FORGE",
            to=["ATLAS", "BOLT"],
            subject="Urgent: System Down",
            priority="CRITICAL",
            body={"message": "Database connection failed"}
        )
        
        message = SynapseMessage.from_file(filepath)
        
        # Test 1: Filter by to_agent (match)
        filter1 = MessageFilter(to_agent="ATLAS")
        results.assert_true(filter1.matches(message), "Filter matches to_agent=ATLAS")
        
        # Test 2: Filter by to_agent (no match)
        filter2 = MessageFilter(to_agent="CLIO")
        results.assert_true(not filter2.matches(message), "Filter rejects to_agent=CLIO")
        
        # Test 3: Filter by from_agent (match)
        filter3 = MessageFilter(from_agent="FORGE")
        results.assert_true(filter3.matches(message), "Filter matches from_agent=FORGE")
        
        # Test 4: Filter by priority (match)
        filter4 = MessageFilter(priority="CRITICAL")
        results.assert_true(filter4.matches(message), "Filter matches priority=CRITICAL")
        
        # Test 5: Filter by keywords (match)
        filter5 = MessageFilter(keywords=["urgent", "system"])
        results.assert_true(filter5.matches(message), "Filter matches keywords")
        
        # Test 6: Filter by keywords (no match)
        filter6 = MessageFilter(keywords=["happy", "sunshine"])
        results.assert_true(not filter6.matches(message), "Filter rejects non-matching keywords")
        
        # Test 7: Multiple filters (match all)
        filter7 = MessageFilter(
            to_agent="ATLAS",
            priority="CRITICAL",
            keywords=["system"]
        )
        results.assert_true(filter7.matches(message), "Multiple filters match")
        
        # Test 8: Multiple filters (one fails)
        filter8 = MessageFilter(
            to_agent="ATLAS",
            priority="LOW"
        )
        results.assert_true(not filter8.matches(message), "Multiple filters reject when one fails")
    
    return results.summary()


def test_callback_execution():
    """Test callback registration and execution."""
    print("\n[TEST] Callback Execution")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create watcher
        watcher = SynapseWatcher(synapse_path=temp_path, poll_interval=0.1)
        
        # Track callback invocations
        callback_calls = []
        
        def test_callback(message):
            callback_calls.append(message.msg_id)
        
        # Register callback
        watcher.register_callback(test_callback)
        results.assert_equal(len(watcher.callbacks), 1, "Callback registered")
        
        # Start watcher in background
        import threading
        watcher_thread = threading.Thread(target=watcher.start, daemon=True)
        watcher_thread.start()
        
        time.sleep(0.2)  # Let watcher initialize
        
        # Create new message
        create_test_message(temp_path, "callback_test_001")
        
        # Wait for detection
        time.sleep(0.3)
        
        # Stop watcher
        watcher.stop()
        time.sleep(0.2)
        
        # Verify callback was called
        results.assert_true(len(callback_calls) > 0, "Callback was invoked")
        results.assert_true("callback_test_001" in callback_calls, "Correct message ID passed to callback")
    
    return results.summary()


def test_deduplication():
    """Test that same message isn't processed twice."""
    print("\n[TEST] Message Deduplication")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create watcher
        watcher = SynapseWatcher(synapse_path=temp_path, poll_interval=0.1)
        
        # Track callback invocations
        callback_calls = []
        
        def test_callback(message):
            callback_calls.append(message.msg_id)
        
        watcher.register_callback(test_callback)
        
        # Create message BEFORE starting watcher
        create_test_message(temp_path, "dedup_test_001")
        
        # Start watcher
        import threading
        watcher_thread = threading.Thread(target=watcher.start, daemon=True)
        watcher_thread.start()
        
        # Wait several poll cycles
        time.sleep(0.5)
        
        # Stop watcher
        watcher.stop()
        time.sleep(0.2)
        
        # Verify existing message was NOT processed
        results.assert_equal(len(callback_calls), 0, "Existing messages ignored (not duplicated)")
    
    return results.summary()


def test_error_handling():
    """Test graceful handling of errors."""
    print("\n[TEST] Error Handling")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create watcher
        watcher = SynapseWatcher(synapse_path=temp_path, poll_interval=0.1)
        
        # Callback that crashes
        def crashing_callback(message):
            raise ValueError("Intentional crash!")
        
        # Normal callback
        success_calls = []
        def normal_callback(message):
            success_calls.append(message.msg_id)
        
        # Register both
        watcher.register_callback(crashing_callback)
        watcher.register_callback(normal_callback)
        
        # Start watcher
        import threading
        watcher_thread = threading.Thread(target=watcher.start, daemon=True)
        watcher_thread.start()
        
        time.sleep(0.2)
        
        # Create message
        create_test_message(temp_path, "error_test_001")
        
        time.sleep(0.3)
        
        # Stop watcher
        watcher.stop()
        time.sleep(0.2)
        
        # Verify normal callback still executed despite crash
        results.assert_true(len(success_calls) > 0, "Normal callback executed despite other callback crash")
        results.assert_true("error_test_001" in success_calls, "Correct message processed")
    
    return results.summary()


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("SYNAPSEWATCHER v1.0 - TEST SUITE")
    print("="*60)
    
    all_passed = True
    
    all_passed &= test_message_loading()
    all_passed &= test_message_filter()
    all_passed &= test_callback_execution()
    all_passed &= test_deduplication()
    all_passed &= test_error_handling()
    
    print("\n" + "="*60)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED!")
    else:
        print("[FAILED] SOME TESTS FAILED")
    print("="*60 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
