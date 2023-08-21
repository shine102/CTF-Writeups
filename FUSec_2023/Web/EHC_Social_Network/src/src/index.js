const crypto = require('crypto');
const express = require('express');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

// ==============================================================================
// =============================== Middleware ===================================
const app = express();
app.use(express.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use("/", express.static(__dirname + "/static"));
app.use(cookieParser());

// ==============================================================================
// =============================== Phase 1 ======================================

class Tweet {
  constructor() {
    this.tweets = [];
    this.salt = `salt-${crypto.randomBytes(10).toString}`;
  }

  makeTweet({ name, thoughts }) {
    const status = this.tweets.length;
    this.tweets.push(name + ' used to say: <br>"' + thoughts + '"');
    return {
      status,
      hash: this.makeHash(status),
    };
  }

  retrieveTweet({ status, hash }) {
    if (hash !== this.makeHash(status)) return { error: 'wrong hash!' };
    if (status >= this.tweets.length) return { error: 'no fucking tweet like this!' };
    return { tweet_content: this.tweets[status] };
  }

  makeHash(status) {
    var hash = crypto
      .createHmac('ripemd160WithRSA', this.salt)
      .update(status.toString())
      .digest('hex');
    console.log("hash: ", hash)
    return hash;
  }
}

const tw = new Tweet();
tw.makeTweet({ name: "Prime user", thoughts: process.env.FLAG });

app.post('/tweet', (req, res) => {
  try {
    const thoughts = req.body.thoughts ?? '';
    const name = req.body.name ?? '';
    if (thoughts && name) {
      const { status, hash } = tw.makeTweet({ name: name.toString(), thoughts: thoughts.toString() });
      res.send(`status=${status}&hash=${hash}`);
      return;
    }
    else {
      res.send('Missing');
      return;
    }
  } catch (error) {
    res.send(error);
  }
});

app.get('/get_tweet', (req, res) => {
  try {
    const { status, hash } = req.query;
    const tweet = tw.retrieveTweet({
      status: parseInt(status ?? '-1'),
      hash: (hash ?? '').toString(),
    });
    if (tweet.error) {
      res.send(tweet.error);
    } else {
      res.send(tweet.tweet_content);
    }
  } catch (error) {
    res.send(error);
  }
});

app.get('/hidden', (req, res, next) => {
  try {
    res.sendFile(__dirname + "/static/hidden.html");
  } catch (error) {
    res.send(error);
  }
});


app.post('/hidden', (req, res, next) => {
  try {
    const code = req.body.code ?? '';
    if (code == process.env.FLAG) {
      const prime_token = jwt.sign({ isPrime: true }, process.env.JWT_SECRET_KEY);
      res.cookie('prime', prime_token);
      res.send('prime');
    }
    else res.send('Non-prime');
    return;
  } catch (error) {
    res.send(error);
  }
});

// ==============================================================================
// =============================== Phase 2 ======================================



app.get('/prime', (req, res) => {
  try {
    const prime_token = req.cookies['prime'];
    if (jwt.verify(prime_token, process.env.JWT_SECRET_KEY)) {
      res.sendFile(__dirname + "/static/prime.html");
    } else {
      return res.status(401).send(error);
    }
  } catch (error) {
    return res.status(401).send(error);
  }
});

app.post('/quote1', function (req, res, next) {
  try {
    const prime_token = req.cookies['prime'];
    if (jwt.verify(prime_token, process.env.JWT_SECRET_KEY)) {
      console.log(req.body.list);
      const Quote = req.body.list.toString();
      console.log("Quote: ", Quote)
      const getQuote = require("./static/" + Quote);
      res.json(getQuote.all());
    } else {
      return res.status(401).send(error);
    }
  } catch (error) {
    return res.status(401).send(error);
  }
})

app.post('/quote2', function (req, res, next) {
  try {
    const prime_token = req.cookies['prime'];
    if (jwt.verify(prime_token, process.env.JWT_SECRET_KEY)) {
      const Quote1 = require("./static/top-quote-1.js")
      const Quote2 = require("./static/top-quote-2.js")
      let superQuote = combine(Quote1.all(), Quote2.all())
      let data = req.body.data || "";
      superQuote = combine(superQuote, data);
      res.json(superQuote);
    } else {
      return res.status(401).send(error);
    }
  } catch (error) {
    return res.status(401).send(error);
  }
})

const combine = (sink, source) => {
  for (var property in source) {
    if (typeof sink[property] === 'object' && typeof source[property] === 'object') {
      combine(sink[property], source[property]);
    } else {
      sink[property] = source[property];
    }
  }
  return sink
};

// ==============================================================================

app.listen(3000, () => {
  console.log('listening on port 3000');
});