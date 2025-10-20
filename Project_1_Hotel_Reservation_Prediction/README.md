# Project 1: Hotel Reservation Prediction - CI/CD Setup with Jenkins and Docker

This project sets up a **CI/CD environment for ML projects** using **Jenkins** and **Docker**, with Google Cloud integration. Follow the steps below to set up your environment and deploy your project.

---

## 1. Python Environment Setup

1. **Create a virtual environment:**

```bash
python -m venv venv
```

2. **Activate the environment:**

* Linux/macOS:

```bash
source venv/bin/activate
```

* Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

3. **Install the project:**

```bash
pip install -e .
```

4. **Optional:** Add Google Cloud SDK to your `PATH`:

```bash
export PATH="<YOUR_GOOGLE_CLOUD_SDK_PATH>:$PATH"
```

5. **Verify Google Cloud SDK installation:**

```bash
gcloud version
```

6. **Set credentials for Google Cloud access:**

```bash
export GOOGLE_APPLICATION_CREDENTIALS="<PATH_TO_SERVICE_ACCOUNT_JSON>"
```

---

## 2. Docker & Jenkins Setup

1. **Login to Docker:**

```bash
docker login
```

2. **Build Jenkins Docker image:**

```bash
docker build --platform=linux/amd64 -t jenkins-dind .
```

3. **Check Docker images:**

```bash
docker images
```

4. **Run Jenkins container:**

```bash
docker run --platform linux/amd64 --privileged -d \
  --name jenkins-dind \
  -p 8080:8080 -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  jenkins-dind
```

5. **Verify container is running:**

```bash
docker ps
```

6. **Get Jenkins setup password:**

```bash
docker logs jenkins-dind
```

7. **Access Jenkins UI:**
   Open [http://localhost:8080](http://localhost:8080)

---

## 3. Jenkins Container Maintenance

1. **Open interactive bash in Jenkins container:**

```bash
docker exec -u root -it jenkins-dind bash
```

2. **Install Python inside Jenkins container:**

```bash
apt update -y
apt install -y python3 python3-pip python3-venv
ln -s /usr/bin/python3 /usr/bin/python
docker restart jenkins-dind
```

---

## 4. GitHub Access

1. Create a **personal access token** in GitHub: [https://github.com/settings/tokens/new](https://github.com/settings/tokens/new)

* Give `repo` permission to allow Jenkins to interact with the repository.

---

## 5. Deploy Project Docker Image to GCR

1. **Install Google Cloud SDK inside Jenkins container:**

```bash
docker exec -u root -it jenkins-dind bash
apt update -y
apt-get install -y curl apt-transport-https ca-certificates gnupg
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud-google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud-google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-sdk.list
apt-get update && apt-get install -y google-cloud-sdk
```

2. **Verify GCloud installation:**

```bash
gcloud --version
```

3. **Add Jenkins user to Docker and root groups:**

```bash
usermod -aG docker jenkins
usermod -aG root jenkins
```

4. **Build and push your project image to GCR:**

```bash
docker build -t <GCR_PROJECT>/<IMAGE_NAME>:<TAG> .
docker push <GCR_PROJECT>/<IMAGE_NAME>:<TAG>
```

---

## Notes & Best Practices

* **Isolation:** Keep Jenkins CI/CD and your ML project separate to avoid dependency conflicts.
* **Docker-in-Docker:** Required for building and deploying images inside Jenkins.
* **Environment Agnostic:** Paths and commands should be adjusted for your OS. Avoid hardcoding OS-specific paths.
* **Security:** Use environment variables and secret management instead of hardcoding credentials.
