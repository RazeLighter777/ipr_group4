# Blog as a Service 


## How to run the project
```
sudo docker compose build
sudo docker compose push
kubectl apply -f manifest/
```


## Sources used
- [Redis StatefulSet](https://schoolofdevops.github.io/ultimate-kubernetes-bootcamp/13_redis_statefulset/)
Used to understand how kubernetes syntax works. Although we did not end up using redis, it was a good starting point to understand how to create a service.
- [Server Sessions](https://testdriven.io/blog/flask-server-side-sessions/)
Used to understand how to use client side sessions in flask.
- [Mysql initialization](https://stackoverflow.com/questions/45681780/how-to-initialize-mysql-container-when-created-on-kubernetes)
We used this to understand how to initialize a mysql container when created on kubernetes.
- [ChatGPT for HTML](https://chat.openai.com/share/5308b651-07d0-4ad9-baa1-122a6e4ebdb0)
Used to generate the HTML for the blog pages since we were having trouble with the CSS and making the pages look good.
- [ChatGPT for fetching posts](https://chat.openai.com/share/5bed63c1-44f0-4f85-9922-932971ea74b2)
Used to generate the code for fetching posts from the api using jquery.
- [Github Copilot](https://copilot.github.com/)
Used as an autocompletion source for the persistentvolume and persistentvolumeclaim yaml sections.
Also used for the environment variables in the deployment yaml.
Finally, used to generate the sql queries for the database.