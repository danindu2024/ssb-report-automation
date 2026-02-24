"""
HTML Builder Engine for SSB Monthly Report.
Combines data and charts into Jinja2 templates.
"""
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from config import BASE_DIR, ASSETS_DIR, CHARTS_DIR, OUTPUT_DIR

class HTMLReportBuilder:
    def __init__(self, mode="preview"):
        self.mode = mode
        self.template_dir = BASE_DIR / "templates"
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        
        # Add custom filters
        self.env.filters['format_number'] = self._format_number
        self.env.filters['format_currency'] = self._format_currency

    def _format_number(self, value):
        try:
            return f"{int(float(value)):,}"
        except:
            return value

    def _format_currency(self, value):
        try:
            return f"රු {float(value):,.2f}"
        except:
            return value

    def build_cover_page(self, data):
        template = self.env.get_template('section_cover.html')
        return template.render(
            month=data.get("report_month", ""),
            mode=self.mode
        )

    def build_scorecards(self, scorecards):
        if not scorecards: return ""
        template = self.env.get_template('section_scorecards.html')
        return template.render(scorecards=scorecards)

    def build_districts(self, districts, charts):
        if not districts: return ""
        template = self.env.get_template('section_districts.html')
        
        # Bug #4 fix: charts live in OUTPUT_DIR/charts, not ASSETS_DIR
        chart_paths = {
            k: (CHARTS_DIR / v).as_uri()
            for k, v in charts.items() if v
        }
        
        return template.render(districts=districts, charts=chart_paths)

    def build_events_section(self, events):
        if not events: return ""
        template = self.env.get_template('section_events.html')
        
        # Format events strictly for template consumption
        formatted_events = []
        for e in events:
            # We assume the image_processor has created standard '01.jpg', '02.jpg' etc 
            # in the processed folder. We'll link to '01.jpg' as the main cover photo for the event card.
            photo_folder = e.get("PHOTO_FOLDER", "")
            img_path = f"file:///{ASSETS_DIR.parent}/assets/images/events/processed/{photo_folder}/01.jpg"
            
            formatted_events.append({
                "title": e.get("EVENT_TITLE"),
                "date": e.get("EVENT_DATE"),
                "description": e.get("DESCRIPTION"),
                "location": e.get("LOCATION"),
                "image_url": img_path
            })
            
        return template.render(events=formatted_events)

    def build_complete_html(self, data):
        """Builds all available sections and injects into base.html."""
        sections = []
        
        sections.append(self.build_cover_page(data))
        sections.append(self.build_scorecards(data.get("scorecards", [])))
        sections.append(self.build_districts(data.get("districts", []), data.get("charts", {})))
        sections.append(self.build_events_section(data.get("events", [])))
        # NOTE: board, hr, training, pensions, it_projects, audit sections
        # will be rendered inline using a generic table template until dedicated
        # section templates are created in a future sprint.
        
        base_template = self.env.get_template('base.html')
        
        # Bug #3 fix: correct path separator for cross-platform file URI
        fonts_uri = ASSETS_DIR.joinpath('fonts').as_uri() + '/'
        
        html_output = base_template.render(
            content='\n'.join(sections),   # Bug #1 fix: was '\\n' (literal backslash-n)
            mode=self.mode,
            fonts_dir=fonts_uri
        )
        
        # Bug #2 fix: ensure the output/html directory exists before writing
        html_debug_path = OUTPUT_DIR / "html" / "debug_report.html"
        html_debug_path.parent.mkdir(parents=True, exist_ok=True)
        html_debug_path.write_text(html_output, encoding="utf-8")
            
        return html_output
