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