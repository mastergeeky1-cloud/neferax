# Scaling Plan — Neferax Framework

## Current State
- 89 pentesting tools across 11 categories
- 11 attack chains (scan, recon, web, exploit, brute, osint, ad, wireless, password, sql, full)
- CLI + TUI dual interface
- HTML reporting per tool + aggregated chain reports
- Permission-aware execution

## Phase 1: Multi-Target & Batch Processing

### Parallel Execution (Next)
```bash
# Scan multiple targets simultaneously
neferax scan --parallel --threads 10 targets.txt

# Batch file format (IP:port or URL per line)
neferax recon --input targets.txt --output-dir ./engagements/
```

**Implementation:**
- Add `--parallel` / `--threads N` flag to chains
- Use `concurrent.futures.ThreadPoolExecutor` for parallel tool runs
- Per-thread HTML reports merged into single engagement report
- Rate limiting to avoid DoS detection

### CIDR / Range Expansion
```bash
# Auto-expand CIDR ranges
neferax scan 10.10.10.0/24 --expand
# Expands to individual IPs, runs tools on each
```

## Phase 2: Distributed Architecture

### Agent Mode
```
┌─────────────┐     ┌──────────┐     ┌──────────┐
│   Neferax    │────▶│ Agent 1  │────▶│  Target  │
│   (Server)   │     ├──────────┤     │  Network │
│              │────▶│ Agent 2  │────▶│          │
│  Web UI +    │     ├──────────┤     └──────────┘
│   Reports    │────▶│ Agent N  │
└─────────────┘     └──────────┘
```

- Server distributes scan jobs to remote agents
- Agents run tools, stream results back
- Single pane-of-glass reporting

### Message Queue (Redis / NATS)
- Jobs published to Redis streams
- Workers consume and execute
- Results stored in PostgreSQL/MongoDB

## Phase 3: Database-Backed Storage

### Schema
```
engagements
├── id, name, target, status, created_at
├── tools_results
│   ├── id, engagement_id, tool, target, output, exit_code, duration
│   └── findings
│       ├── id, result_id, severity, title, description, cve, remediation
└── reports
    └── id, engagement_id, format (html/pdf/json), path
```

### Queries
```sql
-- All critical findings across all engagements
SELECT * FROM findings WHERE severity = 'critical';

-- Tool performance stats
SELECT tool, AVG(duration), COUNT(*) FROM tools_results GROUP BY tool;
```

## Phase 4: Plugin System

```python
# /usr/share/hackingtool/plugins/my_tool.py
from nefereax.plugin import BaseTool

class MyCustomTool(BaseTool):
    name = "my_tool"
    category = "recon"
    methods = ["custom_scan", "api_enum"]
    
    def run(self, target):
        # Custom logic
        return self.report(output, exit_code)
```

- Hot-reload plugins from `~/.hackingtool/plugins/`
- Community plugin marketplace
- Each plugin self-documents its methods, requirements, and dependencies

## Phase 5: API-First Architecture

### REST API
```
GET  /api/v1/tools                    # List all tools
POST /api/v1/scan                     # Start a scan
GET  /api/v1/scan/{id}                # Get scan status
GET  /api/v1/scan/{id}/results        # Get scan results
GET  /api/v1/scan/{id}/report         # Download HTML/PDF report
POST /api/v1/chain/{name}             # Run attack chain
```

### Web Dashboard
- Real-time scan progress via WebSocket
- Interactive findings browser
- Timeline view of execution
- Export to PDF, JSON, CSV, Splunk

## Phase 6: CI/CD Integration

```yaml
# .github/workflows/security-scan.yml
- uses: mastergeeky1-cloud/neferax-action@v1
  with:
    target: ${{ secrets.SCAN_TARGET }}
    chain: full
    output: report.html
```

- GitHub Action wrapper
- Slack / Discord / Email notifications
- Jira ticket creation for findings

---

## Additional Power Tools to Add

