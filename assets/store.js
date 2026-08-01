/* ============================================================
   store.js — the only thing on this site that touches localStorage.
   Every key is namespaced 'agai:' so nothing can collide with another
   project served from the same GitHub Pages origin (github.io is one
   origin for every repo the account publishes — this matters).

   API:
     Store.set(key, value)
     Store.get(key, fallback)
     Store.saveScore(activityId, score, max)   // keeps the BEST score
     Store.getScore(activityId)                // -> {score, max} | null
     Store.allScores()                         // -> { id: {score, max} }
     Store.reset()
   ============================================================ */

var Store = (function () {
  'use strict';

  var PREFIX = 'agai:';
  var SCORES_KEY = 'scores';

  /* Private browsing and locked-down browsers can throw on access, so
     every call is guarded. A failed write must never break a page. */
  function backend() {
    try {
      var ls = window.localStorage;
      var probe = PREFIX + '__probe';
      ls.setItem(probe, '1');
      ls.removeItem(probe);
      return ls;
    } catch (e) {
      return null;
    }
  }

  var ls = backend();
  var memory = {};                 // fallback so the page still works

  function set(key, value) {
    var raw = JSON.stringify(value);
    if (ls) {
      try { ls.setItem(PREFIX + key, raw); return true; } catch (e) { /* quota */ }
    }
    memory[key] = raw;
    return false;
  }

  function get(key, fallback) {
    var raw = null;
    if (ls) {
      try { raw = ls.getItem(PREFIX + key); } catch (e) { raw = null; }
    }
    if (raw === null && Object.prototype.hasOwnProperty.call(memory, key)) {
      raw = memory[key];
    }
    if (raw === null || raw === undefined) {
      return fallback === undefined ? null : fallback;
    }
    try {
      return JSON.parse(raw);
    } catch (e) {
      return fallback === undefined ? null : fallback;
    }
  }

  function remove(key) {
    if (ls) { try { ls.removeItem(PREFIX + key); } catch (e) {} }
    delete memory[key];
  }

  function allScores() {
    var scores = get(SCORES_KEY, {});
    return (scores && typeof scores === 'object') ? scores : {};
  }

  function getScore(activityId) {
    var entry = allScores()[activityId];
    if (!entry || typeof entry.score !== 'number') return null;
    return { score: entry.score, max: entry.max };
  }

  /* Best-score semantics: replaying an activity can only improve the
     stored result, so a student can retry without losing their record. */
  function saveScore(activityId, score, max) {
    var scores = allScores();
    var existing = scores[activityId];
    if (!existing || score > existing.score) {
      scores[activityId] = { score: score, max: max, at: new Date().toISOString() };
      set(SCORES_KEY, scores);
    } else if (existing.max !== max) {
      existing.max = max;                 // activity was re-scored
      set(SCORES_KEY, scores);
    }
    return getScore(activityId);
  }

  /* Clears every agai: key, including test results — not just scores. */
  function reset() {
    if (ls) {
      try {
        var doomed = [];
        for (var i = 0; i < ls.length; i++) {
          var k = ls.key(i);
          if (k && k.indexOf(PREFIX) === 0) doomed.push(k);
        }
        for (var j = 0; j < doomed.length; j++) ls.removeItem(doomed[j]);
      } catch (e) {}
    }
    memory = {};
  }

  return {
    set: set,
    get: get,
    remove: remove,
    saveScore: saveScore,
    getScore: getScore,
    allScores: allScores,
    reset: reset
  };
})();
