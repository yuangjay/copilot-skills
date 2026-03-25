---
name: system-redevelopment
description: 'Iterative system development and refinement. Use for creating or improving systems in an endless loop until they meet user requirements. Triggers on: iterative development, system refinement, re-development, continuous improvement, openclaw-like workflows.'
argument-hint: 'Describe the system to develop or refine (e.g., "build a recommendation engine", "improve the CI/CD pipeline")'
---

# System Redevelopment

## When to Use

Invoke this skill for tasks requiring iterative development and refinement of systems:
- Building new systems from scratch with user feedback loops
- Redeveloping or improving existing systems to meet evolving requirements
- Continuous improvement workflows, such as OpenClaw-like processes
- Debugging and optimizing systems through repeated cycles

## Procedures

### Initial Development

1. **Understand Requirements**:
   - Gather detailed user requirements.
   - Clarify ambiguous or conflicting needs.
2. **Draft the System**:
   - Create an initial version of the system based on the requirements.
   - Use modular and extensible design principles.
3. **Validate**:
   - Test the system against the initial requirements.
   - Identify gaps, bugs, or areas for improvement.

### Iterative Refinement

1. **Collect Feedback**:
   - Present the system to the user for review.
   - Gather specific feedback on what works and what doesn’t.
2. **Redesign and Redevelop**:
   - Address feedback by modifying or extending the system.
   - Ensure changes are incremental and reversible.
3. **Test and Validate**:
   - Re-test the system after each iteration.
   - Confirm that changes align with user expectations.
4. **Repeat**:
   - Continue the loop until the system fully meets user requirements.

### MANDATORY Deployment Decision Gate

> **THIS GATE MUST BE EXECUTED BEFORE ANY DEPLOYMENT STEP. NO EXCEPTIONS.**

Before deploying any application, follow this strict decision tree in order:

```
STEP 1: Run `docker --version` to check if Docker is available.
        └── If Docker IS available     → PROCEED with Docker Deployment (MANDATORY)
        └── If Docker is NOT available → PROCEED to STEP 2

STEP 2: Run `python -m venv --help` to check if venv is available.
        └── If venv IS available       → PROCEED with .venv Deployment
        └── If venv is NOT available   → PROCEED to STEP 3 (last resort only)

STEP 3: Direct deployment ONLY as absolute last resort.
        → Document clearly WHY Docker and .venv were skipped.
```

**RULE: You MUST NEVER skip Docker and go straight to .venv without first running `docker --version` and confirming Docker is unavailable.**

---

### Deployment Method 1: Docker (DEFAULT — ALWAYS TRY FIRST)

**ALWAYS create these files regardless of which deployment method is ultimately used:**
- `Dockerfile` — defines the container environment
- `docker-compose.yml` — for easier orchestration
- `.dockerignore` — to exclude unnecessary files

**Steps:**
1. Verify Docker is available: `docker --version`
2. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 5001
   CMD ["python", "app.py"]
   ```
3. Create `docker-compose.yml`:
   ```yaml
   version: '3'
   services:
     app:
       build: .
       ports:
         - "5001:5001"
   ```
4. Build: `docker build -t <app-name> .`
5. Run: `docker-compose up` or `docker run -p 5001:5001 <app-name>`
6. Verify the app is running by checking the exposed port.

---

### Deployment Method 2: Virtual Environment (.venv) — FALLBACK ONLY

**ONLY use this if Docker is confirmed unavailable. You MUST document why Docker was skipped.**

**Steps:**
1. Create: `python -m venv .venv`
2. Activate: `source .venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Run: `python app.py`
5. Include a `start.sh` script to automate these steps.

---

### Deployment Method 3: Direct Deployment — LAST RESORT ONLY

**ONLY use this if BOTH Docker AND .venv are confirmed unavailable. Document this explicitly.**

**Steps:**
1. Install dependencies globally: `pip install -r requirements.txt`
2. Run: `python app.py`
3. Document clearly: why Docker was unavailable, why .venv was unavailable.

### Finalization

1. **Document the System**:
   - Provide clear documentation for the final system.
   - Include usage instructions, limitations, and future improvement suggestions.
