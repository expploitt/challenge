# Landbot Backend Challenge

## Description

From UmiShop, we have concluded that we want to improve web sales using Landbot.

For this reason, you have to create a bot in Landbot that asks the client for their name, email, and phone number and later, using a Webhook node, send it to our API and register the new user.

> Hint: Ngrok will provide you an URL to your localhost.

From the product department, they insist on the importance of knowing the origin of customers.

All registered users should receive a welcome email after 1 minute.

On the other hand, the product department wants a system to be notified when a customer requests assistance from a bot. The bot will ask the client for the topic (Sales, Pricing,...). Then, you have to create a bot that will communicate through Webhook to our API and our API will send the question to the different channels depending on the selected topic.

``` 
Topic    | Channel   
----------------------
Sales    | Slack
Pricing  | Email
```

> Note: Slack and Email are suggestions. Select the channels that you like the most.

The product department has in mind to expand the topics and communication channels.

## The solution should:
- Be written in Python using DRF + Django + Celery
- App dockerized
- Have a clear structure
- Be easy to grow with new functionality

## Bonus Points For:
- Tests
- Useful comments
- Documentation
- CI
- Commit messages
- Clear scalability

# Solution

## Umishop Bot

The Umishop bot was created using the Landbot platform. For this purpose, the determined flow for the interaction with the customer and the consecutive calls to the internal Umishop API or external ones (boxes with extra functionalities already offered by Landbot) were traced.

Due to the use of webhooks, the only configuration needed is to update the URL of the two webhooks used. For this, the domain variable *umishop_api* has been defined so that it is not necessary to modify the bot flow.

In this case, as we use ngrok as a proxy, we would have to modify the domain variable by the new URL provided by ngrok.

## Umishop API / Web

A django project has been created with DRF as a backend solution with two applications: umishop_api and webapp.

An accessible API is provided as umishop_api/ which consists of the following methods:


- /user (POST): endpoint available for user registration. It is necessary to pass username, email and phone number.
- /topic (POST): endpoint available for forwarding user queries to the channels available for customer service (Sales, Princing, etc.). It is necessary to provide username, email, phone and topic in the body of the message.

For the moment, email for Sales and Slack for Pricing are integrated as communication channels. For the email it was decided to use SendGrid due to the facilities that it provides. 

Due to the forwarding of the client messages to the channels may take some time (depending on the availability of the external APIs or network), to avoid the blocking of the umishop API it was decided to use Celery for the execution of async tasks. There are two tasks:

- send_email -> Sends an email to the specified email address configured in the environment file being the user the "from" part.
- send_slack -> Sends a ping to the specified Slack application channel using the client's slack API.

## Deployment

### Docker Compose
To facilitate the deployment of the different systems explained above, a docker compose is available to initialise the different elements.

```docker
version: "3.9"

services:
  db:
    image: postgres
    env_file: project/.env
    volumes:
      - postgres_data:/var/lib/postgresql/data/
  backend:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  redis:
    image: redis:alpine
  celery:
    build: .
    command: celery -A project worker -l info
    depends_on:
      - backend
      - redis
      - db
volumes:
  postgres_data:
```

> **Db**. a Postgres database. The idea is to have in an external container the data persisted with a volume. 

> **Backend**. The django application. It listens in port 8000 and enables the Umishop API and the webapp to serve the basic html page.

> **Redis**. Storage backend to support the requests of the differents tasks available in the Celery server.

> **Celery**. Worker server to attend the computation requests from django backend.

### Env file

Environment configuration file. It contains the common django variables for database and django configuration.

Apart from that, it contains:

```env_file

# Sendgrip server configuration. It is necessary to add all the information to allow umishop backend to stablish connection with SendGrip API.
SENDGRIP_EMAIL_HOST='sendgrip_email_host'
SENDGRIP_EMAIL_PORT='sendgrip_port'
SENDGRIP_EMAIL_HOST_USER='sendgrip_user'
SENDGRIP_EMAIL_HOST_PASSWORD='sendgrip_password'


# SLACK CONFIGURATION. It is necessary to add the token for the SLACK account used to connect with the Slack API
SLACK_TOKEN='slack_token'
SLACK_CHANNEL='channel'


# EMAIL CHANNEL CONFIG. Email to send the questions from clients to channel Sales
EMAIL_SALES='example@example.com'
```


### How to deploy


```bash
>   git clone https://github.com/hello-umi/backend-challenge.git
>   cd backend-challenge
# Configure your enviroment variables with sendgrip settings, slack settings.
>   docker-compose up --build
```

Now open a terminal and run:
```bash
>   ngrok http 8000
```

Now go to landbot and update the webhook domain variable with the ngrok proxy URL.

Open your browser and visit ngrok_url:8000/index.html

> Note: if you are not allow to open, please, update the ALLOWED_HOST variable in django.


## Improvements

Some good aproachs to improve performance could be:

1. Add nginx and Gunicorn to our deployment. By this way would be possible to scale our application with multiples instances and also the security using a proxy.
2. Adding automatic testing to the project (unit, integration, e2e, etc) instead of doing manually.
3. Add some CI software to run this automatic testing and automate deployments.