### Cloud Security (10 tools)
| Tool | Purpose | Install |
|---|---|---|
| `s3scanner` | Find open S3 buckets | `pip install s3scanner` |
| `cloudfox` | Cloud pentesting (AWS/Azure/GCP) | `go install` |
| `prowler` | AWS security auditing | `pip install prowler` |
| `scoutsuite` | Multi-cloud security | `pip install scoutsuite` |
| `gcp-scanner` | GCP resource enumeration | `pip install gcp-scanner` |
| `cloudsploit` | Cloud security scanning | `npm install -g cloudsploit` |
| `kics` | Infrastructure-as-Code scanner | `brew install kics` |
| `tfsec` | Terraform security scanner | `go install` |
| `checkov` | IaC misconfiguration scanner | `pip install checkov` |
| `azucar` | Azure security auditing | `git clone` |

### Container Security (8 tools)
| Tool | Purpose | Install |
|---|---|---|
| `trivy` | Container vuln scanner | `apt install trivy` |
| `grype` | Container vulnerability DB | `apt install grype` |
| `kubectl` | Kubernetes CLI | `apt install kubectl` |
| `kube-hunter` | K8s penetration testing | `pip install kube-hunter` |
| `kubescape` | K8s security scanning | `curl | bash` |
| `popeye` | K8s cluster sanitizer | `go install` |
| `dockle` | Dockerfile linter | `apt install dockle` |
| `hadolint` | Dockerfile linting | `apt install hadolint` |

### Mobile Security (5 tools)
| Tool | Purpose | Install |
|---|---|---|
| `apktool` | APK reverse engineering | `apt install apktool` |
| `dex2jar` | DEX to JAR converter | `apt install dex2jar` |
| `jadx` | Dex to Java decompiler | `apt install jadx` |
| `objection` | Runtime mobile exploration | `pip install objection` |
| `mobsf` | Mobile security framework | `docker run opensecurity/mobsf` |

### Advanced Exploitation (7 tools)
| Tool | Purpose | Install |
|---|---|---|
| `bloodhound` | AD attack path mapping | `apt install bloodhound` |
| `certipy` | AD CS exploitation | `pip install certipy-ad` |
| `krbrelayx` | Kerberos relay attacks | `pip install krbrelayx` |
| `kerbrute` | Kerberos user enumeration | `go install` |
| `donpapi` | AD dump tool | `git clone` |
| `chisel` | Fast TCP/UDP tunnel | `go install` |
| `ligolo-ng` | Advanced tunneling proxy | `go install` |

### Automation & Reporting (5 tools)
| Tool | Purpose | Install |
|---|---|---|
| `nuclei` | Fast YAML-based vuln scanner | `go install` |
| `catp` | Automated pentest platform | `docker compose` |
| `pe-parse` | Windows PE parser | `apt install pe-parse` |
| `flare-floss` | Malware string extractor | `pip install flare-floss` |
| `dcfldd` | Enhanced dd for forensics | `apt install dcfldd` |

---

## Implementation Priority

1. **Weeks 1-2**: Parallel execution, batch input files, CIDR expansion
2. **Weeks 3-4**: Plugin system, community tool sharing
3. **Weeks 5-6**: REST API, web dashboard MVP
4. **Weeks 7-8**: Database storage, findings management
5. **Weeks 9-10**: Agent mode, distributed scanning
6. **Weeks 11-12**: CI/CD integration, marketplace

## Resource Requirements

| Phase | CPU | RAM | Storage | Network |
|---|---|---|---|---|
| Current | 2 cores | 4 GB | 10 GB | 100 Mbps |
| Phase 1 | 4 cores | 8 GB | 20 GB | 100 Mbps |
| Phase 2-3 | 8 cores | 16 GB | 100 GB | 1 Gbps |
| Phase 4-6 | 16+ cores | 32 GB | 500 GB | 1 Gbps |

## Security Considerations

- All agents authenticate via mutual TLS
- Scan results encrypted at rest (AES-256) and in transit (TLS 1.3)
- Role-based access control (viewer, operator, admin)
- Audit logging for all actions
- Rate limiting to prevent target overwhelm
- Safe mode: dry-run to validate config before execution
