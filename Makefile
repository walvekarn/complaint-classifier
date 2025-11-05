.PHONY: charts clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  make charts  - Generate visualization charts from classified data"
	@echo "  make clean   - Remove generated chart files"
	@echo "  make help    - Show this help message"

# Generate charts using papermill
charts:
	@echo "Generating charts from classified data..."
	papermill notebooks/generate_charts.ipynb notebooks/generate_charts_output.ipynb
	@echo "Charts generated successfully in charts/ directory"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -f charts/*.png
	rm -f notebooks/generate_charts_output.ipynb
	@echo "Clean complete"

