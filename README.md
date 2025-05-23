# 🚀 AgentForge

AgentForge is a powerful, modular GenAI-based multi-agent system that automates code refactoring, DevOps operations, test generation, and web modernization using Large Language Models (LLMs). The project uses domain-specific agents to intelligently transform and optimize legacy systems, streamline CI/CD pipelines, and auto-generate code artifacts—all orchestrated through LangChain-style workflows.

---

## 📁 Project Structure

.github/workflows/
├── generated_pipeline.yml # GitHub Actions pipeline for CI/CD

backend/app/
├── Main API app (FastAPI or similar)

agent/common_files/
├── Core agent logic, prompt engine, and utilities

agent/db_agent/
├── Refactors stored procedures, validates schemas, and tunes performance

agent/devops_agent/
├── Automates infrastructure setup, pipeline creation, cost estimation

agent/test_agent/
├── Generates unit, integration, feature, and UI test cases (Selenium, Playwright)

agent/web_agent/
├── Transforms legacy frontend (ASP.NET/HTML) to React, optimizes frontend logic

langgraph/
├── Orchestration logic for multi-agent workflows

converted/
├── Output folder for converted/refactored code and reports

frontend/
├── React + Vite frontend interface




---

## ✨ Key Features

### 🧠 LLM-Powered Agents

- **DB Agent**
  - Refactors SQL Stored Procedures
  - Optimizes for performance and security
  - Extracts schemas and validates DB structures

- **DevOps Agent**
  - Auto-generates Jenkins pipelines and Terraform modules
  - Validates IaC (Infrastructure as Code)
  - Provides autoscaling, monitoring, and cost estimation

- **Test Agent**
  - Generates:
    - Unit tests
    - Integration tests
    - Playwright/Selenium UI tests
    - Feature files (for BDD)
  - Handles RCA (Root Cause Analysis) prompts

- **Web Agent**
  - Converts:
    - ASP.NET to React
    - HTML to JSX
    - CSS optimizations and routing setup
  - Automates state management and form handling

---

## 🔄 LangGraph Orchestration

Each agent is coordinated via `langgraph/`, which defines:
- `db_graph.py` – orchestrates DB-related tasks
- `devops_graph.py` – manages DevOps flows
- `test_graph.py` – handles test generation flows
- `web_graph.py` – web modernization pipelines

---

## 🧪 Prompts Library

Every agent has its own set of reusable **Jinja2 prompt templates**:
- `db_prompts/` – e.g., `add_try_catch.j2`, `refactor_procedure.j2`
- `devops_prompts/` – e.g., `terraform_module.j2`, `jenkins_pipeline.j2`
- `web_prompts/` – e.g., `convert_asp.net_to_react.j2`, `Optimize_Css.j2`
- `Playwright_prompts/` – test automation templates

---

## 🖥️ Frontend

The frontend is built with **React + Vite** to provide:
- UI for uploading legacy code
- Selecting target transformation (e.g., convert, optimize)
- Viewing the converted outputs
- Triggering multi-agent workflows

---

## 📦 Setup Instructions

### 🔧 Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend app (e.g., FastAPI)
uvicorn backend.app.main:app --reload


🌐 Frontend Setup
cd frontend
npm install
npm run dev

✅ Running LangGraph Pipelines
Each pipeline can be triggered independently:

bash
Copy
Edit
python langgraph/db_graph.py
python langgraph/devops_graph.py
python langgraph/test_graph.py
python langgraph/web_graph.py


✅ CI/CD Integration
GitHub Actions workflow is defined in .github/workflows/generated_pipeline.yml

Automates:

Test runs

Build validation

Deployment pipelines

🧠 Tech Stack
LLM-based Prompt Engineering

LangChain / LangGraph

FastAPI (Backend)

React + Vite (Frontend)

Jinja2 Templates

Terraform, Jenkins, Playwright, Selenium

🤝 Contributing
We welcome contributions! Here's how to get started:

Fork the repo

Create a new branch: git checkout -b feature/my-feature

Commit your changes: git commit -am 'Add new feature'

Push to the branch: git push origin feature/my-feature

Create a pull request

📄 License
This project is licensed under the MIT License.

🙌 Acknowledgements
Thanks to open-source tools and LLM frameworks that made this project possible:
LangChain, OpenAI, HuggingFace, Jinja2, Playwright, Terraform, and the OSS community.

