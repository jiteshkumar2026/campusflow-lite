import sqlite3
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

NOTICE_URL = "https://uktech.ac.in/en/feature/news-and-announcements"   
SELECTOR = 'div.notice-list a[href$="news-and-announcements"]' 
DB_PATH = "campusflow.db"
CACHE_SECONDS = 30 * 60

def _conn():
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS notices
                   (title TEXT, link TEXT, fetched_at REAL)""")
    return con

def _scrape(limit=10):
    r = requests.get(NOTICE_URL, timeout=10,
                     headers={"User-Agent": "Mozilla/5.0 (CampusFlow student project)"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    items, seen = [], set()
    for a in soup.select(SELECTOR):
        title = a.get_text(" ", strip=True)
        href = a.get("href")
        if title and href and title not in seen:
            seen.add(title)
            items.append({"title": title, "link": urljoin(NOTICE_URL, href)})
        if len(items) >= limit:
            break
    return items

def get_notifications(limit=10):
    """Returns [{'title','link'}]. Uses cache; falls back to old data if site is down."""
    con = _conn()
    row = con.execute("SELECT MAX(fetched_at) FROM notices").fetchone()
    fresh = row[0] and (time.time() - row[0] < CACHE_SECONDS)
    if not fresh:
        try:
            items = _scrape(limit)
            if items:
                con.execute("DELETE FROM notices")
                con.executemany("INSERT INTO notices VALUES (?,?,?)",
                                [(i["title"], i["link"], time.time()) for i in items])
                con.commit()
        except Exception as e:
            print("Notice fetch failed:", e)    # keep showing cached data
    rows = con.execute("SELECT title, link FROM notices").fetchall()
    con.close()
    return [{"title": t, "link": l} for t, l in rows]

if __name__ == "__main__":
    for n in get_notifications():
        print(n)