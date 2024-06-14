# Deploying simple app to EC2

## Setup EC2 instance

1.  Create AWS account and sign in to the cloud console.
2.  Go to the EC2 services and create a new instance.
3.  Choose the settings you want for your instance to have. This includes:

    - The physical hardware given to you, these come in pre configured chunks.

    - The AMI you want to use. We’ll be using Ubuntu AMI, It is the OS installed on your virtual machine.

    - Security group, here you must allow the ports you want to access be open and if accessing from any IP is okay. In our case allow traffic from HTTP and HTTPS and IP from anywhere (0.0.0.0).
    - Choose the SSH RSA key pair and if you haven’t created one on AWS then ask for it to generate one and make sure to store the private key given to you.
    - Add storage and how much you need accordingly.

## Configure EC2 instance

1.  Connect to your instance via SSH using the private key given to you. The instance host ip and hostname can be found on the instance page.
2.  Install Docker on EC2 instance:

    ```bash
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl start docker
    ```

3.  Configure Docker, creating volume and network for the communication of App and MySQL and in case MySQL crashes we don't lose our data:

    ```bash
    docker network create mynetwork
    docker volume create mysql_data
    ```

4.  Spin up the MySQL container:

    ```bash
    docker run -d \
    --name mysql \
    --network mynetwork \
    -e MYSQL_ROOT_PASSWORD=example \
    -e MYSQL_DATABASE=harbour_food \
    -e MYSQL_USER=user \
    -e MYSQL_PASSWORD=password \
    -p 3306:3306 \
    -v mysql_data:/var/lib/mysql \
    mysql:latest
    ```

5.  Create a .env file in the root directory of your user and add the following variables:

    ```.env
    SQL_URI="mysql+pymysql://user:password@mysql:3306/harbour_food"

    SERVICE_URL="URL_OF_EXTERNAL_TRANSACTION_SERVICE"
    ```

    Your App container will use this .env file to set it's environment variables.

## Setting up deployment pipeline

1. On your GitHub repository which is storing your app add this file in the path .github/workflows/deploy.yaml

- This will ensure your deployment is automatically updated on every push to the main branch.

```yaml
name: Build & Deployment

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Build and Push Docker image
        run: |
          docker build -t ttl.sh/distributed-sample-app .
          docker push ttl.sh/distributed-sample-app

  production:
    runs-on: ubuntu-latest

    steps:
      - name: Deploy to EC2
        env:
          DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
          DEPLOY_USER: ubuntu
          SSH_KEY: ${{ secrets.SSH_KEY }}
        run: |
          echo "${SSH_KEY}" > ssh_key
          chmod 600 ssh_key
          ssh -o StrictHostKeyChecking=no -i ssh_key ${DEPLOY_USER}@${DEPLOY_HOST} << 'EOF'
            sudo docker stop distributed-sample-app || true
            sudo docker rm distributed-sample-app || true
            sudo docker run -d -p 80:8000 --env-file ./.env --name distributed-sample-app --network mynetwork ttl.sh/distributed-sample-app:latest
```

2. Go to your repository settings and under `secrets and variables` on `actions` add the DEPLOY_HOST and SSH_KEY as secrets for your repository.

3. Push your changes to main and see the pipeline running. This will spin up a docker container of your app and it communicates with the MySQL container through the docker network.
