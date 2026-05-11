# Target
    https://medium.com

# Teck  Stack
## 1. graphql
You can see that at 
```javascript
window.__GRAPHQL_URI__ = "https://medium.com/_/graphql";
```
## 2. oauth
- google
- facebook
- email

## 3. nodejs

# Sub domains
### Actif ( working )
- `cdn-videos.medium.com`
- `fegrless-she-wrote.medium.com`
- `go.medium.com`
- `url2204.mail.medium.com`
- `www.medium.com`
### Non actif
- `url104.mail.medium.com`
- `https://api.medium.com/v1/me`
- `37114207.mail.medium.com`
- `cdn-audio-1.medium.com`
- `cdn-videos-1.medium.com`
- `help.medium.com`
- `jss.medium.com`
- `link.medium.com`
- `read.medium.com`
- `status.medium.com`
- `url9532.mail.medium.com`


# robots.txt
```yaml
Disallow:  /m/   /me/  /@me$  /@me/  /*/edit$  /*/*/edit$   /media/  /p/*/share   /r/   /trending   /search?q$   /search?q=
    /*/search?q=  /*/search/*?q=  /*/*source=

User-Agent : Amazonbot  Applebot-Extended Bytespider  ClaudeBot  FacebookBot  GoogleOther  GPTBot  meta-externalagent

Allow :
    - /_/api/users/*/meta
    - /_/api/users/*/profile/stream
    - /_/api/posts/*/responses
    - /_/api/posts/*/responsesStream
    - /_/api/posts/*/related
    - /about   /business   /earn   /gift  /membership   /partner-program  /verified-authors

Sitemap: 
    - https://medium.com/sitemap/sitemap.xml
    - https://medium.com/license.xml
```

# Try to
- fuzzing & try to bypass **unauthorized** paths
- try to access to  `/_/graphql`
- IDOR on users