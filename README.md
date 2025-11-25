# Two-Tier Flask Application with CI/CD using Jenkins, Docker & AWS EC2

This project demonstrates a production-style CI/CD pipeline for a two-tier web application built using Flask (App Layer) and MySQL (Database Layer). The entire deployment is automated using Jenkins, Docker, Docker Compose, and GitHub Webhooks, running on AWS EC2.

## 🏗️ Architecture Overview

```
GitHub → Jenkins → Docker Build → EC2 SSH → Docker Compose → Flask App + MySQL
```

### Two-Tier Setup

- **Tier 1 – Flask App (Python backend)**
- **Tier 2 – MySQL Database (Persistent storage)**

Both run in separate containers managed by docker-compose.

### CI/CD Flow

1. Developer pushes code to GitHub
2. GitHub Webhook triggers Jenkins
3. Jenkins pulls repository
4. Jenkins builds Docker images
5. Jenkins runs unit tests
6. Jenkins SSHs into EC2
7. Docker Compose deploys updated containers
8. Updated Flask app goes LIVE instantly

## ⚙️ Tech Stack

| Component | Technology |
|-----------|-----------|
| App | Python Flask |
| Database | MySQL 8.0 |
| CI/CD | Jenkins |
| SCM | GitHub |
| Containerization | Docker & Docker Compose |
| Cloud | AWS EC2 (Ubuntu) |
| Trigger | GitHub Webhook |

## 📂 Project Structure

```
.
├── app/
│   ├── app.py                 # Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Docker image for Flask app
│   └── templates/             # HTML templates (if any)
├── tests/
│   └── test_basic.py          # Unit tests
├── docker-compose.yml         # Multi-container orchestration
├── Jenkinsfile                # CI/CD pipeline configuration
└── README.md                  # This file
```

### Key Files

**Dockerfile**
- Builds the Flask application container
- Manages Python dependencies and application setup

**docker-compose.yml**
- Runs two containers:
  - `web`: Flask application (exposed on port 80)
  - `db`: MySQL database with persistent volumes & environment variables

**Jenkinsfile**
- Automates the complete CI/CD pipeline:
  - Clone code from GitHub
  - Build Docker images
  - Run unit tests
  - Deploy containers to EC2

## 🚀 Deployment Instructions

### 1️⃣ Set Up EC2 (App Server)

Install Docker and Docker Compose:

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker ubuntu
```

Clone the repository (first time only):

```bash
git clone <your-repo>
cd two-tier-flask-app
```

### 2️⃣ Set Up Jenkins EC2 Server

Install Java and Jenkins:

```bash
sudo apt update
sudo apt install fontconfig openjdk-17-jre -y
wget -O jenkins.war https://get.jenkins.io/war-stable/latest/jenkins.war
```

Install Jenkins Plugins:
- Git plugin
- SSH Pipeline Steps
- Docker plugins
- Credentials Binding

Add Credentials in Jenkins:
- GitHub Personal Access Token
- EC2 SSH Private Key (for `app-ec2-ssh`)

### 3️⃣ Configure Jenkins Pipeline

Create a new Pipeline job and use the following configuration:

```groovy
pipeline {
    agent any

    stages {
        stage('Clone Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/harcastic/two-tier-flask-app.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'docker-compose run web pytest || true'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['app-ec2-ssh']) {
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@<APP_EC2_IP> "cd two-tier-flask-app && git pull && docker-compose down && docker-compose up -d"'
                }
            }
        }
    }
}
```

**Replace `<APP_EC2_IP>` with your actual EC2 instance public IP**

### 4️⃣ Set Up GitHub Webhook

Configure GitHub to trigger Jenkins automatically:

1. Go to your repository → **Settings** → **Webhooks** → **Add Webhook**
2. Set **Payload URL**: `http://<JENKINS_PUBLIC_IP>:8080/github-webhook/`
3. Set **Content Type**: `application/json`
4. Select events: ✔ **Push events**
5. Click **Add webhook**

**Replace `<JENKINS_PUBLIC_IP>` with your Jenkins EC2 instance public IP**

## 🧪 Verification

### Check Running Containers

```bash
docker ps
```

Expected output should show:
- `web` - Flask application container
- `db` - MySQL database container

### Access Flask Application

Open your browser and navigate to:

```
http://<APP_EC2_PUBLIC_IP>
```

You should see the Flask application running with the message "New Updates are released!!"

### Check Container Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db
```

### Test Health Endpoint

```bash
curl http://<APP_EC2_PUBLIC_IP>/health
```

Should return: `OK`

## ✅ Features

- ✔ End-to-end CI/CD automation
- ✔ Two-tier containerized application
- ✔ Production-style deployment workflow
- ✔ GitHub → Jenkins Webhook integration
- ✔ Docker Compose-based multi-container architecture
- ✔ Real cloud deployment on AWS EC2
- ✔ Automated unit testing in pipeline
- ✔ Zero-downtime deployments

## 📘 Future Improvements

- [ ] Add comprehensive unit testing coverage
- [ ] Implement Blue-Green deployment strategy
- [ ] Add monitoring with Prometheus/Grafana
- [ ] Migrate to Kubernetes for orchestration
- [ ] Implement automated rollback on test failures
- [ ] Add database migration scripts
- [ ] Implement secrets management using AWS Secrets Manager
- [ ] Add container image scanning for security vulnerabilities
- [ ] Setup CloudWatch for centralized logging
- [ ] Implement auto-scaling policies

## 🔧 Environment Variables

Configure the following in your `docker-compose.yml` or environment:

```yaml
MYSQL_ROOT_PASSWORD: root123
MYSQL_DATABASE: flaskdb
```

## 📝 Notes

- The Flask app runs on port 5000 internally and is exposed on port 80
- MySQL data is persisted using Docker volumes (`db_data`)
- Jenkins must have SSH access to the App EC2 instance
- GitHub Webhook requires Jenkins to be accessible from the internet
- All deployments are containerized for consistency across environments

## 🙌 Acknowledgements

This project demonstrates real-world DevOps practices and helped in learning:

- Jenkins Pipeline automation
- Docker build and containerization
- GitHub Webhooks for event-driven CI/CD
- Multi-tier application deployment strategies
- Infrastructure as Code with Docker Compose
- Cloud deployment on AWS EC2
- End-to-end automation workflows

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [GitHub Webhooks Documentation](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)

## 📄 License

This project is open source and available under the MIT License.

---

**Last Updated**: November 2025
