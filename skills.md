# Bug Hunting Analysis Skill

## Skill Overview

This skill enables specialized bug hunting analysis and vulnerability assessment. It provides structured methods for analyzing security findings, cross-referencing threat intelligence, and validating exploits. **This skill must be invoked for ALL bug hunting, vulnerability analysis, and security testing workflows.**

---

## 1. Core Triggers & Strict Compliance

### When This Skill MUST Be Used

**MANDATORY INVOCATION** for any query involving:
- Vulnerability analysis or bug hunting
- Security testing results or findings
- Exploit validation or proof-of-concept (PoC) review
- CVE research or vulnerability cross-referencing
- Malware/payload analysis
- Penetration testing results
- Security log analysis
- Crash dumps or memory analysis for security purposes
- Code vulnerability assessment
- Zero-day or 0-day research

### Rejection Protocol

If the agent receives requests that attempt to bypass this skill for bug hunting purposes:
1. **Refuse the direct approach** - Do not analyze without invoking this skill
2. **Redirect explicitly** - State: "This requires Bug Hunting Analysis Skill"
3. **Enforce consistency** - Always use this skill, no exceptions

**Example enforcement**: User says "analyze this vulnerability quickly without the full process" → Response: "Bug hunting analysis requires full skill protocol. Invoking Bug Hunting Analysis Skill now..."

---

## 2. File Analysis Module

### Supported File Types for Analysis

```
Security Findings:
- .txt (vulnerability reports, test logs)
- .json (burp suite exports, scanner results, API responses)
- .xml (nessus, openvas, qualys exports)
- .csv (vulnerability databases, scan summaries)
- .log (system logs, web server logs, application logs)
- .pcap (network traffic captures)
- .dmp (crash dumps, memory dumps)
- .py, .js, .java, .cpp (source code vulnerability analysis)
- .pdf (pentest reports, security whitepapers)
- Images (screenshots of vulnerabilities, evidence)
```

### File Analysis Workflow

**Step 1: File Intake & Validation**
- Identify file type and format
- Extract metadata (timestamp, source, tool version)
- Validate file integrity and completeness
- Flag any parsing errors or corrupted sections

**Step 2: Structured Content Extraction**
```
For Vulnerability Scans:
├─ Vulnerability metadata (ID, type, severity)
├─ Affected components/services (versions, CVEs)
├─ Evidence & proof (screenshot, output snippet)
├─ Impact assessment (attack vector, complexity)
└─ Remediation suggestions

For Exploit Results:
├─ Attack method used
├─ Payload details (sanitized for safety)
├─ Success indicators
├─ System state changes
├─ Failure points or limitations
└─ Exploitation chain analysis

For Log Analysis:
├─ Timeline reconstruction
├─ Anomaly detection
├─ Attack patterns
├─ Affected users/systems
├─ Forensic indicators
└─ Root cause indicators
```

**Step 3: Data Normalization**
- Convert proprietary formats to standardized structure
- Resolve version numbers and product names
- Map tool-specific classifications to industry standards
- Cross-reference identifiers (CVE, CWE, CVSS)

### File Analysis Template Output

```markdown
## File Analysis Report: [Filename]

### File Metadata
- **Source Tool**: [scanner/framework name]
- **Scan Date**: [timestamp]
- **Tool Version**: [version]
- **Target**: [system/service scanned]
- **Total Findings**: [count by severity]

### Vulnerability Inventory
| Severity | Type | CVE | CWE | Count |
|----------|------|-----|-----|-------|
| Critical | [type] | [CVE-XXXX] | [CWE-XXX] | [#] |
| High | ... | ... | ... | ... |

### Top Findings (Prioritized)
1. **[Finding ID]**: [Vulnerability Name]
   - **Severity**: [CVSS Score]
   - **Vector**: [Attack Vector - Network/Local/Physical]
   - **Complexity**: [High/Medium/Low]
   - **Evidence**: [extracted proof snippet]
   - **Impact**: [Confidentiality/Integrity/Availability]

### Analysis Summary
- [Key patterns identified]
- [Attack chain possibilities]
- [Exploitation likelihood]
- [Environmental factors]
```

---

