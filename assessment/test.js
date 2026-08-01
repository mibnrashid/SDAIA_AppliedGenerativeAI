/* ============================================================
   test.js — the shared engine for both tests.

   The page sets window.TEST_MODE to 'pretest' or 'posttest' before
   loading this file. Everything else is identical, which is the point:
   the two tests cannot drift apart.

   Layout decision — all 20 questions on ONE page, not one per screen:
   a 15-minute in-class test on laptops rewards skimming, skipping the
   hard one and coming back, and seeing how much is left; a one-per-screen
   wizard adds 20 transitions and hides progress behind a bar.

   Storage: agai:pretest / agai:posttest -> {score, max, at}
   ============================================================ */

(function () {
  'use strict';

  var MODE = window.TEST_MODE === 'posttest' ? 'posttest' : 'pretest';
  var IS_POST = MODE === 'posttest';
  var LABEL = IS_POST ? 'Post-test' : 'Pre-test';

  var form, list, bar, meter, countEl, submitBtn, resultEl;

  document.addEventListener('DOMContentLoaded', function () {
    form = document.getElementById('test-form');
    list = document.getElementById('qlist');
    bar = document.getElementById('testbar');
    meter = document.getElementById('meter-fill');
    countEl = document.getElementById('answered-count');
    submitBtn = document.getElementById('submit-test');
    resultEl = document.getElementById('result');

    render();
    form.addEventListener('change', updateProgress);
    form.addEventListener('submit', onSubmit);
    updateProgress();
  });

  function render() {
    QUESTIONS.forEach(function (q, i) {
      var li = document.createElement('li');

      var fs = document.createElement('fieldset');
      fs.className = 'q';
      fs.id = 'q-' + q.id;

      var legend = document.createElement('legend');
      legend.innerHTML =
        '<span class="q__num">' + (i + 1) + '.</span>' + escapeHtml(q.q) +
        '<span class="q__topic">' + escapeHtml(q.topic) + '</span>';
      fs.appendChild(legend);

      var opts = document.createElement('div');
      opts.className = 'opts';

      q.options.forEach(function (text, oi) {
        var label = document.createElement('label');
        label.className = 'opt';
        label.dataset.option = String(oi);

        var input = document.createElement('input');
        input.type = 'radio';
        input.name = q.id;
        input.value = String(oi);

        var span = document.createElement('span');
        span.textContent = text;

        label.appendChild(input);
        label.appendChild(span);
        opts.appendChild(label);
      });

      fs.appendChild(opts);
      li.appendChild(fs);
      list.appendChild(li);
    });
  }

  function answeredCount() {
    var n = 0;
    QUESTIONS.forEach(function (q) {
      if (form.elements[q.id] && form.elements[q.id].value !== '') n++;
    });
    return n;
  }

  function updateProgress() {
    var n = answeredCount();
    countEl.textContent = n + ' of ' + QUESTIONS.length + ' answered';
    meter.style.width = Math.round((n / QUESTIONS.length) * 100) + '%';
    meter.parentNode.setAttribute('aria-valuenow', String(n));
  }

  function onSubmit(e) {
    e.preventDefault();

    var unanswered = QUESTIONS.length - answeredCount();
    if (unanswered > 0) {
      var ok = window.confirm(
        unanswered + ' question' + (unanswered === 1 ? '' : 's') +
        ' still blank. Submit anyway? Blank counts as wrong.');
      if (!ok) return;
    }

    var score = 0;
    QUESTIONS.forEach(function (q) {
      var field = form.elements[q.id];
      var picked = field && field.value !== '' ? parseInt(field.value, 10) : -1;
      if (picked === q.answer) score++;
      markQuestion(q, picked);
    });

    Store.set(MODE, { score: score, max: QUESTIONS.length, at: new Date().toISOString() });
    showResult(score);
  }

  /* The pre-test must not reveal answers. The post-test must. */
  function markQuestion(q, picked) {
    var fs = document.getElementById('q-' + q.id);
    var labels = fs.querySelectorAll('.opt');

    Array.prototype.forEach.call(labels, function (label, oi) {
      label.querySelector('input').disabled = true;
      if (!IS_POST) return;

      if (oi === q.answer) {
        label.classList.add('opt--correct');
        label.insertAdjacentHTML('beforeend', '<span class="opt__mark">Correct</span>');
      } else if (oi === picked) {
        label.classList.add('opt--wrong');
        label.insertAdjacentHTML('beforeend', '<span class="opt__mark">Your answer</span>');
      }
    });

    if (IS_POST) {
      var ex = document.createElement('div');
      ex.className = 'explain';
      ex.innerHTML = '<strong>Why</strong>' + escapeHtml(q.explanation);
      fs.appendChild(ex);
    }
  }

  function showResult(score) {
    bar.hidden = true;

    var html =
      '<h2 class="result__score">' + score + ' / ' + QUESTIONS.length + '</h2>' +
      '<p class="lede" style="margin-inline:auto">' +
        (IS_POST
          ? 'That is your post-test score. Read it out for the SDAIA sheet, then look through the answers below.'
          : 'That is your starting point. It measures the course, not you — a low score today is exactly what Sunday morning is for.') +
      '</p>';

    if (IS_POST) {
      var pre = Store.get('pretest', null);
      if (pre && typeof pre.score === 'number') {
        var delta = score - pre.score;
        var word = delta > 0 ? '+' + delta : String(delta);
        html += '<p class="result__delta">You went from <strong>' + pre.score +
                '</strong> to <strong>' + score + '</strong>. <strong>' + word + '</strong>.</p>';
      } else {
        html += '<p class="result__delta">No pre-test score saved on this device, so there is no comparison to show.</p>';
      }
    }

    html +=
      '<div class="result__actions">' +
        '<button type="button" class="btn" id="copy-result">Copy my result</button>' +
        '<a class="btn btn--ghost" href="../index.html">Back to the course home</a>' +
      '</div>' +
      '<p id="copy-status" class="small" aria-live="polite"></p>';

    resultEl.innerHTML = html;
    resultEl.hidden = false;
    resultEl.setAttribute('tabindex', '-1');
    resultEl.focus();
    resultEl.scrollIntoView({ behavior: 'smooth', block: 'start' });

    document.getElementById('copy-result')
      .addEventListener('click', function () { copyResult(score); });
  }

  /* One tap, because students read this out for the attendance sheet. */
  function copyResult(score) {
    var text = LABEL + ': ' + score + '/' + QUESTIONS.length;
    var status = document.getElementById('copy-status');

    function done() { status.innerHTML = '<span class="copied">Copied — ' + escapeHtml(text) + '</span>'; }
    function failed() { status.textContent = 'Could not copy automatically. Your result is: ' + text; }

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }

    /* execCommand path, for browsers that block the async clipboard on
       a page served from file:// — which happens at a venue. */
    function fallback() {
      try {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.style.cssText = 'position:absolute;left:-9999px';
        document.body.appendChild(ta);
        ta.select();
        var ok = document.execCommand('copy');
        document.body.removeChild(ta);
        ok ? done() : failed();
      } catch (e) {
        failed();
      }
    }
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c];
    });
  }
})();
