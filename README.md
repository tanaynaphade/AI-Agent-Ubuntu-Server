# Ubuntu AI Agent

A containerized Ubuntu environment with an AI-powered terminal assistant that converts natural language instructions into executable bash commands using Google's Gemini AI.

## Features

- **Natural Language to Commands**: Convert plain English instructions into bash commands
- **Interactive CLI**: Review and approve commands before execution
- **Containerized Environment**: Isolated Ubuntu 22.04 environment with essential tools
- **AI-Powered**: Uses Google Gemini 2.5 Flash model for command generation
- **Safe Execution**: Commands are displayed for review before execution
- **Non-root User**: Runs with a dedicated `agent` user with sudo privileges

## Prerequisites

- Docker and Docker Compose installed
- Google Gemini API key

## Quick Start

1. **Clone or download the project files**

2. **Set up your Gemini API key**
   
   Replace `Gemini-Key` with your actual API key in:
   - `agent/agent.py` (line 8)
   - `docker-compose.yaml` (line 19)

3. **Build and run the container**
   ```bash
   docker-compose up -d --build
   ```

4. **Access the container**
   ```bash
   docker exec -it ubuntu-ai-agent bash
   ```

5. **Start using the AI agent**
   ```bash
   agent "list all files in the current directory"
   agent "show system information"
   agent "create a new directory called projects"
   ```

## Usage

The AI agent accepts natural language commands and converts them to bash commands:

```bash
# Basic usage
agent "your instruction here"

# Examples
agent "show disk usage"
agent "find all Python files in the current directory"
agent "install nodejs using apt"
agent "create a backup of the home directory"
```

### Command Flow

1. **Input**: You provide a natural language instruction
2. **AI Processing**: Gemini AI converts your instruction to bash commands
3. **Review**: The system shows you the proposed commands
4. **Confirmation**: You approve or reject the commands
5. **Execution**: Approved commands are executed with output displayed

## Project Structure

```
.
├── Dockerfile              # Container configuration
├── docker-compose.yaml     # Docker Compose setup
├── requirements.txt        # Python dependencies
├── agent/
│   └── agent.py            # Main AI agent script
├── workspace/              # Mounted workspace directory
└── logs/                   # Log files directory
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key
- `AGENT_MODE`: Set to "interactive" for interactive mode
- `PYTHONPATH`: Python path configuration
- `TERM`: Terminal type for better display

### Resource Limits

The container is configured with:
- **CPU**: 2.0 cores (limit), 0.5 cores (reservation)
- **Memory**: 2GB (limit), 512MB (reservation)

## Security Features

- **Non-root execution**: Runs as `agent` user with sudo privileges
- **Command review**: All commands are displayed before execution
- **Isolated environment**: Containerized for security
- **Controlled access**: Uses environment variables for API keys

## Installed Tools

The container includes:
- Python 3 with pip and venv
- Essential utilities: curl, wget, git, vim, nano, htop, tree, jq
- Build tools and development utilities
- Google Generative AI SDK

## API Configuration

The agent uses Google's Gemini 2.5 Flash model with:
- **Temperature**: 0.2 (for more deterministic outputs)
- **API Version**: v1alpha
- **Model**: gemini-2.5-flash

## Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Replace `Gemini-Key` in both `agent.py` and `docker-compose.yaml`

## Examples

```bash
# System administration
agent "show running processes"
agent "check memory usage"
agent "list network connections"

# File operations
agent "create a backup of important files"
agent "find large files over 100MB"
agent "compress the logs directory"

# Development tasks
agent "set up a Python virtual environment"
agent "install git and configure user settings"
agent "clone a repository and install dependencies"
```

## Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```
   Error: Please set the GEMINI_API_KEY environment variable
   ```
   **Solution**: Update your API key in the configuration files

2. **Permission Denied**
   ```
   Error: Permission denied
   ```
   **Solution**: The agent user has sudo privileges; use `sudo` for system operations

3. **Container Won't Start**
   ```
   Error: Container exits immediately
   ```
   **Solution**: Check Docker logs with `docker logs ubuntu-ai-agent`

### Debug Mode

To run the container in debug mode:
```bash
docker-compose up --build
```

## Development

### Modifying the Agent

1. Edit `agent/agent.py` for functionality changes
2. Update `requirements.txt` for new dependencies
3. Rebuild the container: `docker-compose up --build`

### Adding New Tools

Add new tools to the Dockerfile:
```dockerfile
RUN apt-get update && apt-get install -y \
    your-new-tool \
    && rm -rf /var/lib/apt/lists/*
```

## Safety Notes

- Always review commands before execution
- The agent has sudo privileges - use with caution
- Commands are executed with shell access to the container
- Consider the security implications of the commands being generated

## Contributing

Feel free to submit issues and enhancement requests. When contributing:

1. Test your changes thoroughly
2. Update documentation as needed
3. Follow security best practices
4. Consider backward compatibility

## License

This project is provided as-is for educational and development purposes.

---

**Note**: Replace placeholder API keys with your actual Gemini API key before use.