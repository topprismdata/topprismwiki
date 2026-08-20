# FAQ

## Why are WeChat and Office adapters not bundled?

They involve private data, platform permissions and local tools. The public
package publishes a stable evidence contract so deployments can provide a
compatible adapter without publishing sensitive data or internal CLIs.

## Why is the dashboard read-only?

It is a rebuildable projection. Formal writes, retries and source governance must
go through the Runner and explicit authorization so a browser action cannot skip
evidence and transaction gates.

## Does `accepted` mean production knowledge is fully validated?

It means the reference Runner's batch and commit checks passed. Production still
needs adapter, entity, relationship, Obsidian and permission gates.

## Why do names and filenames not prove relationships?

They show co-occurrence, not customer, project, delivery, adoption or identity
evidence. Formal relationships require direct evidence and namespace validation.
