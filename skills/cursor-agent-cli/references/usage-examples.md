# Cursor Agent Usage Examples

## Scenario 1: Planning a Refactor (Plan Mode)

**User Intent**: "Plan how to refactor the database layer to use a repository pattern."

**Command**:

```bash
cursor-agent --print --mode plan "Analyze the current database layer and propose a refactor plan to use the repository pattern. Focus on decoupling the business logic from the ORM."
```

## Scenario 2: Explaining Complex Code (Ask Mode)

**User Intent**: "How does the authentication middleware work?"

**Command**:

```bash
cursor-agent --print --mode ask "Explain the logic in src/middleware/auth.ts and how it validates JWT tokens."
```

## Scenario 3: Automated Bug Fix (Default Mode)

**User Intent**: "Fix the failing tests in the user service."

**Approval Prompt**: "I've detected that this task requires full agent permissions to modify files and execute commands. OK to proceed with `cursor-agent`?"

**Command**:

```bash
cursor-agent --print "Run the tests in services/user-service.test.ts, identify the cause of any failures, and apply the necessary fixes."
```

## Scenario 4: Exploring MCP Tools

**User Intent**: "What tools are available in the 'google-search' MCP?"

**Command**:

```bash
cursor-agent mcp list-tools google-search
```

## Scenario 5: Generating Project Rules

**User Intent**: "Create a rule for consistent error handling."

**Command**:

```bash
cursor-agent generate-rule "Ensure all API endpoints follow the RFC 7807 problem details standard for error responses."
```

## Scenario 6: Resuming a Prior Session

**User Intent**: "Continue from where I left off in the last session."

**Command**:

```bash
# Resume the most recent conversation
cursor-agent --resume

# Resume a specific conversation by thread ID
cursor-agent --resume <thread-id>

# List all available prior conversations
cursor-agent ls
```

## Scenario 7: Cloud Handoff for Background Execution

**User Intent**: "Start this long-running migration task and let it continue while I'm away."

**Usage** (within interactive `cursor-agent` session):

```text
& Run the full database migration, execute all integration tests, and open a PR if tests pass.
```

The agent hands off to Cursor's Cloud Agent and continues asynchronously. Resume at `cursor.com/agents`.
