import docker
import os

class DockerManager:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path
        self.client = docker.from_env()
        self.image_ids = []

    def build_image(self, tag=None):
        if tag is None:
            tag = os.path.basename(self.dockerfile_path)
        image, logs = self.client.images.build(path=self.dockerfile_path, tag=tag)
        image_id = image.id
        self.image_ids.append(image_id)
        return image_id, logs

    def run_image(self, image_id, command=None, ports=None, volumes=None, detach=True):
        container = self.client.containers.run(image_id, command=command, ports=ports, volumes=volumes, detach=detach)
        return container.id

    def run_python_file(self, image_id, file_path, ports=None):
        volumes = {
            os.path.abspath(file_path): {
                'bind': '/app/script.py',
                'mode': 'ro',
            }
        }
        command = 'python /app/script.py'
        container_id = self.run_image(image_id, command=command, ports=ports, volumes=volumes)
        return container_id

    def run_flask_app(self, image_id, app_directory, port_mapping=None):
        volumes = {
            os.path.abspath(app_directory): {
                'bind': '/app',
                'mode': 'ro',
            }
        }
        command = 'python /app/app.py'
        if port_mapping is None:
            port_mapping = {'5000/tcp': 5000}
        container_id = self.run_image(image_id, command=command, ports=port_mapping, volumes=volumes)
        return container_id

    def run_java_app(self, image_id, app_jar, ports=None):
        volumes = {
            os.path.abspath(app_jar): {
                'bind': '/app/app.jar',
                'mode': 'ro',
            }
        }
        command = 'java -jar /app/app.jar'
        container_id = self.run_image(image_id, command=command, ports=ports, volumes=volumes)
        return container_id

    def run_spring_boot_app(self, image_id, app_directory, port_mapping=None):
        volumes = {
            os.path.abspath(app_directory): {
                'bind': '/app',
                'mode': 'ro',
            }
        }
        command = './gradlew bootRun'
        if port_mapping is None:
            port_mapping = {'8080/tcp': 8080}
        container_id = self.run_image(image_id, command=command, ports=port_mapping, volumes=volumes)
        return container_id

    def run_openai_agent(self, image_id, agent_script, openai_api_key, port_mapping=None):
        volumes = {
            os.path.abspath(agent_script): {
                'bind': '/app/agent.py',
                'mode': 'ro',
            }
        }
        
        environment = {
            'OPENAI_API_KEY': openai_api_key
        }
        
        command = 'python /app/agent.py'
        
        if port_mapping is None:
            port_mapping = {'8000/tcp': 8000}
        
        container = self.client.containers.run(
            image_id,
            command=command,
            ports=port_mapping,
            volumes=volumes,
            environment=environment,
            detach=True
        )
        
        return container.id

    def run_express_app(self, image_id, app_directory, port_mapping=None):
        volumes = {
            os.path.abspath(app_directory): {
                'bind': '/app',
                'mode': 'rw',
            }
        }
        command = 'node /app/app.js'
        if port_mapping is None:
            port_mapping = {'3000/tcp': 3000}
        container_id = self.run_image(image_id, command=command, ports=port_mapping, volumes=volumes)
        return container_id