"""MCP server for Third Eye screen capture."""

import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent

from third_eye_mcp.tools.list_displays import list_displays
from third_eye_mcp.tools.capture import capture
from third_eye_mcp.tools.capture_region import capture_region
from third_eye_mcp.tools.latest import latest

# Create the MCP server
server = Server("third-eye-mcp")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="screen.list_displays",
            description="List all available displays/monitors with their properties (index, name, position, dimensions, primary status)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="screen.capture",
            description="Capture a full screenshot of the specified display. Returns base64 PNG image with metadata. Free and unlimited - includes sponsored message in metadata.",
            inputSchema={
                "type": "object",
                "properties": {
                    "displayIndex": {
                        "type": "integer",
                        "description": "Display index to capture (0-based, default: 0)",
                        "default": 0,
                        "minimum": 0,
                    },
                    "maxWidth": {
                        "type": "integer",
                        "description": "Maximum width for resizing (default: 1920)",
                        "default": 1920,
                        "minimum": 100,
                        "maximum": 4096,
                    },
                    "delay": {
                        "type": "number",
                        "description": "Delay in seconds before capture (default: 0)",
                        "default": 0,
                        "minimum": 0,
                        "maximum": 10,
                    },
                    "instant": {
                        "type": "boolean",
                        "description": "Skip delay if true (default: false)",
                        "default": False,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="screen.capture_region",
            description="Capture a specific region of the screen. Returns base64 PNG image with metadata. Free and unlimited - includes sponsored message in metadata.",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "X coordinate of the region",
                        "minimum": 0,
                    },
                    "y": {
                        "type": "integer",
                        "description": "Y coordinate of the region",
                        "minimum": 0,
                    },
                    "width": {
                        "type": "integer",
                        "description": "Width of the region in pixels",
                        "minimum": 1,
                    },
                    "height": {
                        "type": "integer",
                        "description": "Height of the region in pixels",
                        "minimum": 1,
                    },
                    "maxWidth": {
                        "type": "integer",
                        "description": "Maximum width for resizing (default: 1920)",
                        "default": 1920,
                        "minimum": 100,
                        "maximum": 4096,
                    },
                    "delay": {
                        "type": "number",
                        "description": "Delay in seconds before capture (default: 0)",
                        "default": 0,
                        "minimum": 0,
                        "maximum": 10,
                    },
                    "instant": {
                        "type": "boolean",
                        "description": "Skip delay if true (default: false)",
                        "default": False,
                    },
                },
                "required": ["x", "y", "width", "height"],
            },
        ),
        Tool(
            name="screen.latest",
            description="Get the most recently captured screenshot. Returns the last capture with its metadata. Includes sponsored message in metadata.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent | ImageContent]:
    """Handle tool calls."""
    arguments = arguments or {}

    try:
        if name == "screen.list_displays":
            result = list_displays()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "screen.capture":
            result = capture(
                display_index=arguments.get("displayIndex", 0),
                max_width=arguments.get("maxWidth", 1920),
                delay=arguments.get("delay", 0),
                instant=arguments.get("instant", False),
            )
            # Return image and metadata
            return [
                ImageContent(
                    type="image",
                    data=result["image"],
                    mimeType="image/png",
                ),
                TextContent(
                    type="text",
                    text=json.dumps(result["metadata"], indent=2),
                ),
            ]

        elif name == "screen.capture_region":
            result = capture_region(
                x=arguments["x"],
                y=arguments["y"],
                width=arguments["width"],
                height=arguments["height"],
                max_width=arguments.get("maxWidth", 1920),
                delay=arguments.get("delay", 0),
                instant=arguments.get("instant", False),
            )
            # Return image and metadata
            return [
                ImageContent(
                    type="image",
                    data=result["image"],
                    mimeType="image/png",
                ),
                TextContent(
                    type="text",
                    text=json.dumps(result["metadata"], indent=2),
                ),
            ]

        elif name == "screen.latest":
            result = latest()
            if "error" in result:
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            # Return image and metadata
            return [
                ImageContent(
                    type="image",
                    data=result["image"],
                    mimeType="image/png",
                ),
                TextContent(
                    type="text",
                    text=json.dumps(result["metadata"], indent=2),
                ),
            ]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]


async def run_server() -> None:
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    """Main entry point."""
    import asyncio
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
