# /init privacy contract

`/init` is powerful because it can inspect local Hermes history. Treat that access as narrowly scoped.

## Allowed by default when the user invokes `/init`

Read-only local inspection of:

- Hermes `state.db` session/message tables
- visible user/assistant message content needed to identify workflows
- session metadata such as source, title, timestamps, model, counts
- tool names/counts without tool-call arguments
- installed skill names/descriptions
- non-secret profile files such as `SOUL.md`, `USER.md`, `MEMORY.md`, `MACHINE.md`, when present
- safe file metadata needed to understand the Hermes installation

## Excluded from mining/export

Do not persist or intentionally inspect:

- provider reasoning / chain-of-thought columns
- `reasoning`, `reasoning_content`, `reasoning_details`
- Codex reasoning/message replay blobs
- `api_content`
- system prompts stored in session metadata
- model configuration blobs that may contain provider details
- raw tool-call arguments
- `.env` contents
- browser cookies/session storage
- API tokens, keys, passwords, credential files
- private keys

## Redaction

The audit script redacts common credential patterns from visible message text before writing its private corpus. Treat this as defense in depth, not permission to surface secrets.

If a message contains something that still looks credential-like, omit it from evidence notes.

## Persistence

Audit artifacts belong under:

```text
$HERMES_HOME/init-audit/<timestamp>/
```

They are private working files. Never copy them into a public skill repository, commit them, upload them, or include raw history in generated public docs unless the user explicitly requests that specific action.

Generated general-purpose skills should contain generalized workflow rules, not private quotes, names, account information, client data, or project secrets.

## Communication

Report aggregate evidence such as:

> Video-production requests occurred across 14 sessions; repeated friction was capture setup and unverified final renders.

Avoid unnecessary raw quoting of historical messages.

## Side effects

Normal `/init` authorizes the read-only audit and writing its private local report. It does **not** authorize:

- software installation
- provider signup
- spending API credits
- sending/publishing/deploying
- deleting or rewriting Hermes history
- modifying global Hermes configuration
- publishing generated skills

`/init auto` additionally authorizes creating/updating the top recommended **local skill files** after analysis. All other side-effect gates remain in force.

## Database safety

Open SQLite using read-only mode. Do not run migrations, VACUUM, PRAGMA writes, deletes, updates, or cleanup against the user's live `state.db`.

Hermes uses WAL mode and may be writing concurrently. Keep queries bounded/simple and tolerate a transient read failure by reporting it rather than attempting to repair the database.