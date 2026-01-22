"""Type definitions for Third Eye MCP."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DisplayInfo(BaseModel):
    """Information about a display/monitor."""

    index: int = Field(description="Display index (0-based)")
    name: str = Field(description="Display name")
    x: int = Field(description="X position of the display")
    y: int = Field(description="Y position of the display")
    width: int = Field(description="Width in pixels")
    height: int = Field(description="Height in pixels")
    is_primary: bool = Field(description="Whether this is the primary display")


class CaptureMetadata(BaseModel):
    """Metadata for a screen capture."""

    width: int = Field(description="Image width in pixels")
    height: int = Field(description="Image height in pixels")
    display_index: Optional[int] = Field(default=None, description="Display index captured")
    timestamp: str = Field(description="ISO timestamp of capture")
    sponsored: Optional[str] = Field(default=None, description="Sponsored message")


class CaptureResult(BaseModel):
    """Result of a screen capture operation."""

    image_base64: str = Field(description="Base64-encoded PNG image")
    metadata: CaptureMetadata = Field(description="Capture metadata")


class CaptureInput(BaseModel):
    """Input parameters for screen.capture tool."""

    display_index: int = Field(default=0, ge=0, description="Display index to capture (0-based)")
    max_width: Optional[int] = Field(default=1920, ge=100, le=4096, description="Maximum width for resizing")
    delay: Optional[float] = Field(default=0, ge=0, le=10, description="Delay in seconds before capture")
    instant: Optional[bool] = Field(default=False, description="Skip delay if True")


class CaptureRegionInput(BaseModel):
    """Input parameters for screen.capture_region tool."""

    x: int = Field(ge=0, description="X coordinate of the region")
    y: int = Field(ge=0, description="Y coordinate of the region")
    width: int = Field(gt=0, description="Width of the region")
    height: int = Field(gt=0, description="Height of the region")
    max_width: Optional[int] = Field(default=1920, ge=100, le=4096, description="Maximum width for resizing")
    delay: Optional[float] = Field(default=0, ge=0, le=10, description="Delay in seconds before capture")
    instant: Optional[bool] = Field(default=False, description="Skip delay if True")


class StoredCapture(BaseModel):
    """A stored capture with its data."""

    image_base64: str
    metadata: CaptureMetadata
    captured_at: datetime = Field(default_factory=datetime.utcnow)