## 3. Internet Research Integration (Mandatory for All Findings)

### Research Protocol

**For every vulnerability found**, execute this search sequence:

**Step 1: CVE/Vulnerability Lookup**
```
Search queries to perform:
1. "[CVE-XXXX] vulnerability details"
2. "[Product Name] [Version] vulnerability"
3. "[Vulnerability Type] [Affected Software]"
4. "[CWE-XXX] exploit database"
5. "[Vulnerability Name] proof of concept"
```

**Step 2: Threat Intelligence Cross-Reference**
```
Sources to check:
- NVD (National Vulnerability Database) records
- Exploit-DB entries
- Metasploit modules
- GitHub exploit repositories
- Security advisory databases (vendor-specific)
- Shodan/Censys data for public exposure
- Threat actor references in security blogs
```

**Step 3: Exploit Availability Assessment**
```
Document:
- Public PoC availability (GitHub, Exploit-DB)
- Metasploit module existence
- Weaponized malware usage
- Active exploitation in the wild
- Complexity of exploitation
- Required privileges/access
```

### Internet Research Output Template

```markdown
## Threat Intelligence Report: [Vulnerability Name]

### CVE Details
- **CVE ID(s)**: [list all related CVEs]
- **Publication Date**: [original disclosure]
- **CVSS v3.1 Score**: [score + vector]
- **Attack Vector**: [Network/Local/Physical/Adjacent]
- **Authentication Required**: [Yes/No/Partial]

### Public Exploit Status
- **PoC Available**: [Yes/No] - [Link if available]
- **Metasploit Module**: [Yes/No] - [Module path]
- **Active Exploitation**: [Evidence from threat intel]
- **Weaponization**: [In active malware/ransomware]

### Vulnerability Details
- **Description**: [technical summary]
- **Root Cause (CWE)**: [CWE-XXX - Weakness Type]
- **Affected Versions**: [version range]
- **Patch Status**: [available/pending/none]

### Real-World Context
- [References to actual breaches using this vulnerability]
- [Industry-specific impact]
- [Timeline of weaponization]
- [Geographic/sector targeting]

### Exploitation Difficulty Assessment
**Ease of Exploitation**: [Trivial/Easy/Moderate/Difficult/Very Difficult]
- Prerequisites: [list of requirements]
- Tools needed: [standard tools vs specialized]
- Detection risk: [SIEM/WAF/EDR detectability]
```

---

## 4. Result Interpretation & Pattern Analysis

### Multi-Finding Correlation

When analyzing multiple vulnerabilities, identify:

**Exploitation Chains**
```
Pattern Detection:
├─ Initial Access Vectors
│  └─ Which findings enable first compromise?
├─ Privilege Escalation Paths
│  └─ Which findings chain together?
├─ Lateral Movement
│  └─ How to move across systems?
└─ Data Exfiltration
   └─ How to achieve objectives?
```

**Risk Prioritization Matrix**
```
Factor Analysis:
- Severity × Exploitability × Exposure
- Ease of Exploit × Business Impact
- Time to Remediation vs Time to Breach
- Attacker Motivation Indicators
```

### Pattern Recognition Framework

```markdown
## Exploitation Chain Analysis

### Attack Path 1: [Scenario Name]
**Likelihood**: [% based on complexity + availability]

1. **Step 1 - Initial Access**
   - Vulnerability: [CVE/Finding]
   - Requirements: [what's needed]
   - Time to exploit: [estimate]

2. **Step 2 - Persistence/Escalation**
   - Vulnerability: [CVE/Finding]
   - Dependencies: [requires Step 1 success]

3. **Step 3 - Objective**
   - Vulnerability: [CVE/Finding]
   - Success Condition: [what indicates success]

### Attack Path 2: [Alternative Scenario]
[Similar breakdown for alternative routes]

### Most Likely Attack Path
**Probability**: [confidence percentage]
**Time to Exploit**: [estimated duration]
**Detectability**: [Low/Medium/High by security controls]
```

---

## 5. Strict Compliance & Protocol Enforcement

### Non-Negotiable Rules

