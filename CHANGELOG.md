# Changelog

All notable changes to this project are recorded here.

## [Unreleased]

### Added

- Model training and evaluation API endpoints (`POST /api/v1/train`, `GET /api/v1/metrics`)
- Model registry system for in-memory trained model storage
- Complete TF-IDF + Logistic Regression implementation with train/eval/predict
- Professional Next.js frontend with Tailwind CSS
- Analysis Workbench page for interactive pragmatic inference
- Experiments page with model training UI and metrics visualization
- Dataset Explorer page with Circa integration and license information
- Docker and docker-compose configuration for local development
- Comprehensive deployment documentation with hosting options and cost estimates
- Complete README with setup instructions for both backend and frontend

### Completed Milestones

- ✅ Milestone 0: Repository bootstrap with Git, docs, and conventions
- ✅ Milestone 1: Schemas and validation with group-aware splits
- ✅ Milestone 2: FastAPI skeleton with health and metadata endpoints
- ✅ Milestone 3: Circa loader with TSV validation and label normalization
- ✅ Milestone 4: TF-IDF baseline with real training and evaluation
- ✅ Milestone 6: Next.js workbench with API integration and error states
- ⚠️ Milestone 5: Evidence diagnostics (basic spans implemented)
- ⚠️ Milestone 7: Experiments UI complete, transformer models pending
- 🔄 Milestone 8: Docker configuration complete, testing pending

## [0.1.0] - 2026-10-28

### Initial Release

- Repository conventions, research documentation, and dataset requirements
- Dataset schemas, Circa label mapping, group-aware splits, synthetic fixture, and tests
- FastAPI health, dataset, model, metrics, and inference endpoints
- Backend test suite with 22 passing tests
