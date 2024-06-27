import os
import tempfile
import shutil
from app.utils.docker_manager import DockerManager

def run_python_code_in_docker(code):
    # Create a temporary directory to hold the code and Dockerfile
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save the code to a file
        code_file_path = os.path.join(temp_dir, "script.py")
        with open(code_file_path, "w") as code_file:
            code_file.write(code)
        
        # Define the Dockerfile content
        dockerfile_content = """
        FROM python:3.9-slim
        WORKDIR /app
        COPY script.py /app/script.py
        CMD ["python", "/app/script.py"]
        """
        
        # Save the Dockerfile
        dockerfile_path = os.path.join(temp_dir, "Dockerfile")
        with open(dockerfile_path, "w") as dockerfile:
            dockerfile.write(dockerfile_content)
        
        # Initialize DockerManager and build the image
        docker_manager = DockerManager(temp_dir)
        image_id, build_logs = docker_manager.build_image()
        
        # Run the image with the command to execute the script
        container_id = docker_manager.run_image(image_id, command=None, detach=True)
        
        # Wait for the container to finish running
        container = docker_manager.client.containers.get(container_id)
        container.wait()
        
        # Fetch the container logs which contain the script output
        logs = container.logs().decode("utf-8")
    
    finally:
        # Clean up temporary files
        shutil.rmtree(temp_dir)
    
    return logs