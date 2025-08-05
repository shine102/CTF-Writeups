# Introduction
- https://www.cloudsecuritychampionship.com/
- every month, 1 challenge released, starting from June 2025
- challenges will cover various topics in cloud security
- Until now (August 2025), I managed to solve 2 challenges.
- I will update this README.md file with writeups for each challenge as I solve them.
- Challenges list:
  - June 2025: [Challenge 1](https://www.cloudsecuritychampionship.com/challenge/1)
  - July 2025: [Challenge 2](https://www.cloudsecuritychampionship.com/challenge/2)

# CTF Writeup
## Challenge 1
### Description
#### Perimeter Leak
After weeks of exploits and privilege escalation you've gained access to what you hope is the final server that you can then use to extract out the secret flag from an S3 bucket.
It won't be easy though. The target uses an AWS data perimeter to restrict access to the bucket contents.
Good luck!

### Writeup
- too ez, solve yourself :)

## Challenge 2
### Description
#### Contain Me If You Can
You've found yourself in a containerized environment.
To get the flag, you must move laterally and escape your container. Can you do it?
The flag is placed at /flag on the host's file system.
Good luck!

#### Hints:
- Can you spot any interesting established network connections?
- This network connection is plain-text. Can you think of a way to take advantage of it?
- `COPY ... FROM PROGRAM` can be used to execute arbitrary code in PostgreSQL.
- The PostgreSQL administrator of this environment needed a really easy and convenient way to become root for maintenance purposes.
- The `core_pattern` file in procfs is often used to perform a container escape.

### Writeup
- This one is hard for me, about lateral movement and container escape.
- The hints are very helpful, show us the path to solve the challenge.
- Briefly step-by-step:
  1. Use `netstat` to find established connections, found a connection to a PostgreSQL database.
  2. Use `tcpdump` to capture the traffic, found that the connection is plain-text.
  3. Key point here is to capture the credentials from the traffic. The connection is established whenever the container starts, actually you can not use `tcpdump` faster than the connection established. So we need a trick here:
  4. Use `tcpkill` to kill the connection, while listening to the traffic with `tcpdump`. This way, the container will try to re-establish the connection and when it doing that, the credential will be exchanged between 2 host => we can capture the credentials.
  5. Use the captured credentials to connect to the PostgreSQL database.
  6. Use the `COPY ... FROM PROGRAM` command to execute arbitrary code, I used it to connect to my reverse shell.
  7. Follow the instructions in these articles to escape the container:
       - https://kubehound.io/reference/attacks/CE_UMH_CORE_PATTERN/ (most important)
       - https://pwning.systems/posts/escaping-containers-for-fun/
  8. Finally, I got the flag from the host's file system.
![img](./image.png)