2. **Handover**:
   - Ensure the user is satisfied with the final system.
   - Transfer ownership and provide support for initial usage.

## Key Principles

- **User-Centric Design**: Always prioritize user feedback and requirements.
- **Incremental Changes**: Make small, testable changes in each iteration.
- **Reversibility**: Ensure changes can be undone if they don’t work as expected.
- **Continuous Validation**: Test the system after every change to ensure quality.
- **Documentation**: Keep records of changes and decisions for transparency.
- **Docker First — Non-Negotiable**: ALWAYS attempt Docker deployment first. NEVER skip it in favour of .venv or direct deployment without explicitly checking `docker --version` and confirming Docker is unavailable.
- **Fallback is NOT a Default**: `.venv` and direct deployment are fallbacks only — they MUST NOT be used as the default or convenient shortcut.
- **Audit Trail**: Always document which deployment method was used and why alternatives were skipped.

## Examples

**Build a Recommendation Engine:**
> `/system-redevelopment create a recommendation engine for e-commerce`

**Improve a CI/CD Pipeline:**
> `/system-redevelopment refine the CI/CD pipeline to reduce deployment time`

**Optimize a Search Algorithm:**
> `/system-redevelopment optimize the search algorithm for better relevance`

**Develop a Chatbot:**
> `/system-redevelopment build a chatbot for customer support`

### Comprehensive Software Development Lifecycle

#### Planning Phase
1. **Requirement Analysis**:
   - Conduct stakeholder interviews to gather requirements.
   - Create user stories, use cases, and acceptance criteria.
2. **Feasibility Study**:
   - Assess technical and financial feasibility.
   - Identify potential risks and mitigation strategies.

#### Design Phase
1. **System Architecture**:
   - Design the overall system architecture.
   - Use UML diagrams for clarity.
2. **UI/UX Prototyping**:
   - Create wireframes and mockups.
   - Use tools like Figma or Adobe XD.

#### Development Phase (TDD Focus)
1. **Test-Driven Development (TDD)**:
   - Write test cases before writing code.
   - Use tools like `pytest`, `unittest`, or `Jest`.
2. **Incremental Development**:
   - Implement features iteratively.
   - Ensure each feature passes its test cases before proceeding.
3. **Continuous Integration (CI)**:
   - Set up CI pipelines for automated testing.
   - Use tools like GitHub Actions, Jenkins, or GitLab CI.

#### Testing Phase
1. **Unit Testing**:
   - Test individual components in isolation.
   - Ensure high code coverage.
2. **Integration Testing**:
   - Test interactions between components.
   - Use tools like Postman for API testing.
3. **End-to-End Testing**:
   - Simulate real-world user scenarios.
   - Use tools like Selenium or Cypress.

#### Deployment Phase
1. **Docker Deployment**:
   - Build and run Docker containers.
   - Use `docker-compose` for multi-container setups.
2. **Virtual Environment Deployment**:
   - Provide `.venv` setup instructions as a fallback.
3. **Direct Deployment**:
   - Document global dependency installation for last-resort setups.

#### Maintenance Phase
1. **Monitoring and Logging**:
   - Use tools like Prometheus and Grafana for monitoring.
   - Implement logging with ELK Stack.
2. **Bug Tracking**:
   - Use issue trackers like Jira or GitHub Issues.
   - Prioritize and address bugs promptly.

### Automated Testing and Version Control

1. **Automated Testing**:
   - Run all test cases automatically before committing changes.
   - Add new test cases for every new feature or bug fix.
2. **Version Control with Git**:
   - Commit changes only after all tests pass.
   - Include detailed commit messages with verification steps.
   - Example commit message:
     ```
     feat: Add user authentication
     - Implement login and registration endpoints
     - Add unit tests for authentication logic
     - Verification steps:
       1. Run `pytest` to ensure all tests pass.
       2. Test login and registration manually via Postman.
     ```
3. **Traceability**:
   - Maintain a clear history of changes for easy rollback.
   - Ensure each commit is linked to a specific requirement or bug report.
