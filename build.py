#!/usr/bin/env python3
"""스마트스토어·쿠팡·오픈마켓 셀러 마진·수수료·ROAS 계산기 (0520goeus/seller-margin-calc) — 26개 고단가 B2B SEO 페이지."""
from __future__ import annotations

import html
import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
KST = timezone(timedelta(hours=9))
NOW = datetime.now(KST)

SITE_NAME = "셀러 마진·수수료 계산기"
SITE_URL = "https://0520goeus.github.io/seller-margin-calc"
INDEXNOW_KEY = "c92f8104e73a4c1190b5d21a8e41f009"
GOOGLE_FILE = "google873809343766a3b6.html"
ADSENSE_CLIENT = "ca-pub-8749404731911210"
COUPANG_TRACKING = "AF9170267"
COUPANG_WIDGET_ID = 1049499
PROD_DIR = Path("/Users/seogdaehyeon/Documents/수익자동화/상품")

DISCLOSURE = "이 페이지는 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
COUPANG_BOX = (
    '<section class="card">'
    f'<p style="font-size:12.5px;color:var(--sub);margin:0 0 8px;">{DISCLOSURE}</p>'
    '<h2>📦 셀러 필수 택배박스·라벨프린터·포장 소모품 최저가</h2>'
    '<script src="https://ads-partners.coupang.com/g.js"></script>'
    f'<script>new PartnersCoupang.G({{"id":{COUPANG_WIDGET_ID},"template":"carousel",'
    f'"trackingCode":"{COUPANG_TRACKING}","width":"100%","height":"140","tsource":""}});</script>'
    "</section>"
)

