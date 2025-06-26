# main.py
import os
from movie_generator import create_movie_from_prompt
from config import MovieConfig
from video_assembler import VideoAssembler
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a movie from a story prompt')
    parser.add_argument('prompt', type=str, help='Story prompt for the movie')
    parser.add_argument('--style', type=str, default='cinematic', 
                       choices=['cinematic', 'documentary', 'noir'],
                       help='Visual style preset')
    parser.add_argument('--duration', type=int, default=180,
                       help='Target duration in seconds (default: 180)')
    parser.add_argument('--output', type=str, default='my_movie.mp4',
                       help='Output filename')
    
    args = parser.parse_args()
    
    # Setup directories
    MovieConfig.setup_directories()
    
    # Generate movie components
    print(f"Generating movie from prompt: {args.prompt}")
    print(f"Style: {args.style}")
    print(f"Target duration: {args.duration} seconds")
    
    # Create the movie
    result = create_movie_from_prompt(args.prompt)
    
    # Assemble video (when actual video generation is available)
    # assembler = VideoAssembler("output")
    # assembler.assemble_video("output/production/shot_list.json", args.output)
    
    print(f"\nMovie generation complete!")
    print(f"Check the output directories for generated content:")
    print("- Scripts: output/scripts/")
    print("- Concept Art: output/concept_art/")
    print("- Storyboards: output/storyboards/")
    print("- Characters: output/characters/")
    print("- Production Documents: output/production/")

if __name__ == "__main__":
    main()