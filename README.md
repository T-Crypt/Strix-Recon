```markdown
# Strix - Recon LLM Based Reconnaissance Assistant

Strix is a reconnaissance assistant leveraging a Large Language Model (LLM) to automate and enhance information gathering during penetration testing or security assessments.  It streamlines the recon process, providing insightful findings and prioritizing potential attack vectors.

## Features

* **LLM-Powered Analysis:**  Uses an LLM to analyze reconnaissance data, identifying key findings and potential vulnerabilities.
* **Automated Reconnaissance:** Automates common reconnaissance tasks, such as subdomain enumeration, port scanning, and service detection.
* **Flexible Targeting:** Supports IP addresses, domain names, and URLs as targets.
* **Layered Approach:**  Allows you to control the depth and breadth of reconnaissance with configurable layers.
* **OpenVPN Integration:** Supports the use of OpenVPN configurations for reconnaissance through a proxy.
* **Host File Support:** Allows you to specify a custom hosts file for resolving domain names.
* **Interactive Mode:** Provides an interactive shell for exploring reconnaissance data and executing commands.
* **Force Rebuild:** Forces a rebuild of the Docker image, ensuring the latest dependencies and configurations are used.

## Installation

1.  **Dependencies:** Ensure you have Docker and Python 3 installed.
2.  **Clone Repository:** Clone this repository to your local machine.  *(Replace with your actual repo link)*
3.  **Run Strix:**  Navigate to the directory containing `strix.py` and execute it with the appropriate parameters.

## Usage

### Basic Usage

```bash
python strix.py <target>
```

Where `<target>` can be:

*   **IP Address:** `python strix.py 10.10.11.58`
*   **Domain Name:** `python strix.py dog.htb`
*   **URL:** `python strix.py https://example.com`

This will run Strix with default settings and a single layer of reconnaissance.

### Advanced Flags

| Flag                | Description                                                               | Example                               |
| ------------------- | ------------------------------------------------------------------------- | ------------------------------------- |
| `--layer <int>`     | Specifies the number of reconnaissance layers to execute.                  | `python strix.py --layer 4 example.com` |
| `--interactive`      | Enables interactive mode, providing a shell for exploring the results.       | `python strix.py --interactive https://target.edu` |
| `--timeout <float>`  | Sets the timeout (in seconds) for individual reconnaissance tasks.           | `python strix.py --timeout 1.5 https://target.edu` |
| `--ovpn <path>`     | Specifies the path to an OpenVPN configuration file.                       | `python strix.py --ovpn vpn.ovpn target.com` |
| `--hosts <path>`    | Specifies the path to a custom hosts file.                               | `python strix.py --hosts hosts.txt target.com` |
| `--force-build`     | Forces a rebuild of the Docker image. Useful for ensuring the latest updates. | `python strix.py --force-build 10.10.11.58` |

**Examples:**

*   **Run Strix with 4 layers of reconnaissance:**

    ```bash
    python strix.py --layer 4 example.com
    ```

*   **Run Strix in interactive mode with a timeout of 1.5 seconds:**

    ```bash
    python strix.py --interactive --timeout 1.5 https://target.edu
    ```

*   **Run Strix with a specific OpenVPN configuration and hosts file:**

    ```bash
    python strix.py --layer 4 --ovpn vpn.ovpn --hosts hosts.txt target.com
    ```

*   **Force a rebuild of the Docker image and run against an IP address:**

    ```bash
    python strix.py --force-build 10.10.11.58
    ```

## Configuration

The configuration for Strix is primarily managed through environment variables and the `tools.yaml` file.  *(You might want to explain the `tools.yaml` file's structure and purpose here)*.  You can set environment variables before running `strix.py` to customize its behavior.

## Contributing

Contributions are welcome!  Please fork this repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This tool is intended for ethical security assessments and penetration testing only.  Use it responsibly and in accordance with all applicable laws and regulations.
```

Key improvements and explanations:

* **Clearer Introduction:**  Provides a concise overview of Strix and its purpose.
* **Features Section:** Highlights the key features for potential users.
* **Installation Instructions:**  Provides basic instructions for getting started.
* **Usage Section:**  Organizes the usage examples with a table and clear explanations.
* **Configuration Section:**  Points the user towards how the script is configured.  *Important:  You need to fill in details about `tools.yaml` here.*
* **Contributing and License:** Standard sections for open-source projects.
* **Disclaimer:**  Important legal disclaimer about ethical use.
* **Markdown Formatting:** Uses markdown formatting for readability.
* **Concise Language:** Uses clear and concise language throughout.
* **Emphasis on Ethical Use:** Reinforces the importance of using the tool ethically and responsibly.



Remember to replace the bracketed placeholders with your specific information! Also, add details to the "Configuration" section explaining the `tools.yaml` file.
