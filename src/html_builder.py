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

    def build_cover_page(self, month):
        template = self.env.get_template('section_cover.html')
        return template.render(
            month=month,
            mode=self.mode
        )

    def build_scorecards(self, scorecards, month):
        if not scorecards: return ""
        template = self.env.get_template('section_scorecards.html')
        return template.render(
            scorecards=scorecards,
            month=month,
            icons_dir=self.env.globals.get('icons_dir', '')
        )

    def build_toc(self):
        template = self.env.get_template('section_toc.html')
        return template.render(icons_dir=self.env.globals.get('icons_dir', ''))

    def build_vision(self):
        template = self.env.get_template('section_vision.html')
        return template.render(icons_dir=self.env.globals.get('icons_dir', ''))

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

    def build_board(self, board):
        if not board: return ""
        template = self.env.get_template('section_board.html')
        
        formatted_board = []
        for member in board:
            photo = member.get("PHOTO_FILENAME", "")
            if photo:
                img_path = ASSETS_DIR.joinpath('images/directors/processed', photo).as_uri()
            else:
                img_path = ""
            
            member_dict = dict(member)
            member_dict["photo_url"] = img_path
            formatted_board.append(member_dict)
            
        return template.render(board=formatted_board)

    def build_hr(self, hr_stats):
        if not hr_stats: return ""
        template = self.env.get_template('section_hr.html')
        return template.render(hr_stats=hr_stats)

    def build_training(self, training):
        if not training: return ""
        template = self.env.get_template('section_training.html')
        return template.render(training=training)

    def build_pensions(self, pensions):
        if not pensions: return ""
        template = self.env.get_template('section_pensions.html')
        return template.render(pensions=pensions)

    def build_it_projects(self, it_projects):
        if not it_projects: return ""
        template = self.env.get_template('section_it.html')
        return template.render(it_projects=it_projects)

    def build_audit(self, audit):
        if not audit: return ""
        template = self.env.get_template('section_audit.html')
        return template.render(audit=audit)

    def build_complete_html(self, data):
        """Builds all available sections and injects into base.html."""
        sections = []
        month = data.get("report_month", "")

        # Front Matter
        sections.append(self.build_cover_page(month))
        sections.append(self.build_toc())
        sections.append(self.build_vision())
        sections.append(self.build_scorecards(data.get("scorecards", []), month))
        sections.append(self.build_districts(data.get("districts", []), data.get("charts", {})))
        sections.append(self.build_events_section(data.get("events", [])))
        sections.append(self.build_board(data.get("board", [])))
        sections.append(self.build_hr(data.get("hr_stats", [])))
        sections.append(self.build_training(data.get("training", [])))
        sections.append(self.build_pensions(data.get("pensions", [])))
        sections.append(self.build_it_projects(data.get("it_projects", [])))
        sections.append(self.build_audit(data.get("audit", [])))
        
        base_template = self.env.get_template('base.html')
        
        # Bug #3 fix: correct path separator for cross-platform file URI
        fonts_uri = ASSETS_DIR.joinpath('fonts').as_uri() + '/'
        css_uri = ASSETS_DIR.joinpath('css').as_uri() + '/'
        icons_uri = ASSETS_DIR.joinpath('icons').as_uri() + '/'
        
        html_output = base_template.render(
            content='\n'.join(sections),   # Bug #1 fix: was '\\n' (literal backslash-n)
            mode=self.mode,
            fonts_dir=fonts_uri,
            css_dir=css_uri,
            icons_dir=icons_uri
        )
        
        # Bug #2 fix: ensure the output/html directory exists before writing
        html_debug_path = OUTPUT_DIR / "html" / "debug_report.html"
        html_debug_path.parent.mkdir(parents=True, exist_ok=True)
        html_debug_path.write_text(html_output, encoding="utf-8")
            
        return html_output
