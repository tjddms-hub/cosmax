import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------------------
# 기본 페이지 설정
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="돈포겟 · 실험 스케줄 관리",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit 기본 여백/헤더를 최소화해서 페이지가 화면을 최대한 채우도록 함
st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] > .main .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
        }
        header[data-testid="stHeader"] {
            height: 0rem;
        }
        [data-testid="stToolbar"] {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 앱 화면 (HTML/CSS/JS)
# ---------------------------------------------------------------------------
APP_HTML = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>돈포겟 · 실험 스케줄 관리</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet" />
<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-database-compat.js"></script>
<style>
  :root {
    --bg: #ffffff;
    --surface: #f7f7f8;
    --surface-2: #ececee;
    --border: #dedee1;
    --text: #121214;
    --text-muted: #6c6c72;
    --accent: #ff0000;
    --accent-strong: #cc0000;
    --accent-soft: #fde3e1;
    --btn: #161618;
    --btn-strong: #000000;
    --btn-ink: #ffffff;
    --danger: #d92b2b;
    --shadow: 0 10px 24px rgba(0, 0, 0, 0.14);
    --radius-lg: 20px;
    --radius-md: 14px;
    --radius-sm: 10px;
  }

  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: "Noto Sans KR", -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo",
      "Malgun Gothic", "Segoe UI", sans-serif;
    font-size: 15px;
    -webkit-font-smoothing: antialiased;
    min-height: 100vh;
    overscroll-behavior-y: none;
  }
  .mono {
    font-variant-numeric: tabular-nums;
  }
  button {
    font-family: inherit;
    cursor: pointer;
    transition: transform 0.08s ease;
  }
  button:active {
    transform: scale(0.96);
  }
  select { font-family: inherit; }

  .page-loader {
    position: fixed;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.55);
    z-index: 50;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.15s ease;
  }
  .page-loader.show { opacity: 1; }
  .page-loader .spinner {
    width: 34px;
    height: 34px;
    border-radius: 999px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    animation: spin 0.6s linear infinite;
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  button:focus-visible,
  input:focus-visible,
  select:focus-visible,
  [tabindex]:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
  @media (prefers-reduced-motion: reduce) {
    * { animation-duration: 0.001ms !important; transition-duration: 0.001ms !important; }
  }

  #app {
    max-width: 860px;
    margin: 0 auto;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
  }

  /* ---------- top bar ---------- */
  .topbar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 18px 20px 14px;
    flex-shrink: 0;
  }
  .topbar .back {
    width: 34px;
    height: 34px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
  }
  .topbar .titles { min-width: 0; }
  .topbar h1 { font-size: 19px; margin: 0; font-weight: 800; letter-spacing: -0.01em; }
  .topbar p { font-size: 13px; margin: 2px 0 0; color: var(--text-muted); }
  .brand {
    display: flex;
    align-items: baseline;
    gap: 8px;
  }
  .brand .mark {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -0.02em;
  }
  .brand .mark span { color: var(--accent-strong); }
  .brand .tag { font-size: 13px; color: var(--text-muted); }

  .sync-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 11.5px;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 999px;
    background: var(--surface-2);
    color: var(--text-muted);
    margin-top: 6px;
  }
  .sync-badge.online { color: #1a8a4a; background: #e3f6ea; }
  .sync-badge.offline { color: var(--danger); background: var(--surface-2); }

  .topbar.hero {
    justify-content: space-between;
    background: linear-gradient(135deg, var(--accent-soft) 0%, var(--surface) 48%, var(--surface-2) 100%);
    border-radius: 0 0 var(--radius-lg) var(--radius-lg);
    padding: 22px 20px 26px;
  }
  .brand-logo-card {
    background: #fff;
    border-radius: var(--radius-sm);
    padding: 10px 16px;
    box-shadow: var(--shadow);
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }
  .brand-logo-card img { height: 24px; display: block; }
  .brand-mini-logo {
    height: 18px;
    margin-left: auto;
    flex-shrink: 0;
  }

  main { flex: 1; padding: 0 20px 32px; }

  /* ---------- home: lab pills ---------- */
  .lab-row {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 4px 0 14px;
    scrollbar-width: none;
  }
  .lab-row::-webkit-scrollbar { display: none; }
  .pill {
    flex-shrink: 0;
    padding: 9px 16px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
  }
  .pill.active {
    background: var(--btn);
    border-color: var(--btn);
    color: var(--btn-ink);
  }
  .pill.ghost {
    color: var(--btn-strong);
    border-color: var(--btn);
    border-style: dashed;
  }

  .calendar-cta {
    display: block;
    width: 100%;
    text-align: center;
    background: var(--surface-2);
    border: 1px solid var(--btn);
    color: var(--btn-strong);
    border-radius: var(--radius-md);
    padding: 12px 14px;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 22px;
  }

  .section-label {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 4px 0 10px;
  }

  .project-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  @media (max-width: 480px) {
    .project-grid { grid-template-columns: 1fr; }
  }
  .project-card {
    text-align: left;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    min-height: 108px;
    color: var(--text);
    transition: border-color 0.15s, transform 0.1s;
  }
  .project-card:hover { border-color: var(--accent); }
  .project-card:active { transform: scale(0.99); }
  .project-card .card-icon { font-size: 26px; line-height: 1; }
  .project-card .name { font-size: 17px; font-weight: 800; letter-spacing: -0.01em; }
  .project-card .meta { font-size: 13px; color: var(--text-muted); }
  .project-card .next {
    margin-top: auto;
    font-size: 13px;
    color: var(--accent-strong);
    font-weight: 700;
  }
  .project-card.add {
    align-items: center;
    justify-content: center;
    border-style: dashed;
    border-color: var(--btn);
    color: var(--btn-strong);
    font-size: 14px;
    font-weight: 600;
  }

  .platform-switch {
    display: flex;
    gap: 8px;
    margin-top: 28px;
    padding-top: 18px;
    border-top: 1px solid var(--border);
  }
  .switch-btn {
    flex: 1;
    text-align: center;
    text-decoration: none;
    padding: 11px 12px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 700;
  }
  .switch-btn.active {
    background: var(--btn);
    border-color: var(--btn);
    color: var(--btn-ink);
  }

  /* ---------- mobile view mode override ---------- */
  body.mode-mobile #app {
    max-width: 430px;
  }
  body.mode-mobile .project-grid {
    grid-template-columns: 1fr;
  }
  body.mode-mobile .sheet {
    max-width: 430px;
  }

  /* ---------- calendar ---------- */
  .cal-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
  }
  .cal-nav .month {
    font-size: 20px;
    font-weight: 800;
  }
  .cal-nav .navbtns { display: flex; gap: 6px; }
  .navbtn, .today-btn {
    width: 32px;
    height: 32px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
  }
  .today-btn {
    width: auto;
    padding: 0 12px;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-muted);
  }
  .weekday-row {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    margin-bottom: 6px;
  }
  .weekday-row span {
    text-align: center;
    font-size: 13px;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.03em;
  }
  .day-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 4px;
  }
  .day-cell {
    aspect-ratio: 1;
    border-radius: var(--radius-sm);
    background: transparent;
    border: 1px solid transparent;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3px;
    position: relative;
    color: var(--text);
    font-variant-numeric: tabular-nums;
    font-size: 14.5px;
    font-weight: 500;
  }
  .day-cell.pad { visibility: hidden; }
  .day-cell:not(.pad):hover { background: var(--surface-2); }
  .day-cell.today { border-color: var(--accent); font-weight: 700; }
  .day-cell .dot {
    width: 5px;
    height: 5px;
    border-radius: 999px;
    background: var(--accent);
  }
  .day-cell .dot.none { background: transparent; }

  /* ---------- day timeline view ---------- */
  #view-day.active {
    display: flex;
    flex-direction: column;
    height: 100vh;
    position: relative;
  }
  .day-filters {
    padding: 2px 20px 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex-shrink: 0;
  }
  .chip-row {
    display: flex;
    gap: 6px;
    overflow-x: auto;
    scrollbar-width: none;
  }
  .chip-row::-webkit-scrollbar { display: none; }
  .filter-chip {
    flex-shrink: 0;
    padding: 6px 13px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 600;
    white-space: nowrap;
  }
  .filter-chip.active {
    background: var(--btn);
    border-color: var(--btn);
    color: var(--btn-ink);
  }

  .timeline-scroll {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    padding: 8px 20px 110px;
  }
  .timeline-body {
    display: flex;
    align-items: flex-start;
  }
  .hour-rail {
    width: 52px;
    flex-shrink: 0;
    position: relative;
  }
  .hour-rail .tick {
    position: absolute;
    left: 0;
    right: 8px;
    text-align: right;
    font-size: 12px;
    color: var(--text-muted);
    transform: translateY(-6px);
  }
  .track {
    flex: 1;
    position: relative;
    border-left: 1px solid var(--border);
    margin-left: 4px;
  }
  .track .gridline {
    position: absolute;
    left: 0;
    right: 0;
    border-top: 1px solid var(--border);
  }
  .track .now-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 0;
    border-top: 2px solid var(--accent);
    z-index: 5;
  }
  .track .now-dot {
    position: absolute;
    left: -4px;
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: var(--accent);
    z-index: 6;
  }
  .timeline-empty {
    position: absolute;
    top: 24px;
    left: 8px;
    right: 8px;
    text-align: center;
    color: var(--text-muted);
    font-size: 14px;
  }
  .entry-block {
    position: absolute;
    border-radius: 8px;
    padding: 5px 8px;
    overflow: hidden;
    color: #fff;
    border: none;
    text-align: left;
    box-shadow: 0 1px 3px rgba(20, 10, 8, 0.25);
  }
  .entry-block .eb-time {
    font-size: 12px;
    font-weight: 700;
    opacity: 0.92;
  }
  .entry-block .eb-title {
    font-size: 13.5px;
    font-weight: 700;
    line-height: 1.25;
  }
  .entry-block .eb-meta {
    font-size: 11.5px;
    opacity: 0.88;
    margin-top: 1px;
  }

  .fab {
    position: absolute;
    right: 24px;
    bottom: 28px;
    width: 56px;
    height: 56px;
    border-radius: 999px;
    background: var(--btn);
    color: var(--btn-ink);
    border: none;
    font-size: 26px;
    font-weight: 700;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 15;
  }

  /* ---------- sheet (add / edit entry) ---------- */
  .backdrop {
    position: fixed;
    inset: 0;
    background: rgba(20, 10, 8, 0.45);
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
    z-index: 20;
  }
  .backdrop.open { opacity: 1; pointer-events: auto; }
  .sheet {
    position: fixed;
    left: 50%;
    bottom: 0;
    width: 100%;
    max-width: 860px;
    transform: translate(-50%, 100%);
    background: var(--surface);
    border-radius: 22px 22px 0 0;
    box-shadow: var(--shadow);
    z-index: 21;
    transition: transform 0.25s ease;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    border: 1px solid var(--border);
    border-bottom: none;
  }
  .sheet.open { transform: translate(-50%, 0); }
  .sheet-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px 10px;
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
    position: relative;
  }
  .sheet-head .grip {
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: 36px;
    height: 4px;
    border-radius: 999px;
    background: var(--border);
  }
  .sheet-head h2 { font-size: 17px; margin: 0; font-weight: 800; }
  .sheet-head .close {
    width: 30px;
    height: 30px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--surface-2);
    color: var(--text-muted);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .sheet-form {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
  }
  .sheet-fields {
    overflow-y: auto;
    flex: 1;
    min-height: 0;
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .field-label {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.03em;
    margin-bottom: -4px;
  }
  .field-select {
    width: 100%;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 12px;
    font-size: 15px;
    color: var(--text);
  }
  .time-range-row {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .range-dash {
    color: var(--text-muted);
    font-size: 13px;
    flex-shrink: 0;
  }
  .time-select-group {
    display: flex;
    align-items: center;
    gap: 3px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0 4px;
    flex-shrink: 0;
  }
  .time-select-group select {
    background: transparent;
    border: none;
    color: var(--text);
    font-size: 15px;
    padding: 9px 2px;
    appearance: none;
    text-align: center;
  }
  .time-select-group .colon {
    color: var(--text-muted);
    font-size: 14px;
  }
  .time-presets {
    display: flex;
    gap: 6px;
    overflow-x: auto;
    scrollbar-width: none;
  }
  .time-presets::-webkit-scrollbar { display: none; }
  .time-presets .chip {
    flex-shrink: 0;
    padding: 6px 12px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--surface-2);
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
  }
  .time-presets .chip.active {
    background: var(--btn);
    border-color: var(--btn);
    color: var(--btn-ink);
  }
  .sheet-fields input[type="text"] {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 12px;
    font-size: 16px;
    color: var(--text);
    width: 100%;
  }
  .sheet-actions {
    display: flex;
    gap: 8px;
    padding: 12px 18px calc(14px + env(safe-area-inset-bottom));
    border-top: 1px solid var(--border);
    flex-shrink: 0;
  }
  .btn-secondary {
    flex: 1;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
  }
  .btn-secondary.danger-text { color: var(--danger); border-color: var(--danger); }
  .sheet-actions button[type="submit"] {
    flex: 2;
    background: var(--btn);
    color: var(--btn-ink);
    border: none;
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    font-size: 14.5px;
    font-weight: 700;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
  }

  /* ---------- generic modal (add lab / add project) ---------- */
  .modal-wrap {
    position: fixed;
    inset: 0;
    z-index: 30;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.15s ease;
  }
  .modal-wrap.open { opacity: 1; pointer-events: auto; }
  .modal-wrap .backdrop2 {
    position: absolute;
    inset: 0;
    background: rgba(20, 10, 8, 0.45);
  }
  .modal-box {
    position: relative;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow);
    width: 100%;
    max-width: 340px;
    padding: 20px;
  }
  .modal-box h3 { margin: 0 0 12px; font-size: 17px; font-weight: 800; }
  .modal-box input {
    width: 100%;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 12px;
    font-size: 16px;
    color: var(--text);
    margin-bottom: 14px;
  }
  .modal-actions { display: flex; gap: 8px; justify-content: flex-end; }
  .modal-actions button {
    padding: 8px 14px;
    border-radius: var(--radius-sm);
    font-size: 14px;
    font-weight: 600;
    border: 1px solid var(--border);
    background: var(--surface-2);
    color: var(--text);
  }
  .modal-actions button.primary {
    background: var(--btn);
    border-color: var(--btn);
    color: var(--btn-ink);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
  }

  .userlist-box { max-width: 400px; }
  .userlist-box h3 span { color: var(--text-muted); font-weight: 600; }
  .user-list {
    max-height: 360px;
    overflow-y: auto;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-bottom: 14px;
  }
  .user-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 8px;
    border-radius: var(--radius-sm);
    background: var(--surface-2);
  }
  .user-avatar {
    width: 26px;
    height: 26px;
    border-radius: 999px;
    color: #fff;
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .user-name { font-size: 13.5px; font-weight: 600; }

  .view { display: none; }
  .view.active { display: block; }
</style>
</head>
<body>
<div id="app">

  <div class="page-loader" id="page-loader" aria-hidden="true">
    <div class="spinner"></div>
  </div>

  <!-- ===== HOME ===== -->
  <section class="view active" id="view-home">
    <div class="topbar hero">
      <div class="brand">
        <span class="mark">돈<span>포</span>겟</span>
        <span class="tag">실험 스케줄, 놓치지 않게</span>
      </div>
      <div class="brand-logo-card">
        <img class="cosmax-logo" alt="COSMAX" />
      </div>
    </div>
    <main>
      <span class="sync-badge" id="sync-badge">● 동기화 확인 중</span>
      <div class="section-label" style="margin-top:14px;">연구실</div>
      <div class="lab-row" id="lab-row"></div>
      <button type="button" class="calendar-cta" id="btn-open-calendar">📅 캘린더 보기</button>
      <button type="button" class="calendar-cta" id="btn-open-userlist">👥 사용자 목록</button>

      <div class="section-label">프로젝트</div>
      <div class="project-grid" id="project-grid"></div>

      <div class="platform-switch">
        <button type="button" class="switch-btn" id="btn-mode-pc">🖥 PC 화면</button>
        <button type="button" class="switch-btn" id="btn-mode-mobile">📱 모바일 화면</button>
      </div>
    </main>
  </section>

  <!-- ===== CALENDAR (month) ===== -->
  <section class="view" id="view-calendar">
    <div class="topbar">
      <button class="back" id="btn-back" aria-label="뒤로">‹</button>
      <div class="titles">
        <h1 id="cal-project-name">연구실</h1>
        <p id="cal-lab-name">연구실 일정</p>
      </div>
      <img class="cosmax-logo brand-mini-logo" alt="COSMAX" />
    </div>
    <main>
      <div class="cal-nav">
        <button class="navbtn" id="btn-prev-month" aria-label="이전 달">‹</button>
        <span class="month mono" id="cal-month-label">2026.07</span>
        <div class="navbtns">
          <button class="today-btn" id="btn-today">오늘</button>
          <button class="navbtn" id="btn-next-month" aria-label="다음 달">›</button>
        </div>
      </div>
      <div class="weekday-row">
        <span>일</span><span>월</span><span>화</span><span>수</span><span>목</span><span>금</span><span>토</span>
      </div>
      <div class="day-grid" id="day-grid"></div>
    </main>
  </section>

  <!-- ===== DAY TIMELINE ===== -->
  <section class="view" id="view-day">
    <div class="topbar">
      <button class="back" id="btn-day-back" aria-label="뒤로">‹</button>
      <div class="titles">
        <h1 id="day-title">7월 15일 (수)</h1>
        <p id="day-subtitle">연구실 일정</p>
      </div>
      <img class="cosmax-logo brand-mini-logo" alt="COSMAX" />
    </div>
    <div class="day-filters">
      <div class="chip-row" id="lab-filter-row"></div>
      <div class="chip-row" id="person-filter-row"></div>
    </div>
    <div class="timeline-scroll">
      <div class="timeline-body">
        <div class="hour-rail" id="hour-rail"></div>
        <div class="track" id="track"></div>
      </div>
    </div>
    <button type="button" class="fab" id="btn-add-entry" aria-label="일정 추가">+</button>
  </section>

  <!-- ===== ADD / EDIT ENTRY SHEET ===== -->
  <div class="backdrop" id="sheet-backdrop"></div>
  <div class="sheet" id="day-sheet">
    <div class="sheet-head">
      <div class="grip"></div>
      <h2 id="sheet-title-label">일정 추가</h2>
      <button class="close" id="btn-sheet-close" aria-label="닫기">✕</button>
    </div>
    <form class="sheet-form" id="sheet-form">
      <div class="sheet-fields">
        <div>
          <div class="field-label">프로젝트</div>
          <select id="select-project" class="field-select" aria-label="프로젝트"></select>
        </div>

        <div>
          <div class="field-label">시간</div>
          <div class="time-range-row">
            <div class="time-select-group">
              <select id="select-hour" class="mono" aria-label="시작 시"></select>
              <span class="colon">:</span>
              <select id="select-minute" class="mono" aria-label="시작 분"></select>
            </div>
            <span class="range-dash">~</span>
            <div class="time-select-group">
              <select id="select-end-hour" class="mono" aria-label="종료 시"></select>
              <span class="colon">:</span>
              <select id="select-end-minute" class="mono" aria-label="종료 분"></select>
            </div>
          </div>
          <div class="time-presets" id="time-presets" style="margin-top:8px;">
            <button type="button" class="chip" data-time="09:00">09:00</button>
            <button type="button" class="chip" data-time="11:00">11:00</button>
            <button type="button" class="chip" data-time="14:00">14:00</button>
            <button type="button" class="chip" data-time="17:00">17:00</button>
          </div>
        </div>

        <div>
          <div class="field-label">일정 내용</div>
          <input type="text" id="input-title" placeholder="예: 40℃ 챔버 pH 측정" required aria-label="일정 내용" />
        </div>

        <div>
          <div class="field-label">등록자</div>
          <select id="select-registrant" class="field-select" aria-label="등록자" required></select>
        </div>
      </div>
      <div class="sheet-actions">
        <button type="button" class="btn-secondary danger-text" id="btn-delete-entry" style="display:none;">삭제</button>
        <button type="submit" id="submit-btn">추가</button>
      </div>
    </form>
  </div>

  <!-- ===== GENERIC MODAL ===== -->
  <div class="modal-wrap" id="modal-wrap">
    <div class="backdrop2" id="modal-backdrop"></div>
    <div class="modal-box">
      <h3 id="modal-title">새 연구실</h3>
      <input type="text" id="modal-input" placeholder="이름 입력" />
      <div class="modal-actions">
        <button id="modal-cancel">취소</button>
        <button class="primary" id="modal-confirm">추가</button>
      </div>
    </div>
  </div>

  <!-- ===== USER LIST MODAL ===== -->
  <div class="modal-wrap" id="userlist-wrap">
    <div class="backdrop2" id="userlist-backdrop"></div>
    <div class="modal-box userlist-box">
      <h3>사용자 목록 <span id="userlist-count"></span></h3>
      <div class="user-list" id="user-list"></div>
      <div class="modal-actions">
        <button class="primary" id="userlist-close">닫기</button>
      </div>
    </div>
  </div>

</div>

<script>
(function () {
  "use strict";

  var STORAGE_KEY = "donforget_v2";
  var USERNAME_KEY = "donforget_username";
  var WEEKDAY_KO = ["일", "월", "화", "수", "목", "금", "토"];
  var MINUTE_STEPS = [0, 10, 20, 30, 40, 50];
  var HOUR_PX = 64;
  var REGISTRANT_PALETTE = ["#e63946", "#f4732a", "#c9184a", "#a4161a", "#bb4d00", "#8a5a44"];
  var COSMAX_LOGO = "data:image/jpeg;base64,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";

  function uid() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  }

  function seedData() {
    var lab1 = uid(), lab2 = uid();
    var p1 = uid(), p2 = uid(), p3 = uid();
    var today = new Date();
    var d = function (offset) {
      var t = new Date(today);
      t.setDate(t.getDate() + offset);
      return fmtDate(t);
    };
    var schedules = {};
    schedules[p1] = {};
    schedules[p1][d(0)] = [
      { id: uid(), startTime: "09:30", endTime: "10:00", title: "40℃ 챔버 1주차 pH/점도 측정", memo: "샘플 A-01~A-06", registeredBy: "박서연" },
      { id: uid(), startTime: "14:00", endTime: "14:30", title: "색상 변화 관찰", memo: "", registeredBy: "김도현" }
    ];
    schedules[p1][d(3)] = [
      { id: uid(), startTime: "10:00", endTime: "10:30", title: "냉장(4℃) 샘플 분리 여부 확인", memo: "", registeredBy: "박서연" }
    ];
    schedules[p2] = {};
    schedules[p2][d(1)] = [
      { id: uid(), startTime: "11:00", endTime: "12:30", title: "SPF 처방 3차 배합 완료", memo: "유화 안정성 확인 필요", registeredBy: "이현우" }
    ];
    schedules[p3] = {};

    return {
      labs: [
        { id: lab1, name: "제형연구실" },
        { id: lab2, name: "안정성평가실" }
      ],
      projects: [
        { id: p1, labId: lab2, name: "리뉴얼 크림 안정성시험" },
        { id: p2, labId: lab1, name: "선크림 처방 최적화" },
        { id: p3, labId: lab1, name: "저자극 클렌저 R&D" }
      ],
      schedules: schedules
    };
  }

  function load() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch (e) {}
    var seeded = seedData();
    save(seeded);
    return seeded;
  }

  function save(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {}
    if (syncRef) syncRef.set(state);
  }

  var state = load();

  /* ---------- realtime shared sync (Firebase Realtime Database) ---------- */
  // Firebase 콘솔(console.firebase.google.com)에서 만든 프로젝트의 설정값을 아래에 붙여넣으세요.
  var FIREBASE_CONFIG = {
    apiKey: "REPLACE_ME",
    authDomain: "REPLACE_ME",
    databaseURL: "REPLACE_ME",
    projectId: "REPLACE_ME"
  };
  var SYNC_PATH = "donforget_shared";
  var syncRef = null;

  function setSyncStatus(mode) {
    var badge = document.getElementById("sync-badge");
    if (!badge) return;
    if (mode === "online") {
      badge.textContent = "● 실시간 동기화 중";
      badge.className = "sync-badge online";
    } else {
      badge.textContent = "● 오프라인 (이 기기에만 저장됨)";
      badge.className = "sync-badge offline";
    }
  }

  function rerenderCurrentView() {
    var activeView = document.querySelector(".view.active");
    if (!activeView) return;
    if (activeView.id === "view-home") renderHome();
    else if (activeView.id === "view-calendar") renderCalendar();
    else if (activeView.id === "view-day") renderDayView();
  }

  function initSync() {
    if (typeof firebase === "undefined" || FIREBASE_CONFIG.apiKey === "REPLACE_ME") {
      setSyncStatus("offline");
      return;
    }
    try {
      firebase.initializeApp(FIREBASE_CONFIG);
      syncRef = firebase.database().ref(SYNC_PATH);
      syncRef.on(
        "value",
        function (snapshot) {
          var remote = snapshot.val();
          if (remote) {
            state = remote;
            rerenderCurrentView();
          } else {
            syncRef.set(state);
          }
          setSyncStatus("online");
        },
        function () {
          setSyncStatus("offline");
        }
      );
    } catch (e) {
      setSyncStatus("offline");
    }
  }

  var nav = {
    activeLabId: state.labs[0] ? state.labs[0].id : null,
    scope: null,
    monthCursor: new Date(),
    selectedDate: null,
    dayLabFilter: null,
    dayPersonFilter: null
  };

  var editingId = null;
  var editingProjectId = null;
  var editingMemo = "";

  function fmtDate(dt) {
    var y = dt.getFullYear();
    var m = String(dt.getMonth() + 1).padStart(2, "0");
    var d = String(dt.getDate()).padStart(2, "0");
    return y + "-" + m + "-" + d;
  }

  function esc(s) {
    var div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  var pageLoaderTimeout = null;
  function flashPageLoader() {
    var loader = document.getElementById("page-loader");
    loader.classList.add("show");
    clearTimeout(pageLoaderTimeout);
    pageLoaderTimeout = setTimeout(function () {
      loader.classList.remove("show");
    }, 280);
  }

  function showView(id) {
    flashPageLoader();
    document.querySelectorAll(".view").forEach(function (v) {
      v.classList.toggle("active", v.id === id);
    });
  }

  function labById(id) {
    return state.labs.find(function (l) { return l.id === id; });
  }

  function labNameOf(id) {
    var l = labById(id);
    return l ? l.name : "";
  }

  /* ---------- HOME ---------- */
  function renderHome() {
    var labRow = document.getElementById("lab-row");
    labRow.innerHTML = "";

    var allPill = document.createElement("button");
    allPill.className = "pill" + (nav.activeLabId === "__ALL__" ? " active" : "");
    allPill.textContent = "전체 연구실";
    allPill.addEventListener("click", function () {
      nav.activeLabId = "__ALL__";
      renderHome();
    });
    labRow.appendChild(allPill);

    state.labs.forEach(function (lab) {
      var pill = document.createElement("button");
      pill.className = "pill" + (lab.id === nav.activeLabId ? " active" : "");
      pill.textContent = lab.name;
      pill.addEventListener("click", function () {
        nav.activeLabId = lab.id;
        renderHome();
      });
      labRow.appendChild(pill);
    });
    var addLab = document.createElement("button");
    addLab.className = "pill ghost";
    addLab.textContent = "+ 새 연구실";
    addLab.addEventListener("click", function () {
      openModal("새 연구실", "연구실 이름", function (val) {
        var lab = { id: uid(), name: val };
        state.labs.push(lab);
        nav.activeLabId = lab.id;
        save(state);
        renderHome();
      });
    });
    labRow.appendChild(addLab);

    var cta = document.getElementById("btn-open-calendar");
    cta.textContent = "📅 " + (nav.activeLabId === "__ALL__" ? "전체 연구실" : labNameOf(nav.activeLabId)) + " 캘린더 보기";

    var grid = document.getElementById("project-grid");
    grid.innerHTML = "";
    var projects = nav.activeLabId === "__ALL__"
      ? state.projects.slice()
      : state.projects.filter(function (p) { return p.labId === nav.activeLabId; });

    projects.forEach(function (proj) {
      var entries = flattenSchedule(proj.id);
      var upcoming = entries
        .filter(function (e) { return e.date >= fmtDate(new Date()); })
        .sort(function (a, b) { return (a.date + a.startTime).localeCompare(b.date + b.startTime); })[0];

      var card = document.createElement("button");
      card.className = "project-card";
      card.innerHTML =
        '<div class="card-icon">' + projectEmoji(proj.name) + "</div>" +
        '<div class="name">' + esc(proj.name) + "</div>" +
        '<div class="meta">' + esc(labNameOf(proj.labId)) + " · 일정 " + entries.length + "건</div>" +
        (upcoming
          ? '<div class="next">다음: ' + esc(shortDate(upcoming.date)) + " " + esc(upcoming.startTime) + "</div>"
          : '<div class="next" style="color:var(--text-muted)">등록된 일정 없음</div>');
      card.addEventListener("click", function () {
        openCalendarScope({ type: "lab", labId: proj.labId });
      });
      grid.appendChild(card);
    });

    if (nav.activeLabId !== "__ALL__") {
      var addCard = document.createElement("button");
      addCard.className = "project-card add";
      addCard.textContent = "+ 새 프로젝트";
      addCard.addEventListener("click", function () {
        if (!nav.activeLabId) return;
        openModal("새 프로젝트", "프로젝트 이름", function (val) {
          var proj = { id: uid(), labId: nav.activeLabId, name: val };
          state.projects.push(proj);
          save(state);
          renderHome();
        });
      });
      grid.appendChild(addCard);
    }
  }

  function projectEmoji(name) {
    if (/선크림|SPF|자외선/i.test(name)) return "☀️";
    if (/클렌저|세안|워시|비누/i.test(name)) return "🧼";
    if (/안정성|챔버|보관|유통기한/i.test(name)) return "🌡️";
    if (/향|퍼퓸|프래그런스/i.test(name)) return "🌸";
    if (/크림|로션|에센스|세럼|앰플/i.test(name)) return "🧴";
    return "🧪";
  }

  function shortDate(dateStr) {
    var parts = dateStr.split("-");
    return parseInt(parts[1], 10) + "월 " + parseInt(parts[2], 10) + "일";
  }

  function flattenSchedule(projectId) {
    var map = state.schedules[projectId] || {};
    var out = [];
    Object.keys(map).forEach(function (date) {
      map[date].forEach(function (item) {
        out.push({ date: date, startTime: item.startTime, title: item.title });
      });
    });
    return out;
  }

  document.getElementById("btn-open-calendar").addEventListener("click", function () {
    if (nav.activeLabId === "__ALL__") openCalendarScope({ type: "all" });
    else openCalendarScope({ type: "lab", labId: nav.activeLabId });
  });

  /* ---------- SCOPE HELPERS ---------- */
  function getProjectsInScope(scope) {
    if (!scope) return [];
    if (scope.type === "all") return state.projects;
    return state.projects.filter(function (p) { return p.labId === scope.labId; });
  }

  function getEntriesForDate(dateStr, scope) {
    var projects = getProjectsInScope(scope);
    var out = [];
    projects.forEach(function (proj) {
      var dayList = (state.schedules[proj.id] || {})[dateStr] || [];
      dayList.forEach(function (item) {
        out.push({
          id: item.id,
          startTime: item.startTime,
          endTime: item.endTime,
          title: item.title,
          memo: item.memo || "",
          registeredBy: item.registeredBy || "",
          projectId: proj.id,
          projectName: proj.name,
          labId: proj.labId,
          labName: labNameOf(proj.labId)
        });
      });
    });
    return out;
  }

  function dateHasEntries(dateStr, scope) {
    return getEntriesForDate(dateStr, scope).length > 0;
  }

  /* ---------- CALENDAR (month) ---------- */
  function openCalendarScope(scope) {
    nav.scope = scope;
    nav.monthCursor = new Date();
    showView("view-calendar");
    renderCalendar();
  }

  function renderCalendar() {
    var scope = nav.scope;
    if (!scope) { showView("view-home"); renderHome(); return; }

    var title = scope.type === "all" ? "전체 연구실" : labNameOf(scope.labId);
    var subtitle = scope.type === "all" ? "전체 연구실 통합 일정" : "연구실 일정";
    document.getElementById("cal-project-name").textContent = title;
    document.getElementById("cal-lab-name").textContent = subtitle;

    var y = nav.monthCursor.getFullYear();
    var m = nav.monthCursor.getMonth();
    document.getElementById("cal-month-label").textContent = y + "." + String(m + 1).padStart(2, "0");

    var firstDay = new Date(y, m, 1);
    var startWeekday = firstDay.getDay();
    var daysInMonth = new Date(y, m + 1, 0).getDate();
    var todayStr = fmtDate(new Date());

    var grid = document.getElementById("day-grid");
    grid.innerHTML = "";

    for (var i = 0; i < startWeekday; i++) {
      var pad = document.createElement("div");
      pad.className = "day-cell pad";
      grid.appendChild(pad);
    }

    for (var day = 1; day <= daysInMonth; day++) {
      var dateStr = fmtDate(new Date(y, m, day));
      var hasEntries = dateHasEntries(dateStr, scope);
      var cell = document.createElement("button");
      cell.className = "day-cell" + (dateStr === todayStr ? " today" : "");
      cell.innerHTML = "<span>" + day + "</span><span class=\"dot" + (hasEntries ? "" : " none") + "\"></span>";
      cell.addEventListener("click", function (ds) {
        return function () { openDayView(ds); };
      }(dateStr));
      grid.appendChild(cell);
    }
  }

  document.getElementById("btn-back").addEventListener("click", function () {
    showView("view-home");
    renderHome();
  });
  document.getElementById("btn-prev-month").addEventListener("click", function () {
    nav.monthCursor.setMonth(nav.monthCursor.getMonth() - 1);
    renderCalendar();
  });
  document.getElementById("btn-next-month").addEventListener("click", function () {
    nav.monthCursor.setMonth(nav.monthCursor.getMonth() + 1);
    renderCalendar();
  });
  document.getElementById("btn-today").addEventListener("click", function () {
    nav.monthCursor = new Date();
    renderCalendar();
  });

  /* ---------- DAY TIMELINE ---------- */
  function openDayView(dateStr) {
    nav.selectedDate = dateStr;
    nav.dayLabFilter = null;
    nav.dayPersonFilter = null;
    showView("view-day");
    renderDayView();
  }

  document.getElementById("btn-day-back").addEventListener("click", function () {
    showView("view-calendar");
    renderCalendar();
  });

  function renderChip(container, label, isActive, onClick) {
    var chip = document.createElement("button");
    chip.type = "button";
    chip.className = "filter-chip" + (isActive ? " active" : "");
    chip.textContent = label;
    chip.addEventListener("click", onClick);
    container.appendChild(chip);
  }

  function renderDayView() {
    var scope = nav.scope;
    var dateStr = nav.selectedDate;
    var parts = dateStr.split("-").map(Number);
    var dt = new Date(parts[0], parts[1] - 1, parts[2]);
    document.getElementById("day-title").textContent =
      parts[1] + "월 " + parts[2] + "일 (" + WEEKDAY_KO[dt.getDay()] + ")";
    document.getElementById("day-subtitle").textContent =
      scope.type === "all" ? "전체 연구실" : labNameOf(scope.labId);

    var scopedEntries = getEntriesForDate(dateStr, scope);

    var labFilterRow = document.getElementById("lab-filter-row");
    labFilterRow.innerHTML = "";
    if (scope.type === "all") {
      labFilterRow.style.display = "";
      renderChip(labFilterRow, "전체 연구실", nav.dayLabFilter === null, function () {
        nav.dayLabFilter = null;
        renderDayView();
      });
      state.labs.forEach(function (lab) {
        renderChip(labFilterRow, lab.name, nav.dayLabFilter === lab.id, function () {
          nav.dayLabFilter = lab.id;
          renderDayView();
        });
      });
    } else {
      labFilterRow.style.display = "none";
    }

    var afterLabFilter = scopedEntries.filter(function (e) {
      return !nav.dayLabFilter || e.labId === nav.dayLabFilter;
    });

    var personFilterRow = document.getElementById("person-filter-row");
    personFilterRow.innerHTML = "";
    var people = [];
    afterLabFilter.forEach(function (e) {
      if (e.registeredBy && people.indexOf(e.registeredBy) === -1) people.push(e.registeredBy);
    });
    if (people.length) {
      personFilterRow.style.display = "";
      renderChip(personFilterRow, "전체 등록자", nav.dayPersonFilter === null, function () {
        nav.dayPersonFilter = null;
        renderDayView();
      });
      people.forEach(function (name) {
        renderChip(personFilterRow, name, nav.dayPersonFilter === name, function () {
          nav.dayPersonFilter = name;
          renderDayView();
        });
      });
    } else {
      personFilterRow.style.display = "none";
    }

    var finalEntries = afterLabFilter.filter(function (e) {
      return !nav.dayPersonFilter || e.registeredBy === nav.dayPersonFilter;
    });

    renderTimeline(finalEntries, dateStr);
  }

  function toMinutes(t) {
    var p = t.split(":").map(Number);
    return p[0] * 60 + p[1];
  }

  function layoutDayEntries(entries) {
    var sorted = entries.slice().sort(function (a, b) {
      return toMinutes(a.startTime) - toMinutes(b.startTime);
    });
    sorted.forEach(function (e) {
      var s = toMinutes(e.startTime);
      var en = e.endTime ? toMinutes(e.endTime) : s + 60;
      e._start = s;
      e._end = Math.max(en, s + 15);
    });

    var groups = [];
    var current = [];
    var currentEnd = -1;
    sorted.forEach(function (e) {
      if (current.length && e._start >= currentEnd) {
        groups.push(current);
        current = [];
        currentEnd = -1;
      }
      current.push(e);
      currentEnd = Math.max(currentEnd, e._end);
    });
    if (current.length) groups.push(current);

    groups.forEach(function (group) {
      var lanes = [];
      group.forEach(function (e) {
        var laneIdx = -1;
        for (var i = 0; i < lanes.length; i++) {
          if (lanes[i] <= e._start) { laneIdx = i; break; }
        }
        if (laneIdx === -1) { laneIdx = lanes.length; lanes.push(0); }
        lanes[laneIdx] = e._end;
        e._lane = laneIdx;
      });
      group.forEach(function (e) { e._laneCount = lanes.length; });
    });

    return sorted;
  }

  function registrantColor(name) {
    if (!name) return "#9a9aa0";
    var hash = 0;
    for (var i = 0; i < name.length; i++) hash = (hash * 31 + name.charCodeAt(i)) >>> 0;
    return REGISTRANT_PALETTE[hash % REGISTRANT_PALETTE.length];
  }

  function renderTimeline(entries, dateStr) {
    var laidOut = layoutDayEntries(entries);

    var rangeStartHour = 7;
    var rangeEndHour = 21;
    laidOut.forEach(function (e) {
      rangeStartHour = Math.min(rangeStartHour, Math.floor(e._start / 60));
      rangeEndHour = Math.max(rangeEndHour, Math.ceil(e._end / 60));
    });
    var totalHours = rangeEndHour - rangeStartHour;

    var hourRail = document.getElementById("hour-rail");
    var track = document.getElementById("track");
    hourRail.style.height = track.style.height = (totalHours * HOUR_PX) + "px";
    hourRail.innerHTML = "";
    track.innerHTML = "";

    for (var h = rangeStartHour; h <= rangeEndHour; h++) {
      var topPx = (h - rangeStartHour) * HOUR_PX;
      var tick = document.createElement("div");
      tick.className = "tick mono";
      tick.style.top = topPx + "px";
      tick.textContent = String(h).padStart(2, "0") + ":00";
      hourRail.appendChild(tick);

      if (h !== rangeStartHour) {
        var line = document.createElement("div");
        line.className = "gridline";
        line.style.top = topPx + "px";
        track.appendChild(line);
      }
    }

    var todayStr = fmtDate(new Date());
    if (dateStr === todayStr) {
      var now = new Date();
      var nowMin = now.getHours() * 60 + now.getMinutes();
      if (nowMin >= rangeStartHour * 60 && nowMin <= rangeEndHour * 60) {
        var nowTop = ((nowMin - rangeStartHour * 60) / 60) * HOUR_PX;
        var nowLine = document.createElement("div");
        nowLine.className = "now-line";
        nowLine.style.top = nowTop + "px";
        track.appendChild(nowLine);
        var nowDot = document.createElement("div");
        nowDot.className = "now-dot";
        nowDot.style.top = (nowTop - 3) + "px";
        track.appendChild(nowDot);
      }
    }

    if (!laidOut.length) {
      var empty = document.createElement("div");
      empty.className = "timeline-empty";
      empty.textContent = "등록된 일정이 없습니다";
      track.appendChild(empty);
    }

    laidOut.forEach(function (e) {
      var top = ((e._start - rangeStartHour * 60) / 60) * HOUR_PX;
      var height = Math.max(((e._end - e._start) / 60) * HOUR_PX, 30);
      var widthPct = 100 / e._laneCount;
      var leftPct = widthPct * e._lane;
      var block = document.createElement("button");
      block.type = "button";
      block.className = "entry-block";
      block.style.top = top + "px";
      block.style.height = (height - 2) + "px";
      block.style.left = "calc(" + leftPct + "% + 2px)";
      block.style.width = "calc(" + widthPct + "% - 6px)";
      block.style.background = registrantColor(e.registeredBy);
      block.innerHTML =
        '<div class="eb-time mono">' + esc(e.startTime) + (e.endTime ? "–" + esc(e.endTime) : "") + "</div>" +
        '<div class="eb-title">' + esc(e.title) + "</div>" +
        '<div class="eb-meta">' + esc(e.projectName) + (e.registeredBy ? " · " + esc(e.registeredBy) : "") + "</div>";
      block.addEventListener("click", function (entry) {
        return function () { openEditEntry(entry); };
      }(e));
      track.appendChild(block);
    });
  }

  /* ---------- ADD / EDIT ENTRY SHEET ---------- */
  function populateHourMinute(hourId, minId) {
    var hourSel = document.getElementById(hourId);
    var minSel = document.getElementById(minId);
    for (var h = 0; h < 24; h++) {
      var opt = document.createElement("option");
      opt.value = String(h).padStart(2, "0");
      opt.textContent = String(h).padStart(2, "0") + "시";
      hourSel.appendChild(opt);
    }
    MINUTE_STEPS.forEach(function (m) {
      var opt = document.createElement("option");
      opt.value = String(m).padStart(2, "0");
      opt.textContent = String(m).padStart(2, "0") + "분";
      minSel.appendChild(opt);
    });
  }

  function populateTimeSelects() {
    populateHourMinute("select-hour", "select-minute");
    populateHourMinute("select-end-hour", "select-end-minute");
  }

  function populateProjectSelect() {
    var sel = document.getElementById("select-project");
    sel.innerHTML = "";
    state.projects.forEach(function (p) {
      var opt = document.createElement("option");
      opt.value = p.id;
      opt.textContent = labNameOf(p.labId) + " · " + p.name;
      sel.appendChild(opt);
    });
  }

  function defaultProjectForScope() {
    var scope = nav.scope;
    if (scope && scope.type === "lab") {
      var match = state.projects.find(function (p) { return p.labId === scope.labId; });
      if (match) return match.id;
    }
    return state.projects.length ? state.projects[0].id : null;
  }

  function getStartTime() {
    return document.getElementById("select-hour").value + ":" + document.getElementById("select-minute").value;
  }

  function getEndTime() {
    return document.getElementById("select-end-hour").value + ":" + document.getElementById("select-end-minute").value;
  }

  function setTimeSelects(hourId, minId, timeStr) {
    var parts = timeStr.split(":");
    document.getElementById(hourId).value = parts[0];
    var target = parseInt(parts[1], 10);
    var nearest = MINUTE_STEPS.reduce(function (best, m) {
      return Math.abs(m - target) < Math.abs(best - target) ? m : best;
    }, 0);
    document.getElementById(minId).value = String(nearest).padStart(2, "0");
  }

  function setStartTime(timeStr) {
    setTimeSelects("select-hour", "select-minute", timeStr);
    syncPresetActive();
  }

  function setEndTime(timeStr) {
    setTimeSelects("select-end-hour", "select-end-minute", timeStr);
  }

  function addOneHour(timeStr) {
    var parts = timeStr.split(":").map(Number);
    var h = Math.min(parts[0] + 1, 23);
    return String(h).padStart(2, "0") + ":" + String(parts[1]).padStart(2, "0");
  }

  function syncPresetActive() {
    var current = getStartTime();
    document.querySelectorAll("#time-presets .chip").forEach(function (chip) {
      chip.classList.toggle("active", chip.dataset.time === current);
    });
  }

  function openSheet() {
    document.getElementById("sheet-backdrop").classList.add("open");
    document.getElementById("day-sheet").classList.add("open");
  }

  function closeSheet() {
    document.getElementById("sheet-backdrop").classList.remove("open");
    document.getElementById("day-sheet").classList.remove("open");
  }

  function resetForm() {
    editingId = null;
    editingProjectId = null;
    editingMemo = "";
    populateProjectSelect();
    var preferred = defaultProjectForScope();
    if (preferred) document.getElementById("select-project").value = preferred;
    document.getElementById("input-title").value = "";
    populateRegistrantSelect(localStorage.getItem(USERNAME_KEY) || USER_LIST[0]);
    setStartTime("09:00");
    setEndTime("10:00");
  }

  function openAddEntry() {
    resetForm();
    document.getElementById("sheet-title-label").textContent = "일정 추가";
    document.getElementById("submit-btn").textContent = "추가";
    document.getElementById("btn-delete-entry").style.display = "none";
    openSheet();
  }

  function openEditEntry(entry) {
    editingId = entry.id;
    editingProjectId = entry.projectId;
    editingMemo = entry.memo || "";
    populateProjectSelect();
    document.getElementById("select-project").value = entry.projectId;
    setStartTime(entry.startTime);
    setEndTime(entry.endTime || addOneHour(entry.startTime));
    document.getElementById("input-title").value = entry.title;
    populateRegistrantSelect(entry.registeredBy || USER_LIST[0]);
    document.getElementById("sheet-title-label").textContent = "일정 수정";
    document.getElementById("submit-btn").textContent = "수정 완료";
    document.getElementById("btn-delete-entry").style.display = "";
    openSheet();
  }

  document.getElementById("btn-add-entry").addEventListener("click", openAddEntry);
  document.getElementById("btn-sheet-close").addEventListener("click", closeSheet);
  document.getElementById("sheet-backdrop").addEventListener("click", closeSheet);

  document.getElementById("btn-delete-entry").addEventListener("click", function () {
    if (!editingId || !editingProjectId) return;
    var list = (state.schedules[editingProjectId] || {})[nav.selectedDate] || [];
    state.schedules[editingProjectId][nav.selectedDate] = list.filter(function (x) { return x.id !== editingId; });
    save(state);
    closeSheet();
    renderDayView();
  });

  document.getElementById("sheet-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var projectId = document.getElementById("select-project").value;
    if (!projectId) return;
    var startTime = getStartTime();
    var endTime = getEndTime();
    var title = document.getElementById("input-title").value.trim();
    var registeredBy = document.getElementById("select-registrant").value;
    if (!title || !registeredBy) return;

    localStorage.setItem(USERNAME_KEY, registeredBy);

    if (!state.schedules[projectId]) state.schedules[projectId] = {};
    if (!state.schedules[projectId][nav.selectedDate]) state.schedules[projectId][nav.selectedDate] = [];

    if (editingId) {
      if (editingProjectId && state.schedules[editingProjectId] && state.schedules[editingProjectId][nav.selectedDate]) {
        state.schedules[editingProjectId][nav.selectedDate] =
          state.schedules[editingProjectId][nav.selectedDate].filter(function (x) { return x.id !== editingId; });
      }
      state.schedules[projectId][nav.selectedDate].push({
        id: editingId, startTime: startTime, endTime: endTime, title: title, memo: editingMemo, registeredBy: registeredBy
      });
    } else {
      state.schedules[projectId][nav.selectedDate].push({
        id: uid(), startTime: startTime, endTime: endTime, title: title, memo: "", registeredBy: registeredBy
      });
    }
    save(state);
    closeSheet();
    renderDayView();
  });

  document.getElementById("select-hour").addEventListener("change", syncPresetActive);
  document.getElementById("select-minute").addEventListener("change", syncPresetActive);
  document.querySelectorAll("#time-presets .chip").forEach(function (chip) {
    chip.addEventListener("click", function () {
      setStartTime(chip.dataset.time);
      setEndTime(addOneHour(chip.dataset.time));
    });
  });

  populateTimeSelects();

  /* ---------- GENERIC MODAL ---------- */
  var modalCallback = null;

  function openModal(title, placeholder, onConfirm) {
    document.getElementById("modal-title").textContent = title;
    var input = document.getElementById("modal-input");
    input.value = "";
    input.placeholder = placeholder;
    modalCallback = onConfirm;
    document.getElementById("modal-wrap").classList.add("open");
    setTimeout(function () { input.focus(); }, 50);
  }

  function closeModal() {
    document.getElementById("modal-wrap").classList.remove("open");
    modalCallback = null;
  }

  document.getElementById("modal-cancel").addEventListener("click", closeModal);
  document.getElementById("modal-backdrop").addEventListener("click", closeModal);
  document.getElementById("modal-confirm").addEventListener("click", function () {
    var val = document.getElementById("modal-input").value.trim();
    if (!val) return;
    var cb = modalCallback;
    closeModal();
    if (cb) cb(val);
  });
  document.getElementById("modal-input").addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      document.getElementById("modal-confirm").click();
    }
  });

  /* ---------- USER LIST ---------- */
  var USER_LIST = [
    "김민준", "이서연", "박도현", "최지우", "정하은",
    "강민서", "조현우", "윤지호", "장서윤", "임수빈",
    "한예린", "오승민", "서다은", "신태윤", "권은서",
    "황소율", "안재원", "송나연", "전준서", "홍채원",
    "유지민", "고은우", "문서진", "양시우", "손유나",
    "배현진", "백승우", "허지안", "남도윤", "노은채"
  ];

  function populateRegistrantSelect(selected) {
    var sel = document.getElementById("select-registrant");
    sel.innerHTML = "";
    var names = USER_LIST.slice();
    if (selected && names.indexOf(selected) === -1) names.unshift(selected);
    names.forEach(function (name) {
      var opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name;
      sel.appendChild(opt);
    });
    if (selected) sel.value = selected;
  }

  function renderUserList() {
    var list = document.getElementById("user-list");
    list.innerHTML = "";
    USER_LIST.forEach(function (name) {
      var row = document.createElement("div");
      row.className = "user-row";
      row.innerHTML =
        '<span class="user-avatar" style="background:' + registrantColor(name) + '">' + esc(name.charAt(0)) + "</span>" +
        '<span class="user-name">' + esc(name) + "</span>";
      list.appendChild(row);
    });
    document.getElementById("userlist-count").textContent = "(" + USER_LIST.length + "명)";
  }

  function openUserList() {
    renderUserList();
    document.getElementById("userlist-wrap").classList.add("open");
  }

  function closeUserList() {
    document.getElementById("userlist-wrap").classList.remove("open");
  }

  document.getElementById("btn-open-userlist").addEventListener("click", openUserList);
  document.getElementById("userlist-close").addEventListener("click", closeUserList);
  document.getElementById("userlist-backdrop").addEventListener("click", closeUserList);

  /* ---------- view mode (PC / mobile) ---------- */
  var VIEWMODE_KEY = "donforget_viewmode";
  var viewMode = localStorage.getItem(VIEWMODE_KEY) || "pc";

  function applyViewMode() {
    document.body.classList.toggle("mode-mobile", viewMode === "mobile");
    document.getElementById("btn-mode-pc").classList.toggle("active", viewMode === "pc");
    document.getElementById("btn-mode-mobile").classList.toggle("active", viewMode === "mobile");
  }

  function setViewMode(mode) {
    viewMode = mode;
    localStorage.setItem(VIEWMODE_KEY, mode);
    applyViewMode();
  }

  document.getElementById("btn-mode-pc").addEventListener("click", function () { setViewMode("pc"); });
  document.getElementById("btn-mode-mobile").addEventListener("click", function () { setViewMode("mobile"); });

  /* ---------- init ---------- */
  document.querySelectorAll(".cosmax-logo").forEach(function (img) {
    img.src = COSMAX_LOGO;
  });
  applyViewMode();
  renderHome();
  initSync();
})();
</script>
</body>
</html>
"""

components.html(
    APP_HTML,
    height=1400,
    scrolling=True,
)

# ---------------------------------------------------------------------------
# 참고: Firebase 실시간 동기화
# ---------------------------------------------------------------------------
# 위 HTML 안의 FIREBASE_CONFIG 값(apiKey, authDomain, databaseURL, projectId)이
# 현재 "REPLACE_ME"로 되어 있어요. Firebase 콘솔(console.firebase.google.com)에서
# 프로젝트를 만든 뒤 해당 값들을 채워 넣으면 여러 사용자 간 실시간 동기화가
# 활성화됩니다.