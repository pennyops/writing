#!/usr/bin/env python3
"""roast_facts.py <url> : first-visitor fact sheet for a shop review (shop-roast lane).
Fetches the page with curl (read-only, one GET per page, no forms, no probing) and prints:
title/meta description, H1/H2s, price mentions, sats/BTC/Lightning mentions, shipping/returns/contact
mentions, image sources (flags mockup/placeholder images), and internal links worth reading next.
Content-only review aid: NOT a security tool. Never use it to test or scan anything."""
import re, subprocess, sys, html
from urllib.parse import urljoin, urlparse

def get(url):
    r = subprocess.run(['curl', '-sL', '-m', '25', '-A', 'Mozilla/5.0', url], capture_output=True)
    return r.stdout.decode('utf-8', 'replace')

def text(h):
    h = re.sub(r'(?is)<(script|style).*?</\1>', ' ', h)
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))).strip()

def main(url):
    h = get(url)
    t = text(h)
    host = urlparse(url).netloc
    def grab(p): return [html.unescape(re.sub('<[^>]+>', '', m)).strip() for m in re.findall(p, h, re.I | re.S)]
    print('URL:', url, '| html bytes:', len(h), '| text chars:', len(t))
    print('TITLE:', grab(r'<title[^>]*>(.*?)</title>')[:1])
    print('META DESC:', re.findall(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', h, re.I)[:1])
    print('H1:', grab(r'<h1[^>]*>(.*?)</h1>')[:5])
    print('H2:', grab(r'<h2[^>]*>(.*?)</h2>')[:10])
    for label, pat in [('PRICES', r'[$€£]\s?\d[\d,.]*|\d[\d,.]*\s?(?:sats|sat|USD|EUR)\b'),
                       ('BTC/LN', r'[^.]{0,60}\b(?:lightning|bitcoin|btcpay|on-?chain|sats)\b[^.]{0,60}'),
                       ('SHIP/RETURNS/CONTACT', r'[^.]{0,60}\b(?:shipping|delivery|returns?|refund|contact|email)\b[^.]{0,60}'),
                       ('DEADLINES/TRUST', r'[^.]{0,60}\b(?:christmas|holiday|order by|reviews?|testimonial|guarantee)\b[^.]{0,60}')]:
        ms = list(dict.fromkeys(m.strip() for m in re.findall(pat, t, re.I)))
        print(f'{label} ({len(ms)}):', ms[:8])
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)', h, re.I)
    flag = [i for i in imgs if re.search(r'mock|placeholder|stock|unsplash', i, re.I)]
    print(f'IMAGES: {len(imgs)} total, {len(flag)} look like mockups/stock:', flag[:5])
    links = {urljoin(url, l) for l in re.findall(r'href=["\']([^"\'#]+)', h, re.I)}
    internal = sorted(l for l in links if urlparse(l).netloc == host)
    print(f'INTERNAL LINKS ({len(internal)}):', internal[:25])

if __name__ == '__main__':
    main(sys.argv[1])
