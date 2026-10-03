// Stil-Fingerabdruck einer Seite: berechnete Stile und Lage aller sichtbaren Elemente als JSON.
// Fuer Regressionstests nach Umbauten (CSS zusammenfuehren, CMS): vorher und nachher vergleichen (_tools/fpdiff.py).
(function(){
  const K=['display','position','color','backgroundColor','backgroundImage','fontFamily','fontSize','fontWeight','fontStyle','lineHeight','letterSpacing','textTransform','borderTopWidth','borderTopColor','borderRadius','paddingTop','paddingLeft','marginTop','opacity','transform','boxShadow','gap','gridTemplateColumns','zIndex','overflow','textAlign'];
  const out=[]; let i=0;
  for (const el of document.querySelectorAll('body *')) {
    if (el.closest('script,style,svg defs')) continue;
    const r=el.getBoundingClientRect(); const cs=getComputedStyle(el);
    if (cs.display==='none') continue;
    const sig=[el.tagName, (el.getAttribute('class')||'').replace(/\b(in|vis|on|lit|is-on|is-best|zdone|mb-[a-z]+|loaded|mready)\b/g,'').trim(), Math.round(r.x), Math.round(r.y+scrollY), Math.round(r.width), Math.round(r.height)];
    for (const k of K) sig.push(cs[k]);
    const b=getComputedStyle(el,'::before'), a=getComputedStyle(el,'::after');
    if (b.content && b.content!=='none') sig.push('B:'+b.content+'|'+b.backgroundColor+'|'+b.borderRadius+'|'+b.width);
    if (a.content && a.content!=='none') sig.push('A:'+a.content+'|'+a.backgroundColor+'|'+a.borderRadius+'|'+a.width);
    if (el.children.length===0) sig.push((el.textContent||'').trim().slice(0,40));
    out.push(sig.join('¦')); i++;
  }
  return JSON.stringify({url:location.pathname, n:i, items:out});
})()
