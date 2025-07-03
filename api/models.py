from pydantic import BaseModel, Field
from typing import Optional, List

# --- Modelos Generales ---
class ApiResponse(BaseModel):
    status: str = Field(..., description="Status of the API response (success/error)")
    message: str = Field(..., description="A human-readable message describing the response")
    data: Optional[dict] = Field(None, description="Optional data payload")

# --- Modelos de Autenticación ---
class LoginRequest(BaseModel):
    username: str = Field(..., description="Username for login")
    password: str = Field(..., description="Password for login")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Type of the token")

# --- Modelos para Módulos ---

# Mod-Voice
class VoicePreset(BaseModel):
    name: str = Field(..., description="Name of the voice preset")
    description: Optional[str] = Field(None, description="Description of the preset")
    settings: dict = Field(..., description="JSON object of voice settings")

class VoiceControlRequest(BaseModel):
    action: str = Field(..., description="Action to perform (start/stop)", example="start")
    preset: Optional[str] = Field(None, description="Name of the voice preset to use", example="robot")

# Mod-Streaming
class StreamingOverlay(BaseModel):
    name: str = Field(..., description="Name of the streaming overlay")
    url: str = Field(..., description="URL or path to the overlay asset")
    active: bool = Field(False, description="Whether the overlay is currently active")

class StreamingControlRequest(BaseModel):
    action: str = Field(..., description="Action to perform (start/stop/activate_overlay)", example="activate_overlay")
    overlay_name: Optional[str] = Field(None, description="Name of the overlay to activate/deactivate", example="alert_donation")

# Mod-Therapy
class JournalEntryCreate(BaseModel):
    content: str = Field(..., description="Content of the journal entry")

class JournalEntryResponse(BaseModel):
    id: int = Field(..., description="ID of the journal entry")
    content_preview: str = Field(..., description="Preview of the encrypted content")
    sentiment: Optional[str] = Field(None, description="Sentiment analysis result")
    created_at: str = Field(..., description="Timestamp of creation")

# Mod-Activism
class AnonymizeFileRequest(BaseModel):
    file_path: str = Field(..., description="Path to the file to anonymize")
    output_path: Optional[str] = Field(None, description="Optional output path for the anonymized file")

# Mod-Educator
class NarrationRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    language: Optional[str] = Field(None, description="Language for narration (e.g., en, es)")

class NarrationResponse(BaseModel):
    audio_url: str = Field(..., description="URL to the generated audio file")

# Mod-Devtools
class RunTestsRequest(BaseModel):
    module_name: Optional[str] = Field(None, description="Specific module to test, or all if None")

# Mod-Accessibility
class ApplyThemeRequest(BaseModel):
    theme_name: str = Field(..., description="Name of the theme to apply")