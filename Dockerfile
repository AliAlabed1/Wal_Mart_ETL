# Use Arch Linux base image
FROM archlinux:latest

# Set the working directory in the container
WORKDIR /workspaces

# Update Arch and install necessary packages
RUN pacman -Syu --noconfirm && pacman -S --noconfirm python python-pip git python-virtualenv

# Clone the Git repository each time the container is started
CMD ["sh", "-c", "git clone https://github.com/AliAlabed1/Wal_Mart_ETL.git && \
    cd Wal_Mart_ETL && \
    python -m venv venv && \
    source venv/bin/activate && \
    pip install -r requierments.txt && \
    cd src/main && \
    py main.py"]