# 25 High-CPC Korean E-Commerce Seller Fee & Margin Calculator Pages
CHANNELS = [
    ("smartstore-basic", "네이버 스마트스토어 (영세·중소)", 3.98, 29900, 12500, "네이버페이 주문관리수수료(영세~중소 구간) + 쇼핑검색 유입수수료(2%) 합산 기준"),
    ("smartstore-general", "네이버 스마트스토어 (일반 사업자)", 5.63, 29900, 12500, "일반 사업자 결제수수료 3.63% + 네이버 쇼핑 연동수수료 2.0% = 5.63% 기준"),
    ("smartstore-brand", "네이버 브랜드스토어", 6.0, 49000, 21000, "브랜드스토어 기본 수수료 및 연동 수수료 합산 기준"),
    ("coupang-living", "쿠팡 윙 — 생활용품·주방", 10.8, 24900, 9500, "쿠팡 마켓플레이스 생활·주방 카테고리 판매수수료 10.8% (부가세 별도 시 11.88%)"),
    ("coupang-fashion", "쿠팡 윙 — 패션·의류·잡화", 10.5, 34900, 13000, "쿠팡 패션·의류 카테고리 기본 판매수수료 10.5% 기준"),
    ("coupang-digital", "쿠팡 윙 — 가전·디지털", 7.8, 89000, 52000, "가전·디지털 카테고리는 수수료가 5.8~7.8%로 낮지만 반품·AS 비용 반영 필수"),
    ("coupang-food", "쿠팡 윙 — 식품·건강기능식품", 10.6, 29900, 11500, "쿠팡 가공식품·건강기능식품 판매수수료 10.6% 기준"),
    ("coupang-beauty", "쿠팡 윙 — 뷰티·화장품", 9.6, 26000, 8500, "쿠팡 화장품·뷰티 카테고리 판매수수료 9.6% 기준"),
    ("coupang-pet", "쿠팡 윙 — 반려동물 용품", 10.8, 22900, 8800, "반려동물 사료·용품 카테고리 판매수수료 10.8% 기준"),
    ("coupang-rocket-growth", "쿠팡 로켓그로스 (입출고+배송비 포함)", 10.8, 25900, 9200, "로켓그로스 판매수수료 10.8% 외에 소형·중형 풀필먼트 입출고/배송비 약 3,500~4,500원 반영"),
    ("gmarket-general", "G마켓 (지마켓) 일반 카테고리", 12.0, 29900, 12000, "지마켓 일반 판매수수료 12% + 서버이용료 고려"),
    ("auction-general", "옥션 (Auction) 일반 카테고리", 12.0, 29900, 12000, "옥션 일반 카테고리 12% 수수료 기준"),
    ("11st-general", "11번가 일반 판매자", 13.0, 29900, 12000, "11번가 기본 판매수수료 13% 기준"),
    ("aliexpress-kr", "알리익스프레스 K-Venue 국내셀러", 5.0, 24900, 10000, "알리익스프레스 K-Venue 입점 프로모션·기본 수수료 구간 시뮬레이션"),
    ("ably-fashion", "에이블리 (ABLY) 패션·뷰티", 11.0, 32000, 12000, "에이블리 입점 판매수수료 및 결제수수료 합산 약 11% 기준"),
    ("zigzag-fashion", "지그재그 (Zigzag) 패션 셀러", 12.5, 35000, 13000, "지그재그 통합결제 및 유입 수수료 기준"),
    ("musinsa-brand", "무신사·29CM 입점 브랜드", 28.0, 69000, 22000, "패션 플랫폼 위탁/입점 수수료 25~30% 구간 손익분기 계산"),
    ("ohouse-living", "오늘의집 인테리어·가구 셀러", 14.0, 59000, 26000, "오늘의집 리빙·인테리어 카테고리 평균 수수료 14% 기준"),
    ("kakao-shopping", "카카오톡 쇼핑하기·선물하기", 11.0, 29000, 11000, "카카오 커머스 기본 수수료 및 톡딜 프로모션 마진 계산"),
    ("own-mall-pg", "카페24·아임웹 자사몰 (PG 수수료)", 3.3, 39000, 14000, "자사몰 PG 결제수수료 약 3.3% — 대신 메타·네이버 광고비(ROAS) 비중 반영 필수"),
    ("kmong-digital", "크몽 (Kmong) 디지털 템플릿·서비스", 16.4, 29000, 0, "크몽 50만 원 이하 거래 수수료 약 16.4% (원가 0원 디지털 상품 순수익 계산)"),
    ("overseas-purchase-agent", "해외구매대행 (타오바오·아마존 소싱)", 10.8, 49000, 21000, "해외 소싱 원가 + 배대지 배송비 + 관부가세·마켓수수료 포함 순마진 계산"),
    ("consignment-dome", "위탁판매 (도매꾹·도매매·오너클랜)", 5.63, 19900, 11500, "재고 없는 위탁판매 시 공급가·배송비·수수료 제외 실제 건당 순이익 계산"),
    ("roas-breakeven", "목표 ROAS (광고수익률) 손익분기 계산기", 5.63, 35000, 14000, "광고비를 태웠을 때 적자가 나지 않는 최소 ROAS(%)와 최대 허용 CPA(원) 계산"),
    ("simple-vs-general-vat", "간이과세자 vs 일반과세자 부가세 마진 비교", 5.63, 29900, 12500, "연매출 1억 400만 원 미만 간이과세자(업종별 부가가치율 15%)와 일반과세자(10%)의 순수익 차이"),
]


def esc(s) -> str:
    return html.escape(str(s or ""), quote=True)


