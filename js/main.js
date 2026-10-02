document.addEventListener('DOMContentLoaded', function () {
  var L = (document.documentElement.lang || 'fr').slice(0, 2);
  var M = {
    fr: { req: 'Merci de compléter les champs obligatoires et de cocher la case de consentement.', wip: 'Le formulaire est en cours d\'activation. Écrivez-nous directement à ', sending: 'Envoi en cours', ok: 'Merci. Votre demande est bien arrivée, nous revenons vers vous très vite.', ko: 'L\'envoi n\'a pas abouti. Écrivez-nous directement à ', btn: 'Envoyer ma demande' },
    de: { req: 'Bitte füllen Sie die Pflichtfelder aus und bestätigen Sie die Einwilligung.', wip: 'Das Formular wird gerade aktiviert. Schreiben Sie uns direkt an ', sending: 'Wird gesendet', ok: 'Vielen Dank. Ihre Anfrage ist bei uns eingegangen, wir melden uns rasch.', ko: 'Das Senden hat nicht geklappt. Schreiben Sie uns direkt an ', btn: 'Anfrage senden' },
    en: { req: 'Please complete the required fields and tick the consent box.', wip: 'The form is being activated. Please write to us directly at ', sending: 'Sending', ok: 'Thank you. Your request has arrived, we will get back to you shortly.', ko: 'Sending failed. Please write to us directly at ', btn: 'Send my request' }
  }[L] || {};
  var mail = '<a href="mailto:lrohmer@leadr.ch">lrohmer@leadr.ch</a>.';
  var bar = document.querySelector('.mbar');
  if (bar && !document.querySelector('.form')) {
    var onS = function () { var on = window.scrollY > 640; bar.classList.toggle('show', on); bar.setAttribute('aria-hidden', on ? 'false' : 'true'); bar.querySelectorAll('a').forEach(function (a) { a.tabIndex = on ? 0 : -1; }); };
    window.addEventListener('scroll', onS, { passive: true }); onS();
  }
  var t = document.querySelector('.nav-toggle'), n = document.getElementById('nav');
  if (t && n) t.addEventListener('click', function () {
    var o = n.classList.toggle('open'); t.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
  var f = document.querySelector('.form');
  if (f) f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var msg = f.querySelector('.form-msg');
    msg.className = 'form-msg';
    if (!f.checkValidity()) { msg.classList.add('err'); msg.textContent = M.req; f.reportValidity(); return; }
    var b = f.querySelector('button'); b.disabled = true; b.textContent = M.sending;
    fetch(f.action, { method: 'POST', body: new FormData(f), headers: { 'Accept': 'application/json' } })
      .then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (d) { if (d && (d.success === false || d.success === 'false')) throw 0; f.reset(); msg.textContent = M.ok; })
      .catch(function () { msg.classList.add('err'); msg.innerHTML = M.ko + mail; })
      .finally(function () { b.disabled = false; b.textContent = M.btn; });
  });
});
