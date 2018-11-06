# About
Simple Slack bot to submit hashes to a Cuckoo Sandbox instance.

## Methods:

```
@bot submit <hash>
```

Cuckoo will use it's VTI key to download the hash given and return a taskid.

```
@bot status <taskid>
```

View the current status of the sample being analyzed

```
@bot score <taskid>
```

View the score given to the sample after processing.  Will also provide any signature detection matches.

