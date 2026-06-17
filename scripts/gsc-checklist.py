"""
gsc-checklist.py
────────────────
GSC "URL 검사 → 색인 생성 요청"을 수동으로 진행하기 위한 체크리스트 도구.
※ 자동화 아님 — 클릭/요청은 사용자가 직접 GSC에서 수행합니다.

사용법:
  python scripts/gsc-checklist.py

기능:
  - data/gsc-priority-urls.txt 의 URL 목록을 보여줌
  - 더블클릭 또는 "🌐 GSC에서 열기" → 클립보드 복사 + GSC 검사창 열림
  - "✅ 완료 처리" → .gsc-checklist-done.json 의 done 목록에 추가, 리스트에서 제거
"""

import os
import json
import webbrowser
import tkinter as tk
from tkinter import messagebox

BASE_DIR  = os.path.join(os.path.dirname(__file__), "..")
URLS_FILE = os.path.join(BASE_DIR, "data", "gsc-priority-urls.txt")
DONE_FILE = os.path.join(BASE_DIR, "data", ".gsc-checklist-done.json")

SITE_URL          = "https://wooriwin.com/"
GSC_INSPECT_BASE  = "https://search.google.com/search-console/inspect?resource_id="


def load_urls():
    if not os.path.exists(URLS_FILE):
        return []
    with open(URLS_FILE, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def load_done():
    if os.path.exists(DONE_FILE):
        with open(DONE_FILE, encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("done", []))
    return set()


def save_done(done):
    with open(DONE_FILE, "w", encoding="utf-8") as f:
        json.dump({"done": sorted(done)}, f, ensure_ascii=False, indent=2)


class ChecklistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GSC 색인 요청 체크리스트")
        self.root.geometry("640x520")

        self.all_urls = load_urls()
        self.done     = load_done()
        self.pending  = [u for u in self.all_urls if u not in self.done]

        info = tk.Label(
            root,
            text="URL을 더블클릭하면 클립보드에 복사됩니다.\n"
                 "GSC 검사창에 붙여넣고 직접 검사 → 색인 생성 요청을 누르세요.",
            justify="left", anchor="w", padx=10, pady=8,
        )
        info.pack(fill="x")

        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True, padx=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            frame, yscrollcommand=scrollbar.set, font=("Consolas", 10)
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        for url in self.pending:
            self.listbox.insert(tk.END, url)

        self.listbox.bind("<Double-Button-1>", self.copy_to_clipboard)

        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=8)
        tk.Button(btn_frame, text="🌐 GSC에서 열기", command=self.open_gsc).pack(side="left", padx=4)
        tk.Button(btn_frame, text="✅ 완료 처리",   command=self.mark_done).pack(side="left", padx=4)

        self.status = tk.Label(root, text="", anchor="w", padx=10, pady=4)
        self.status.pack(fill="x")
        self.update_status()

    def update_status(self):
        self.status.config(
            text=f"남은 항목: {len(self.pending)} / 전체: {len(self.all_urls)}"
                 f"  (완료: {len(self.done)})"
        )

    def get_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("알림", "먼저 목록에서 URL을 선택하세요.")
            return None
        return self.listbox.get(sel[0]), sel[0]

    def copy_to_clipboard(self, event=None):
        picked = self.get_selected()
        if not picked:
            return
        url, _ = picked
        self.root.clipboard_clear()
        self.root.clipboard_append(url)
        messagebox.showinfo("복사", f"클립보드에 복사됨: {url}")

    def open_gsc(self):
        picked = self.get_selected()
        if not picked:
            return
        url, _ = picked
        self.root.clipboard_clear()
        self.root.clipboard_append(url)
        webbrowser.open(GSC_INSPECT_BASE + SITE_URL)
        messagebox.showinfo("열림", f"브라우저로 GSC 열림 (클립보드에도 복사됨): {url}")

    def mark_done(self):
        picked = self.get_selected()
        if not picked:
            return
        url, idx = picked
        self.done.add(url)
        self.pending.remove(url)
        self.listbox.delete(idx)
        save_done(self.done)
        self.update_status()
        messagebox.showinfo("완료", f"완료 처리됨: {url}")


def main():
    root = tk.Tk()
    ChecklistApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
