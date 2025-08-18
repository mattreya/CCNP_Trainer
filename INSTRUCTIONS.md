# How to Add Your Own Quiz Questions

You can add your own questions to the quiz by creating a JSON file in the appropriate question bank directory.

## 1. Find the Correct Directory

The question bank is organized by domain. The available domains are:

*   `architecture`
*   `automation`
*   `infrastructure`
*   `network_assurance`
*   `security`
*   `virtualization`

You can find these directories in the `question_bank` folder.

## 2. Create a JSON File

Create a new JSON file in the directory that corresponds to the topic of your questions. The filename should be the topic name in lowercase (e.g., `ospf.json`, `bgp.json`).

## 3. Add Your Questions

The JSON file should contain a list of questions. Each question should be a JSON object with the following format:

```json
[
    {
        "question": "What is the default administrative distance of OSPF?",
        "options": {
            "A": "90",
            "B": "100",
            "C": "110",
            "D": "120"
        },
        "answer": "C"
    },
    {
        "question": "Which command is used to enable OSPF on a router?",
        "options": {
            "A": "router ospf <process-id>",
            "B": "enable ospf",
            "C": "ip ospf enable",
            "D": "ospf run"
        },
        "answer": "A"
    }
]
```

**Important:**

*   The file must be a valid JSON file.
*   The `options` object must have four options: "A", "B", "C", and "D".
*   The `answer` must be one of the option keys (e.g., "A", "B", "C", or "D").

## Example

To add questions about BGP, you would create a file named `bgp.json` in the `question_bank/infrastructure` directory with the following content:

```json
[
    {
        "question": "What is the default administrative distance of eBGP?",
        "options": {
            "A": "20",
            "B": "90",
            "C": "170",
            "D": "200"
        },
        "answer": "A"
    },
    {
        "question": "What is the default administrative distance of iBGP?",
        "options": {
            "A": "20",
            "B": "90",
            "C": "170",
            "D": "200"
        },
        "answer": "D"
    }
]
```
