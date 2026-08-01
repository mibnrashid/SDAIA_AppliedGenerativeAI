/* ============================================================
   activities.js — the activity registry.

   One list, read by the home page progress strip and by the activities
   hub, so the ids and the maximum scores can never disagree. Every
   activity page calls Store.saveScore() with the id used here.
   ============================================================ */

var ACTIVITIES = [
  {
    id: 'tokenizer-race',
    num: '01',
    day: 1,
    minutes: 8,
    max: 24,
    file: 'tokenizer-race.html',
    title: 'Tokenizer Race',
    desc: 'Guess how many tokens a sentence costs. Eight rounds, English and Arabic.'
  },
  {
    id: 'chunk-lab',
    num: '02',
    day: 2,
    minutes: 20,
    max: 8,
    file: 'chunk-lab.html',
    title: 'Chunk Lab',
    desc: 'Place the chunk boundaries in a real policy document, then see which questions your chunking can answer.'
  },
  {
    id: 'be-the-agent',
    num: '03',
    day: 3,
    minutes: 15,
    max: 8,
    file: 'be-the-agent.html',
    title: 'Be the Agent',
    desc: 'You play the model. Choose the tool calls, recover from an error, reach the answer.'
  },
  {
    id: 'cost-auction',
    num: '04',
    day: 4,
    minutes: 12,
    max: 15,
    file: 'cost-auction.html',
    title: 'Cost Auction',
    desc: 'Five deployments in plain language. Estimate the monthly bill, then see the arithmetic.'
  },
  {
    id: 'red-team',
    num: '05',
    day: 5,
    minutes: 25,
    max: 15,
    file: 'red-team.html',
    title: 'Red Team',
    desc: 'Break a document assistant five ways, then turn the defences on and try again.'
  }
];

/* Total points available across every activity. */
var ACTIVITIES_MAX = ACTIVITIES.reduce(function (sum, a) { return sum + a.max; }, 0);
