import uuid
import xml.etree.ElementTree as ET
from typing import List, Optional

DEFAULTS = {
    "dx": 1092,
    "dy": 609,
    "grid": 1,
    "gridSize": 10,
    "guides": 1,
    "tooltips": 1,
    "connect": 1,
    "arrows": 1,
    "fold": 1,
    "page": 1,
    "pageScale": 1,
    "pageWidth": 850,
    "pageHeight": 1100,
    "background": "#ffffff",
    "math": 0,
    "shadow": 0,
    "host": "app.diagrams.net",
    "agent": "PythonDrawioXMLGenerator",
    "version": "28.0.4"
}

class DrawioXML:
    def __init__(
        self,
        name: str = "Diagram",
        dx: int = DEFAULTS["dx"], dy: int = DEFAULTS["dy"],
        grid: int = DEFAULTS["grid"], gridSize: int = DEFAULTS["gridSize"],
        guides: int = DEFAULTS["guides"], tooltips: int = DEFAULTS["tooltips"],
        connect: int = DEFAULTS["connect"], arrows: int = DEFAULTS["arrows"],
        fold: int = DEFAULTS["fold"], page: int = DEFAULTS["page"],
        pageScale: int = DEFAULTS["pageScale"], pageWidth: int = DEFAULTS["pageWidth"],
        pageHeight: int = DEFAULTS["pageHeight"], background: str = DEFAULTS["background"],
        math: int = DEFAULTS["math"], shadow: int = DEFAULTS["shadow"],
        host: str = DEFAULTS["host"], agent: Optional[str] = None,
        version: str = DEFAULTS["version"]
    ) -> None:
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
        self.agent = agent if agent else DEFAULTS["agent"]
        self.version = version

        self.cells: List[ET.Element] = []
        self.root_cells = [
            ET.Element("mxCell", id="0"),
            ET.Element("mxCell", id="1", parent="0")
        ]

    def _generate_id(self) -> str:
        return str(uuid.uuid4())

    def add_rectangle(
        self, x: int, y: int, width: int, height: int,
        fill: str = "#ffffff", stroke: str = "#000000",
        value: str = "", rounded: int = 0
    ) -> None:
        cell_id = self._generate_id()
        style = f"rounded={rounded};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fillStyle=solid;"
        cell = ET.Element(
            "mxCell",
            id=cell_id, value=value, style=style, vertex="1", parent="1"
        )
        geometry = ET.SubElement(
            cell, "mxGeometry",
            x=str(x), y=str(y), width=str(width), height=str(height), as_="geometry"
        )
        geometry.attrib["as"] = "geometry"  # correct key for as
        self.cells.append(cell)

    def add_line(
        self, x1: int, y1: int, x2: int, y2: int,
        stroke: str = "#000000", value: str = "",
        startArrow: str = "classic", endArrow: str = "none"
    ) -> None:
        cell_id = self._generate_id()
        style = (
            f"endArrow={endArrow};startArrow={startArrow};html=1;rounded=0;"
            f"fontFamily=Helvetica;fontSize=12;fontColor=default;strokeColor={stroke};"
        )
        cell = ET.Element(
            "mxCell",
            id=cell_id, value=value, style=style, edge="1", parent="1"
        )
        geometry = ET.SubElement(
            cell, "mxGeometry", width="50", height="50", relative="1", as_="geometry"
        )
        geometry.attrib["as"] = "geometry"  # correct key for as
        ET.SubElement(geometry, "mxPoint", x=str(x1), y=str(y1), as_="sourcePoint").attrib["as"] = "sourcePoint"
        ET.SubElement(geometry, "mxPoint", x=str(x2), y=str(y2), as_="targetPoint").attrib["as"] = "targetPoint"
        self.cells.append(cell)

    def generate_xml(self) -> str:
        mxfile = ET.Element(
            "mxfile", host=self.host, agent=self.agent, version=self.version
        )
        diagram = ET.SubElement(
            mxfile, "diagram", name=self.name, id=self._generate_id()
        )
        mxGraphModel = ET.SubElement(
            diagram, "mxGraphModel",
            dx=str(self.dx), dy=str(self.dy), grid=str(self.grid),
            gridSize=str(self.gridSize), guides=str(self.guides),
            tooltips=str(self.tooltips), connect=str(self.connect),
            arrows=str(self.arrows), fold=str(self.fold), page=str(self.page),
            pageScale=str(self.pageScale), pageWidth=str(self.pageWidth),
            pageHeight=str(self.pageHeight), background=self.background,
            math=str(self.math), shadow=str(self.shadow)
        )
        root = ET.SubElement(mxGraphModel, "root")
        for cell in self.root_cells + self.cells:
            root.append(cell)
        return ET.tostring(mxfile, encoding="utf-8", xml_declaration=True).decode("utf-8")

    def save(self, filepath: str) -> None:
        try:
            xml_content = self.generate_xml()
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(xml_content)
            print(f"✅ File saved: {filepath}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")

# ===== Example usage =====

if __name__ == "__main__":
    dxml = DrawioXML(name="5x5 Grid Example")
    rect_w, rect_h = 100, 60
    rows, cols = 5, 5
    for r in range(rows):
        for c in range(cols):
            fill = "#ff0000" if (r + c) % 2 == 0 else "#0000ff"
            x = c * rect_w
            y = r * rect_h
            dxml.add_rectangle(x, y, rect_w, rect_h, fill=fill, stroke="#000000", value=f"R{r}C{c}")
    for r in range(rows):
        for c in range(cols - 1):
            x1 = c * rect_w + rect_w
            y1 = r * rect_h + rect_h // 2
            x2 = (c + 1) * rect_w
            y2 = y1
            dxml.add_line(x1, y1, x2, y2, stroke="#000000", value="→")
    dxml.save("grid_example.drawio")
