/* ============================================================
   deck.js — the slide engine. Vanilla, no dependencies, offline.

   Authoring format:
     <div class="deck" data-title="Day 1 — From token to typed output">
       <section class="slide slide--title"> … </section>
       <section class="slide"> …
         <aside class="notes"><p>What I say out loud.</p></aside>
       </section>
     </div>

   Everything else on the page — top bar, dot strip, counter, notes
   panel, help overlay, print furniture — is built here at load.

   Keys: → ← Space PageDown PageUp Home End · P notes · F fullscreen
         ? help · Esc close
   ============================================================ */

(function () {
  'use strict';

  /* The deck lives in slides/, the logos in assets/. Derive the assets
     path from this script's own URL so the engine works from any depth
     and stays relative — GitHub Pages project sites break on absolute
     paths. */
  var ASSETS = (function () {
    var src = (document.currentScript && document.currentScript.src) || '';
    return src ? src.replace(/[^/]+$/, '') : '../assets/';
  })();

  var CANVAS_W = 1280;
  var CANVAS_H = 720;

  document.addEventListener('DOMContentLoaded', function () {
    var deck = document.querySelector('.deck');
    if (!deck) return;
    new Deck(deck);
  });

  function Deck(deck) {
    var self = this;

    this.deck = deck;
    this.title = deck.getAttribute('data-title') || document.title;
    this.slides = Array.prototype.slice.call(deck.querySelectorAll('.slide'));
    this.index = 0;
    this.notesOpen = false;

    document.body.classList.add('deck-body');

    this.wrapSlides();
    this.buildBar();
    this.buildStage();
    this.buildDots();
    this.buildCounter();
    this.buildNotes();
    this.buildHelp();
    this.bindKeys();
    this.bindPointer();
    this.bindHash();

    window.addEventListener('resize', function () { self.fit(); });
    window.addEventListener('orientationchange', function () { self.fit(); });

    this.go(this.indexFromHash(), { replaceHash: true });
    this.fit();
  }

  /* ---- Structure ------------------------------------------ */

  /* Each slide is wrapped so that print can give it a page of its own,
     a logo header and its notes underneath. Notes are lifted out of the
     slide (they must not take part in the slide's flex layout). */
  Deck.prototype.wrapSlides = function () {
    var self = this;

    this.slides.forEach(function (slide, i) {
      var wrap = document.createElement('div');
      wrap.className = 'slide-wrap';

      /* Running head for print. The logos themselves live inside the
         slide (see stampLogos) so they print with it and match the
         slide's own background. */
      var head = document.createElement('div');
      head.className = 'slide-print-head';
      head.setAttribute('aria-hidden', 'true');
      head.innerHTML =
        '<span>' + escapeHtml(self.title) + '</span>' +
        '<span>' + (i + 1) + ' / ' + self.slides.length + '</span>';

      var box = document.createElement('div');
      box.className = 'slide-print-box';

      slide.parentNode.insertBefore(wrap, slide);
      wrap.appendChild(head);
      wrap.appendChild(box);
      box.appendChild(slide);

      var notes = slide.querySelector('.notes');
      if (notes) wrap.appendChild(notes);       // out of the slide, into the wrap

      self.stampLogos(slide, i === 0 || i === self.slides.length - 1);

      slide.setAttribute('role', 'group');
      slide.setAttribute('aria-roledescription', 'slide');
      slide.setAttribute('aria-label', 'Slide ' + (i + 1) + ' of ' + self.slides.length);
      slide.dataset.index = String(i);
      self.notesFor = self.notesFor || [];
      self.notesFor[i] = notes ? notes.innerHTML : '';
    });
  };

  /* Both logos on every slide: SDAIA Academy left, SDAIA right.
     Large on the first and last slide, small and quiet in between.
     Each logo ships as a colour and a white PNG; deck.css shows the
     white pair on dark slide layouts.

     Only the large pair carries alt text. The small pair repeats on
     every slide and is decorative there — announcing "SDAIA Academy,
     SDAIA" twenty-six times to a screen reader is noise, not access. */
  Deck.prototype.stampLogos = function (slide, big) {
    var alt = big ? ' alt="SDAIA Academy"' : ' alt=""';
    var altS = big ? ' alt="Saudi Data and AI Authority (SDAIA)"' : ' alt=""';

    var logos = document.createElement('div');
    logos.className = 'slide__logos';
    if (!big) logos.setAttribute('aria-hidden', 'true');
    logos.innerHTML =
      '<span class="slide__logo">' +
        '<img class="l-color" src="' + ASSETS + 'academy_color.png"' + alt + '>' +
        '<img class="l-white" src="' + ASSETS + 'academy_white.png"' + alt + '>' +
      '</span>' +
      '<span class="slide__logo">' +
        '<img class="l-color" src="' + ASSETS + 'sdaia_color.png"' + altS + '>' +
        '<img class="l-white" src="' + ASSETS + 'sdaia_white.png"' + altS + '>' +
      '</span>';

    if (big) slide.classList.add('slide--logos-big');
    slide.appendChild(logos);
  };

  Deck.prototype.buildBar = function () {
    var self = this;
    var bar = document.createElement('div');
    bar.className = 'deck-bar';
    bar.innerHTML =
      '<a class="deck-bar__home" href="../index.html">← Course home</a>' +
      '<span class="deck-bar__title">' + escapeHtml(this.title) + '</span>';

    this.notesBtn = button('Notes (P)', 'Toggle presenter notes');
    this.notesBtn.setAttribute('aria-pressed', 'false');
    this.notesBtn.addEventListener('click', function () { self.toggleNotes(); });

    this.fsBtn = button('Fullscreen (F)', 'Toggle fullscreen');
    this.fsBtn.addEventListener('click', function () { self.toggleFullscreen(); });

    this.printBtn = button('Print to PDF', 'Print this deck, one slide per page');
    this.printBtn.addEventListener('click', function () { self.print(); });

    this.helpBtn = button('?', 'Keyboard shortcuts');
    this.helpBtn.addEventListener('click', function () { self.toggleHelp(true); });

    bar.appendChild(this.notesBtn);
    bar.appendChild(this.fsBtn);
    bar.appendChild(this.printBtn);
    bar.appendChild(this.helpBtn);
    document.body.insertBefore(bar, document.body.firstChild);
    this.bar = bar;
  };

  /* The deck is moved inside a fixed, centred stage so the scaled
     canvas has something to be centred in. */
  Deck.prototype.buildStage = function () {
    var stage = document.createElement('div');
    stage.className = 'deck-stage';
    this.deck.parentNode.insertBefore(stage, this.deck);
    stage.appendChild(this.deck);
    this.stage = stage;

    var live = document.createElement('div');
    live.className = 'sr-only';
    live.setAttribute('aria-live', 'polite');
    live.style.cssText = 'position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;';
    document.body.appendChild(live);
    this.live = live;
  };

  Deck.prototype.buildDots = function () {
    var self = this;
    var dots = document.createElement('nav');
    dots.className = 'deck-dots';
    dots.setAttribute('aria-label', 'Slides');

    this.dots = this.slides.map(function (slide, i) {
      var dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'deck-dot';
      dot.setAttribute('aria-label', 'Go to slide ' + (i + 1));
      dot.addEventListener('click', function () { self.go(i); });
      dots.appendChild(dot);
      return dot;
    });

    document.body.appendChild(dots);
  };

  Deck.prototype.buildCounter = function () {
    var counter = document.createElement('div');
    counter.className = 'deck-counter';
    document.body.appendChild(counter);
    this.counter = counter;
  };

  Deck.prototype.buildNotes = function () {
    var panel = document.createElement('aside');
    panel.className = 'deck-notes';
    panel.id = 'deck-notes';
    panel.hidden = true;
    panel.setAttribute('aria-label', 'Presenter notes');
    panel.innerHTML = '<p class="deck-notes__label">Presenter notes</p><div class="deck-notes__body"></div>';
    document.body.appendChild(panel);
    this.notesPanel = panel;
    this.notesBody = panel.querySelector('.deck-notes__body');
    this.notesBtn.setAttribute('aria-controls', 'deck-notes');
  };

  Deck.prototype.buildHelp = function () {
    var self = this;
    var help = document.createElement('div');
    help.className = 'deck-help';
    help.hidden = true;
    help.setAttribute('role', 'dialog');
    help.setAttribute('aria-modal', 'true');
    help.setAttribute('aria-label', 'Keyboard shortcuts');
    help.innerHTML =
      '<div class="deck-help__panel">' +
        '<h2>Keyboard shortcuts</h2>' +
        '<dl>' +
          '<dt><kbd>→</kbd> <kbd>Space</kbd> <kbd>PgDn</kbd></dt><dd>Next slide</dd>' +
          '<dt><kbd>←</kbd> <kbd>PgUp</kbd></dt><dd>Previous slide</dd>' +
          '<dt><kbd>Home</kbd> / <kbd>End</kbd></dt><dd>First / last slide</dd>' +
          '<dt><kbd>P</kbd></dt><dd>Presenter notes</dd>' +
          '<dt><kbd>F</kbd></dt><dd>Fullscreen</dd>' +
          '<dt><kbd>?</kbd></dt><dd>This help</dd>' +
          '<dt><kbd>Esc</kbd></dt><dd>Close</dd>' +
        '</dl>' +
        '<p class="small muted">Click the left or right third of the screen, or swipe, to move between slides. The URL ends in the slide number, so a refresh keeps your place.</p>' +
        '<p><button type="button" class="btn" data-help-close>Close</button></p>' +
      '</div>';
    document.body.appendChild(help);

    help.querySelector('[data-help-close]').addEventListener('click', function () { self.toggleHelp(false); });
    help.addEventListener('click', function (e) {
      if (e.target === help) self.toggleHelp(false);      // click the backdrop
    });
    this.help = help;
  };

  /* ---- Navigation ----------------------------------------- */

  Deck.prototype.go = function (index, opts) {
    opts = opts || {};
    var n = this.slides.length;
    index = Math.max(0, Math.min(n - 1, index));
    this.index = index;

    this.slides.forEach(function (slide, i) {
      slide.classList.toggle('is-active', i === index);
    });
    this.dots.forEach(function (dot, i) {
      if (i === index) dot.setAttribute('aria-current', 'true');
      else dot.removeAttribute('aria-current');
    });

    this.counter.textContent = (index + 1) + ' / ' + n;
    this.notesBody.innerHTML = this.notesFor[index] ||
      '<p class="muted">No notes on this slide.</p>';
    this.live.textContent = 'Slide ' + (index + 1) + ' of ' + n;

    var hash = '#' + (index + 1);
    if (window.location.hash !== hash) {
      /* replaceState, not a hash assignment: paging through 26 slides
         should not fill the back button with 26 entries. */
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, '', hash);
      } else if (!opts.replaceHash) {
        window.location.hash = hash;
      }
    }
  };

  Deck.prototype.next = function () { this.go(this.index + 1); };
  Deck.prototype.prev = function () { this.go(this.index - 1); };

  Deck.prototype.indexFromHash = function () {
    var raw = (window.location.hash || '').replace('#', '');
    var n = parseInt(raw, 10);
    return isNaN(n) ? 0 : n - 1;
  };

  Deck.prototype.bindHash = function () {
    var self = this;
    window.addEventListener('hashchange', function () {
      var i = self.indexFromHash();
      if (i !== self.index) self.go(i);
    });
  };

  /* ---- Fit to viewport ------------------------------------ */

  Deck.prototype.fit = function () {
    var barH = this.bar ? this.bar.offsetHeight : 0;
    var dotsH = 34;
    var availW = window.innerWidth - 24;
    var availH = window.innerHeight - barH - dotsH - 16;
    var scale = Math.min(availW / CANVAS_W, availH / CANVAS_H);
    if (!isFinite(scale) || scale <= 0) scale = 1;

    this.deck.style.transform = 'scale(' + scale + ')';
    /* Keep the scaled canvas visually centred in the space left below
       the bar (the stage itself covers the whole viewport). */
    this.stage.style.paddingTop = (barH - dotsH) + 'px';
  };

  /* ---- Input ---------------------------------------------- */

  Deck.prototype.bindKeys = function () {
    var self = this;

    document.addEventListener('keydown', function (e) {
      if (e.defaultPrevented) return;

      var t = e.target;
      var typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' ||
                         t.tagName === 'SELECT' || t.isContentEditable);

      if (e.key === 'Escape') {
        if (!self.help.hidden) { self.toggleHelp(false); e.preventDefault(); }
        else if (self.notesOpen) { self.toggleNotes(false); e.preventDefault(); }
        return;
      }

      /* Let people type into the live widgets on slides without
         paging the deck out from under them. */
      if (typing) return;

      switch (e.key) {
        case 'ArrowRight':
        case 'PageDown':
          self.next(); e.preventDefault(); break;
        case ' ':
        case 'Spacebar':
          /* Space on a focused button must still press the button. */
          if (t && (t.tagName === 'BUTTON' || t.tagName === 'A')) return;
          self.next(); e.preventDefault(); break;
        case 'ArrowLeft':
        case 'PageUp':
          self.prev(); e.preventDefault(); break;
        case 'Home':
          self.go(0); e.preventDefault(); break;
        case 'End':
          self.go(self.slides.length - 1); e.preventDefault(); break;
        case 'p': case 'P':
          self.toggleNotes(); e.preventDefault(); break;
        case 'f': case 'F':
          self.toggleFullscreen(); e.preventDefault(); break;
        case '?':
          self.toggleHelp(self.help.hidden); e.preventDefault(); break;
        default: break;
      }
    });
  };

  Deck.prototype.bindPointer = function () {
    var self = this;

    /* Click the outer thirds to page. Clicks on anything interactive,
       or on the chrome, are left alone. */
    this.stage.addEventListener('click', function (e) {
      if (e.target.closest('a, button, input, textarea, select, label, .deck-bar, .deck-notes, .deck-help')) return;
      var third = window.innerWidth / 3;
      if (e.clientX < third) self.prev();
      else if (e.clientX > third * 2) self.next();
    });

    var x0 = null, y0 = null;
    this.stage.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1) return;
      x0 = e.touches[0].clientX;
      y0 = e.touches[0].clientY;
    }, { passive: true });

    this.stage.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var t = e.changedTouches[0];
      var dx = t.clientX - x0;
      var dy = t.clientY - y0;
      x0 = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
        if (dx < 0) self.next(); else self.prev();
      }
    }, { passive: true });
  };

  /* ---- Toggles -------------------------------------------- */

  Deck.prototype.toggleNotes = function (force) {
    this.notesOpen = (force === undefined) ? !this.notesOpen : !!force;
    this.notesPanel.hidden = !this.notesOpen;
    this.notesBtn.setAttribute('aria-pressed', this.notesOpen ? 'true' : 'false');
    document.body.classList.toggle('notes-open', this.notesOpen);
    this.fit();
  };

  Deck.prototype.toggleHelp = function (show) {
    if (show) {
      this.helpReturn = document.activeElement;
      this.help.hidden = false;
      this.help.querySelector('[data-help-close]').focus();
    } else {
      this.help.hidden = true;
      if (this.helpReturn && this.helpReturn.focus) this.helpReturn.focus();
    }
  };

  Deck.prototype.toggleFullscreen = function () {
    var el = document.documentElement;
    if (!document.fullscreenElement) {
      if (el.requestFullscreen) el.requestFullscreen();
    } else if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  };

  /* Print: the class is a hook for anything that needs to know, the
     @media print block in deck.css does the real work. */
  Deck.prototype.print = function () {
    document.body.classList.add('printing');
    window.addEventListener('afterprint', function handler() {
      document.body.classList.remove('printing');
      window.removeEventListener('afterprint', handler);
    });
    window.print();
  };

  /* ---- Helpers -------------------------------------------- */

  function button(label, title) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'deck-btn';
    b.textContent = label;
    b.title = title;
    return b;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c];
    });
  }
})();
