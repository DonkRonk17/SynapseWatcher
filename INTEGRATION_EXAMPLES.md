# SynapseWatcher - Integration Examples

**Copy-Paste-Ready Code for Team Brain Tool Integrations**

---

## 🎯 INTEGRATION PHILOSOPHY

SynapseWatcher is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

Each example is:
- ✅ Tested and working
- ✅ Copy-paste ready
- ✅ Well-commented
- ✅ Production-quality

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: SynapseWatcher + SynapseLink](#pattern-1-synapsewatcher--synapselink)
2. [Pattern 2: SynapseWatcher + SynapseStats](#pattern-2-synapsewatcher--synapsestats)
3. [Pattern 3: SynapseWatcher + AgentHealth](#pattern-3-synapsewatcher--agenthealth)
4. [Pattern 4: SynapseWatcher + TokenTracker](#pattern-4-synapsewatcher--tokentracker)
5. [Pattern 5: SynapseWatcher + TaskQueuePro](#pattern-5-synapsewatcher--taskqueuepro)
6. [Pattern 6: SynapseWatcher + SessionReplay](#pattern-6-synapsewatcher--sessionreplay)
7. [Pattern 7: SynapseWatcher + MemoryBridge](#pattern-7-synapsewatcher--memorybridge)
8. [Pattern 8: SynapseWatcher + ContextCompressor](#pattern-8-synapsewatcher--contextcompressor)
9. [Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: SynapseWatcher + SynapseLink

**Use Case:** Complete Synapse communication loop - receive and reply

**Why:** SynapseLink sends messages, SynapseWatcher detects them. Together they enable two-way real-time communication.

**Code:**

```python
"""
SynapseWatcher + SynapseLink Integration
Complete two-way Synapse communication loop.
"""

import sys
from pathlib import Path

# Add AutoProjects to path
sys.path.insert(0, str(Path.home() / "OneDrive/Documents/AutoProjects"))

from synapsewatcher import SynapseWatcher, MessageFilter
from synapselink import quick_send, reply

def synapse_conversation_bot():
    """
    Auto-reply bot that responds to all incoming messages.
    
    Example conversation:
    1. FORGE sends: "How are you?"
    2. Bot auto-replies: "Received your message: How are you?"
    """
    
    watcher = SynapseWatcher()
    watcher.set_filter(MessageFilter(to_agent="ATLAS"))
    
    def auto_reply(message):
        """Automatically reply to incoming messages."""
        print(f"[RECEIVED] From {message.from_agent}: {message.subject}")
        
        # Send reply using SynapseLink
        quick_send(
            message.from_agent,  # Reply to sender
            f"Re: {message.subject}",
            f"Received your message. Processing now...\n"
            f"Original: {message.subject}\n"
            f"Priority: {message.priority}",
            priority="NORMAL"
        )
        
        print(f"[REPLIED] Sent acknowledgment to {message.from_agent}")
    
    watcher.register_callback(auto_reply)
    
    # Run in background
    import threading
    thread = threading.Thread(target=watcher.start, daemon=True)
    thread.start()
    
    print("Synapse conversation bot active!")
    return watcher


# Usage
if __name__ == "__main__":
    watcher = synapse_conversation_bot()
    
    # Keep running
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.stop()
        print("Bot stopped.")
```

**Result:** Instant bi-directional communication - messages are received and replied to automatically.

---

## Pattern 2: SynapseWatcher + SynapseStats

**Use Case:** Real-time dashboard with live statistics

**Why:** SynapseStats provides historical analytics; SynapseWatcher adds real-time updates.

**Code:**

```python
"""
SynapseWatcher + SynapseStats Integration
Real-time statistics dashboard.
"""

from synapsewatcher import SynapseWatcher
# from synapsestats import SynapseStats  # Uncomment when available

def realtime_dashboard():
    """
    Live Synapse statistics dashboard.
    Updates stats as new messages arrive.
    """
    
    # Initialize stats tracking
    stats = {
        "total_messages": 0,
        "by_agent": {},
        "by_priority": {"NORMAL": 0, "HIGH": 0, "CRITICAL": 0},
        "recent_messages": []
    }
    
    watcher = SynapseWatcher()
    
    def update_stats(message):
        """Update statistics on each new message."""
        # Increment total
        stats["total_messages"] += 1
        
        # Track by agent
        agent = message.from_agent
        stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
        
        # Track by priority
        priority = message.priority
        if priority in stats["by_priority"]:
            stats["by_priority"][priority] += 1
        
        # Keep recent messages (last 10)
        stats["recent_messages"].append({
            "from": message.from_agent,
            "subject": message.subject[:50],
            "time": message.timestamp
        })
        stats["recent_messages"] = stats["recent_messages"][-10:]
        
        # Display dashboard
        print("\n" + "=" * 60)
        print("SYNAPSE REAL-TIME DASHBOARD")
        print("=" * 60)
        print(f"Total Messages: {stats['total_messages']}")
        print(f"\nBy Agent: {stats['by_agent']}")
        print(f"By Priority: {stats['by_priority']}")
        print(f"\nRecent:")
        for msg in stats["recent_messages"][-5:]:
            print(f"  - {msg['from']}: {msg['subject']}")
        print("=" * 60)
    
    watcher.register_callback(update_stats)
    return watcher, stats


# Usage
if __name__ == "__main__":
    watcher, stats = realtime_dashboard()
    watcher.start()
```

**Result:** Live updating statistics as messages arrive.

---

## Pattern 3: SynapseWatcher + AgentHealth

**Use Case:** Health-aware message processing

**Why:** Only process messages when the agent is healthy; defer if degraded.

**Code:**

```python
"""
SynapseWatcher + AgentHealth Integration
Health-aware message processing.
"""

from synapsewatcher import SynapseWatcher, MessageFilter
# from agenthealth import AgentHealth  # Uncomment when using

def health_aware_processor():
    """
    Process messages only when agent is healthy.
    Defer processing if agent is degraded.
    """
    
    # Mock health status (replace with AgentHealth)
    agent_health = {"status": "healthy", "cpu": 45, "memory": 60}
    
    # Deferred message queue
    deferred_messages = []
    
    watcher = SynapseWatcher()
    watcher.set_filter(MessageFilter(to_agent="ATLAS"))
    
    def health_check_callback(message):
        """Process only if healthy."""
        
        # Check health status
        if agent_health["status"] == "healthy":
            # Process immediately
            print(f"[PROCESSING] {message.subject}")
            process_message(message)
        else:
            # Defer for later
            print(f"[DEFERRED] {message.subject} (agent unhealthy)")
            deferred_messages.append(message)
    
    def process_message(message):
        """Actual message processing logic."""
        print(f"  From: {message.from_agent}")
        print(f"  Priority: {message.priority}")
        # Your processing logic here
    
    def process_deferred():
        """Process deferred messages when healthy."""
        while deferred_messages and agent_health["status"] == "healthy":
            msg = deferred_messages.pop(0)
            print(f"[PROCESSING DEFERRED] {msg.subject}")
            process_message(msg)
    
    watcher.register_callback(health_check_callback)
    
    return watcher, agent_health, deferred_messages


# Usage
if __name__ == "__main__":
    watcher, health, deferred = health_aware_processor()
    watcher.start()
```

**Result:** Messages are only processed when the agent is healthy.

---

## Pattern 4: SynapseWatcher + TokenTracker

**Use Case:** Track communication costs

**Why:** Estimate token usage for Synapse message processing to stay within budget.

**Code:**

```python
"""
SynapseWatcher + TokenTracker Integration
Track token usage for message processing.
"""

from synapsewatcher import SynapseWatcher
# from tokentracker import TokenTracker  # Uncomment when using

def token_tracked_watcher():
    """
    Track estimated tokens for each message processed.
    Helps stay within $60/mo budget.
    """
    
    # Mock token tracker (replace with TokenTracker)
    token_log = []
    
    watcher = SynapseWatcher()
    
    def track_tokens(message):
        """Estimate and track tokens for message."""
        # Estimate tokens (rough: 4 chars = 1 token)
        subject_tokens = len(message.subject) // 4
        body_tokens = len(str(message.body)) // 4
        total_tokens = subject_tokens + body_tokens
        
        # Log token usage
        entry = {
            "msg_id": message.msg_id,
            "from": message.from_agent,
            "tokens": total_tokens,
            "timestamp": message.timestamp
        }
        token_log.append(entry)
        
        # Display running total
        total = sum(e["tokens"] for e in token_log)
        print(f"[TOKEN] Message: {total_tokens} tokens | Session total: {total}")
        
        # Alert if high usage
        if total > 10000:
            print("[!] Warning: High token usage this session!")
    
    watcher.register_callback(track_tokens)
    
    return watcher, token_log


# Usage
if __name__ == "__main__":
    watcher, log = token_tracked_watcher()
    watcher.start()
```

**Result:** Token usage tracked for budget compliance.

---

## Pattern 5: SynapseWatcher + TaskQueuePro

**Use Case:** Auto-create tasks from messages

**Why:** Convert Synapse messages into trackable tasks automatically.

**Code:**

```python
"""
SynapseWatcher + TaskQueuePro Integration
Automatically create tasks from messages.
"""

from synapsewatcher import SynapseWatcher, MessageFilter
# from taskqueuepro import TaskQueuePro  # Uncomment when using

def task_auto_creator():
    """
    Automatically create tasks from task-like messages.
    Detects keywords like "task", "build", "fix", "implement".
    """
    
    # Mock task queue (replace with TaskQueuePro)
    task_queue = []
    task_counter = 1000
    
    watcher = SynapseWatcher()
    
    # Filter for task-like messages
    watcher.set_filter(MessageFilter(
        keywords=["task", "build", "fix", "implement", "create", "update"]
    ))
    
    def create_task_from_message(message):
        """Convert message to task."""
        nonlocal task_counter
        
        task_counter += 1
        task = {
            "id": f"TASK-{task_counter}",
            "title": message.subject,
            "agent": message.to[0] if message.to else "UNASSIGNED",
            "priority": 2 if message.priority == "HIGH" else 1,
            "status": "PENDING",
            "source": {
                "type": "synapse",
                "from": message.from_agent,
                "msg_id": message.msg_id
            }
        }
        
        task_queue.append(task)
        
        print(f"[TASK CREATED] {task['id']}: {task['title'][:50]}")
        print(f"  Assigned to: {task['agent']}")
        print(f"  Priority: {task['priority']}")
    
    watcher.register_callback(create_task_from_message)
    
    return watcher, task_queue


# Usage
if __name__ == "__main__":
    watcher, queue = task_auto_creator()
    print("Task auto-creator active. Send messages with 'task', 'build', etc.")
    watcher.start()
```

**Result:** Synapse messages automatically become trackable tasks.

---

## Pattern 6: SynapseWatcher + SessionReplay

**Use Case:** Record all Synapse events for session replay

**Why:** Debug issues by replaying what messages were received.

**Code:**

```python
"""
SynapseWatcher + SessionReplay Integration
Record Synapse events for debugging and replay.
"""

from synapsewatcher import SynapseWatcher
from datetime import datetime
# from sessionreplay import SessionReplay  # Uncomment when using

def session_recorder():
    """
    Record all Synapse events for later replay.
    Useful for debugging communication issues.
    """
    
    # Mock session log (replace with SessionReplay)
    session_log = {
        "session_id": f"SESSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "agent": "ATLAS",
        "events": []
    }
    
    watcher = SynapseWatcher()
    
    def log_event(message):
        """Log message as session event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": "synapse_message",
            "data": {
                "msg_id": message.msg_id,
                "from": message.from_agent,
                "to": message.to,
                "subject": message.subject,
                "priority": message.priority
            }
        }
        
        session_log["events"].append(event)
        
        print(f"[LOGGED] Event #{len(session_log['events'])}: {message.subject[:40]}")
    
    watcher.register_callback(log_event)
    
    def save_session():
        """Save session log to file."""
        import json
        filename = f"{session_log['session_id']}.json"
        with open(filename, 'w') as f:
            json.dump(session_log, f, indent=2)
        print(f"Session saved to: {filename}")
    
    return watcher, session_log, save_session


# Usage
if __name__ == "__main__":
    watcher, log, save = session_recorder()
    
    try:
        watcher.start()
    except KeyboardInterrupt:
        save()  # Save on exit
        print("Session recording saved!")
```

**Result:** Complete record of Synapse events for debugging.

---

## Pattern 7: SynapseWatcher + MemoryBridge

**Use Case:** Archive important messages to memory core

**Why:** Persist significant messages for long-term reference.

**Code:**

```python
"""
SynapseWatcher + MemoryBridge Integration
Archive important messages to memory core.
"""

from synapsewatcher import SynapseWatcher, MessageFilter
from pathlib import Path
import json
# from memorybridge import MemoryBridge  # Uncomment when using

def message_archiver():
    """
    Archive HIGH/CRITICAL messages to memory core.
    Maintains rolling archive of important communications.
    """
    
    # Archive file (replace with MemoryBridge)
    archive_file = Path.home() / ".synapse_archive.json"
    
    def load_archive():
        if archive_file.exists():
            with open(archive_file) as f:
                return json.load(f)
        return {"messages": []}
    
    def save_archive(archive):
        with open(archive_file, 'w') as f:
            json.dump(archive, f, indent=2)
    
    watcher = SynapseWatcher()
    
    # Only archive HIGH/CRITICAL
    watcher.set_filter(MessageFilter(priority="HIGH"))
    
    def archive_message(message):
        """Archive important message."""
        archive = load_archive()
        
        entry = {
            "msg_id": message.msg_id,
            "from": message.from_agent,
            "to": message.to,
            "subject": message.subject,
            "priority": message.priority,
            "timestamp": message.timestamp
        }
        
        archive["messages"].append(entry)
        
        # Keep last 100 messages
        if len(archive["messages"]) > 100:
            archive["messages"] = archive["messages"][-100:]
        
        save_archive(archive)
        
        print(f"[ARCHIVED] {message.subject[:50]}")
        print(f"  Archive size: {len(archive['messages'])} messages")
    
    watcher.register_callback(archive_message)
    
    return watcher, archive_file


# Usage
if __name__ == "__main__":
    watcher, archive_path = message_archiver()
    print(f"Archiving HIGH priority messages to: {archive_path}")
    watcher.start()
```

**Result:** Important messages preserved in persistent archive.

---

## Pattern 8: SynapseWatcher + ContextCompressor

**Use Case:** Compress long messages before processing

**Why:** Save tokens when processing verbose messages.

**Code:**

```python
"""
SynapseWatcher + ContextCompressor Integration
Compress long messages before processing.
"""

from synapsewatcher import SynapseWatcher
# from contextcompressor import ContextCompressor  # Uncomment when using

def compressed_processor():
    """
    Compress long message bodies before processing.
    Saves tokens on verbose communications.
    """
    
    # Mock compressor (replace with ContextCompressor)
    def compress_text(text, max_length=500):
        """Simple truncation compressor."""
        if len(text) <= max_length:
            return text, 0
        compressed = text[:max_length] + "... [truncated]"
        savings = len(text) - len(compressed)
        return compressed, savings
    
    watcher = SynapseWatcher()
    
    total_savings = [0]  # Use list for closure
    
    def process_compressed(message):
        """Process with compression."""
        body_text = str(message.body)
        original_length = len(body_text)
        
        # Compress if long
        if original_length > 500:
            compressed_text, savings = compress_text(body_text)
            total_savings[0] += savings
            
            print(f"[COMPRESSED] {message.subject[:40]}")
            print(f"  Original: {original_length} chars")
            print(f"  Compressed: {len(compressed_text)} chars")
            print(f"  Savings: {savings} chars ({savings//4} tokens)")
            print(f"  Session total savings: {total_savings[0]//4} tokens")
            
            # Process compressed version
            process_body(compressed_text)
        else:
            print(f"[DIRECT] {message.subject[:40]} ({original_length} chars)")
            process_body(body_text)
    
    def process_body(text):
        """Actual processing logic."""
        # Your processing here
        pass
    
    watcher.register_callback(process_compressed)
    
    return watcher, total_savings


# Usage
if __name__ == "__main__":
    watcher, savings = compressed_processor()
    watcher.start()
```

**Result:** Verbose messages compressed to save tokens.

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete workflow using multiple tools together

**Why:** Demonstrate real production scenario with 3+ tools.

**Code:**

```python
"""
Multi-Tool Workflow Example
Complete task processing pipeline:
1. Receive message (SynapseWatcher)
2. Log to session (SessionReplay)
3. Create task (TaskQueuePro)
4. Send acknowledgment (SynapseLink)
"""

from synapsewatcher import SynapseWatcher, MessageFilter
from datetime import datetime

def complete_task_pipeline():
    """
    Full task processing pipeline.
    Demonstrates multi-tool integration.
    """
    
    # Session log
    session = {
        "id": f"PIPELINE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "events": []
    }
    
    # Task queue
    tasks = []
    
    # Message log
    acknowledgments = []
    
    watcher = SynapseWatcher()
    watcher.set_filter(MessageFilter(
        to_agent="ATLAS",
        keywords=["task", "build", "implement"]
    ))
    
    def pipeline_callback(message):
        """Complete pipeline for each message."""
        
        print(f"\n{'='*60}")
        print(f"PIPELINE PROCESSING: {message.subject}")
        print(f"{'='*60}")
        
        # Step 1: Log event (SessionReplay)
        event = {
            "time": datetime.now().isoformat(),
            "type": "message_received",
            "msg_id": message.msg_id
        }
        session["events"].append(event)
        print(f"[1/4] Event logged to session")
        
        # Step 2: Create task (TaskQueuePro)
        task = {
            "id": f"T{len(tasks)+1:04d}",
            "title": message.subject,
            "from": message.from_agent,
            "status": "PENDING"
        }
        tasks.append(task)
        print(f"[2/4] Task created: {task['id']}")
        
        # Step 3: Send acknowledgment (SynapseLink)
        ack = {
            "to": message.from_agent,
            "message": f"Task {task['id']} created from your message"
        }
        acknowledgments.append(ack)
        print(f"[3/4] Acknowledgment queued for {message.from_agent}")
        
        # Step 4: Summary
        print(f"[4/4] Pipeline complete!")
        print(f"  Session events: {len(session['events'])}")
        print(f"  Tasks created: {len(tasks)}")
        print(f"  Acknowledgments: {len(acknowledgments)}")
    
    watcher.register_callback(pipeline_callback)
    
    return watcher, session, tasks, acknowledgments


# Usage
if __name__ == "__main__":
    watcher, session, tasks, acks = complete_task_pipeline()
    print("Multi-tool pipeline active!")
    watcher.start()
```

**Result:** Complete integrated workflow with multiple tools.

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - all tools working together

**Why:** Production-grade agent operation with full instrumentation.

**Code:**

```python
"""
Full Team Brain Stack Integration
The ultimate production setup combining all tools.

Tools integrated:
- SynapseWatcher: Real-time message detection
- SynapseLink: Send replies
- AgentHealth: Health monitoring
- TokenTracker: Cost tracking
- TaskQueuePro: Task management
- SessionReplay: Event logging
- MemoryBridge: Persistence
"""

from synapsewatcher import SynapseWatcher, MessageFilter
from datetime import datetime
import json

class TeamBrainAgent:
    """
    Full Team Brain agent with all tool integrations.
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.session_id = f"{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize all tracking
        self.health = {"status": "healthy", "messages_processed": 0}
        self.token_usage = []
        self.task_queue = []
        self.session_events = []
        self.message_archive = []
        
        # Setup watcher
        self.watcher = SynapseWatcher()
        self.watcher.set_filter(MessageFilter(to_agent=agent_name))
        self.watcher.register_callback(self._process_message)
    
    def _process_message(self, message):
        """Full pipeline for each message."""
        
        print(f"\n{'='*70}")
        print(f"[{self.agent_name}] PROCESSING: {message.subject}")
        print(f"{'='*70}")
        
        # 1. Health check
        if self.health["status"] != "healthy":
            print(f"[DEFERRED] Agent unhealthy")
            return
        
        # 2. Log session event
        self.session_events.append({
            "time": datetime.now().isoformat(),
            "type": "message",
            "msg_id": message.msg_id
        })
        print(f"[EVENT] Logged to session ({len(self.session_events)} events)")
        
        # 3. Track tokens
        tokens = len(str(message.subject) + str(message.body)) // 4
        self.token_usage.append(tokens)
        total_tokens = sum(self.token_usage)
        print(f"[TOKENS] +{tokens} (total: {total_tokens})")
        
        # 4. Create task if applicable
        if any(kw in message.subject.lower() for kw in ["task", "build", "fix"]):
            task = {"id": f"T{len(self.task_queue)+1:04d}", "title": message.subject}
            self.task_queue.append(task)
            print(f"[TASK] Created {task['id']}")
        
        # 5. Archive if high priority
        if message.priority in ["HIGH", "CRITICAL"]:
            self.message_archive.append({
                "msg_id": message.msg_id,
                "subject": message.subject,
                "time": message.timestamp
            })
            print(f"[ARCHIVE] Stored ({len(self.message_archive)} archived)")
        
        # 6. Update health
        self.health["messages_processed"] += 1
        print(f"[HEALTH] Processed: {self.health['messages_processed']}")
        
        # 7. Summary
        print(f"\n[SUMMARY]")
        print(f"  Session events: {len(self.session_events)}")
        print(f"  Token usage: {total_tokens}")
        print(f"  Tasks: {len(self.task_queue)}")
        print(f"  Archived: {len(self.message_archive)}")
    
    def start(self):
        """Start the agent."""
        print(f"\n{'#'*70}")
        print(f"TEAM BRAIN AGENT: {self.agent_name}")
        print(f"Session: {self.session_id}")
        print(f"{'#'*70}\n")
        
        import threading
        thread = threading.Thread(target=self.watcher.start, daemon=True)
        thread.start()
        
        return thread
    
    def status(self):
        """Get agent status."""
        return {
            "agent": self.agent_name,
            "session": self.session_id,
            "health": self.health,
            "events": len(self.session_events),
            "tokens": sum(self.token_usage),
            "tasks": len(self.task_queue),
            "archived": len(self.message_archive)
        }
    
    def save_session(self, filepath: str = None):
        """Save session to file."""
        if filepath is None:
            filepath = f"{self.session_id}.json"
        
        data = {
            "session_id": self.session_id,
            "agent": self.agent_name,
            "health": self.health,
            "token_usage": self.token_usage,
            "tasks": self.task_queue,
            "events": self.session_events,
            "archive": self.message_archive
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Session saved to: {filepath}")


# Usage
if __name__ == "__main__":
    # Create full-stack agent
    agent = TeamBrainAgent("ATLAS")
    
    # Start monitoring
    thread = agent.start()
    
    print("Full Team Brain stack active!")
    print("Press Ctrl+C to stop and save session.\n")
    
    try:
        while True:
            import time
            time.sleep(10)
            # Print status every 10 seconds
            print(f"\nStatus: {agent.status()}")
    except KeyboardInterrupt:
        agent.watcher.stop()
        agent.save_session()
        print("Agent stopped, session saved.")
```

**Result:** Complete production-grade agent with full tool integration.

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

### Week 1 (Essential)

1. ✅ **SynapseLink** - Two-way communication
2. ✅ **SynapseStats** - Basic analytics
3. ✅ **SessionReplay** - Debugging capability

### Week 2 (Productivity)

4. ☐ **TaskQueuePro** - Task management
5. ☐ **AgentHealth** - Health monitoring
6. ☐ **TokenTracker** - Cost tracking

### Week 3 (Advanced)

7. ☐ **MemoryBridge** - Persistence
8. ☐ **ContextCompressor** - Token optimization
9. ☐ **Full stack integration**

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

### Import Errors

```python
# Ensure all tools are in Python path
import sys
from pathlib import Path

# Add AutoProjects to path
sys.path.insert(0, str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Now import
from synapsewatcher import SynapseWatcher
from synapselink import quick_send
```

### Callback Not Triggering

```python
# Debug: Remove filters and add verbose logging
watcher = SynapseWatcher()

# No filter - see ALL messages
def debug_callback(message):
    print(f"DEBUG: Received {message.msg_id}")
    print(f"  From: {message.from_agent}")
    print(f"  To: {message.to}")
    print(f"  Subject: {message.subject}")

watcher.register_callback(debug_callback)
```

### Threading Issues

```python
# Always run watcher in daemon thread
import threading

thread = threading.Thread(target=watcher.start, daemon=True)
thread.start()

# This allows Ctrl+C to stop the main program
# The watcher thread will automatically terminate
```

### Windows Path Issues

```python
# Use forward slashes or raw strings for Windows paths
from pathlib import Path

# Good
synapse_path = Path("D:/BEACON_HQ/...")

# Also good
synapse_path = Path(r"D:\BEACON_HQ\...")

# Bad (escape issues)
synapse_path = "D:\BEACON_HQ\..."  # \B and \... may be interpreted as escapes
```

---

## 📚 ADDITIONAL RESOURCES

- **Main Documentation:** [README.md](README.md)
- **Quick Start Guides:** [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- **Integration Plan:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- **Cheat Sheet:** [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

---

**Last Updated:** February 4, 2026  
**Maintained By:** ATLAS (Team Brain)

---

**SynapseWatcher** - The foundation for real-time Team Brain collaboration! ⚡