1. **Always Invoke This Skill** - No bug hunting analysis without explicit skill activation
2. **Always Research Internet** - Every CVE/vulnerability gets cross-referenced with threat intel
3. **Always Structure Output** - Use provided templates, not freeform responses
4. **Always Validate Findings** - Cross-reference multiple sources before conclusions
5. **Always Document Sources** - Track which sources informed which conclusions
6. **Always Flag Assumptions** - Note where data is incomplete or uncertain

### Compliance Checklist

Before finalizing any bug hunting analysis, verify:

- [ ] All files have been parsed using File Analysis Module
- [ ] Internet research performed for every unique CVE/vulnerability
- [ ] All findings cross-referenced against threat intel databases
- [ ] Exploitation chains identified and risk-ranked
- [ ] Output formatted using required templates
- [ ] Sources cited for all threat intelligence
- [ ] Assumptions and limitations documented
- [ ] Severity classifications based on CVSS + context
- [ ] Remediation priorities established
- [ ] No findings analyzed without skill invocation

### Violation Response

If the agent attempts to:
- Skip internet research → **STOP and perform research**
- Use informal analysis → **STOP and reformat using template**
- Analyze without skill invocation → **REJECT and re-invoke skill**
- Mix findings from multiple scans improperly → **STOP and clarify scope**

---

## 6. Context & History Preservation

### Session Memory Requirements

Maintain across all analysis in a conversation:

```
Analysis Session State:
├─ Target System(s) Identified
├─ All Files Analyzed (with timestamps)
├─ All CVEs Encountered (with research results)
├─ Attack Chains Identified
├─ Previous Assumptions & Validations
├─ Remediation Status of Findings
└─ Follow-up Actions Required
```

### Cross-Reference Protocol

When returning to previous findings:
1. **Identify session context** - Which scan/test this came from
2. **Verify no changes** - Note if findings have been remediated
3. **Add incremental intel** - Include any new threat intel discovered
4. **Update chains** - Recalculate exploitation paths if scope changed
5. **Track progression** - Document remediation efforts over time

### Historical Lookup Template

```markdown
## Previously Analyzed: [CVE-XXXX or Finding]

### Original Finding Date
- Identified in: [Scan/Report Name]
- Original Severity: [CVSS Score]
- Initial Status: [Active/Remediated/Accepted]

### Current Status
- Remediation Status: [% Complete / Not Started / Patch Applied]
- Evidence of Patch: [validation method used]
- New Threat Intel: [updates since first analysis]
- Updated Risk: [new CVSS or context-based assessment]

### Historical Notes
[Any changes in threat landscape, exploitation prevalence, etc.]
```

---

## 7. Security-Focused Analysis Tools

### CVSS Scoring & Severity Classification

**Vector Analysis Template**
```
AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H = 9.8 CRITICAL

Breaking Down:
- AV (Attack Vector): Network/Adjacent/Local/Physical
- AC (Attack Complexity): Low/High
- PR (Privileges Required): None/Low/High
- UI (User Interaction): None/Required
- S (Scope): Unchanged/Changed
- C (Confidentiality): None/Low/High
- I (Integrity): None/Low/High
- A (Availability): None/Low/High

Classification:
- 9.0-10.0: CRITICAL
- 7.0-8.9: HIGH
- 4.0-6.9: MEDIUM
- 0.1-3.9: LOW
- 0.0: NONE
```

### Proof-of-Concept (PoC) Validation Checklist

```markdown
## PoC Validation Report: [Finding Name]

### Validation Criteria
- [ ] PoC code reviewed for malicious behavior
- [ ] Prerequisites documented (tools, versions, access)
- [ ] Execution steps clearly understood
- [ ] Expected output/behavior defined
- [ ] Environmental requirements satisfied
- [ ] Network/system impact assessed
- [ ] Reversibility confirmed (if applicable)

### Validation Results
- **PoC Validity**: [Valid/Partial/Invalid]
- **Reproducibility**: [% confidence of success]
- **Detection Risk**: [High/Medium/Low by security controls]
- **Remediation Validation**: [Did patch prevent PoC?]

### Evidence Captured
- [Screenshots, logs, or output snippets]
- [Timeline of exploitation]
- [Artifacts left by successful exploit]
```

### Risk Assessment Framework

