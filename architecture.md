# Architecture Proposal — Question 2

## 🏗️ Suggested Architecture for Production Deployment

### Components

| Component          | Description                                                  |
|--------------------|--------------------------------------------------------------|
| FastAPI            | Serves the portfolio optimization logic                      |
| Docker             | Containerize the application for reproducible deployment     |
| Kubernetes (K8s)   | Orchestrate multiple containers for scaling and resiliency   |
| Cloud Provider     | (GCP, AWS, Azure) Infrastructure hosting and autoscaling     |
| CI/CD (GitHub Actions) | Automate testing, builds and deployments                |
| Logging & Monitoring | Prometheus + Grafana or equivalent for operational insights |
| API Gateway        | Handle request routing, auth, rate limiting (optional)       |

### Rationale

- **Scalability**: Easily handle increased usage with horizontal scaling.
- **Reliability**: Isolate failures, restart failed containers automatically.
- **Portability**: Docker ensures consistency across environments.
- **Automation**: CI/CD for continuous integration and safe deployments.
- **Observability**: Alerts and logs to monitor usage and stability.

## 👥 Team Setup

This architecture is maintainable by small teams and extensible for production-level APIs.