CSS = """
:root{--bg:#0f172a;--card:#1e293b;--line:#334155;--ink:#f8fafc;--sub:#94a3b8;--accent:#38d9a9;--blue:#3b82f6;--warn:#f59e0b}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 -apple-system,"Apple SD Gothic Neo",sans-serif}
header{background:#090d16;border-bottom:1px solid var(--line);padding:16px 20px}
.wrap{max-width:940px;margin:0 auto;padding:0 18px}
header .wrap{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
header a{color:var(--sub);text-decoration:none;font-size:14px;font-weight:600}
header .brand{color:#fff;font-size:19px;font-weight:800}
nav{display:flex;gap:14px;flex-wrap:wrap}
main{padding:28px 0 60px;display:grid;gap:22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:24px}
h1{margin:0 0 8px;font-size:27px;letter-spacing:-.02em}h2{margin:0 0 14px;font-size:20px}
.sub{color:var(--sub);margin:0 0 16px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:11px}
.tile{display:grid;gap:4px;padding:14px 15px;border:1px solid var(--line);border-radius:12px;background:#0f172a;color:var(--ink);text-decoration:none}
.tile:hover{border-color:var(--accent)}
.tile b{font-size:15px}.tile small{color:var(--sub)}
label{display:grid;gap:6px;font-size:13.5px;color:var(--sub);margin-bottom:12px}
input{width:100%;padding:11px 13px;border-radius:10px;border:1px solid var(--line);background:#0f172a;color:#fff;font:inherit;font-size:15px}
.res-box{background:#0f172a;border:2px solid var(--accent);border-radius:14px;padding:22px;display:grid;gap:11px}
.big{font-size:36px;font-weight:800;color:var(--accent)}
.row{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px dashed var(--line);font-size:14.5px}
.preview-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:14px}
.preview-grid img{width:100%;border-radius:12px;border:1px solid var(--line)}
.faq{background:#0f172a;padding:14px 16px;border-radius:10px;margin-bottom:10px}
footer{border-top:1px solid var(--line);padding:24px 0 44px;color:var(--sub);font-size:13.5px}
footer a{color:var(--accent);text-decoration:none}
"""


def calc_widget(default_sell: int, default_cost: int, default_fee: float) -> str:
    return f"""
    <div class="grid2">
      <div>
        <label>판매가 (원) <input id="sell" type="number" value="{default_sell}" oninput="calc()"></label>
        <label>매입 원가 (원, 부가세 포함) <input id="cost" type="number" value="{default_cost}" oninput="calc()"></label>
        <label>마켓 수수료율 (%) <input id="fee" type="number" step="0.01" value="{default_fee}" oninput="calc()"></label>
        <label>고객 결제 배송비 (원) <input id="shipIn" type="number" value="3000" oninput="calc()"></label>
        <label>실제 택배비+포장비 (원) <input id="shipOut" type="number" value="3200" oninput="calc()"></label>
        <label>주문 1건당 광고비 (원) <input id="ad" type="number" value="1500" oninput="calc()"></label>
      </div>
      <div class="res-box">
        <div>1건 판매 시 실제 순수익 (세후)</div>
        <div class="big" id="netProfit">0원</div>
        <div class="row"><span>순수익 마진율</span><strong id="marginPct" style="color:var(--accent)">0%</strong></div>
        <div class="row"><span>손익분기 최소 ROAS (광고수익률)</span><strong id="beRoas" style="color:var(--warn)">0%</strong></div>
        <div class="row"><span>마켓 판매·결제 수수료</span><span id="feeWon">0원</span></div>
        <div class="row"><span>납부 예상 부가세 (매출-매입)</span><span id="vatWon">0원</span></div>
        <div class="row"><span>손익분기 최소 판매가</span><strong id="breakEven">0원</strong></div>
        <div class="row"><span>월 100건 / 500건 순수익</span><strong id="monthCombo">0원</strong></div>
      </div>
    </div>
    <script>
    function won(n){{return Math.round(n).toLocaleString('ko-KR') + '원';}}
    function calc(){{
      const sell=parseFloat(document.getElementById('sell').value)||0;
      const cost=parseFloat(document.getElementById('cost').value)||0;
      const feePct=parseFloat(document.getElementById('fee').value)||0;
      const shipIn=parseFloat(document.getElementById('shipIn').value)||0;
      const shipOut=parseFloat(document.getElementById('shipOut').value)||0;
      const ad=parseFloat(document.getElementById('ad').value)||0;
      const feeWon=sell*(feePct/100)+shipIn*0.033;
      const rev=sell+shipIn;
      const ded=cost+feeWon+shipOut+ad;
      const vat=Math.max(0,(rev-ded)/11);
      const net=rev-ded-vat;
      const margin=sell>0?(net/sell*100):0;
      const preAdMargin=sell>0?((net+ad)/sell):0;
      const beRoas=preAdMargin>0?(100/preAdMargin):9999;
      const breakEven=(cost+shipOut-shipIn+ad)/Math.max(0.1,(1-feePct/100));
      document.getElementById('netProfit').textContent=won(net);
      document.getElementById('marginPct').textContent=margin.toFixed(1)+'%';
      document.getElementById('beRoas').textContent=Math.round(beRoas)+'% 이상';
      document.getElementById('feeWon').textContent=won(feeWon);
      document.getElementById('vatWon').textContent=won(vat);
      document.getElementById('breakEven').textContent=won(breakEven);
      document.getElementById('monthCombo').textContent=won(net*100)+' / '+won(net*500);
    }}
    calc();
    </script>"""


