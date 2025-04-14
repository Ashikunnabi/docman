# Docman

**Docman** is a modern and efficient document management system designed to simplify the organization, storage, and retrieval of digital documents. Built with scalability, security, and ease of use in mind, it leverages cutting-edge web technologies to provide a robust solution for managing documents.

---

## Key Features

- **Role-Based Access Control (RBAC):** Manage user roles and permissions securely.
- **RESTful API:** Integrate seamlessly with external systems using Django REST Framework.
- **Document Handling:** Upload, view, and manage documents with support for formats like PDF.
- **Elasticsearch Integration:** Full-text search capabilities for quick document retrieval.
- **Dockerized Deployment:** Simplified deployment using Docker and Docker Compose.
- **Custom Middleware:** Includes utilities for logging, authentication, and more.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)
- A `.env` file with proper environment variables (see below).

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/docman.git
cd docman
```

### 2. Configure Environment Variables

Copy the example `.env` file and update it with your configuration:

```bash
cp .env.example .env
```

Edit the `.env` file to include the following variables:

```env
# Database Configuration
DB_NAME=docman_db
DB_USER=docman_user
DB_PASSWORD=secure_password
DB_HOST=db
DB_PORT=5432

# Django Configuration
SECRET_KEY=your_secret_key
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

# Elasticsearch Configuration
ES_JAVA_OPTS=-Xms512m -Xmx512m
```

### 3. Build and Run the Project

Run the following command to build and start the services:

```bash
docker-compose up --build
```

This will start the following services:

- **Web (Django):** The main application server.
- **Database (PostgreSQL):** The relational database for storing application data.
- **Nginx:** Reverse proxy for serving the application.
- **Elasticsearch:** Full-text search engine for document indexing.

### 4. Access the Application

Once the services are running, you can access the application at:

- **Frontend:** [http://localhost:8082](http://localhost:8082)
- **API Documentation (if available):** [http://localhost:8082/api/docs](http://localhost:8082/api/docs)

---

## Project Structure

```
docman/
├── apps/                     # Custom Django apps
├── conf/                     # Django project configuration
├── docker/                   # Docker configuration files
│   ├── web/                  # Dockerfile for Django app
│   ├── nginx/                # Dockerfile for Nginx
├── static/                   # Static files
├── templates/                # HTML templates
├── .env.example              # Example environment variables
├── docker-compose.yaml       # Docker Compose configuration
├── requirements.txt          # Python dependencies
└── manage.py                 # Django management script
```

---

## Stopping the Project

To stop the running containers, use:

```bash
docker-compose down
```

This will stop and remove all containers, networks, and volumes created by `docker-compose up`.

---

## Troubleshooting

- **Database Connection Issues:** Ensure the `DB_HOST` in your `.env` file matches the service name (`db`) in `docker-compose.yaml`.
- **Elasticsearch Memory Errors:** Adjust the `ES_JAVA_OPTS` in your `.env` file to allocate more memory if needed.
- **Port Conflicts:** Ensure the ports defined in `docker-compose.yaml` (e.g., `8082`) are not in use by other applications.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Submit a pull request.
