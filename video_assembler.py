# video_assembler.py
import os
import json
import subprocess
from typing import List, Dict
import requests
from pathlib import Path
import time

class VideoAssembler:
    """Assembles final video from generated components"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.shots_path = self.project_path / "shots"
        self.audio_path = self.project_path / "audio"
        self.output_path = self.project_path / "output"
        
    def create_edit_decision_list(self, shot_list_path: str) -> Dict:
        """Creates an EDL from the shot list"""
        with open(shot_list_path, 'r') as f:
            shot_list = json.load(f)
            
        edl = {
            "version": "1.0",
            "project_name": shot_list.get("project_name", "untitled"),
            "timeline": []
        }
        
        current_time = 0
        for shot in shot_list.get("shots", []):
            edit_point = {
                "shot_number": shot["shot_number"],
                "in_point": current_time,
                "out_point": current_time + shot["duration"],
                "file_path": f"shots/shot_{shot['shot_number']:03d}.mp4",
                "transitions": shot.get("transitions", {"in": "cut", "out": "cut"})
            }
            edl["timeline"].append(edit_point)
            current_time += shot["duration"]
            
        return edl
    
    def generate_ffmpeg_filter_complex(self, edl: Dict) -> str:
        """Generates FFmpeg filter complex for video assembly"""
        filters = []
        inputs = []
        
        for i, edit in enumerate(edl["timeline"]):
            inputs.append(f"-i {edit['file_path']}")
            
            # Add any transitions or effects here
            if edit["transitions"]["in"] == "fade":
                filters.append(f"[{i}:v]fade=t=in:st=0:d=1[v{i}]")
            else:
                filters.append(f"[{i}:v]copy[v{i}]")
        
        # Concatenate all video streams
        concat_inputs = "".join([f"[v{i}]" for i in range(len(edl["timeline"]))])
        filters.append(f"{concat_inputs}concat=n={len(edl['timeline'])}:v=1:a=0[outv]")
        
        return ";".join(filters)
    
    def assemble_video(self, edl_path: str, output_filename: str):
        """Assembles the final video using FFmpeg"""
        edl = self.create_edit_decision_list(edl_path)
        
        # Build FFmpeg command
        cmd = ["ffmpeg", "-y"]
        
        # Add input files
        for edit in edl["timeline"]:
            cmd.extend(["-i", str(self.project_path / edit["file_path"])])
        
        # Add filter complex
        filter_complex = self.generate_ffmpeg_filter_complex(edl)
        cmd.extend(["-filter_complex", filter_complex])
        
        # Add output settings
        cmd.extend([
            "-map", "[outv]",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            str(self.output_path / output_filename)
        ])
        
        # Execute FFmpeg
        try:
            subprocess.run(cmd, check=True)
            print(f"Video assembled successfully: {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error assembling video: {e}")
            
    def add_audio_track(self, video_path: str, audio_path: str, output_path: str):
        """Adds audio track to video"""
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"Audio added successfully: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error adding audio: {e}")

# Regular functions instead of tools
def generate_video_shot(prompt: str, duration: int, shot_number: int) -> str:
    """
    Generates a video shot using AI video generation API.
    This is a placeholder for actual video generation - 
    replace with actual Runway Gen-4 or similar API when available.
    """
    # Placeholder for video generation
    # In production, this would call Runway Gen-4, Google Veo, or similar
    
    video_path = f"output/shots/shot_{shot_number:03d}.mp4"
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    
    # Create a placeholder video file
    # In real implementation, this would be the generated video
    placeholder_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=black:s=1920x1080:d={duration}",
        "-vf", f"drawtext=text='Shot {shot_number}':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
        video_path
    ]
    
    try:
        subprocess.run(placeholder_cmd, check=True, capture_output=True)
        return video_path
    except:
        return ""

def generate_audio_track(description: str, duration: int, audio_type: str = "music") -> str:
    """
    Generates audio track (music, sfx, ambience) using AI audio generation.
    This is a placeholder for actual audio generation.
    """
    audio_path = f"output/audio/{audio_type}_{int(time.time())}.mp3"
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    
    # Placeholder for audio generation
    # In production, this would call ElevenLabs, Suno, or similar
    
    # Create a placeholder audio file
    placeholder_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"anullsrc=duration={duration}",
        "-c:a", "mp3",
        audio_path
    ]
    
    try:
        subprocess.run(placeholder_cmd, check=True, capture_output=True)
        return audio_path
    except:
        return ""