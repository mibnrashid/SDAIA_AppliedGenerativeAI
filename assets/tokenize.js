/* ============================================================
   tokenize.js — an APPROXIMATE tokenizer, written here on purpose.

   Why not a real one: every page on this site must work with the wifi
   off, and a real BPE vocabulary is megabytes. The teaching point is the
   RATIO between scripts, not the exact number, and the ratio is what a
   simple character-rate heuristic gets right.

   The heuristic, documented so it can be defended in the room:
     · Latin/Western script  ~4 characters per token
     · Arabic script         ~2 characters per token
       (Arabic is under-represented in tokenizer training data, so words
        break into more, smaller pieces — this is the whole lesson)
     · Punctuation           its own token
     · Whitespace            rides along with the token that follows,
                             which is how real BPE tokenizers behave

   Always label output "approximate" on screen.
   ============================================================ */

var Tok = (function () {
  'use strict';

  var ARABIC = /[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]/;
  var PUNCT = /[.,!?;:()\[\]{}"'\u2014\u2013\/\\@#$%^&*+=<>|~`\u060C\u061B\u061F]/;

  function isArabic(ch) { return ARABIC.test(ch); }

  /* Split text into display pieces. pieces().length is the token
     estimate, so the number on screen always matches the chips. */
  function pieces(text) {
    var out = [];
    var i = 0;

    while (i < text.length) {
      var lead = '';

      /* Collect leading whitespace and attach it to the next piece. */
      while (i < text.length && /\s/.test(text[i])) { lead += text[i]; i++; }
      if (i >= text.length) {
        if (lead && out.length) out[out.length - 1] += lead;
        else if (lead) out.push(lead);
        break;
      }

      var ch = text[i];

      if (PUNCT.test(ch)) {
        out.push(lead + ch);
        i++;
        continue;
      }

      /* A run of word characters in one script. */
      var arabic = isArabic(ch);
      var run = '';
      while (i < text.length && !/\s/.test(text[i]) && !PUNCT.test(text[i]) &&
             isArabic(text[i]) === arabic) {
        run += text[i];
        i++;
      }

      var size = arabic ? 2 : 4;
      for (var j = 0; j < run.length; j += size) {
        out.push((j === 0 ? lead : '') + run.slice(j, j + size));
      }
    }

    return out;
  }

  function estimate(text) {
    if (!text) return 0;
    return pieces(text).length;
  }

  /* Rough character counts per script, for explaining a result. */
  function profile(text) {
    var arabic = 0, other = 0;
    for (var i = 0; i < text.length; i++) {
      if (/\s/.test(text[i])) continue;
      if (isArabic(text[i])) arabic++; else other++;
    }
    return { arabic: arabic, other: other, chars: text.length };
  }

  return { estimate: estimate, pieces: pieces, profile: profile, isArabic: isArabic };
})();
