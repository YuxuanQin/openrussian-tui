from __future__ import annotations
import re

try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'pip install httpx'")

from textual import getters, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Markdown, Footer, Header


def add_acute_accent(text: str) -> str:
    """
    Replace X' with X + combining acute accent (U+0301).
    Example: Человe'к ==> Челове́к
    """
    def replace_match(match):
        char = match.group(1)
        return char + '\u0301'  # This is a normal Python string — safe!
    
    return re.sub(r"([^'])'", replace_match, text)

class OpenRussian(App):
    CSS_PATH = "openrussian.tcss"
    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle dark mode")]

    results = getters.query_one("#results", Markdown)
    input = getters.query_one(Input)

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a word", id="dictionary-search")
        with VerticalScroll(id="results-container"):
            yield Markdown(id="results")
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = "textual-light" if self.theme == "textual-dark" else "textual-dark"

    async def on_input_changed(self, message: Input.Changed) -> None:
        if message.value:
            self.lookup_word(message.value)
        else:
            await self.results.update("")

    @work(exclusive=True)
    async def lookup_word(self, word: str) -> None:
        url = f"https://api.openrussian.org/suggestions?q={word}&lang=en"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                results = response.json()
            except Exception as e:
                await self.results.update(f"# Error\nFailed to fetch data: `{type(e).__name__}`")
                return

        if word == self.input.value.strip():
            markdown = self.make_word_markdown(results)
            await self.results.update(markdown)

    # ✅ THIS METHOD MUST BE HERE, INSIDE THE CLASS
    def make_word_markdown(self, results: object) -> str:
        """Convert OpenRussian API results into rich bilingual markdown."""
        lines = []
    
        # Handle malformed or error responses
        if not isinstance(results, dict) or "result" not in results:
            lines.append("# Error")
            lines.append("Invalid response from dictionary API.")
            return "\n".join(lines)
    
        result_data = results["result"]
        term = result_data.get("term", "").strip()
        
        if not term:
            lines.append("# No word found")
            return "\n".join(lines)
    
        # Main heading: the Russian word
        lines.append(f"# {term}")
        lines.append("")
    
        # === Translations / Meanings ===
        words = result_data.get("words", [])
        if words:
            first_word = words[0]
            tls2 = first_word.get("tls2", [])
            
            if tls2:
                lines.append("## English Translations")
                lines.append("")
                for i, group in enumerate(tls2):
                    translations = group.get("translation", [])
                    if translations:
                        trans_str = ", ".join(translations)
                        lines.append(f"- {trans_str}")
                lines.append("")
            else:
                # Fallback to 'tls' if tls2 is absent
                tls = first_word.get("tls", [])
                all_trans = []
                for group in tls:
                    if isinstance(group, list):
                        all_trans.extend(str(t) for t in group)
                if all_trans:
                    lines.append("## English Translations")
                    lines.append("")
                    lines.append(", ".join(all_trans))
                    lines.append("")
    
        # === Bilingual Examples ===
        sentences = result_data.get("sentences", [])
        if sentences:
            lines.append("## Example Sentences")
            lines.append("")
            for sent in sentences[:6]:  # Show up to 6 examples
                ru = sent.get("ru", "").strip()
                en = sent.get("tl", "").strip()
                if ru or en:
                    if ru:
                        ru_formatted = add_acute_accent(ru)
                        lines.append(f"+ **{ru_formatted}**")
                    if en:
                        lines.append(f"\n   {en}")
                    lines.append("")  # Blank line between examples
    
        # Final fallback message
        if len(lines) <= 2:  # Only has "# term"
            lines.append("_No translations or examples available._")

        return "\n".join(lines)


if __name__ == "__main__":
    app = OpenRussian()
    app.run()