def write_page(rel: str, title: str, desc: str, body: str) -> str:
    canon = f"{SITE_URL}/" if rel == "index.html" else f"{SITE_URL}/{rel}"
    page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}">
<link rel="stylesheet" href="{SITE_URL}/style.css"><meta name="google-site-verification" content="E0MKLI_9g0wTNR9pjNKmxb_QGiA51AIK93dV9qBKumg"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8749404731911210" crossorigin="anonymous"></script><script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"셀러 마진 계산기 & 엑셀 템플릿 스토어","url":"https://0520goeus.github.io/seller-margin-calc/"}}</script><meta property="og:title" content="셀러 마진 계산기 & 엑셀 템플릿 스토어"><meta property="og:type" content="website">
</head>
<body>
<header><div class="wrap">
  <a class="brand" href="{SITE_URL}/">📊 {SITE_NAME}</a>
  <nav>
    <a href="{SITE_URL}/#markets">마켓별 수수료 (25종)</a>
    <a href="https://0520goeus.github.io/vs-pick/">가성비 VS 사전</a>
    <a href="https://0520goeus.github.io/life-fee-calc/">직구관세·가전용량</a>
    <a href="https://0520goeus.github.io/money-calc-kr/">연봉 실수령액</a>
    <a href="https://0520goeus.github.io/benefit-calc-kr/">지원금·실업급여</a>
  </nav>
</div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap">
  <p>패밀리 사이트: <a href="https://0520goeus.github.io/price-note/">해뎐 가격노트</a> · <a href="https://0520goeus.github.io/elec-calc/">전기세 얼마</a> · <a href="https://0520goeus.github.io/life-money-lab/">생활비 물가 연구소</a> · <a href="https://0520goeus.github.io/vs-pick/">가성비 VS 사전</a> · <a href="https://0520goeus.github.io/life-fee-calc/">가전용량·직구관세</a> · <a href="https://0520goeus.github.io/money-calc-kr/">실수령액 계산기</a> · <a href="https://0520goeus.github.io/benefit-calc-kr/">지원금·실업급여</a> · <a href="https://lifefixnote-kr.blogspot.com/">생활해결 노트</a></p>
