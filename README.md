# Social Networking Application

This project is a social networking application built with Django and Django REST Framework. It includes features such as user authentication, friend requests, and search functionality.

## Table of Contents

- [Social Networking Application](#social-networking-application)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Running the Project](#running-the-project)

## Installation

To get started with this project, follow these steps:

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### Setup

1. **Clone the Repository:**

   `git clone https://github.com/priyanshuarora595/social-network.git`
   `cd socal-network`

2. **Build and Start the Containers:**

   `docker-compose up --build`

   This command will build the Docker images and start the containers for both the Django application and PostgreSQL database.


3. **Create a Superuser (Optional):**

   If you want to create a superuser for accessing the Django admin interface:

   `docker-compose exec social_network python manage.py createsuperuser`

## Running the Project

Once the containers are running, you can access the Django application at `http://127.0.0.1:8000`.
