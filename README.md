# Simple DevOps Pipeline Demo

A minimal Flask app used purely as a vehicle to practice a full Jenkins CI/CD
pipeline: **Clone → Build → Test → Compile → Docker Build → Docker Tag →
Docker Login → Docker Push → Clean Workspace** — matching the stage view
you're aiming to reproduce in Jenkins.

## Project structure

```
simple-devops-pipeline/
├── app/
│   ├── app.py              # Flask application
│   └── requirements.txt    # Runtime dependencies
├── tests/
│   ├── test_app.py         # pytest unit tests
│   └── requirements-test.txt
├── Dockerfile               # Multi-stage build
├── Jenkinsfile               # Declarative pipeline (all 9 stages)
├── .dockerignore
├── .gitignore
└── README.md
```

## 1. Push this to GitHub

```bash
cd simple-devops-pipeline
git init
git add .
git commit -m "Initial commit: simple devops pipeline demo"
git branch -M main
git remote add origin https://github.com/vamshii9989/simple-devops-pipeline.git
git push -u origin main
```

## 2. Run locally (optional, sanity check before wiring up Jenkins)

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r ../tests/requirements-test.txt
python app.py          # visit http://localhost:5000
```

Run tests:
```bash
pytest ../tests/
```

Build & run with Docker:
```bash
docker build -t simple-devops-pipeline .
docker run -p 5000:5000 simple-devops-pipeline
```

## 3. Set up the Jenkins job

1. **Update the Jenkinsfile placeholders**:
   - `DOCKER_IMAGE` → your actual Docker Hub `username/reponame`
   - The `git` step URL → your actual GitHub repo URL
2. **Add Docker Hub credentials in Jenkins**:
   - Jenkins → Manage Jenkins → Credentials → Add Credentials
   - Kind: *Username with password*
   - ID: `dockerhub-creds` (must match the Jenkinsfile)
3. **Create a new Pipeline job**:
   - New Item → Pipeline
   - Pipeline definition: *Pipeline script from SCM*
   - SCM: Git → your repo URL → branch `main` → Script Path: `Jenkinsfile`
4. Make sure the Jenkins agent has `python3`, `pip`, `docker`, and `git`
   installed and the Jenkins user has permission to run `docker` commands
   (add the `jenkins` user to the `docker` group on Linux agents).
5. Click **Build Now** — the Stage View will populate with the same 9
   stages shown in your screenshot.

## Notes

- The `Compile` stage uses `python -m py_compile` since Python doesn't have
  a traditional compile step — this validates syntax and mirrors that stage
  in the pipeline view.
- `Clean Work Space` uses Jenkins' built-in `cleanWs()` step plus a Docker
  logout/prune to keep the agent tidy between builds.
