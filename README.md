# Convert LWN.net Articles into Pocket Article

> Heavily inspired on https://github.com/jd/lwn2pocket/

**These scripts require a LWN.net Subscription. If you're not a subscriber
already, consider becoming one, their content is amazing :)**

[Pocket](https://getpocket.com) doesn't always plays nice with 
[LWN.net](https://lwn.net) Articles. Pocket can't convert subscriber-only
content into an article since they don't have access to it. Sometimes Pcoket
fails to convert the content into an article for free pages as well.

These scripts will try to generate a "Subscriber free link" for LWN links in
your Pocket queue. If it fails, it will generate a shorten link using 
[bit.ly](http://bit.ly) to trick Pocket into re-evaluating the article. The
script will add the generated link (either the Subscriber free link or the
shorten link) to Pocket, and if it succeeds it will delete the original link
from Pocket (yep, these scripts can be destructive, use at your own risk).

## Running

```bash
# Build your docker image
docker build . --tag lwn-to-pocket
# Get your Pocket Access Token (requires POCKET_CONSUMER_KEY) in the env file
docker run --rm -it --env-file=/path/to/env-file lwn-to-pocket:latest --get-pocket-token
# Convert non-article LWN.net links in your Pocket queue into Articles
docker run --rm --env-file=/path/to/env-file lwn-to-pocket:latest
```

### Environment File

```bash
LWNNET_USERNAME=<lwn username>
LWNNET_PASSWORD=<lwn password>
POCKET_CONSUMER_KEY=<pocket consumer key from https://getpocket.com/developer/>
POCKET_ACCESS_TOKEN=<pocket access token generated with --get-pocket-token>
BITLY_ACCESS_TOKEN=<bitly access token from Basic Authentication in https://dev.bitly.com/authentication.html>
```

## Security Suggestion

Instead of storing your passwords and API keys in a plain text file, encrypt it
with GPG and use `<(gpg -q -d /path/to/encrypted-file)` instead of 
`/path/to/env-file`.

# License

Copyright 2019 Matheus Marchini <mat@mmarchini.me>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
