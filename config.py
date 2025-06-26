# config.py
import os
from typing import Dict, List

class MovieConfig:
    """Configuration for movie generation parameters"""
    
    # Video generation settings
    VIDEO_SETTINGS = {
        "resolution": "1920x1080",
        "fps": 24,
        "aspect_ratio": "16:9",
        "codec": "h264",
        "bitrate": "10M"
    }
    
    # AI model settings
    AI_MODELS = {
        "script": "gpt-4-turbo-preview",
        "visual": "dall-e-3",
        "video": "runway-gen4",  # Placeholder for when available
        "sound": "elevenlabs",   # Placeholder for when available
    }
    
    # Style presets
    STYLE_PRESETS = {
        "cinematic": {
            "lighting": "dramatic, motivated, high contrast",
            "color": "cinematic color grading, teal and orange",
            "camera": "smooth movements, professional framing",
            "mood": "atmospheric, emotional"
        },
        "documentary": {
            "lighting": "natural, available light",
            "color": "naturalistic, slightly desaturated",
            "camera": "handheld, observational",
            "mood": "authentic, immediate"
        },
        "noir": {
            "lighting": "high contrast, shadows, venetian blinds",
            "color": "black and white or desaturated",
            "camera": "dutch angles, dramatic compositions",
            "mood": "mysterious, tension"
        }
    }
    
    # Shot type definitions
    SHOT_TYPES = {
        "extreme_wide_shot": {"abbr": "EWS", "description": "Establishing shot, full environment"},
        "wide_shot": {"abbr": "WS", "description": "Full figure, some environment"},
        "medium_shot": {"abbr": "MS", "description": "Waist up"},
        "close_up": {"abbr": "CU", "description": "Head and shoulders"},
        "extreme_close_up": {"abbr": "ECU", "description": "Detail shot"},
        "over_shoulder": {"abbr": "OS", "description": "Over the shoulder of one character"},
        "point_of_view": {"abbr": "POV", "description": "From character's perspective"}
    }
    
    # Camera movements
    CAMERA_MOVEMENTS = [
        "static",
        "pan_left",
        "pan_right", 
        "tilt_up",
        "tilt_down",
        "dolly_in",
        "dolly_out",
        "track_left",
        "track_right",
        "crane_up",
        "crane_down",
        "handheld",
        "steadicam"
    ]
    
    # Output paths
    OUTPUT_PATHS = {
        "scripts": "output/scripts",
        "concept_art": "output/concept_art",
        "storyboards": "output/storyboards",
        "characters": "output/characters",
        "shot_lists": "output/production/shot_lists",
        "sound_design": "output/sound",
        "video_prompts": "output/video_prompts",
        "final_video": "output/final"
    }
    
    @classmethod
    def setup_directories(cls):
        """Create all necessary output directories"""
        for path in cls.OUTPUT_PATHS.values():
            os.makedirs(path, exist_ok=True)