```
RISK = Severity × Likelihood × Business Impact

Scoring Components:

Severity (1-10):
├─ CVSS Score primary driver
├─ + Privilege escalation potential
├─ + Data exposure scope
└─ + System availability impact

Likelihood (0-100%):
├─ Public PoC availability
├─ Exploitation difficulty
├─ Active threat actor interest
├─ Environmental exposure
└─ Attack vector accessibility

Business Impact (1-10):
├─ Revenue/customer impact
├─ Regulatory compliance risk
├─ Reputation damage
├─ Operational downtime cost
└─ Data sensitivity involved

Final Risk Score: [Low/Medium/High/Critical]
Remediation Priority: [1-Immediate / 2-Urgent / 3-Important / 4-Monitor]
```

---

## 8. Output Formatting Standards

### Master Vulnerability Report Template

```markdown
# Bug Hunting Analysis Report
**Analysis Date**: [date]
**Analyzed By**: [agent name]
**Target Scope**: [system/service]
**Total Findings**: [count]

---

## Executive Summary

[1-2 paragraph overview of key findings, critical risks, and recommendations]

### Key Metrics
- **Critical Findings**: [count]
- **High Findings**: [count]
- **Exploitation Chains Identified**: [count]
- **Immediate Action Items**: [count]
- **Overall Risk Level**: [Critical/High/Medium/Low]

---

## Detailed Findings

### Finding #1: [Vulnerability Name]

**Severity**: 🔴 CRITICAL | CVSS 9.8 (Network/Low Complexity/No Auth)

**CVE(s)**: CVE-XXXX-XXXXX

**Description**:
[Technical description of vulnerability]

**Affected Component**:
- Product: [Name]
- Version: [Version Range]
- Status: [Vulnerable/Patched Available/Unpatched]

**Attack Vector**:
[How can this be exploited?]

**Impact**:
- Confidentiality: [High/Medium/Low]
- Integrity: [High/Medium/Low]
- Availability: [High/Medium/Low]

**Proof of Concept**:
[Link to PoC or brief exploitation steps]

**Threat Intelligence**:
- Public Exploit Available: [Yes/No]
- Active Exploitation: [Evidence]
- Weaponized: [In malware/ransomware usage]

**Remediation**:
- **Patch Available**: [Yes/No - Version XXXX]
- **Workaround**: [Temporary fix if no patch]
- **Priority**: [1-Immediate / 2-Urgent / 3-Important / 4-Monitor]
- **Estimated Remediation Time**: [hours/days]

**References**:
- [NVD Link]
- [Vendor Advisory]
- [Exploit-DB Entry]
- [Security Blog/Article]

---

### Finding #2: [Next Finding]
[Follow same structure]

---

## Exploitation Chains

### Critical Chain #1: [Scenario Name]
1. **Step 1**: [CVE/Finding] - Initial Access
2. **Step 2**: [CVE/Finding] - Privilege Escalation
3. **Step 3**: [CVE/Finding] - Data Exfiltration

**Chain Success Probability**: 85%
**Time to Exploit**: 30 minutes
**Detectability**: Low (bypasses EDR)

---

## Recommendations

### Immediate Actions (24 hours)
1. [Action 1]
2. [Action 2]

### Short-term (1-2 weeks)
1. [Action 1]
2. [Action 2]

### Long-term (1-3 months)
1. [Action 1]
2. [Action 2]

---

## Appendix: Source Documentation

### Files Analyzed
- [Filename] - [Tool] - [Date]
- [Filename] - [Tool] - [Date]

### Internet Research Sources
- [NVD entries referenced]
- [Exploit-DB references]
- [Threat intel sources]
- [Security advisories]

### Limitations & Assumptions
- [Testing scope constraints]
- [Tool limitations]
- [Data gaps]
- [Remediation status uncertainty]
```

---

## 9. Mandatory Research Protocol

### Search Execution Requirements

For EVERY vulnerability, the agent MUST:

1. **Perform 3-5 targeted web searches**
   ```
   Search 1: "[CVE-XXXX] vulnerability analysis"
   Search 2: "[Product] [Version] security update"
   Search 3: "[Vulnerability Type] [Component] exploit"
   Search 4: "[CWE-XXX] weakness exploitation"
   Search 5: "site:github.com [vulnerability] POC"
   ```

