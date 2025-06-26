# movie_generator.py
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai_tools.tools import FileReadTool
import os
import requests
import re
import subprocess
import json
from typing import List, Dict
from openai import OpenAI
import base64
from pathlib import Path
import time

# Configure LLM
llm = ChatOpenAI(
    openai_api_base="https://api.openai.com/v1",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4-turbo-preview"
)

# File reading tool for templates
file_read_tool = FileReadTool(
    file_path='movie_template.md',
    description='A tool to read the movie script template file and understand the expected output format.'
)

# Define tools as functions that will be called by agents
def generate_concept_art(scene_description: str, style: str = "cinematic") -> str:
    """
    Generates concept art for a scene using DALL-E 3.
    Returns the path to the saved image.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"Cinematic concept art: {scene_description}. Style: {style}, photorealistic, dramatic lighting, wide aspect ratio, professional film production quality. No text or watermarks."
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="hd",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Create filename from scene description
        words = scene_description.split()[:5]
        safe_words = [re.sub(r'[^a-zA-Z0-9_]', '', word) for word in words]
        filename = "_".join(safe_words).lower() + "_concept.png"
        filepath = os.path.join(os.getcwd(), "concept_art", filename)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Download the image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(img_response.content)
            return filepath
    except Exception as e:
        print(f"Error generating concept art: {e}")
    return ""

def generate_storyboard(shot_description: str, shot_type: str = "medium_shot") -> str:
    """
    Generates storyboard panels for specific shots using DALL-E 3.
    Shot types: extreme_wide, wide, medium, close_up, extreme_close_up
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    shot_styles = {
        "extreme_wide": "extreme wide shot, establishing shot",
        "wide": "wide shot, full body visible",
        "medium": "medium shot, waist up",
        "close_up": "close-up shot, head and shoulders",
        "extreme_close_up": "extreme close-up, detail shot"
    }
    
    prompt = f"Storyboard panel, {shot_styles.get(shot_type, 'medium shot')}: {shot_description}. Black and white sketch style, professional storyboard art, clear composition, cinematic framing."
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Create filename
        words = shot_description.split()[:3]
        safe_words = [re.sub(r'[^a-zA-Z0-9_]', '', word) for word in words]
        filename = f"{shot_type}_" + "_".join(safe_words).lower() + ".png"
        filepath = os.path.join(os.getcwd(), "storyboards", filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(img_response.content)
            return filepath
    except Exception as e:
        print(f"Error generating storyboard: {e}")
    return ""

def generate_character_design(character_description: str) -> str:
    """
    Generates character design sheets using DALL-E 3.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"Character design sheet showing multiple angles (front, side, three-quarter view) of: {character_description}. Professional concept art style, consistent character across all views, detailed costume design, neutral background."
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="hd",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Create filename from character description
        words = character_description.split()[:3]
        safe_words = [re.sub(r'[^a-zA-Z0-9_]', '', word) for word in words]
        filename = "_".join(safe_words).lower() + "_character.png"
        filepath = os.path.join(os.getcwd(), "characters", filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(img_response.content)
            return filepath
    except Exception as e:
        print(f"Error generating character design: {e}")
    return ""

def create_shot_list(script_content: str) -> str:
    """
    Creates a detailed shot list from the script.
    Returns a JSON string with shot information.
    """
    # This would normally use an AI model to analyze the script
    # For now, we'll create a simple example structure
    shot_list = {
        "project_name": "AI Movie",
        "shots": [
            {
                "shot_number": 1,
                "type": "extreme_wide",
                "description": "Establishing shot of the post-apocalyptic city",
                "duration": 5,
                "camera_movement": "static"
            },
            {
                "shot_number": 2,
                "type": "medium",
                "description": "Robot protagonist introduction",
                "duration": 8,
                "camera_movement": "slow push in"
            },
            {
                "shot_number": 3,
                "type": "close_up",
                "description": "Robot's optical sensors focusing",
                "duration": 3,
                "camera_movement": "static"
            }
        ]
    }
    
    shot_list_path = os.path.join(os.getcwd(), "production", "shot_list.json")
    os.makedirs(os.path.dirname(shot_list_path), exist_ok=True)
    
    with open(shot_list_path, 'w') as f:
        json.dump(shot_list, f, indent=2)
    
    return json.dumps(shot_list)

def generate_sound_description(scene_description: str) -> str:
    """
    Creates a detailed sound design document for the scene.
    """
    sound_categories = {
        "dialogue": "Character speech and vocals",
        "foley": "Footsteps, clothing rustles, object handling",
        "ambience": "Environmental sounds, room tone",
        "sfx": "Special effects sounds",
        "music": "Score and source music"
    }
    
    sound_design = {
        "scene": scene_description,
        "sound_layers": sound_categories,
        "cue_list": [
            {
                "timecode": "00:00:00",
                "type": "ambience",
                "description": "Post-apocalyptic city ambience - distant wind, metal creaking"
            },
            {
                "timecode": "00:00:05",
                "type": "foley",
                "description": "Robot footsteps on rubble"
            },
            {
                "timecode": "00:00:10",
                "type": "sfx",
                "description": "Electronic whirring - robot scanning"
            }
        ]
    }
    
    sound_path = os.path.join(os.getcwd(), "sound", "sound_design.json")
    os.makedirs(os.path.dirname(sound_path), exist_ok=True)
    
    with open(sound_path, 'w') as f:
        json.dump(sound_design, f, indent=2)
    
    return json.dumps(sound_design)

def create_video_prompt(scene_description: str, shot_type: str, duration: int) -> str:
    """
    Creates a detailed prompt for video generation tools like Runway Gen-4.
    """
    video_prompt = {
        "scene": scene_description,
        "technical_specs": {
            "shot_type": shot_type,
            "duration_seconds": duration,
            "fps": 24,
            "resolution": "1920x1080",
            "aspect_ratio": "16:9"
        },
        "style_guide": {
            "cinematography": "cinematic, professional",
            "lighting": "dramatic, motivated lighting",
            "color_grade": "cinematic color grading",
            "camera_movement": "smooth, purposeful"
        },
        "prompt_text": f"Cinematic video: {scene_description}. Shot type: {shot_type}. Professional cinematography, dramatic lighting, smooth camera movement, photorealistic quality."
    }
    
    prompt_path = os.path.join(os.getcwd(), "video_prompts", f"prompt_{shot_type}.json")
    os.makedirs(os.path.dirname(prompt_path), exist_ok=True)
    
    with open(prompt_path, 'w') as f:
        json.dump(video_prompt, f, indent=2)
    
    return json.dumps(video_prompt)

# Define AI Agents
script_writer = Agent(
    role='Screenplay Writer',
    goal='Transform story concepts into professional screenplay format with compelling dialogue and visual storytelling',
    backstory="An experienced screenwriter who understands three-act structure, character arcs, and visual narrative techniques. Skilled at creating engaging dialogue and dynamic scenes.",
    verbose=True,
    llm=llm,
    allow_delegation=False
)

visual_developer = Agent(
    role='Visual Development Artist',
    goal='Create comprehensive visual development including concept art, mood boards, and color scripts',
    backstory="A talented visual development artist with experience in film pre-production. Expert at translating scripts into visual language and establishing aesthetic direction.",
    verbose=True,
    llm=llm,
    allow_delegation=False
)

character_designer = Agent(
    role='Character Designer',
    goal='Design compelling virtual actors with detailed appearance, personality, and movement characteristics',
    backstory="A character designer specializing in creating memorable virtual actors. Understands how visual design reflects personality and supports storytelling.",
    verbose=True,
    llm=llm,
    allow_delegation=False
)

cinematographer = Agent(
    role='Virtual Cinematographer',
    goal='Plan shot compositions, camera movements, and visual flow of the film',
    backstory="An experienced cinematographer who thinks in frames and sequences. Expert at using camera language to enhance emotional storytelling.",
    verbose=True,
    llm=llm,
    allow_delegation=False
)

sound_designer = Agent(
    role='Sound Designer',
    goal='Design comprehensive soundscapes including dialogue, foley, ambience, and music direction',
    backstory="An award-winning sound designer who understands how audio shapes emotional experience. Creates rich, layered soundscapes that support visual narrative.",
    verbose=True,
    llm=llm,
    allow_delegation=False
)

video_director = Agent(
    role='AI Video Generation Director',
    goal='Create detailed prompts and specifications for AI video generation tools',
    backstory="A director specializing in AI video generation, understanding how to translate creative vision into technical prompts that produce compelling footage.",
    verbose=True,
    llm=llm,
    tools=[file_read_tool],
    allow_delegation=False
)

# Create Tasks
task_script = Task(
    description='Write a compelling short film screenplay based on the story prompt. Include proper screenplay format with scene headings, action lines, and dialogue. Target length: 3-5 pages for a 3-5 minute film.',
    agent=script_writer,
    expected_output='A properly formatted screenplay with engaging dialogue, clear action, and visual storytelling'
)

task_visual_dev = Task(
    description='Create comprehensive visual development including concept art for key scenes, mood boards, and establishing the visual style of the film. Generate at least 3 concept art images.',
    agent=visual_developer,
    expected_output='A visual development package with concept art for major scenes and established visual style'
)

task_characters = Task(
    description='Design all characters mentioned in the screenplay, creating detailed visual references and character sheets. Generate character design sheets.',
    agent=character_designer,
    expected_output='Complete character designs for all roles with multiple angles and expression sheets'
)

task_cinematography = Task(
    description='Create a detailed shot list breaking down the screenplay into specific shots with camera angles, movements, and compositions',
    agent=cinematographer,
    expected_output='A comprehensive shot list with camera specifications for each scene'
)

task_sound = Task(
    description='Design the complete sound landscape including dialogue notes, foley requirements, ambience, and music direction',
    agent=sound_designer,
    expected_output='A detailed sound design document with cue sheets and audio requirements'
)

task_video_prompts = Task(
    description='Create detailed prompts for AI video generation tools, incorporating all visual development, cinematography, and directorial vision',
    agent=video_director,
    expected_output='Complete set of video generation prompts ready for production',
    context=[task_script, task_visual_dev, task_cinematography],
    output_file="video_generation_guide.md"
)

# Create Crew
movie_crew = Crew(
    agents=[script_writer, visual_developer, character_designer, cinematographer, sound_designer, video_director],
    tasks=[task_script, task_visual_dev, task_characters, task_cinematography, task_sound, task_video_prompts],
    verbose=True,
    process=Process.sequential
)

def create_movie_from_prompt(story_prompt: str):
    """
    Main function to generate a movie from a story prompt
    """
    print(f"Starting movie generation for: {story_prompt}")
    
    # Create necessary directories
    directories = ['concept_art', 'storyboards', 'characters', 'production', 'sound', 'video_prompts', 'output']
    for dir in directories:
        os.makedirs(dir, exist_ok=True)
    
    # Update the first task with the story prompt
    task_script.description = f'Write a compelling short film screenplay based on this story prompt: "{story_prompt}". Include proper screenplay format with scene headings, action lines, and dialogue. Target length: 3-5 pages for a 3-5 minute film.'
    
    # Execute the crew
    result = movie_crew.kickoff()
    
    # Now generate the visual assets based on the script
    print("\n=== Generating Visual Assets ===")
    
    # Generate some concept art
    try:
        print("Generating concept art...")
        concept1 = generate_concept_art("Post-apocalyptic city with abandoned skyscrapers and overgrown vegetation")
        concept2 = generate_concept_art("Close-up of a lonely robot discovering a small flower growing through concrete")
        concept3 = generate_concept_art("Robot protecting flower from harsh storm in ruined city")
        
        print("Generating character designs...")
        char1 = generate_character_design("Weathered but gentle robot with expressive LED eyes, industrial design with patches of rust")
        
        print("Creating production documents...")
        shot_list = create_shot_list("Robot and flower story")
        sound_design = generate_sound_description("Post-apocalyptic environment with robot protagonist")
        video_prompt = create_video_prompt("Robot discovers flower in ruins", "medium", 5)
        
    except Exception as e:
        print(f"Error generating assets: {e}")
    
    print("\n=== Movie Generation Complete ===")
    print(f"Results saved to project directories")
    print(f"Check video_generation_guide.md for final output")
    
    return result

if __name__ == "__main__":
    # Example story prompt
    story_prompt = "A lonely robot discovers an abandoned flower in a post-apocalyptic city and decides to protect it, learning about hope and purpose"
    
    # Generate the movie
    create_movie_from_prompt(story_prompt)