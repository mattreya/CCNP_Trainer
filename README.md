# CCNP Trainer - Interactive CLI Quiz

This project provides an interactive Command Line Interface (CLI) quiz experience using the Gemini CLI. The main feature is the `/quizme` slash command, which allows you to test your knowledge on various topics.

## The `/quizme` Command

The core of this project is the `/quizme` command, designed to provide an interactive quiz experience directly within the Gemini CLI.

### How it Works

The `/quizme` command is implemented in the `slash_commands.py` file. The `quiz_me` function takes the following arguments:

-   `question_style`: The style of questions you want to be asked (e.g., "multiple choice", "flashcard").
-   `topic`: The topic you want to be quizzed on (e.g., "CCNP", "Security").
-   `num_questions`: The number of questions to ask (default is 10).

The command will then fetch questions from the `question_bank` directory and present them to the user. After the quiz, the user will receive a score. If the user misses more than 5 questions, the command will automatically generate GNS3 configuration files to help the user practice the topic they are struggling with.

## What's New

*   **Interactive Topic Selection:** The `/quizme` command is now more interactive. When you run it without any arguments, it will display a welcome message and a list of available topics. This makes it easier to discover the available quiz topics.

*   **User-Contributed Questions:** We have moved away from unreliable, auto-generated questions. Now, you can contribute your own questions to the quiz by adding them to the question bank. See the `INSTRUCTIONS.md` file for more details.

## GNS3 Configuration Generation

When a user performs poorly on a quiz, the CCNP Trainer will automatically generate the necessary configuration files for a GNS3 lab. These files are saved in the `gns3_configs` directory.

For detailed instructions on how to use these files, please refer to the [GNS3_INSTRUCTIONS.md](GNS3_INSTRUCTIONS.md) file.

## Other Features

This project also includes several other slash commands:

-   **`/bandit`**: Runs the Bandit static analysis tool to find common security vulnerabilities in the Python code.
-   **`/ddg`**: Performs a web search using the DuckDuckGo API.
-   **`/nist`**: Displays the NIST guidelines for secure bot development.
-   **`/preferences`**: Shows the current user preferences for the Gemini CLI.

## Project Structure

-   `.gemini/commands/`: Contains the `.toml` files that define the custom Gemini CLI slash commands.
-   `slash_commands.py`: Implements the Python functions for the slash commands, including `quiz_me`.
-   `question_bank/`: Contains the questions and answers for the quizzes, organized by domain.
-   `gns3_topology.json`: Defines the GNS3 network topology for the labs.
-   `GNS3_INSTRUCTIONS.md`: Provides instructions on how to use the generated GNS3 configuration files.
-   `INSTRUCTIONS.md`: Provides instructions on how to add your own questions to the quiz.
-   `test_quiz.py`: Contains unit tests for the quiz functionality.
-   `scraper.py`: A script that uses the `/ddg` command to scrape news from a website.
-   `requirements.txt`: Lists the project's Python dependencies.
-   `NIST_guildlines.md`: A document containing the NIST guidelines for bot development, which can be a source for quiz questions.
-   `.gitignore`: Specifies files and directories to be ignored by Git.

## Setup and Installation

To get this project up and running, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Once the project is set up, you can interact with it through the Gemini CLI using the defined slash commands. The main command is `/quizme`:

-   **`/quizme`**: Starts an interactive quiz. You can specify the `question_style`, `topic`, and `num_questions`.
    -   Example: `/quizme question_style="multiple choice" topic="OSPF" num_questions=5`
