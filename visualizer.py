"""
MacroHard Visualizer
Generates charts and visual representations of data
"""

from typing import List, Dict
import json


class ChartGenerator:
    """Generate ASCII charts for terminal display"""
    
    def __init__(self, width: int = 50, height: int = 10):
        self.width = width
        self.height = height
    
    def bar_chart(self, data: Dict[str, float], title: str = "") -> str:
        """Create a horizontal bar chart"""
        if not data:
            return "No data to display"
        
        max_value = max(data.values()) if data else 1
        chart_lines = []
        
        if title:
            chart_lines.append(f"\n{title}")
            chart_lines.append("=" * self.width)
        
        for label, value in data.items():
            bar_length = int((value / max_value) * self.width)
            bar = "█" * bar_length
            chart_lines.append(f"{label:>15} | {bar} {value:.2f}")
        
        return "\n".join(chart_lines)
    
    def line_graph(self, values: List[float], labels: List[str] = None) -> str:
        """Create a simple ASCII line graph"""
        if not values:
            return "No data to display"
        
        min_val = min(values)
        max_val = max(values)
        value_range = max_val - min_val if max_val != min_val else 1
        
        graph = []
        graph.append(f"\nMax: {max_val:.2f}")
        
        for row in range(self.height, 0, -1):
            line = "|"
            for i, val in enumerate(values):
                normalized = (val - min_val) / value_range
                if normalized * self.height >= row - 1:
                    line += "●"
                else:
                    line += " "
            graph.append(line)
        
        graph.append("+" + "-" * len(values))
        graph.append(f"Min: {min_val:.2f}")
        
        if labels:
            graph.append(" " + "".join(labels[:len(values)]))
        
        return "\n".join(graph)
    
    def histogram(self, values: List[float], bins: int = 10) -> str:
        """Create a histogram distribution"""
        if not values:
            return "No data to display"
        
        min_val = min(values)
        max_val = max(values)
        bin_width = (max_val - min_val) / bins
        
        # Count values in each bin
        bin_counts = [0] * bins
        for val in values:
            bin_index = min(int((val - min_val) / bin_width), bins - 1)
            bin_counts[bin_index] += 1
        
        # Create histogram
        max_count = max(bin_counts) if bin_counts else 1
        chart_lines = ["\nDistribution:"]
        
        for i, count in enumerate(bin_counts):
            bin_start = min_val + i * bin_width
            bin_end = bin_start + bin_width
            bar_length = int((count / max_count) * 30)
            bar = "▓" * bar_length
            chart_lines.append(f"{bin_start:6.1f}-{bin_end:6.1f} | {bar} ({count})")
        
        return "\n".join(chart_lines)


def export_to_json(data: Dict, filename: str = "output.json") -> None:
    """Export data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Data exported to {filename}")


def format_table(headers: List[str], rows: List[List]) -> str:
    """Format data as an ASCII table"""
    if not headers or not rows:
        return "No data to display"
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Create separator
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    
    # Build table
    table_lines = [separator]
    
    # Headers
    header_row = "|" + "|".join(f" {h:^{col_widths[i]}} " for i, h in enumerate(headers)) + "|"
    table_lines.append(header_row)
    table_lines.append(separator)
    
    # Data rows
    for row in rows:
        data_row = "|" + "|".join(f" {str(cell):<{col_widths[i]}} " for i, cell in enumerate(row)) + "|"
        table_lines.append(data_row)
    
    table_lines.append(separator)
    
    return "\n".join(table_lines)


if __name__ == "__main__":
    # Demo
    viz = ChartGenerator()
    
    # Bar chart demo
    sales_data = {"Q1": 45.5, "Q2": 67.8, "Q3": 52.3, "Q4": 89.2}
    print(viz.bar_chart(sales_data, "Quarterly Sales"))
    
    # Line graph demo
    print("\n")
    trend = [10, 15, 13, 20, 25, 30, 28, 35]
    print(viz.line_graph(trend))
    
    # Table demo
    print("\n")
    table = format_table(
        ["Name", "Score", "Status"],
        [["Alice", "95", "Pass"], ["Bob", "87", "Pass"], ["Charlie", "72", "Pass"]]
    )
    print(table)
