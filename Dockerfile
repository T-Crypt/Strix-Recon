FROM python:3.11-slim

# Set up working directory
WORKDIR /opt/agent

# Copy requirements and install
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy all source code
COPY . /opt/agent

# Add entrypoint
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

# Set PYTHONPATH for the agent package
ENV PYTHONPATH=/opt/agent

ENTRYPOINT ["/opt/entrypoint.sh"]