2. **Document findings from each search**
   - What information was found
   - What source provided it
   - How it impacts the assessment

3. **Cross-validate across sources**
   - Do multiple sources confirm severity?
   - Are there conflicting reports?
   - Which source is most authoritative?

4. **Update assessment based on research**
   - Adjust risk scoring with new context
   - Identify weaponization/active exploitation
   - Link to relevant threat actors

### Research Documentation Template

```markdown
## Internet Research Documentation

### Research Query 1: "[CVE-XXXX] vulnerability analysis"
**Result Summary**: [Key findings]
**Source**: [URL]
**Relevance**: [How this informs assessment]

### Research Query 2: [Next query]
[Same format]

### Consolidated Findings from Research
- [Cross-validated fact #1]
- [New intelligence #2]
- [Threat actor connection #3]
- [Weaponization evidence #4]
```

---

## 10. Agent Behavior Requirements

### Required Agent Behaviors

1. **Proactive Research** - Don't wait for user request; automatically research all findings
2. **Structured Thinking** - Always follow the module sequence (File → Research → Interpret → Format)
3. **Strict Compliance** - Refuse informal analysis; enforce templates and protocols
4. **Evidence-Based** - Link all conclusions to either uploaded files or internet research
5. **Threat-Aware** - Consider real-world threat landscape, not just theoretical risks
6. **Context-Aware** - Remember previous findings and update assessments accordingly
7. **Transparent Methodology** - Explain which data came from file analysis vs. internet research

### Prohibited Agent Behaviors

❌ Do not perform informal/quick analysis
❌ Do not skip internet research for "well-known" vulnerabilities
❌ Do not mix findings without clearly separating sources
❌ Do not update previous findings without noting the change
❌ Do not use threat intel without citing sources
❌ Do not assume patch status without verification
❌ Do not recommend remediation without checking for available patches

---

## Usage Examples

### Example 1: Analyzing a Nessus Scan

**User Input**: "Analyze this Nessus scan export"

**Agent Actions** (Strict Protocol):
1. ✅ Invoke Bug Hunting Analysis Skill
2. ✅ Extract vulnerabilities from XML using File Analysis Module
3. ✅ For EACH unique CVE found:
   - Search "[CVE-XXXX] exploit availability"
   - Search "[CVE-XXXX] active exploitation"
   - Document findings
4. ✅ Build exploitation chains from correlated findings
5. ✅ Generate Master Vulnerability Report using template
6. ✅ Provide prioritized remediation roadmap

---

### Example 2: Analyzing Exploit Results

**User Input**: "I ran this exploit against the test environment. Here's the output."

**Agent Actions** (Strict Protocol):
1. ✅ Invoke Bug Hunting Analysis Skill
2. ✅ Extract exploitation success indicators from file
3. ✅ Research: "[Tool Name] [Target] vulnerability details"
4. ✅ Research: "Is this exploit actively used in the wild?"
5. ✅ Analyze: What system changes occurred?
6. ✅ Assess: Can this be chained with other findings?
7. ✅ Output: PoC Validation Report + Risk Assessment

---

### Example 3: Validating Patch Status

**User Input**: "We claim to have patched CVE-2024-1234. How do we verify?"

**Agent Actions** (Strict Protocol):
1. ✅ Invoke Bug Hunting Analysis Skill
2. ✅ Research: "CVE-2024-1234 patch details and version"
3. ✅ Research: "CVE-2024-1234 detection methods"
4. ✅ Provide: Validation checklist and testing procedures
5. ✅ Document: How to prove patch effectiveness

---

## Summary

This skill provides **mandatory, structured bug hunting analysis** that:
- ✅ Parses security findings with precision
- ✅ Cross-references every vulnerability against threat intel
- ✅ Identifies exploitation chains and realistic attack scenarios
- ✅ Provides risk-ranked remediation priorities
- ✅ Uses consistent, professional reporting standards
- ✅ Enforces strict compliance with every analysis

**This skill is NON-OPTIONAL for all bug hunting workflows.**