</div><div style="margin:14px auto 8px;max-width:960px;display:flex;flex-wrap:wrap;gap:6px;justify-content:center;font-size:12px;"><a href="https://0520goeus.github.io/house-calc-kr/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">부동산·대출·복비</a><a href="https://0520goeus.github.io/car-calc-kr/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">자동차세·유지비</a><a href="https://0520goeus.github.io/money-calc-kr/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">실수령액·금융</a><a href="https://0520goeus.github.io/benefit-calc-kr/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">2026 지원금</a><a href="https://0520goeus.github.io/life-fee-calc/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">평수가전·직구관세</a><a href="https://0520goeus.github.io/elec-calc/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">전기세 계산기</a><a href="https://0520goeus.github.io/vs-pick/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">가성비 VS 124종</a><a href="https://0520goeus.github.io/price-note/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">588 생필품 시세</a><a href="https://0520goeus.github.io/seller-margin-calc/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">셀러마진·엑셀</a><a href="https://0520goeus.github.io/kr-trend-brief/" style="padding:4px 9px;border-radius:6px;background:rgba(148,163,184,.18);color:inherit;text-decoration:none;">실시간 트렌드</a></div>
</footer></body></html>"""
    out = DIST / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return canon


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / "style.css").write_text(CSS, encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    (DIST / GOOGLE_FILE).write_text(f"google-site-verification: {GOOGLE_FILE}", encoding="utf-8")
    (DIST / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    (DIST / "ads.txt").write_text(f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")

    for img_name in ("마진템플릿_대표이미지.png", "마진템플릿_상세이미지.png"):
        src = PROD_DIR / img_name
        if src.exists():
            shutil.copy2(src, DIST / img_name)

    urls: list[str] = []
    tiles: list[str] = []

    for slug, name, fee, sell, cost, note in CHANNELS:
        rel = f"m/{slug}.html"
        title = f"{name} 마진·수수료·ROAS 계산기 (수수료 {fee}% 기준)"
        desc = f"{name} 판매수수료 {fee}%와 배송비·포장비·광고비·부가세를 반영한 실제 순수익과 손익분기 ROAS를 계산합니다."
        body = f"""
        <section class="card">
          <h1>{esc(name)} 마진·순수익 계산기</h1>
          <p class="sub">{esc(note)}</p>
          {calc_widget(sell, cost, fee)}
        </section>
        {COUPANG_BOX}
        <section class="card">
          <h2>다품목 정산용 [셀러 마진·정산 자동계산 엑셀 템플릿 v1]</h2>
          <p class="sub">상품이 10개 이상이라면 웹 계산기 대신 매크로 없는 순수 수식형 다채널 정산 엑셀 템플릿으로 월별 순이익을 한 번에 관리할 수 있습니다.</p>
          <div class="preview-grid">
            <img src="{SITE_URL}/마진템플릿_대표이미지.png" alt="셀러 마진정산 자동계산 엑셀 템플릿 대표 이미지" loading="lazy">
            <img src="{SITE_URL}/마진템플릿_상세이미지.png" alt="셀러 마진정산 자동계산 엑셀 템플릿 상세 화면" loading="lazy">
          </div>
        </section>
        """
        urls.append(write_page(rel, title, desc, body))
        tiles.append(f'<a class="tile" href="{SITE_URL}/{rel}"><b>{esc(name)}</b><small>기본 수수료 {fee}% · 순수익/ROAS 계산 →</small></a>')

    home_body = f"""
    <section class="card">
      <h1>스마트스토어·쿠팡·오픈마켓 셀러 마진 & ROAS 계산기</h1>
      <p class="sub">판매가, 원가, 마켓별 수수료, 택배비, 광고비, 부가세까지 모두 넣어 실제 통장에 남는 세후 순수익과 손익분기 ROAS를 즉시 계산하세요.</p>
      {calc_widget(29900, 12500, 5.63)}
    </section>
    {COUPANG_BOX}
    <section class="card" id="markets">
      <h2>마켓·카테고리별 전용 마진 계산기 ({len(tiles)}종)</h2>
      <div class="grid">{"".join(tiles)}</div>
    </section>
    <section class="card">
      <h2>다품목 정산용 [셀러 마진·정산 자동계산 엑셀 템플릿 v1]</h2>
      <div class="preview-grid">
        <img src="{SITE_URL}/마진템플릿_대표이미지.png" alt="셀러 마진정산 자동계산 엑셀 템플릿 대표 이미지" loading="lazy">
        <img src="{SITE_URL}/마진템플릿_상세이미지.png" alt="셀러 마진정산 자동계산 엑셀 템플릿 상세 화면" loading="lazy">
      </div>
    </section>
    """
    urls.insert(0, write_page(
        "index.html",
        "스마트스토어·쿠팡 셀러 마진 계산기 | 마켓별 25종 수수료·ROAS·부가세 자동 계산",
        "스마트스토어, 쿠팡 윙, 로켓그로스, 11번가, 지마켓, 자사몰, 크몽까지 25개 마켓별 실시간 순수익·마진율·손익분기 ROAS 계산기.",
        home_body,
    ))

    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{u}</loc><lastmod>{NOW.strftime('%Y-%m-%d')}</lastmod></url>\n" for u in urls)
        + "</urlset>\n",
        encoding="utf-8",
    )
    (DIST / "urls.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"셀러 마진 계산기 빌드 완료: 총 {len(urls)}페이지")


if __name__ == "__main__":
    main()
