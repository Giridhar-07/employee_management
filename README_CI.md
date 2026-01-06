CI & Deployment
=================

This repository includes GitHub Actions workflows to run tests and deploy to Render.

- CI workflow: `.github/workflows/ci.yml` — runs `run_e2e_local.py` with `APP_CONFIG=testing`.
- Deploy workflow: `.github/workflows/deploy.yml` — runs tests and triggers a Render deploy via the Render API.

Secrets required for deploy:
- `RENDER_SERVICE_ID` — the Render service id to deploy
- `RENDER_API_KEY` — a Render API key with deploy permissions

To enable CI and deployment, add the two secrets in your GitHub repository settings.
