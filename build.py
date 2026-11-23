#!/usr/bin/env python3
"""셀러 마진·정산 실시간 계산기 & 엑셀 템플릿 스토어 (0520goeus/seller-margin-calc)."""
from __future__ import annotations

import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
KST = timezone(timedelta(hours=9))
NOW = datetime.now(KST)

SITE_URL = "https://0520goeus.github.io/seller-margin-calc"
INDEXNOW_KEY = "c92f8104e73a4c1190b5d21a8e41f009"
GOOGLE_FILE = "google873809343766a3b6.html"
COUPANG_TRACKING = "AF9170267"
COUPANG_WIDGET_ID = 1049499

PROD_DIR = Path("/Users/seogdaehyeon/Documents/수익자동화/상품")


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    (DIST / GOOGLE_FILE).write_text(f"google-site-verification: {GOOGLE_FILE}", encoding="utf-8")
    (DIST / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")

    # Copy preview images if present
    for img_name in ("마진템플릿_대표이미지.png", "마진템플릿_상세이미지.png"):
        src = PROD_DIR / img_name
        if src.exists():
            shutil.copy2(src, DIST / img_name)

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>스마트스토어·쿠팡 셀러 마진 계산기 | 수수료·부가세·순수익 자동 계산</title>
<meta name="description" content="판매가, 매입원가, 마켓 수수료, 택배비, 광고비를 넣으면 스마트스토어·쿠팡 셀러의 실제 순수익과 마진율, 손익분기 판매가를 즉시 계산합니다.">
<link rel="canonical" href="{SITE_URL}/">
<meta property="og:title" content="스마트스토어·쿠팡 셀러 마진 계산기">
<meta property="og:description" content="마켓별 수수료·부가세·광고비를 반영한 실제 순수익·마진율 실시간 계산기">
<meta property="og:url" content="{SITE_URL}/">
<style>
:root{{--bg:#0f172a;--card:#1e293b;--line:#334155;--ink:#f8fafc;--sub:#94a3b8;--accent:#38d9a9;--blue:#3b82f6;--warn:#f59e0b}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 -apple-system,"Apple SD Gothic Neo",sans-serif}}
header{{background:#090d16;border-bottom:1px solid var(--line);padding:16px 20px}}
.wrap{{max-width:940px;margin:0 auto;padding:0 18px}}
header .wrap{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}}
header a{{color:var(--sub);text-decoration:none;font-size:14px;font-weight:600}}
header .brand{{color:#fff;font-size:19px;font-weight:800}}
nav{{display:flex;gap:14px;flex-wrap:wrap}}
main{{padding:28px 0 60px;display:grid;gap:22px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:24px}}
h1{{margin:0 0 8px;font-size:28px;letter-spacing:-.02em}}h2{{margin:0 0 14px;font-size:20px}}
.sub{{color:var(--sub);margin:0 0 16px}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}}
label{{display:grid;gap:6px;font-size:13.5px;color:var(--sub);margin-bottom:12px}}
input,select{{width:100%;padding:11px 13px;border-radius:10px;border:1px solid var(--line);background:#0f172a;color:#fff;font:inherit;font-size:15px}}
.chips{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}}
.chip{{background:#0f172a;border:1px solid var(--line);color:var(--ink);padding:7px 13px;border-radius:99px;cursor:pointer;font-size:13px;font-weight:700}}
.chip.on{{background:var(--blue);border-color:var(--blue);color:#fff}}
.res-box{{background:#0f172a;border:2px solid var(--accent);border-radius:14px;padding:22px;display:grid;gap:12px}}
.big{{font-size:38px;font-weight:800;color:var(--accent);letter-spacing:-.03em}}
.row{{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px dashed var(--line);font-size:14.5px}}
.preview-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:14px}}
.preview-grid img{{width:100%;border-radius:12px;border:1px solid var(--line)}}
.faq{{background:#0f172a;padding:14px 16px;border-radius:10px;margin-bottom:10px}}
footer{{border-top:1px solid var(--line);padding:24px 0 44px;color:var(--sub);font-size:13.5px}}
footer a{{color:var(--accent);text-decoration:none}}
</style>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "스마트스토어·쿠팡 셀러 마진 계산기",
  "url": "{SITE_URL}/",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "All"
}}
</script>
</head>
<body>
<header><div class="wrap">
  <a class="brand" href="{SITE_URL}/">셀러 마진·정산 계산기</a>
  <nav>
    <a href="https://0520goeus.github.io/price-note/">해뎐 가격노트</a>
    <a href="https://0520goeus.github.io/elec-calc/">전기세 얼마</a>
    <a href="https://0520goeus.github.io/life-money-lab/">생활비 연구소</a>
    <a href="https://lifefixnote-kr.blogspot.com/">생활해결 노트</a>
  </nav>
</div></header>

<main class="wrap">
  <section class="card">
    <h1>스마트스토어·쿠팡 셀러 실시간 마진 계산기</h1>
    <p class="sub">마켓별 판매수수료, 배송비 마진, 포장비, 광고비, 부가세(10%)를 모두 반영해 실제 통장에 남는 순수익과 마진율을 즉시 계산합니다.</p>
    <div class="chips">
      <button type="button" class="chip on" onclick="setFee(5.63, this)">스마트스토어 (일반 5.63%)</button>
      <button type="button" class="chip" onclick="setFee(10.8, this)">쿠팡 마켓플레이스 (10.8%)</button>
      <button type="button" class="chip" onclick="setFee(13.0, this)">오픈마켓 평균 (13.0%)</button>
      <button type="button" class="chip" onclick="setFee(3.3, this)">자사몰 PG (3.3%)</button>
    </div>

    <div class="grid2">
      <div>
        <label>판매가 (원) <input id="sell" type="number" value="29900" oninput="calc()"></label>
        <label>매입 원가 (원, 부가세 포함) <input id="cost" type="number" value="12500" oninput="calc()"></label>
        <label>마켓 수수료율 (%) <input id="fee" type="number" step="0.01" value="5.63" oninput="calc()"></label>
        <label>고객 결제 배송비 (원) <input id="shipIn" type="number" value="3000" oninput="calc()"></label>
        <label>실제 발송 택배비+포장비 (원) <input id="shipOut" type="number" value="3200" oninput="calc()"></label>
        <label>주문 1건당 광고비 (원) <input id="ad" type="number" value="1500" oninput="calc()"></label>
      </div>

      <div class="res-box">
        <div>1건 판매 시 실제 순수익 (세후)</div>
        <div class="big" id="netProfit">0원</div>
        <div class="row"><span>순수익 마진율</span><strong id="marginPct" style="color:var(--accent)">0%</strong></div>
        <div class="row"><span>마켓 판매·결제 수수료</span><span id="feeWon">0원</span></div>
        <div class="row"><span>납부 예상 부가세 (매출-매입)</span><span id="vatWon">0원</span></div>
        <div class="row"><span>손익분기 최소 판매가 (마진 0원)</span><strong id="breakEven" style="color:var(--warn)">0원</strong></div>
        <div class="row"><span>월 100건 판매 시 예상 순수익</span><strong id="month100">0원</strong></div>
        <div class="row"><span>월 500건 판매 시 예상 순수익</span><strong id="month500">0원</strong></div>
      </div>
    </div>
  </section>

  <section class="card">
    <p style="font-size:12.5px;color:var(--sub);margin:0 0 10px;">이 페이지는 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>
    <h2>셀러 필수 택배·포장·사무 소모품 최저가</h2>
    <script src="https://ads-partners.coupang.com/g.js"></script>
    <script>new PartnersCoupang.G({{"id":{COUPANG_WIDGET_ID},"template":"carousel","trackingCode":"{COUPANG_TRACKING}","width":"100%","height":"140","tsource":""}});</script>
  </section>

  <section class="card">
    <h2>다품목 대량 관리용 [셀러 마진·정산 자동계산 엑셀 템플릿 v1]</h2>
    <p class="sub">MOS Excel Expert가 제작한 매크로 없는 순수 수식형 다채널 정산·마진 시뮬레이터 시트입니다. 상품 수십~수백 개의 마켓별 마진과 월간 정산금을 한눈에 관리할 수 있습니다.</p>
    <div class="preview-grid">
      <img src="{SITE_URL}/마진템플릿_대표이미지.png" alt="셀러 마진정산 자동계산 엑셀 템플릿 대표 이미지" loading="lazy">
      <img src="{SITE_URL}/마진템플릿_상세이미지.png" alt="셀러 마진정산 자동계산 엑셀 템플릿 상세 화면" loading="lazy">
    </div>
  </section>

  <section class="card">
    <h2>자주 묻는 질문 (FAQ)</h2>
    <div class="faq"><strong>Q. 스마트스토어와 쿠팡 수수료에 배송비 수수료도 포함되나요?</strong><p class="sub" style="margin:6px 0 0">네, 실제 마켓 정산에서는 배송비에도 결제 수수료(약 3.3~3.63%)가 부과되므로 이 계산기는 배송비 수수료까지 함께 반영해 보수적으로 순수익을 계산합니다.</p></div>
    <div class="faq"><strong>Q. 일반과세자 부가세(VAT)는 어떻게 계산되나요?</strong><p class="sub" style="margin:6px 0 0">총 매출(판매가+고객배송비)의 부가세 예수금에서 매입원가·수수료·택배비·광고비의 매입세액 공제분을 뺀 실제 납부 예상 부가세를 자동 차감합니다.</p></div>
  </section>
</main>

<footer><div class="wrap">
  <p>패밀리 도구: <a href="https://0520goeus.github.io/price-note/">해뎐 가격노트 (588 생필품)</a> · <a href="https://0520goeus.github.io/elec-calc/">전기세 얼마 (24 가전 계산기)</a> · <a href="https://0520goeus.github.io/life-money-lab/">생활비 물가 연구소</a> · <a href="https://lifefixnote-kr.blogspot.com/">생활해결 노트</a></p>
</div></footer>

<script>
function setFee(v, btn){{
  document.getElementById('fee').value = v;
  document.querySelectorAll('.chip').forEach(c=>c.classList.remove('on'));
  btn.classList.add('on');
  calc();
}}
function won(n){{return Math.round(n).toLocaleString('ko-KR') + '원';}}
function calc(){{
  const sell = parseFloat(document.getElementById('sell').value)||0;
  const cost = parseFloat(document.getElementById('cost').value)||0;
  const feePct = parseFloat(document.getElementById('fee').value)||0;
  const shipIn = parseFloat(document.getElementById('shipIn').value)||0;
  const shipOut = parseFloat(document.getElementById('shipOut').value)||0;
  const ad = parseFloat(document.getElementById('ad').value)||0;

  const feeWon = sell * (feePct/100) + shipIn * 0.033;
  const revTotal = sell + shipIn;
  const deductible = cost + feeWon + shipOut + ad;
  const vat = Math.max(0, (revTotal - deductible) / 11);
  const net = revTotal - deductible - vat;
  const margin = sell > 0 ? (net / sell * 100) : 0;
  const breakEven = (cost + shipOut - shipIn + ad) / Math.max(0.1, (1 - feePct/100));

  document.getElementById('netProfit').textContent = won(net);
  document.getElementById('marginPct').textContent = margin.toFixed(1) + '%';
  document.getElementById('feeWon').textContent = won(feeWon);
  document.getElementById('vatWon').textContent = won(vat);
  document.getElementById('breakEven').textContent = won(breakEven);
  document.getElementById('month100').textContent = won(net * 100);
  document.getElementById('month500').textContent = won(net * 500);
}}
calc();
</script>
</body>
</html>"""
    (DIST / "index.html").write_text(html, encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"<url><loc>{SITE_URL}/</loc><lastmod>{NOW.strftime('%Y-%m-%d')}</lastmod></url>\n</urlset>\n",
        encoding="utf-8",
    )
    (DIST / "urls.txt").write_text(f"{SITE_URL}/\n", encoding="utf-8")
    print("셀러 마진 계산기 스토어 빌드 완료 -> dist/")


if __name__ == "__main__":
    main()
