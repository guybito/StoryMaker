import os
import json
from datetime import datetime

import re


def format_review_text(raw_text: str) -> str:
    html_lines = []
    lines = raw_text.strip().splitlines()

    in_list = False

    def convert_markdown_bold(text):
        return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    for line in lines:
        line = line.strip()

        if not line:
            continue

        line = convert_markdown_bold(line)

        if line.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h3>{line[3:].strip()}</h3>")

        elif line.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h2>{line[2:].strip()}</h2>")

        elif re.match(r"^[-–—]{5,}$", line):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append("<hr>")

        elif ":" in line and not re.match(r"^\d+\s*:", line):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            parts = line.split(":", 1)
            html_lines.append(f"<p><strong>{parts[0].strip()}:</strong> {parts[1].strip()}</p>")

        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<p>{line}</p>")

    if in_list:
        html_lines.append("</ul>")

    return '\n'.join(html_lines)


def convert_story_to_html(input_file_path: str, review_file_path: str, output_filename: str = "story.html"):
    output_dir = "Results/HTML_Stories"
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    title = "Story"
    paragraphs = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        elif stripped.startswith("# *") and stripped.endswith("*"):
            title = stripped.replace("# *", "").replace("*", "").strip()
        else:
            paragraphs.append(stripped)

    # INFO
    creation_timestamp = os.path.getctime(input_file_path)
    creation_date = datetime.fromtimestamp(creation_timestamp).strftime('%d-%m-%Y %H:%M')
    algorithm_type = "Plotto" if "Plotto" in input_file_path else "Plot Genie" if "PlotGenie" in input_file_path else "Unknown"
    word_count = sum(len(p.split()) for p in paragraphs)

    review = ""
    if review_file_path and os.path.exists(review_file_path):
        with open(review_file_path, 'r', encoding='utf-8') as f:
            review = f.read().strip()

    formatted_review = format_review_text(review)

    html_lines = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        f"<title>{title}</title>",
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Merriweather&display=swap');

            :root {
                --bg-color: #fdf6e3;
                --text-color: #2e2e2e;
                --btn-color: #333;
                --btn-hover: #555;
            }

            body.dark-mode {
                --bg-color: #1e1e1e;
                --text-color: #f0f0f0;
                --btn-color: #ddd;
                --btn-hover: #fff;
            }

            html {
                scroll-behavior: smooth;
            }

            body {
                font-family: 'Merriweather', serif;
                background-color: var(--bg-color);
                color: var(--text-color);
                max-width: 800px;
                margin: auto;
                padding: 50px 30px;
                line-height: 2;
                font-size: 1.15em;
                transition: background-color 0.3s, color 0.3s;
            }

            h1 {
                text-align: center;
                font-size: 3em;
                margin-bottom: 50px;
                border-bottom: 3px double #ccc;
                padding-bottom: 20px;
                letter-spacing: 2px;
            }

            p {
                text-align: justify;
                margin-bottom: 1.8em;
            }

            p::first-letter {
                font-size: 130%;
                font-weight: bold;
            }

            #storyContainer {
                min-height: 600px;
                position: relative;
            }

            #paginationControls {
                text-align: center;
                margin-top: 30px;
                min-height: 60px;
                position: sticky;
                bottom: 20px;
                background-color: var(--bg-color);
                padding: 10px;
                border-top: 1px solid #aaa;
            }

            select, label, button {
                font-size: 1em;
                margin: 6px 10px;
            }

            button, select {
                padding: 6px 14px;
                border: none;
                border-radius: 6px;
                background-color: var(--btn-color);
                color: var(--bg-color);
                transition: background-color 0.3s, color 0.3s;
                cursor: pointer;
            }

            button:hover, select:hover {
                background-color: var(--btn-hover);
            }

            label {
                margin: 0 8px;
                cursor: pointer;
            }

            input[type="radio"] {
                margin-right: 4px;
            }

            #backToTop {
                position: fixed;
                bottom: 30px;
                right: 30px;
                padding: 10px 15px;
                font-size: 1em;
                background-color: var(--btn-color);
                color: var(--bg-color);
                border: none;
                border-radius: 8px;
                cursor: pointer;
                display: none;
            }

            #controlsTop > div {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 10px;
                margin-bottom: 10px;
            }

            #controlsTop {
                text-align: center;
                margin-bottom: 30px;
            }
        </style>
        """,
        "</head>",
        "<body>",
        f"<h1>{title}</h1>",
        f"""
            <!-- Info Modal Trigger -->
            <div style="text-align: center; margin-bottom: 20px;">
                <button onclick="document.getElementById('infoModal').style.display='block'">ℹ️ Info</button>
            </div>
            
            <!-- Info Modal -->
            <div id="infoModal" style="display:none; position:fixed; z-index:1000; left:0; top:0; width:100%; height:100%; overflow:auto; background-color:rgba(0,0,0,0.6);">
              <div style="background-color:#fff; margin:10% auto; padding:20px; border:1px solid #888; width:90%; max-width:600px; border-radius:10px; font-family:'Merriweather', serif;">
                <span onclick="document.getElementById('infoModal').style.display='none'" style="float:right; font-size:28px; font-weight:bold; cursor:pointer;">&times;</span>
                <h2>Story Info</h2>
                <p><strong>📅 Creation Date:</strong> {creation_date}</p>
                <p><strong>🧠 Algorithm:</strong> {algorithm_type}</p>
                <p><strong>📝 Word Count:</strong> {word_count}</p>
                <p><strong>📄 Review:</strong> <button onclick="document.getElementById('reviewModal').style.display='block'">View Review</button></p>
              </div>
            </div>
            <!-- Review Modal -->
            <div id="reviewModal" style="display:none; position:fixed; z-index:1000; left:0; top:0; width:100%; height:100%; overflow:auto; background-color:rgba(0,0,0,0.6);">
              <div style="background-color:#fff; margin:5% auto; padding:30px; border:1px solid #888; width:90%; max-width:800px; border-radius:10px; font-family:'Merriweather', serif; max-height:85%; overflow-y:auto;">
                <span onclick="document.getElementById('reviewModal').style.display='none'" style="float:right; font-size:28px; font-weight:bold; cursor:pointer;">&times;</span>
                <h2 style="margin-top:0;">📘 Story Review</h2>
                {formatted_review}
              </div>
            </div>
        """,
        """
        <div id="controlsTop">
            <div>
                <label><input type="radio" name="viewMode" value="full" checked> Continuous Reading</label>
                <label><input type="radio" name="viewMode" value="paged"> Paginated View</label>
            </div>

            <div id="pageOptions" style="display: none;">
                <label><input type="radio" name="pageMode" value="auto" checked> Auto Paragraphs</label>
                <label><input type="radio" name="pageMode" value="manual"> Manual</label>
                <select id="pageSizeSelect" disabled>
        """ + '\n'.join([f'<option value="{i}">{i}</option>' for i in range(2, 11)]) + """
                </select>
            </div>

            <div>
                <button onclick="toggleDarkMode()">🌙 Toggle Dark Mode</button>
                <button onclick="exportToPDF()">📄 Export to PDF</button>
            </div>

        </div>

        <div id="storyContainer"></div>

        <div id="paginationControls" style="display: none;">
            <button id="firstBtn" onclick="firstPage()">⏮ First</button>
            <button id="prevBtn" onclick="prevPage()">◀ Previous</button>
            <span id="pageIndicator">Page 1 of X</span>
            <button id="nextBtn" onclick="nextPage()">Next ▶</button>
            <button id="lastBtn" onclick="lastPage()">Last ⏭</button>
        </div>

        <button id="backToTop" onclick="window.scrollTo({ top: 0, behavior: 'smooth' });">⬆ Back to Top</button>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script>
            const paragraphs = """ + json.dumps(paragraphs, ensure_ascii=False) + """;
            const storyContainer = document.getElementById("storyContainer");
            const pagination = document.getElementById("paginationControls");
            const pageIndicator = document.getElementById("pageIndicator");
            const pageSizeSelect = document.getElementById("pageSizeSelect");
            const pageOptions = document.getElementById("pageOptions");

            const prevBtn = document.getElementById("prevBtn");
            const nextBtn = document.getElementById("nextBtn");
            const firstBtn = document.getElementById("firstBtn");
            const lastBtn = document.getElementById("lastBtn");

            let currentPage = 0;
            let pageSize = 4;

            function getAutoPageSize() {
                return Math.max(2, Math.floor(window.innerHeight / 250));
            }

            function renderPage(page) {
                const totalPages = Math.ceil(paragraphs.length / pageSize);
                const start = page * pageSize;
                const end = start + pageSize;
                storyContainer.innerHTML = paragraphs.slice(start, end).map(p => `<p>${p}</p>`).join('');
                pageIndicator.textContent = `Page ${page + 1} of ${totalPages}`;
                prevBtn.style.display = page > 0 ? "inline-block" : "none";
                firstBtn.style.display = page > 0 ? "inline-block" : "none";
                nextBtn.style.display = (page + 1 < totalPages) ? "inline-block" : "none";
                lastBtn.style.display = (page + 1 < totalPages) ? "inline-block" : "none";
            }

            function switchToPagedView() {
                const mode = document.querySelector('input[name="pageMode"]:checked').value;
                pageSize = (mode === 'auto') ? getAutoPageSize() : parseInt(pageSizeSelect.value);
                currentPage = 0;
                pagination.style.display = 'block';
                renderPage(currentPage);
            }

            function switchToFullView() {
                pagination.style.display = 'none';
                storyContainer.innerHTML = paragraphs.map(p => `<p>${p}</p>`).join('');
            }

            function nextPage() { const totalPages = Math.ceil(paragraphs.length / pageSize); if ((currentPage + 1) < totalPages) { currentPage++; renderPage(currentPage); } }
            function prevPage() { if (currentPage > 0) { currentPage--; renderPage(currentPage); } }
            function firstPage() { currentPage = 0; renderPage(currentPage); }
            function lastPage() { currentPage = Math.ceil(paragraphs.length / pageSize) - 1; renderPage(currentPage); }

            function toggleDarkMode() {
                document.body.classList.toggle("dark-mode");
            }

            function exportToPDF() {
                const { jsPDF } = window.jspdf;
                const doc = new jsPDF();
                const pageHeight = doc.internal.pageSize.height;
                const margin = 15;
                let y = margin;
            
                // Title
                doc.setFontSize(18);
                doc.setFont("times", "bold");
                doc.text(document.title, doc.internal.pageSize.width / 2, y, { align: "center" });
                y += 15;
            
                // Content
                doc.setFontSize(12);
                doc.setFont("times", "normal");
            
                paragraphs.forEach(p => {
                    const lines = doc.splitTextToSize(p, 180);
                    const blockHeight = lines.length * 8;
            
                    if (y + blockHeight > pageHeight - margin) {
                        doc.addPage();
                        y = margin;
                    }
            
                    doc.text(lines, margin, y);
                    y += blockHeight; // space between paragraphs
                });
            
                const safeTitle = document.title.replace(/[^a-z0-9]/gi, "_").toLowerCase();
                doc.save(`${safeTitle}.pdf`);
            }


            document.querySelectorAll('input[name="viewMode"]').forEach(r => {
                r.addEventListener('change', e => {
                    if (e.target.value === 'full') {
                        pageOptions.style.display = 'none';
                        switchToFullView();
                    } else {
                        pageOptions.style.display = 'block';
                        switchToPagedView();
                    }
                });
            });

            document.querySelectorAll('input[name="pageMode"]').forEach(r => {
                r.addEventListener('change', e => {
                    const isManual = e.target.value === 'manual';
                    pageSizeSelect.disabled = !isManual;
                    if (document.querySelector('input[name="viewMode"]:checked').value === 'paged') {
                        switchToPagedView();
                    }
                });
            });

            pageSizeSelect.addEventListener('change', () => {
                if (document.querySelector('input[name="viewMode"]:checked').value === 'paged') {
                    switchToPagedView();
                }
            });

            window.addEventListener('scroll', () => {
                const btn = document.getElementById("backToTop");
                btn.style.display = window.scrollY > 300 ? "block" : "none";
            });

            switchToFullView();
        </script>
        """,
        "</body>",
        "</html>"
    ]

    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))

    print(f"✔ Story successfully converted and saved to: {output_path}")


if __name__ == "__main__":
    convert_story_to_html(
        "PlotGenie/Exp_4/PlotGenieImprovedStories/The House Always Wins_improved.txt",
        "PlotGenie/Exp_4/PlotGenieImprovedReports/17_The_House_Always_Wins_improved_Report_Plot_Genie.txt",
        "The House Always Wins.html"
    )
