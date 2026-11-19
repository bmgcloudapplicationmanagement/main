# Google Compute Engine Configuration

## Virtual Machine Specifications

| Configuration | Value |
|---|---|
| Instance name | bike-repair-vm |
| Region | europe-west1 (Belgium) |
| Zone | europe-west1-b |
| Machine type | e2-small |
| vCPU | 2 (shared-core) |
| RAM | 2 GB |
| Operating system | Ubuntu Minimal 24.04 LTS |
| Storage | 20 GB balanced persistent disk |
| External IP | Ephemeral |
| Estimated monthly cost | $15.45 |

## Configuration Justification

The E2-small instance was selected to provide
sufficient resources for a lightweight containerised
application while minimising infrastructure costs.

A European region was selected because the case
study business operates in Ireland.

Ubuntu was selected for its Docker compatibility
and support for Linux-based application deployment.

## Cost Management

The virtual machine will be stopped when not
in use to minimise compute charges. Persistent
storage costs will continue to apply.
