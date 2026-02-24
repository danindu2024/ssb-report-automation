import sys
import io

# Bug fix: Windows terminal defaults to cp1252, which can't encode emoji or
# Sinhala Unicode characters used in print() calls throughout the pipeline.
# Reconfigure stdout to UTF-8 at process start.
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from cli_config import parse_arguments
from config import initialize_system, MASTER_EXCEL_PATH

# Custom stages
from data_loader import load_master_sheet
from data_validator import validate_data, write_validation_report
from image_processor import process_all_event_images

def main():
    # ---------------------------------------------------------
    # STAGE 0: Setup and Parse args
    # ---------------------------------------------------------
    args = parse_arguments()

    print("\n🚀 Starting Report Generation")
    print(f"   Month: {args.month}")
    print(f"   Mode:  {args.mode.upper()}")
    print("-" * 60)

    # Validate output structure
    if not initialize_system():
        print("❌ System initialization failed. Check permissions/disk space.")
        return 1

    # ---------------------------------------------------------
    # STAGE 1: Data Loading (Extract Excel)
    # ---------------------------------------------------------
    try:
        print("📥 Step 1: Loading Data...")
        # (Using config defined structure, defaulting to the 2026 spec)
        data = load_master_sheet(args.month, MASTER_EXCEL_PATH)
    except Exception as e:
        print(f"❌ Failed to load Excel data: {e}")
        return 1

    # ---------------------------------------------------------
    # STAGE 2: Validation
    # ---------------------------------------------------------
    if not args.skip_validation:
        print("🔎 Step 2: Validating Data...")
        errors, warnings = validate_data(data)

        # Write report regardless of status
        report_path = write_validation_report(errors, warnings, args.month)

        if warnings:
            print(f"   ⚠️  {len(warnings)} warning(s). See report for details.")

        if errors:
            print(f"   ❌ Validation failed with {len(errors)} error(s).")
            print(f"   Detailed report written to: {report_path}")

            # If validate-only flag is set, exit 0 so the coordinator can review
            if args.validate_only:
                print("   Exiting (Validation only run)")
                return 0
            else:
                print("   Fix validation errors before generating PDF!")
                return 1
        else:
            print("   ✓ Validation passed.")
            
    if args.validate_only:
        print("   Exiting (Validation only run)")
        return 0

    # ---------------------------------------------------------
    # STAGE 3: Image Processing
    # ---------------------------------------------------------
    if not args.skip_images:
        print("🖼️ Step 3: Processing Images...")
        try:
            # Send events directly to the processor
            process_all_event_images(data.get("events", []))
        except Exception as e:
            print(f"   ⚠️ Image processing failed (continuing): {e}")

    # ---------------------------------------------------------
    # STAGE 4: Charts and Visualizations
    # ---------------------------------------------------------
    print("📊 Step 4: Generating Charts...")
    try:
        from chart_generator import generate_all_charts
        generated_charts = generate_all_charts(data, args.month)
        # Inject chart filenames back into the data dictionary for the HTML builder
        data["charts"] = generated_charts
    except Exception as e:
        print(f"   ⚠️ Chart generation failed (continuing without charts): {e}")

    # ---------------------------------------------------------
    # STAGE 5: Building HTML Templates
    # ---------------------------------------------------------
    print("📝 Step 5: Building HTML Template...")
    try:
        from html_builder import HTMLReportBuilder
        builder = HTMLReportBuilder(mode=args.mode)
        html_content = builder.build_complete_html(data)
        print("   ✓ HTML built successfully.")
    except Exception as e:
        print(f"   ❌ Error building HTML: {e}")
        return 1

    # ---------------------------------------------------------
    # STAGE 6: Generating PDF
    # ---------------------------------------------------------
    print("📄 Step 6: Generating PDF (WeasyPrint)...")
    try:
        from report_generator import PDFGenerator
        from config import OUTPUT_DIR
        
        output_pdf_path = OUTPUT_DIR / f"SSB_Monthly_Report_{args.month}.pdf"
        
        pdf_gen = PDFGenerator(mode=args.mode)
        success = pdf_gen.generate_pdf(html_content, output_pdf_path)
        
        if success:
            print("-" * 60)
            print(f"✅ Success! View your report: {output_pdf_path}")
            print("-" * 60)
    except Exception as e:
        print(f"   ❌ Error during PDF wrapping: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())