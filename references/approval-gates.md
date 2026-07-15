# Approval Gates

Pause before taking actions that cross a boundary the user has not authorized.

## Requires Explicit Approval

- Deploying, publishing, promoting, or making public changes.
- Sending email, Slack, texts, forms, comments, invites, or external messages.
- Charging money, changing billing, canceling services, or buying tools.
- Deleting, overwriting, resetting, or migrating data.
- Changing production configuration, DNS, auth, permissions, or secrets.
- Opening a pull request or commit if the user only asked for review.
- Installing a skill or plugin into a user or workspace location.

## Safe Without Additional Approval

- Reading local files in the provided workspace.
- Creating drafts, previews, plans, local artifacts, or validation reports.
- Running non-mutating diagnostics.
- Editing deliverables inside the task output folder when the user asked to build or prepare something.

## Response Pattern When Approval Is Missing

Return:

- what is ready
- what action needs approval
- why approval is required
- the exact command/action that would run after approval, if useful
