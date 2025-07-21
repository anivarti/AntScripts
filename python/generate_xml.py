import uuid

class DrawioXML:
    def __init__(self, 
                 name="Diagram",
                 dx=1092, dy=609,
                 grid=1, gridSize=10, guides=1, tooltips=1, connect=1, arrows=1,
                 fold=1, page=1, pageScale=1, pageWidth=850, pageHeight=1100,
                 background="#ffffff", math=0, shadow=0,
                 host="app.diagrams.net", agent=None, version="28.0.4"):
        self.name = name
        self.dx = dx
        self.dy = dy
        self.grid = grid
        self.gridSize = gridSize
        self.guides = guides
        self.tooltips = tooltips
        self.connect = connect
        self.arrows = arrows
        self.fold = fold
        self.page = page
        self.pageScale = pageScale
        self.pageWidth = pageWidth
        self.pageHeight = pageHeight
        self.background = background
        self.math = math
        self.shadow = shadow
        self.host = host
        self.agent = agent or "PythonDrawioXMLGenerator"
        self.version = version
        self.shapes = []
        self.edges = []
        self.root_cells = [
            '<mxCell id="0"/>',
            '<mxCell id="1" parent="0"/>'
        ]

    def add_rectangle(self, x, y, width, height, fill="#ffffff", stroke="#000000", value="", rounded=0):
        """Add a rectangle shape."""
        cell_id = self._generate_id()
        style = f"rounded={rounded};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fillStyle=solid;"
        cell = f'''
        <mxCell id="{cell_id}" value="{value}" style="{style}" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/>
        </mxCell>
        '''
        self.shapes.append(cell.strip())

    def add_line(self, x1, y1, x2, y2, stroke="#000000", value="", startArrow="classic", endArrow="none"):
        """Add a line edge."""
        cell_id = self._generate_id()
        style = f"endArrow={endArrow};startArrow={startArrow};html=1;rounded=0;fontFamily=Helvetica;fontSize=12;fontColor=default;strokeColor={stroke};"
        cell = f'''
        <mxCell id="{cell_id}" value="{value}" style="{style}" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="{x1}" y="{y1}" as="sourcePoint" />
            <mxPoint x="{x2}" y="{y2}" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        '''
        self.edges.append(cell.strip())

    def _generate_id(self):
        # Generate a unique ID for mxCell
        return str(uuid.uuid4())

    def generate_xml(self):
        shapes_str = "\n".join(self.shapes)
        edges_str = "\n".join(self.edges)

        xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="{self.host}" agent="{self.agent}" version="{self.version}">
  <diagram name="{self.name}" id="{self._generate_id()}">
    <mxGraphModel dx="{self.dx}" dy="{self.dy}" grid="{self.grid}" gridSize="{self.gridSize}" guides="{self.guides}" tooltips="{self.tooltips}" connect="{self.connect}" arrows="{self.arrows}" fold="{self.fold}" page="{self.page}" pageScale="{self.pageScale}" pageWidth="{self.pageWidth}" pageHeight="{self.pageHeight}" background="{self.background}" math="{self.math}" shadow="{self.shadow}">
      <root>
        {''.join(self.root_cells)}
        {shapes_str}
        {edges_str}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''
        return xml

    def save(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.generate_xml())
        print(f"✅ File saved: {filepath}")


# ===== Example usage =====

if __name__ == "__main__":
    dxml = DrawioXML(name="5x5 Grid Example")

    # Add a 5x5 grid of alternating red/blue rectangles
    rect_w, rect_h = 100, 60
    rows, cols = 5, 5
    for r in range(rows):
        for c in range(cols):
            fill = "#ff0000" if (r + c) % 2 == 0 else "#0000ff"
            x = c * rect_w
            y = r * rect_h
            dxml.add_rectangle(x, y, rect_w, rect_h, fill=fill, stroke="#000000", value=f"R{r}C{c}")

    # Add some lines connecting rectangles (just as an example)
    for r in range(rows):
        for c in range(cols - 1):
            # horizontal line connecting rect (r,c) to (r,c+1)
            x1 = c * rect_w + rect_w
            y1 = r * rect_h + rect_h // 2
            x2 = (c + 1) * rect_w
            y2 = y1
            dxml.add_line(x1, y1, x2, y2, stroke="#000000", value="→")

    # Save XML file
    dxml.save("grid_example.drawio")

