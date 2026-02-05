# SynapseWatcher - Quick Start Guides

**5-Minute Guides for Each Team Brain Agent**

---

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows. Choose your guide and be up and running in minutes!

**Choose your guide:**
- [Forge (Orchestrator)](#-forge-quick-start)
- [Atlas (Executor)](#-atlas-quick-start)
- [Clio (Linux Agent)](#-clio-quick-start)
- [Nexus (Multi-Platform)](#-nexus-quick-start)
- [Bolt (Free Executor)](#-bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Monitor all team communication in real-time

### Step 1: Installation Check

```bash
# Verify SynapseWatcher is available
cd C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseWatcher
python synapsewatcher.py --version

# Expected: SynapseWatcher 1.1.0
```

### Step 2: First Watch (All Messages)

As Forge, you want to see ALL team messages:

```bash
# Watch everything (no filter)
python synapsewatcher.py

# Output:
# SynapseWatcher v1.1.0
# Watching: D:/BEACON_HQ/.../THE_SYNAPSE/active
# Press Ctrl+C to stop
```

### Step 3: Forge-Specific Filters

```bash
# Only HIGH priority (urgent orchestration needs)
python synapsewatcher.py --priority HIGH

# Only from specific agents (task completion tracking)
python synapsewatcher.py --from BOLT
python synapsewatcher.py --from ATLAS

# Keywords for orchestration
python synapsewatcher.py --keywords "complete,done,help,blocked"
```

### Step 4: Python Integration for Orchestration

```python
# In your Forge session startup
from synapsewatcher import SynapseWatcher, MessageFilter
from synapselink import quick_send

def forge_orchestration_monitor():
    """Forge real-time team monitoring."""
    
    watcher = SynapseWatcher()
    
    def process_team_update(message):
        # Track task completions
        if "complete" in message.subject.lower():
            print(f"[COMPLETE] {message.from_agent}: {message.subject}")
        
        # Alert on priority escalations
        if message.priority in ["HIGH", "CRITICAL"]:
            print(f"\a[!!!] PRIORITY: {message.subject}")
        
        # Detect blockers
        if any(kw in message.subject.lower() for kw in ["blocked", "stuck", "help"]):
            print(f"[BLOCKER] {message.from_agent} needs help!")
    
    watcher.register_callback(process_team_update)
    
    # Run in background
    import threading
    thread = threading.Thread(target=watcher.start, daemon=True)
    thread.start()
    
    print("Forge orchestration monitor active!")
    return watcher

# Start monitoring
watcher = forge_orchestration_monitor()
```

### Step 5: Common Forge Commands

```bash
# Monitor all team activity
python synapsewatcher.py

# Track specific agent output
python synapsewatcher.py --from ATLAS --keywords "complete,deployed"

# Priority only (orchestration alerts)
python synapsewatcher.py --priority HIGH --priority CRITICAL
```

### Next Steps for Forge

1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) → Forge section
2. Try [EXAMPLES.md](EXAMPLES.md) → Example 5 (Orchestration workflow)
3. Add to your session startup routine
4. Create custom callbacks for task tracking

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Receive task assignments and feedback instantly

### Step 1: Installation Check

```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseWatcher
python synapsewatcher.py --version
```

### Step 2: Watch for Atlas Messages

```bash
# Filter to messages for ATLAS
python synapsewatcher.py --to ATLAS

# Expected output when message arrives:
# ================================================================================
# [NEW MESSAGE] forge_task_20260204
# From: FORGE
# To: ATLAS
# Priority: NORMAL
# Subject: Build SynapseWatcher Phase 7 Docs
# ================================================================================
```

### Step 3: Python Integration for Build Sessions

```python
# Atlas build session with task detection
from synapsewatcher import SynapseWatcher, MessageFilter

def atlas_task_monitor():
    """Monitor for task assignments during build session."""
    
    watcher = SynapseWatcher()
    watcher.set_filter(MessageFilter(to_agent="ATLAS"))
    
    def handle_task(message):
        print(f"\n[NEW TASK] {message.subject}")
        print(f"From: {message.from_agent}")
        print(f"Priority: {message.priority}")
        
        # Priority handling
        if message.priority == "HIGH":
            print("[!] HIGH PRIORITY - Consider interrupting current work")
        
        # Auto-acknowledge
        from synapselink import quick_send
        quick_send(
            message.from_agent,
            f"Re: {message.subject}",
            "Received! Will review shortly.",
            priority="NORMAL"
        )
    
    watcher.register_callback(handle_task)
    
    import threading
    thread = threading.Thread(target=watcher.start, daemon=True)
    thread.start()
    
    return watcher

# Start at session begin
watcher = atlas_task_monitor()
```

### Step 4: Common Atlas Commands

```bash
# Watch for Atlas assignments
python synapsewatcher.py --to ATLAS

# Watch for build-related keywords
python synapsewatcher.py --to ATLAS --keywords "build,fix,implement,test"

# Only high priority tasks
python synapsewatcher.py --to ATLAS --priority HIGH
```

### Step 5: Integration with Build Workflow

```python
# Add to build session start
def start_build_session():
    # 1. Start task monitor
    watcher = atlas_task_monitor()
    
    # 2. Announce session start
    from synapselink import quick_send
    quick_send("FORGE", "Atlas Online", "Ready for tasks!")
    
    # 3. Continue with build work...
    return watcher
```

### Next Steps for Atlas

1. Add to session startup template
2. Create task extraction callback
3. Integrate with TODO list management
4. Review [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Run as background daemon on Linux

### Step 1: Linux Installation

```bash
# Clone from GitHub (if not already present)
git clone https://github.com/DonkRonk17/SynapseWatcher.git
cd SynapseWatcher

# Or sync from Windows (WSL)
cp -r /mnt/c/Users/logan/OneDrive/Documents/AutoProjects/SynapseWatcher ~/

# Verify installation
python3 synapsewatcher.py --version
```

### Step 2: First Watch (Linux)

```bash
# Basic watch
python3 synapsewatcher.py

# Watch for Clio messages
python3 synapsewatcher.py --to CLIO

# Watch with custom path (WSL)
python3 synapsewatcher.py --path "/mnt/d/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active"
```

### Step 3: Daemon Mode Setup

**Option A: Simple Background Process**

```bash
# Run in background with nohup
nohup python3 synapsewatcher.py --to CLIO > ~/synapse.log 2>&1 &

# Check if running
ps aux | grep synapsewatcher

# Stop
pkill -f synapsewatcher.py
```

**Option B: Systemd Service (Production)**

```bash
# Create service file
sudo nano /etc/systemd/system/synapsewatcher.service
```

```ini
[Unit]
Description=SynapseWatcher for CLIO
After=network.target

[Service]
Type=simple
User=logan
WorkingDirectory=/home/logan/SynapseWatcher
ExecStart=/usr/bin/python3 /home/logan/SynapseWatcher/synapsewatcher.py --to CLIO
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable synapsewatcher
sudo systemctl start synapsewatcher

# Check status
sudo systemctl status synapsewatcher

# View logs
journalctl -u synapsewatcher -f
```

### Step 4: Cron Alternative

```bash
# Edit crontab
crontab -e

# Add check every minute
* * * * * cd ~/SynapseWatcher && python3 -c "from synapsewatcher import SynapseWatcher; print('Check')" 2>&1 | logger -t synapse
```

### Step 5: Common Clio Commands

```bash
# Filter by sender
python3 synapsewatcher.py --from FORGE

# Filter by keywords
python3 synapsewatcher.py --keywords "clio,linux,ubuntu,server"

# Verbose mode for debugging
python3 synapsewatcher.py --to CLIO --verbose
```

### Next Steps for Clio

1. Set up systemd daemon for persistent monitoring
2. Configure log rotation
3. Add to ABIOS startup
4. Test with Synapse messages

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Cross-platform Synapse monitoring

### Step 1: Platform Detection

```python
# Nexus needs platform-aware paths
import platform
from pathlib import Path

system = platform.system()
print(f"Running on: {system}")

# Platform-specific Synapse paths
if system == "Windows":
    synapse_path = Path("D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")
elif system == "Linux":
    synapse_path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")
else:  # macOS
    synapse_path = Path.home() / "BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active"

print(f"Synapse path: {synapse_path}")
```

### Step 2: First Watch (Cross-Platform)

```bash
# Windows
python synapsewatcher.py --to NEXUS

# Linux
python3 synapsewatcher.py --to NEXUS --path "/mnt/d/BEACON_HQ/.../THE_SYNAPSE/active"

# macOS
python3 synapsewatcher.py --to NEXUS --path ~/BEACON_HQ/.../THE_SYNAPSE/active
```

### Step 3: Cross-Platform Python Integration

```python
from synapsewatcher import SynapseWatcher, MessageFilter
from pathlib import Path
import platform

def nexus_cross_platform_watcher():
    """Platform-aware Synapse watcher for Nexus."""
    
    # Detect platform and set path
    system = platform.system()
    
    if system == "Windows":
        synapse_path = Path("D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")
    elif system == "Linux":
        synapse_path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")
    else:
        synapse_path = Path.home() / "BEACON_HQ" / "MEMORY_CORE_V2" / "03_INTER_AI_COMMS" / "THE_SYNAPSE" / "active"
    
    # Create watcher
    watcher = SynapseWatcher(synapse_path=synapse_path)
    watcher.set_filter(MessageFilter(to_agent="NEXUS"))
    
    def platform_callback(message):
        print(f"[{system}] New message: {message.subject}")
    
    watcher.register_callback(platform_callback)
    return watcher

watcher = nexus_cross_platform_watcher()
```

### Step 4: VS Code Integration (Potential)

```python
# Future: VS Code extension integration
# For now, run in terminal

# Terminal 1: Start watcher
python synapsewatcher.py --to NEXUS

# Terminal 2: Continue development work
# Watcher alerts you to new messages
```

### Step 5: Common Nexus Commands

```bash
# Cross-platform (auto-detect path)
python synapsewatcher.py --to NEXUS

# Explicit Windows path
python synapsewatcher.py --path "D:/BEACON_HQ/.../THE_SYNAPSE/active"

# All platforms verbose
python synapsewatcher.py --to NEXUS --verbose
```

### Next Steps for Nexus

1. Test on all platforms (Windows, Linux, macOS)
2. Document platform-specific quirks
3. Consider VS Code extension integration
4. Add to multi-platform workflow

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Auto-detect and acknowledge task assignments

### Step 1: Verify Access (No API Required!)

```bash
# SynapseWatcher is FREE - no API keys needed!
cd C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseWatcher
python synapsewatcher.py --version

# It's pure Python - runs anywhere
```

### Step 2: Watch for Bolt Assignments

```bash
# Filter to Bolt messages
python synapsewatcher.py --to BOLT

# Filter for task keywords
python synapsewatcher.py --to BOLT --keywords "task,build,execute,implement"
```

### Step 3: Auto-Acknowledge Pattern

```python
from synapsewatcher import SynapseWatcher, MessageFilter
from synapselink import quick_send

def bolt_auto_responder():
    """Auto-acknowledge task assignments."""
    
    watcher = SynapseWatcher()
    watcher.set_filter(MessageFilter(to_agent="BOLT"))
    
    def auto_acknowledge(message):
        """Acknowledge receipt immediately."""
        # Check if it looks like a task
        task_keywords = ["task", "build", "fix", "implement", "execute", "create"]
        is_task = any(kw in message.subject.lower() for kw in task_keywords)
        
        if is_task:
            # Send acknowledgment
            quick_send(
                message.from_agent,
                f"Re: {message.subject}",
                "Task received and queued! Starting shortly.",
                priority="NORMAL"
            )
            print(f"[ACK] Acknowledged: {message.subject}")
        else:
            print(f"[INFO] Received: {message.subject}")
    
    watcher.register_callback(auto_acknowledge)
    
    import threading
    thread = threading.Thread(target=watcher.start, daemon=True)
    thread.start()
    
    return watcher

# Start auto-responder
watcher = bolt_auto_responder()
```

### Step 4: Cost-Free Batch Processing

```python
# Bolt can monitor multiple keywords efficiently
# No API cost - just CPU time!

def bolt_keyword_monitor():
    """Monitor for multiple trigger keywords."""
    
    watcher = SynapseWatcher()
    
    # Multiple keyword categories
    task_keywords = ["task", "build", "implement"]
    urgent_keywords = ["urgent", "asap", "critical"]
    
    def categorize_message(message):
        subject_lower = message.subject.lower()
        
        if any(kw in subject_lower for kw in urgent_keywords):
            print(f"[URGENT] {message.subject}")
        elif any(kw in subject_lower for kw in task_keywords):
            print(f"[TASK] {message.subject}")
        else:
            print(f"[INFO] {message.subject}")
    
    watcher.register_callback(categorize_message)
    return watcher
```

### Step 5: Common Bolt Commands

```bash
# Watch for Bolt assignments
python synapsewatcher.py --to BOLT

# Task-focused filtering
python synapsewatcher.py --to BOLT --keywords "task,build,fix"

# Watch everything (FREE!)
python synapsewatcher.py
```

### Next Steps for Bolt

1. Set up auto-acknowledge in Cline sessions
2. Create task extraction from messages
3. Build queue integration
4. Run continuously during work sessions

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/SynapseWatcher/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message ATLAS for complex issues

---

## 🎯 UNIVERSAL QUICK START (All Agents)

**60-Second Quick Start for Any Agent:**

```bash
# 1. Go to SynapseWatcher
cd C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseWatcher

# 2. Start watching for YOUR messages
python synapsewatcher.py --to YOUR_AGENT_NAME

# 3. That's it! You'll see new messages instantly
```

```python
# Python one-liner
from synapsewatcher import SynapseWatcher; w = SynapseWatcher(); w.register_callback(lambda m: print(m.subject)); w.start()
```

---

**Last Updated:** February 4, 2026  
**Maintained By:** ATLAS (Team Brain)

---

**SynapseWatcher** - Instant notifications for instant collaboration! ⚡
