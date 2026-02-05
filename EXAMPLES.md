# SynapseWatcher - Usage Examples

**10+ Working Examples with Expected Output**

---

## Quick Navigation

- [Example 1: Basic Watching](#example-1-basic-watching)
- [Example 2: Filter by Agent](#example-2-filter-by-agent)
- [Example 3: Priority Filtering](#example-3-priority-filtering)
- [Example 4: Keyword Search](#example-4-keyword-search)
- [Example 5: Combined Filters](#example-5-combined-filters)
- [Example 6: Custom Callback Function](#example-6-custom-callback-function)
- [Example 7: Multiple Callbacks](#example-7-multiple-callbacks)
- [Example 8: Background Watching](#example-8-background-watching)
- [Example 9: Auto-Reply Bot](#example-9-auto-reply-bot)
- [Example 10: Emergency Response System](#example-10-emergency-response-system)
- [Example 11: Message Statistics Tracker](#example-11-message-statistics-tracker)
- [Example 12: Task Assignment Handler](#example-12-task-assignment-handler)

---

## Example 1: Basic Watching

**Scenario:** First time using SynapseWatcher - watch all messages

**Steps:**

```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseWatcher
python synapsewatcher.py
```

**Expected Output:**

```
SynapseWatcher v1.1.0
Watching: D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active
Press Ctrl+C to stop

2026-02-04 10:15:23 - SynapseWatcher - INFO - Watching: D:/BEACON_HQ/...
2026-02-04 10:15:23 - SynapseWatcher - INFO - Poll interval: 1.0s
2026-02-04 10:15:23 - SynapseWatcher - INFO - Callbacks registered: 1
2026-02-04 10:15:23 - SynapseWatcher - INFO - Marked 150 existing messages as seen

# When a new message arrives:
================================================================================
[NEW MESSAGE] forge_task_20260204_001
From: FORGE
To: ATLAS, CLIO
Priority: NORMAL
Subject: Weekly Status Update Request
Time: 2026-02-04T10:16:00
================================================================================
[BEEP!] Check Synapse for new message!
```

**What You Learned:**
- How to start the watcher
- Default output format
- Audio alert (bell) on new messages
- Existing messages are ignored

---

## Example 2: Filter by Agent

**Scenario:** Watch only messages sent to your agent

**Steps:**

```bash
# Watch messages to ATLAS only
python synapsewatcher.py --to ATLAS
```

**Expected Output:**

```
SynapseWatcher v1.1.0
Watching: D:/BEACON_HQ/...
Filters active: {'to_agent': 'ATLAS', 'from_agent': None, 'priority': None, 'keywords': []}
Press Ctrl+C to stop

# Only shows messages TO ATLAS:
================================================================================
[NEW MESSAGE] forge_to_atlas_20260204
From: FORGE
To: ATLAS
Priority: HIGH
Subject: Build SynapseWatcher Phase 7 Docs
================================================================================
```

**What You Learned:**
- `--to` filters by recipient
- Filter status displayed at startup
- Messages to other agents are ignored

---

## Example 3: Priority Filtering

**Scenario:** Only watch HIGH and CRITICAL priority messages

**Steps:**

```bash
# Watch HIGH priority only
python synapsewatcher.py --priority HIGH

# Or CRITICAL only
python synapsewatcher.py --priority CRITICAL
```

**Expected Output:**

```
SynapseWatcher v1.1.0
Watching: D:/BEACON_HQ/...
Filters active: {'to_agent': None, 'from_agent': None, 'priority': 'HIGH', 'keywords': []}

# Only HIGH priority messages appear:
================================================================================
[NEW MESSAGE] urgent_alert_001
From: CLIO
To: ALL_AGENTS
Priority: HIGH
Subject: Server Disk Space Low - Action Required
================================================================================
```

**What You Learned:**
- `--priority` filters by message priority
- NORMAL messages are ignored when filtering
- Use for alert/monitoring systems

---

## Example 4: Keyword Search

**Scenario:** Watch for specific keywords in messages

**Steps:**

```bash
# Watch for urgent keywords
python synapsewatcher.py --keywords "urgent,critical,emergency,help"

# Watch for task-related keywords
python synapsewatcher.py --keywords "task,build,fix,implement"
```

**Expected Output:**

```
SynapseWatcher v1.1.0
Filters active: {'to_agent': None, 'from_agent': None, 'priority': None, 'keywords': ['urgent', 'critical', 'emergency', 'help']}

# Only messages with keywords appear:
================================================================================
[NEW MESSAGE] help_request_001
From: BOLT
To: FORGE
Priority: NORMAL
Subject: Help needed with API integration
================================================================================
```

**What You Learned:**
- `--keywords` accepts comma-separated list
- Keywords are case-insensitive
- Matches subject AND body content

---

## Example 5: Combined Filters

**Scenario:** Multiple filters for precise matching

**Steps:**

```bash
# HIGH priority messages to ATLAS containing "build"
python synapsewatcher.py --to ATLAS --priority HIGH --keywords "build"
```

**Expected Output:**

```
SynapseWatcher v1.1.0
Filters active: {'to_agent': 'ATLAS', 'from_agent': None, 'priority': 'HIGH', 'keywords': ['build']}

# Very specific matches only:
================================================================================
[NEW MESSAGE] forge_high_build_task
From: FORGE
To: ATLAS
Priority: HIGH
Subject: Build TokenTracker v2.0 - URGENT
================================================================================
```

**What You Learned:**
- Filters are AND conditions (all must match)
- More filters = more specific results
- Useful for focused monitoring

---

## Example 6: Custom Callback Function

**Scenario:** Create your own message handler in Python

**Steps:**

```python
from synapsewatcher import SynapseWatcher, SynapseMessage

# Create watcher
watcher = SynapseWatcher()

# Define custom callback
def my_custom_handler(message: SynapseMessage):
    """Process message with custom logic."""
    print(f"CUSTOM: Got message from {message.from_agent}")
    print(f"Subject: {message.subject}")
    
    # Custom logic based on content
    if "urgent" in message.subject.lower():
        print(">>> URGENT MESSAGE - TAKE ACTION!")
    
    # Access message details
    print(f"Body keys: {list(message.body.keys())}")

# Register callback
watcher.register_callback(my_custom_handler)

# Start watching
watcher.start()
```

**Expected Output:**

```
CUSTOM: Got message from FORGE
Subject: Weekly status check
Body keys: ['content', 'metadata']

CUSTOM: Got message from CLIO
Subject: URGENT: System alert
>>> URGENT MESSAGE - TAKE ACTION!
Body keys: ['alert_type', 'severity', 'details']
```

**What You Learned:**
- Create custom Python callback functions
- Access all message attributes
- Implement custom processing logic

---

## Example 7: Multiple Callbacks

**Scenario:** Register multiple handlers for different purposes

**Steps:**

```python
from synapsewatcher import SynapseWatcher

watcher = SynapseWatcher()

# Callback 1: Logging
def log_message(message):
    print(f"[LOG] {message.timestamp}: {message.subject}")

# Callback 2: Statistics
message_count = {"total": 0}
def count_messages(message):
    message_count["total"] += 1
    print(f"[STATS] Total messages: {message_count['total']}")

# Callback 3: Priority alerting
def priority_alert(message):
    if message.priority in ["HIGH", "CRITICAL"]:
        print(f"[ALERT!] Priority message from {message.from_agent}!")

# Register all callbacks
watcher.register_callback(log_message)
watcher.register_callback(count_messages)
watcher.register_callback(priority_alert)

# Start - all callbacks fire for each message
watcher.start()
```

**Expected Output:**

```
[LOG] 2026-02-04T10:30:00: Status update
[STATS] Total messages: 1

[LOG] 2026-02-04T10:31:00: URGENT: Server issue
[STATS] Total messages: 2
[ALERT!] Priority message from CLIO!
```

**What You Learned:**
- Multiple callbacks can be registered
- All callbacks fire for each message
- One callback's error doesn't affect others

---

## Example 8: Background Watching

**Scenario:** Run watcher in background while doing other work

**Steps:**

```python
from synapsewatcher import SynapseWatcher
import threading
import time

# Create watcher
watcher = SynapseWatcher()

def message_handler(message):
    print(f"\n[BACKGROUND] New: {message.subject}\n")

watcher.register_callback(message_handler)

# Start in background thread
thread = threading.Thread(target=watcher.start, daemon=True)
thread.start()

print("Watcher running in background!")
print("Doing other work...")

# Continue with other operations
for i in range(10):
    print(f"Working... {i}")
    time.sleep(2)

# Messages will appear while working:
# Working... 0
# Working... 1
# [BACKGROUND] New: Task assignment
# Working... 2
# Working... 3
```

**Expected Output:**

```
Watcher running in background!
Doing other work...
Working... 0
Working... 1

[BACKGROUND] New: Weekly update from FORGE

Working... 2
Working... 3
Working... 4
```

**What You Learned:**
- Use threading for background watching
- `daemon=True` allows clean exit
- Messages appear while doing other work

---

## Example 9: Auto-Reply Bot

**Scenario:** Automatically reply to incoming messages

**Steps:**

```python
from synapsewatcher import SynapseWatcher, MessageFilter
from synapselink import quick_send

watcher = SynapseWatcher()
watcher.set_filter(MessageFilter(to_agent="ATLAS"))

def auto_reply(message):
    """Automatically reply to messages."""
    print(f"Received: {message.subject}")
    
    # Send auto-reply
    quick_send(
        message.from_agent,
        f"Re: {message.subject}",
        f"Thanks for your message! I received it at {message.timestamp}.\n"
        f"I'll review and respond soon.",
        priority="NORMAL"
    )
    
    print(f"Sent auto-reply to {message.from_agent}")

watcher.register_callback(auto_reply)

print("Auto-reply bot active for ATLAS messages!")
watcher.start()
```

**Expected Output:**

```
Auto-reply bot active for ATLAS messages!
Received: Task assignment for today
Sent auto-reply to FORGE
Received: Question about TokenTracker
Sent auto-reply to CLIO
```

**What You Learned:**
- Integrate with SynapseLink for replies
- Build auto-responder bots
- Useful for acknowledgment systems

---

## Example 10: Emergency Response System

**Scenario:** Trigger emergency workflow on CRITICAL messages

**Steps:**

```python
from synapsewatcher import SynapseWatcher, MessageFilter
import subprocess

watcher = SynapseWatcher()
watcher.set_filter(MessageFilter(priority="CRITICAL"))

def emergency_response(message):
    """Handle CRITICAL priority messages."""
    print("\n" + "!" * 60)
    print("!!! CRITICAL MESSAGE RECEIVED !!!")
    print("!" * 60)
    print(f"From: {message.from_agent}")
    print(f"Subject: {message.subject}")
    print("!" * 60)
    
    # Play alert sound (Windows)
    print('\a\a\a')  # Triple beep
    
    # Could trigger emergency workflow
    # subprocess.run(["python", "emergency_handler.py", message.msg_id])
    
    # Log to emergency file
    with open("emergency_log.txt", "a") as f:
        f.write(f"{message.timestamp}: {message.subject}\n")

watcher.register_callback(emergency_response)

print("Emergency response system active!")
print("Monitoring for CRITICAL priority messages...")
watcher.start()
```

**Expected Output:**

```
Emergency response system active!
Monitoring for CRITICAL priority messages...

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!! CRITICAL MESSAGE RECEIVED !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
From: CLIO
Subject: SERVER DOWN - Production database unreachable
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

**What You Learned:**
- Filter by priority for alerts
- Trigger external scripts/workflows
- Build monitoring/alerting systems

---

## Example 11: Message Statistics Tracker

**Scenario:** Track Synapse communication statistics

**Steps:**

```python
from synapsewatcher import SynapseWatcher
from datetime import datetime

watcher = SynapseWatcher()

# Statistics storage
stats = {
    "total": 0,
    "by_agent": {},
    "by_priority": {},
    "first_message": None,
    "last_message": None
}

def track_statistics(message):
    """Track message statistics."""
    stats["total"] += 1
    
    # By agent
    agent = message.from_agent
    stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
    
    # By priority
    priority = message.priority
    stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
    
    # Timestamps
    if stats["first_message"] is None:
        stats["first_message"] = datetime.now()
    stats["last_message"] = datetime.now()
    
    # Display dashboard
    print("\n" + "=" * 50)
    print("SYNAPSE STATISTICS DASHBOARD")
    print("=" * 50)
    print(f"Total Messages: {stats['total']}")
    print(f"By Agent: {stats['by_agent']}")
    print(f"By Priority: {stats['by_priority']}")
    if stats['first_message']:
        runtime = (stats['last_message'] - stats['first_message']).total_seconds()
        print(f"Running for: {runtime:.0f} seconds")
    print("=" * 50)

watcher.register_callback(track_statistics)
watcher.start()
```

**Expected Output:**

```
==================================================
SYNAPSE STATISTICS DASHBOARD
==================================================
Total Messages: 5
By Agent: {'FORGE': 2, 'CLIO': 2, 'BOLT': 1}
By Priority: {'NORMAL': 3, 'HIGH': 2}
Running for: 127 seconds
==================================================
```

**What You Learned:**
- Track communication patterns
- Build analytics dashboards
- Monitor team activity

---

## Example 12: Task Assignment Handler

**Scenario:** Detect and process task assignments

**Steps:**

```python
from synapsewatcher import SynapseWatcher, MessageFilter
from synapselink import quick_send

watcher = SynapseWatcher()
watcher.set_filter(MessageFilter(
    to_agent="BOLT",
    keywords=["task", "assignment", "build", "implement", "fix"]
))

# Task queue
task_queue = []

def handle_task_assignment(message):
    """Process task assignment messages."""
    # Extract task details
    task = {
        "id": f"TASK-{len(task_queue)+1:04d}",
        "title": message.subject,
        "from": message.from_agent,
        "priority": message.priority,
        "received": message.timestamp,
        "status": "PENDING"
    }
    
    task_queue.append(task)
    
    print(f"\n[NEW TASK] {task['id']}")
    print(f"  Title: {task['title']}")
    print(f"  From: {task['from']}")
    print(f"  Priority: {task['priority']}")
    print(f"  Queue size: {len(task_queue)}")
    
    # Send acknowledgment
    quick_send(
        message.from_agent,
        f"Task Received: {task['id']}",
        f"Task '{task['title']}' has been added to my queue.\n"
        f"Task ID: {task['id']}\n"
        f"Position in queue: {len(task_queue)}",
        priority="NORMAL"
    )

watcher.register_callback(handle_task_assignment)

print("Task handler active for BOLT!")
print("Listening for task assignments...")
watcher.start()
```

**Expected Output:**

```
Task handler active for BOLT!
Listening for task assignments...

[NEW TASK] TASK-0001
  Title: Build user authentication module
  From: FORGE
  Priority: HIGH
  Queue size: 1

[NEW TASK] TASK-0002
  Title: Fix login page CSS
  From: ATLAS
  Priority: NORMAL
  Queue size: 2
```

**What You Learned:**
- Filter for task-like messages
- Build task queue from messages
- Auto-acknowledge assignments

---

## 🎯 Summary

These examples demonstrate:

1. **CLI Usage** - Basic to advanced command-line options
2. **Filtering** - By agent, priority, keywords, or combinations
3. **Custom Callbacks** - Python functions for custom processing
4. **Integrations** - With SynapseLink and other tools
5. **Background Mode** - Non-blocking operation
6. **Real-World Patterns** - Bots, alerts, dashboards, task handlers

---

## 📚 Additional Resources

- **README.md** - Full documentation
- **INTEGRATION_PLAN.md** - Deep integration guide
- **QUICK_START_GUIDES.md** - Agent-specific guides
- **CHEAT_SHEET.txt** - Quick reference

---

**Last Updated:** February 4, 2026  
**Maintained By:** ATLAS (Team Brain)
