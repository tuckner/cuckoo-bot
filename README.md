# About
Simple Slack bot to submit hashes to a Cuckoo Sandbox instance.

## Setup:

1. Create a bot user in Slack and copy the OAuth credentials (https://api.slack.com/bot-users#creating-bot-user)

2. Set the environment variable for 'slack_client' with the OAuth credentials.

3. Set the environment variable for 'cuckoo' with the Cuckoo API URL.

4. If using Docker, fill these in the Dockerfile and build the container.


## Methods:

```
@bot submit <hash>
```

Cuckoo will use it's VTI key to download the hash given and return a taskid.

![](https://s3-us-west-2.amazonaws.com/f5elk/cuckoo2.png)

```
@bot status <taskid>
```

View the current status of the sample being analyzed

```
@bot score <taskid>
```

View the score given to the sample after processing.  Will also provide any signature detection matches.

![](https://s3-us-west-2.amazonaws.com/f5elk/cuckoo1.png)

```
@bot health
```

View the current status/health of the API
